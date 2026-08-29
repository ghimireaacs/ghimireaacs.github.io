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
    case page.data['layout']
    when 'tag'
      # _includes/head.html marks these noindex because most hold a single post;
      # listing a noindexed URL in the sitemap sends two contradictory signals.
      page.data['sitemap'] = false
    when 'category'
      # jekyll-archives keeps the category name on the object, not in `data`.
      name = page.data['title'] || (page.respond_to?(:title) ? page.title : nil)
      entry = intros[name]
      next unless entry

      page.data['description'] = entry['description']
      page.data['intro'] = entry['intro']
    end
  end
end
