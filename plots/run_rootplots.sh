#!/usr/bin/env bash
#use Python >=3.6
#tested with 6.06 and 6.22

action() {
    local src_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && /bin/pwd )"
    local origin="$( pwd )"

    export PYTHONPATH=$PWD:$PYTHONPATH;
    export DATA_DIR=$PWD/../data/ivcv_irradiated_2021;

    cd "$src_dir"
    (
        python3 total_iv/overlay.py --type good;
        python3 total_iv/overlay.py --type bad;
    ) 
    (
        python3 channel_iv/overlay.py --type sensors;
        python3 channel_iv/overlay.py --type channels;
    )
    (
        python3 channel_cv/overlay_CV.py --type sensors;
        python3 channel_cv/overlay_CV.py --type channels;
        python3 channel_cv/overlay_invCV.py --type sensors;
        python3 channel_cv/overlay_invCV.py --type channels;        
    )

    cd "$origin"
}
action "$@"  