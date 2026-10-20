#!/usr/bin/env python3
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
from urllib.robotparser import RobotFileParser


class Page(HTMLParser):
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.titles = []
        self.meta = {}
        self.canonicals = []
        self.discovery = []
        self.schemas = []
        self.resources = []
        self.capture = None
        self.buffer = ""
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for key in ("href", "src"):
            if attrs.get(key):
                self.resources.append(attrs[key])
        if tag == "title":
            self.capture, self.buffer = "title", ""
        elif tag == "script" and attrs.get("type") == "application/ld+json":
            self.capture, self.buffer = "schema", ""
        elif tag == "meta":
            for key in ("name", "property"):
                if key in attrs:
                    self.meta.setdefault(attrs[key], []).append(attrs.get("content", ""))
        elif tag == "link":
            if attrs.get("rel") == "canonical":
                self.canonicals.append(attrs.get("href", ""))
            elif attrs.get("rel") == "describedby":
                self.discovery.append(attrs.get("href", ""))

    def handle_data(self, data):
        if self.capture:
            self.buffer += data

    def handle_endtag(self, tag):
        if tag == "title" and self.capture == "title":
            self.titles.append(self.buffer.strip())
            self.capture = None
        elif tag == "script" and self.capture == "schema":
            self.schemas.append(self.buffer)
            self.capture = None


