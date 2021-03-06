#!/usr/bin/env bash
#use Python 2.7 or >=3.6
#tested with ROOT 6.06 and 6.22
#requires hexplot, make sure the $HEXPLOT_DIR env is set

action() {
    local src_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && /bin/pwd )"
    local origin="$( pwd )"

    export PYTHONPATH=$PWD:$PYTHONPATH;
    export HEXPLOT_DIR=/home/marta/HGCAL_sensor_analysis/;

    export DATA_DIR=$PWD/../data/ivcv_irradiated_2021;
    source /home/marta/root/bin/thisroot.sh; 

    cd "$src_dir"  
    (
        python3 iv_hexplots/hexplots.py;
    )
    # (
    #     python3 Vdep_hexplots/hexplots.py;
    # )     
    # (
    #     python3 annealing_iv/current_vs_annealing.py --EVALVOLTAGE 600;
    #     python3 annealing_iv/current_vs_annealing.py --EVALVOLTAGE -1;
    # )
    # (
    #     python3 annealing_Vdep/Vdep_vs_annealing.py;
    # )     
    # (
    #     python3 Vdep_vs_fluence/Vdep_vs_current.py;
    # )   
    # (
    #     python3 chuck_temp_correction/chuckTemp.py;
    #     python3 chuck_temp_correction/chuckTemp_profile.py;
    # )     
    # (
    #     python3 ch_mapping/channel_mapping.py --geometry LD;
    #     python3 ch_mapping/channel_mapping.py --geometry HD;
    # )    
    cd "$origin"
}
action "$@"  