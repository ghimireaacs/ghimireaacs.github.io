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
