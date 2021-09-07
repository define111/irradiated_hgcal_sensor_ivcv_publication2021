#!/usr/bin/env bash
#use Python >=2.7
#tested with ROOT 5.34 and ROOT 6.14

action() {
    local src_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && /bin/pwd )"
    local origin="$( pwd )"

    export PYTHONPATH=$PWD:$PYTHONPATH;
    export DATA_DIR=$PWD/../data/ivcv_irradiated_2021;

    cd "$src_dir"
    # (example) IV summary plots, responsible: T. Quast, last modification: 15 Jan 2020
    (
        python3 total_iv/overlay.py;
    )    

    cd "$origin"
}
action "$@"  