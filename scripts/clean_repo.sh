#!/usr/bin/env bash

action() {
    local base="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && /bin/pwd )"
    local origin="$( /bin/pwd )"

    local cache_only="$1"

    local project_dir="$( dirname "$base" )"
    cd "$project_dir"

    rm -rf \
        *.aux \
        *.bbl \
        *.bcf \
        *.blg \
        *.fdb_latexmk \
        *.fls \
        *.gz \
        *.log \
        *.out \
        *.toc

    if [ "$cache_only" != "1" ]; then
        rm -rf \
            *.dvi \
            *.eps \
            *.ilg \
            *.lof \
            *.lot \
            *.mp \
            *.pyg \
            *.t1 \
            *.1 \
            _minted-thesis
    else
        echo "clean only cache files, skip other files"
    fi

    cd "$origin"
}
action "$@"
