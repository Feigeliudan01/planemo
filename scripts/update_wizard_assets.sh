#!/bin/bash
# Script to update assets used to build test reports HTML files.

# TODO:
# - implement help(), don't override PLANEMO_ROOT is set externally
#   avoid cd

exists() {
    type "$1" >/dev/null 2>/dev/null
}

ensure_bower() {
    if ! exists "bower";
    then
        echo "bower not on path and not on path, install with npm install -g bower."
        exit 1
    fi
}

PLANEMO_SCRIPTS_DIR=`dirname $0`
PLANEMO_ROOT="$PLANEMO_SCRIPTS_DIR/.."

cd "$PLANEMO_ROOT"

BOWER_PACKAGES="
	bootstrap
  twitter-bootstrap-wizard#master
"
BOWER_ASSETS="
    bootstrap/dist/css/bootstrap.min.css
    bootstrap/dist/js/bootstrap.min.js 
    jquery/dist/jquery.min.js
    twitter-bootstrap-wizard/jquery.bootstrap.wizard.min.js
"

for package in $BOWER_PACKAGES; do
	bower install "$package"
done

for asset in $BOWER_ASSETS; do
	cp "bower_components/$asset" $PLANEMO_ROOT/planemo/wizard/`basename $asset`
done
