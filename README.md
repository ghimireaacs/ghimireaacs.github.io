# Welcome

# Setting Up
1. Install rbenv to manage Ruby Version
   
    `yay -S rbenv`
   
2. Initialize rbenv and store it in '~/.zshrc'

    `rbenv init`
   
    `v ~/.zshrc`

    `eval "$(rbenv init - zsh)"`

4. Install Ruby Build plugin for 'rbenv install' to work

    `git clone https://github.com/rbenv/ruby-build.git`

   `"$(rbenv root)"/plugins/ruby-build`

3. Install ruby 3.2.2 Required for this project

   `rbenv install 3.2.2`

4. Change directory to this project and set local ruby version

   `z ghimireaacs.github.io`

   `rbenv local 3.2.2`
   
6. Install all dependencies

    `bundle install`
   
7. Run on localhost

    `bundle exec jekyll serve --verbose`

# Adding Blogs

1. Write You Blog
    
    - Create a file markdown inside `_posts`
    - Rename file in `YYYY-MM-DD-slug-of-file.md`.
    - Copy Front Matter and Replace with relevant data.
    - Write your blog.

2. Image formatting
    
    - Install libwebp. `sudo apt install webp` in ubuntu or `sudo pacman -S libwebp` for Arch Linux.
    
    ### Manual Conversion
    
    - convert desired file to webp `cwebp image.jpg -o image.webp` manually
    - copy it to correct destination. i.e "assets/img/posts/image.webp" for posts.

    ### Auto Conversion

    - From your root folder
    - Make convert.sh executable `chmod +x convert.sh`
    - run `./convert.sh`
    - This will convert all files to webp, put them in relevant path and remove original files.

# SEO maintenance

The canonical site is `https://ashishghimire.com`. Keep existing post filenames
and permalinks stable so published links continue to work.

- `_includes/head.html` is the Chirpy 7.6 override. It keeps the existing JPEG
  social cards and adds descriptive home-page and pagination titles, crawler
  directives, and a link to `/llms.txt`.
- `_includes/schema.html` publishes one JSON-LD graph linking the author, site,
  article or page, and breadcrumbs. The head removes the SEO plugin's separate
  JSON-LD to avoid duplicate article markup.
- `_data/authors.yml` supplies the default post byline and author profile link.
  `_config.yml` supplies the site-level author metadata.
- `_plugins/archives-metadata-hook.rb` uses `_data/category_intros.yml` for
  category pages and provides fallback descriptions for new categories.
  Individual tag archives remain crawlable but noindex and outside the sitemap.
- `jekyll-sitemap` generates `/sitemap.xml`. Error pages, redirects, and utility
  text files are excluded. `assets/robots.txt` publishes at `/robots.txt`.
- `/llms.txt` regenerates from published, indexable posts on every build, with
  category groups, descriptions, dates, and canonical links. It follows the
  [llms.txt proposal](https://llmstxt.org/). It is a discovery file, not a ranking
  guarantee or crawler permission file. [Google does not use it for ranking](https://developers.google.com/search/docs/fundamentals/ai-optimization-guide).
- Search and retrieval crawlers can access public pages. The existing GPTBot,
  Google-Extended, and CCBot restrictions remain in `robots.txt`.

For each post, keep the visible `title` in the author's voice. Use `seo_title`
when a shorter, clearer search title helps. Write a unique description that
accurately summarizes the article, usually around 120 to 160 characters.
Retain the original publication date; the Git history hook supplies the last
modification date.

Keep the `categories` hierarchy and an `image` mapping with `path` and `alt`.
When updating social cards, build once for reading-time data, then use the
existing generators below and rebuild afterward. They require Pillow and the
fonts specified in each script, and produce 1200 by 630 JPEG cards.

```bash
python3 tools/gen-og-images.py
python3 tools/gen-og-default.py
```

Build and validate before publishing:

```bash
JEKYLL_ENV=production bundle exec jekyll build
python3 tools/check_seo.py _site
```

`bash tools/test.sh` runs both steps. The deployment workflow also runs the SEO
check before publishing. The checker uses Python's standard library and checks
canonical URLs, unique indexable titles, metadata, local resources, author
references in the graph, article dates, breadcrumbs, category redirects, tag
indexing policy, sitemap coverage, crawler access, and `llms.txt` links.

After publishing, verify the HTTPS site in Google Search Console and Bing
Webmaster Tools, then submit `https://ashishghimire.com/sitemap.xml`. For HTML
verification, put actual provider tokens under `webmaster_verifications.google`
and `webmaster_verifications.bing` in `_config.yml`. No placeholder tokens are
published. Inspect the home page and a recent post in Search Console, check
article markup with Google's Rich Results Test, and confirm that the live
`robots.txt`, `llms.txt`, and sitemap return 200.
