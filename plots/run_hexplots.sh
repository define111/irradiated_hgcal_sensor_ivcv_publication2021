#!/usr/bin/env bash
#use Python 2.7 or >=3.6
#tested with ROOT 6.06 and 6.22
#requires hexplot, make sure the $HEXPLOT_DIR env is set

action() {
    local src_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && /bin/pwd )"
    local origin="$( pwd )"

    export PYTHONPATH=$PWD:$PYTHONPATH;
    export DATA_DIR=$PWD/../data/ivcv_irradiated_2021;

    cd "$src_dir"
    (
        echo "HELLO"
        python iv_hexplots/hexplots.py;
        
    )    

    cd "$origin"
}
action "$@"  