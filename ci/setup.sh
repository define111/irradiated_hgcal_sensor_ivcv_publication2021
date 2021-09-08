#created: 07 September 2021
#by Thorben Quast, thorben.quast@cern.ch
#underlying docker image: thorbenquast/lcd_hgc_ana 

export ROOT_SOURCE="/software/ROOT_6_06_06/bin/thisroot.sh";
export HEXPLOT_DIR="/software/hexplot";
export WORKFLOW_DIR="$PWD";

source ${ROOT_SOURCE};
