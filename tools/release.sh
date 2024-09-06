#!/usr/bin/env bash
#
# Build, test, and deploy the site content to 'origin/<pages_branch>'
#
# Requirement: Jekyll, Bundler
#
# Usage: See help information

set -eu

PAGES_BRANCH="gh-pages"
SITE_DIR="_site"
_opt_dry_run=false
_config="_config.yml"
_baseurl=""
_commit_message="[Automation] Site update No.${GITHUB_RUN_NUMBER:-0}" # GITHUB_RUN_NUMBER for incremental commits

help() {
  echo "Build, test, and deploy the site content to 'origin/<pages_branch>'"
  echo
  echo "Usage:"
  echo
  echo "   bash ./tools/deploy.sh [options]"
  echo
  echo "Options:"
  echo '     -c, --config   "<config_a[,config_b[...]]>"    Specify config file(s)'
  echo "     --dry-run                Build site and test, but not deploy"
  echo "     -h, --help               Print this information."
}

init() {
  if [[ -z ${GITHUB_ACTION+x} && $_opt_dry_run == 'false' ]]; then
    echo "ERROR: It is not allowed to deploy outside of the GitHub Action environment."
    echo "Use '-h' for help."
    exit 1
  fi

  _baseurl="$(grep '^baseurl:' _config.yml | sed "s/.*: *//;s/['\"]//g;s/#.*//")"
}

build() {
  # Clean up previous builds
  rm -rf "$SITE_DIR"

  # Build with Jekyll
  JEKYLL_ENV=production bundle exec jekyll build -d "$SITE_DIR$_baseurl" --config "$_config"
}

# Optional test function (currently disabled)
test() {
  bundle exec htmlproofer --disable-external --check-html --allow_hash_href "$SITE_DIR"
}

prepare_site_dir() {
  if [[ -n $_baseurl ]]; then
    mv "$SITE_DIR$_baseurl" "${SITE_DIR}-rename"
    rm -rf "$SITE_DIR"
    mv "${SITE_DIR}-rename" "$SITE_DIR"
  fi
}

setup_gh_pages_branch() {
  if git show-ref --quiet refs/heads/$PAGES_BRANCH; then
    git checkout "$PAGES_BRANCH"
  else
    git checkout --orphan "$PAGES_BRANCH"
  fi
}

deploy() {
  git config --global user.name "GitHub Actions"
  git config --global user.email "41898282+github-actions[bot]@users.noreply.github.com"

  # Remove all files from the current directory (in the gh-pages branch)
  git rm -rf .

  # Add the generated site files
  cp -r "$SITE_DIR"/* .

  # Create or update .nojekyll to bypass Jekyll on GitHub Pages
  [[ -f ".nojekyll" ]] || echo "" >".nojekyll"

  # Commit and push changes to the gh-pages branch
  git add -A
  git commit -m "$_commit_message"
  git push -f origin "$PAGES_BRANCH"
}

main() {
  init
  build
  # test  # Uncomment this line if you want to enable HTML-Proofer testing
  prepare_site_dir

  if $_opt_dry_run; then
    echo "Dry run completed. No deployment was made."
    exit 0
  fi

  setup_gh_pages_branch
  deploy
}

# Parse command-line arguments
while (($#)); do
  opt="$1"
  case $opt in
    -c | --config)
      _config="$2"
      shift
      shift
      ;;
    --dry-run)
      _opt_dry_run=true
      shift
      ;;
    -h | --help)
      help
      exit 0
      ;;
    *)
      # Unknown option
      help
      exit 1
      ;;
  esac
done

main
