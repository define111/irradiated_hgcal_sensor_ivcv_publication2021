#!/usr/bin/env bash
#use Python >=2.7
#tested with ROOT 5.34 and ROOT 6.14

action() {
    local src_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && /bin/pwd )"
    local origin="$( pwd )"

    cd "$src_dir"
    # (example) IV summary plots, responsible: T. Quast, last modification: 15 Jan 2020
    (
        python example_IV_summary/plot.py;
    )    
    # (example) Individual CV plots, responsible: T. Quast, last modification: 15 Jan 2020
    (
        python example_CV_individual/plot.py;
    )
    # (example) Individual CV depletion, responsible: T. Quast, last modification: 15 Jan 2020
    (
        python example_CV_depletion/plot.py;
    )  

    cd "$origin"
}
action "$@"  