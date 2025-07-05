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