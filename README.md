# Welcome

# Setting Up
1. Install rbenv to manage Ruby Version
   
    `yay -S rbenv`
   
3. Initialize rbenv and store it in '~/.zshrc'

    `rbenv init`
    `v ~/.zshrc`
    `eval "$(rbenv init - zsh)"`
   
5. Install ruby 3.2.2 Required for this project

   `rbenv install 3.2.2`
   
7. Change director to thi project and set local ruby version

    `z ghimireaacs.github.io`
    `rbenv local 3.2.2`
   
9. Install all dependencies

    `bundle install`
   
11. Run on localhost

    `bundle exec jekyll serve --verbose`