def check_site(root):
    errors = []
    titles = {}
    canonicals = set()
    post_urls = set()
    origin = "https://ashishghimire.com"

    def check(condition, message):
        if not condition:
            errors.append(message)

    def local_file(url):
        path = root / unquote(urlsplit(url).path).lstrip("/")
        return path / "index.html" if path.is_dir() else path

    sitemap = ET.parse(root / "sitemap.xml")
    sitemap_urls = [node.text for node in sitemap.findall(".//{*}loc")]
    check(len(sitemap_urls) == len(set(sitemap_urls)), "Sitemap has duplicate URLs")
    for url in sitemap_urls:
        check(url.startswith(origin + "/"), f"Sitemap uses a noncanonical host: {url}")
        check(local_file(url).is_file(), f"Sitemap target does not exist: {url}")
    for node in sitemap.findall(".//{*}lastmod"):
        try:
            datetime.fromisoformat(node.text.replace("Z", "+00:00"))
        except (ValueError, AttributeError):
            errors.append(f"Invalid sitemap lastmod: {node.text}")

    pages = sorted(root.rglob("*.html"))
    for path in pages:
        label = str(path.relative_to(root))
        page = Page(path.read_text())
        check(len(page.titles) == 1 and bool(page.titles[0]), f"{label}: expected one nonempty title")
        check(len(page.canonicals) == 1, f"{label}: expected one canonical URL")
        if len(page.canonicals) != 1:
            continue
        canonical = page.canonicals[0]
        page_url = origin + "/" + label.removesuffix("index.html")
        robots = ",".join(page.meta.get("robots", [])).lower()
        noindex = "noindex" in robots
        check(len(page.meta.get("robots", [])) == 1, f"{label}: expected one robots directive")
        if noindex:
            check(page_url not in sitemap_urls, f"{label}: noindex page is in sitemap")
        check(path.name != "404.html" or noindex, f"{label}: error page must be noindex")
        if page_url.startswith(origin + "/tags/") and page_url != origin + "/tags/":
            check(noindex, f"{label}: individual tag archive must remain noindex")
        if noindex and canonical != page_url:
            check(canonical in sitemap_urls, f"{label}: redirect canonical is not an indexable page")
            check(local_file(canonical).is_file(), f"{label}: redirect target is missing")
            check("http-equiv=\"refresh\"" in path.read_text(), f"{label}: non-self canonical needs a redirect")
            continue
        check(canonical.startswith(origin + "/"), f"{label}: canonical must use the HTTPS site URL")
        check(local_file(canonical).resolve() == path.resolve(), f"{label}: canonical points to another page")
        check(canonical not in canonicals, f"{label}: duplicate canonical URL")
        canonicals.add(canonical)
        if not noindex:
            check(canonical in sitemap_urls, f"{label}: indexable page is missing from sitemap")
        if page.titles and not noindex:
            title = page.titles[0]
            check(title not in titles, f"{label}: title duplicates {titles.get(title)}")
            titles[title] = label
        for key in ("description", "og:title", "og:description", "og:url", "og:image", "og:image:alt", "twitter:card"):
            values = page.meta.get(key, [])
            check(len(values) == 1 and bool(values[0]), f"{label}: expected one nonempty {key}")
        check(page.meta.get("og:url") == [canonical], f"{label}: Open Graph URL differs from canonical")
        if not noindex:
            check("max-image-preview:large" in robots, f"{label}: large image previews are not enabled")
        check(origin + "/llms.txt" in page.discovery, f"{label}: llms.txt discovery link missing")
        for image in page.meta.get("og:image", []):
            check(image.startswith("https://"), f"{label}: image URL is not HTTPS")
            if image.startswith(origin + "/"):
                check(local_file(image).is_file(), f"{label}: social image is missing")
        schemas = []
        check(len(page.schemas) == 1, f"{label}: expected one JSON-LD graph")
        for raw in page.schemas:
            try:
                data = json.loads(raw)
                graph = data.get("@graph")
                if not isinstance(graph, list) or not all(isinstance(item, dict) for item in graph):
                    raise ValueError("Expected an object graph")
                schemas.extend(graph)
            except (ValueError, AttributeError):
                errors.append(f"{label}: invalid JSON-LD")
        check(bool(schemas), f"{label}: structured data missing")
        entities = {item["@id"]: item for item in schemas if "@id" in item}
        ids = [item["@id"] for item in schemas if "@id" in item]
        check(len(ids) == len(set(ids)), f"{label}: duplicate schema entity IDs")
        for kind in ("Person", "WebSite"):
            check(sum(item.get("@type") == kind for item in schemas) == 1, f"{label}: expected one {kind} entity")
        if "/posts/" in canonical:
            if not noindex:
                post_urls.add(canonical)
            articles = [item for item in schemas if item.get("@type") == "BlogPosting"]
            check(len(articles) == 1, f"{label}: expected one BlogPosting")
            breadcrumbs = [item for item in schemas if item.get("@type") == "BreadcrumbList"]
            check(len(breadcrumbs) == 1, f"{label}: expected one breadcrumb trail")
            if breadcrumbs:
                trail = breadcrumbs[0].get("itemListElement", [])
                check(len(trail) >= 2, f"{label}: breadcrumb trail is incomplete")
                for position, crumb in enumerate(trail, 1):
                    check(crumb.get("position") == position, f"{label}: breadcrumb positions are out of order")
                    check(crumb.get("item") in sitemap_urls, f"{label}: breadcrumb target is not indexable")
            if articles:
                article = articles[0]
                for key in ("headline", "description", "image", "datePublished", "dateModified"):
                    check(bool(article.get(key)), f"{label}: article {key} missing")
                author = article.get("author") or {}
                author = entities.get(author.get("@id"), author)
                check(author.get("name") == "Ashish Ghimire", f"{label}: author name missing")
                check(author.get("url") == origin + "/about/", f"{label}: author profile URL missing")
                for key in ("datePublished", "dateModified"):
                    try:
                        date = datetime.fromisoformat(article[key].replace("Z", "+00:00"))
                        check(date.tzinfo is not None, f"{label}: {key} needs a timezone")
                    except (KeyError, ValueError):
                        errors.append(f"{label}: invalid {key}")
                check(article.get("url") == canonical, f"{label}: article URL differs from canonical")
                image = article.get("image") or {}
                image_url = image.get("url") if isinstance(image, dict) else image
                check(page.meta.get("og:image") == [image_url], f"{label}: article and social images differ")
        if canonical == origin + "/about/":
            profiles = [item for item in schemas if item.get("@type") == "ProfilePage"]
            check(len(profiles) == 1, "About page: ProfilePage schema missing")
            if profiles:
                person = entities.get(profiles[0].get("mainEntity", {}).get("@id"), {})
                check(person.get("name") == "Ashish Ghimire", "About page: profile does not identify the author")
        if canonical == origin + "/privacy-policy/":
            check(any(item.get("@type") == "WebPage" and item.get("url") == canonical for item in schemas), "Privacy policy must be a WebPage")
        if "/categories/" in canonical or canonical in (origin + "/tags/", origin + "/all-posts/"):
            check(any(item.get("@type") == "CollectionPage" and item.get("url") == canonical for item in schemas), f"{label}: CollectionPage schema missing")
        for resource in page.resources:
            url = urljoin(canonical, resource)
            if url.startswith(origin + "/"):
                check(local_file(url).is_file(), f"{label}: missing local resource {url}")

    robots = RobotFileParser()
    robots.parse((root / "robots.txt").read_text().splitlines())
    for agent in ("Googlebot", "Bingbot", "OAI-SearchBot", "ChatGPT-User", "PerplexityBot", "Perplexity-User", "Claude-SearchBot", "Claude-User"):
        for url in [origin + "/", origin + "/llms.txt", *post_urls]:
            check(robots.can_fetch(agent, url), f"robots.txt blocks {agent}: {url}")
    for agent in ("GPTBot", "Google-Extended", "CCBot"):
        check(not robots.can_fetch(agent, origin + "/"), f"Existing {agent} restriction was removed")
    check(origin + "/sitemap.xml" in (robots.site_maps() or []), "robots.txt sitemap reference missing")

    llms = (root / "llms.txt").read_text()
    check(llms.startswith("# Ashish Ghimire\n"), "llms.txt heading missing or front matter leaked")
    check("{{" not in llms and "{%" not in llms, "llms.txt contains unrendered Liquid")
    check(not re.search(r"^#{3,} ", llms, re.MULTILINE), "llms.txt file lists must use H2 sections")
    links = re.findall(r"\]\((https?://[^)]+)\)", llms)
    counts = Counter(links)
    for url in post_urls:
        check(counts[url] == 1, f"llms.txt must list each published article once: {url}")
    for url in links:
        if url.startswith(origin + "/"):
            check(local_file(url).is_file(), f"llms.txt target does not exist: {url}")
    for url in sitemap_urls:
        check(not url.endswith(("/llms.txt", "/robots.txt", "/404.html")), f"Utility URL in sitemap: {url}")
    if errors:
        print("\n".join(f"FAIL: {error}" for error in errors))
        return 1
    print(f"SEO checks passed: {len(pages)} HTML pages, {len(post_urls)} posts, {len(sitemap_urls)} sitemap URLs.")
    return 0


if __name__ == "__main__":
    sys.exit(check_site(Path(sys.argv[1] if len(sys.argv) > 1 else "_site")))
