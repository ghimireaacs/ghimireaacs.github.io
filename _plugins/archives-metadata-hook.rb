#!/usr/bin/env ruby
#
# Metadata for the pages jekyll-archives generates.
#
# Archive pages have no front matter of their own, so they inherit the site
# description from jekyll-seo-tag. That gave all ten category hubs and every tag
# page the same meta description. This hook gives each category its own
# description from _data/category_intros.yml, and keeps the thin tag archives out
# of the sitemap.

Jekyll::Hooks.register :site, :pre_render do |site|
  intros = site.data['category_intros'] || {}

  site.pages.each do |page|
    name = page.data['title'] || (page.respond_to?(:title) ? page.title : nil)
    case page.data['layout']
    when 'tag'
      # _includes/head.html marks these noindex because most hold a single post;
      # listing a noindexed URL in the sitemap sends two contradictory signals.
      page.data['sitemap'] = false
      page.data['description'] = "Read posts tagged #{name} by #{site.config['title']}, including practical guides, lab notes, and troubleshooting."
    when 'category'
      # jekyll-archives keeps the category name on the object, not in `data`.
      entry = intros[name]
      if entry
        page.data['description'] = entry['description']
        page.data['intro'] = entry['intro']
      else
        page.data['description'] = "Explore #{name} articles by #{site.config['title']}, with hands-on guides, troubleshooting notes, and practical examples."
      end
    end
  end
end
