require 'net/http'
require 'json'
require 'fileutils'

# Strapi API URL
url = 'http://localhost:1337/api/posts'

uri = URI(url)
response = Net::HTTP.get(uri)
posts = JSON.parse(response)

# Check if data exists
if posts['data'].nil? || posts['data'].empty?
  puts "No posts found or error fetching posts!"
  exit
end

# Ensure the _posts directory exists
FileUtils.mkdir_p('_posts')

posts['data'].each do |post|
  title = post['title']
  slug = title.downcase.gsub(' ', '-').gsub(/[^a-z0-9\-]/, '')
  date = post['date'][0..9]  # Extract only the date part
  filename = "_posts/#{date}-#{slug}.md"

  File.open(filename, 'w') do |file|
    file.puts "---"
    file.puts "layout: post"
    file.puts "title: \"#{title}\""
    file.puts "date: #{post['date']}"
    file.puts "categories: #{post['categories']}"
    file.puts "tags: #{post['tags']}"
    file.puts "description: \"#{post['description']}\""
    file.puts "image:"
    file.puts "  path: #{post['imagepath']}"  # Adjusted to match 'imagepath' field
    file.puts "---"
    file.puts post['Content']  # Adjusted to match 'Content' field
  end
end
