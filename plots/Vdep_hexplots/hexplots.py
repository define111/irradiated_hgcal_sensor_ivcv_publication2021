# Author: Thorben Quast, thorben.quast@cern.ch
# Date: 10 September 2021



import common as cm
ROOT = cm.ROOT
ROOT.gROOT.SetBatch(True)
cm.setup_style()

import os, sys
thisdir = os.path.dirname(os.path.realpath(__file__))

from subprocess import Popen
import numpy as np
import pandas as pd

from common.meta import GEOFILES

MEASUREMENTS = {
    "0541_04": {
        "MeasID": "8in_198ch_2019_N0541_04_25E14_neg40_post80minAnnealing",
        "Campaign": "June2021_ALPS", 
        "SensorType": "LD",
        "zmin": 217,
        "zmax": 276,
        "Title": "LD, 200 #mum, 1.9#times10^{15} neq/cm^{2}"
    },
}
EVALVOLTAGE = 600


HEXPLOTCOMMAND = "<HEXPLOTDIR>/bin/HexPlot \
                -g <HEXPLOTDIR>/geo/<GEOFILE> \
                -i <INPUTFILE> \
                -o <OUTPUTFILE> \
                --if <FORMAT> \
                --nd 0 \
                --noinfo \
                --CV -p GEO  --colorpalette <COLORPALETTE>\
                --vn 'Capacitance:<DEF>:<UNIT>' --select <VOLTAGE>\
                --addLabel '<TITLE>'\
                -z <ZMIN>:<ZMAX>"
                
HEXPLOTCOMMAND = HEXPLOTCOMMAND.replace("<HEXPLOTDIR>", os.environ["HEXPLOT_DIR"])
HEXPLOTCOMMAND = HEXPLOTCOMMAND.replace("<VOLTAGE>", "0")
HEXPLOTCOMMAND = HEXPLOTCOMMAND.replace("<COLORPALETTE>", "62")
HEXPLOTCOMMAND = HEXPLOTCOMMAND.replace("<UNIT>", "V")
HEXPLOTCOMMAND = HEXPLOTCOMMAND.replace("<FORMAT>", "null:PADNUM:SELECTOR:VAL")
HEXPLOTCOMMAND = HEXPLOTCOMMAND.replace("<DEF>", "U_{dep} estimate")


for ID in MEASUREMENTS:
    measurement = MEASUREMENTS[ID]
    measID = measurement["MeasID"]
    Campaign = measurement["Campaign"]
    SensorType = measurement["SensorType"]
    Title = measurement["Title"]

    # retrieve paths of processed files as input
    infilepath = os.path.join(os.environ["DATA_DIR"], "iv/<CAMPAIGN>/channelIV/<MEASID>/TGraphErrors.root")
    infilepath = infilepath.replace("<CAMPAIGN>", Campaign)
    infilepath = infilepath.replace("<MEASID>", measID)
    infile = ROOT.TFile(infilepath, "READ")

    # retrieve sensor information

    GEOFILE = GEOFILES[SensorType]
    NCHANNELS = 199 if SensorType == "LD" else 444
    ZMIN = measurement["zmin"]
    ZMAX = measurement["zmax"]
    

    _Vdep_type = "serial"
    if Campaign == "TTU_October2021":
        _Vdep_type = "parallel"
    infile_path = os.path.join(os.environ["DATA_DIR"], "cv/%s/Vdep/%s/Vdep_%s.txt" % (Campaign, measID, _Vdep_type))
    infile_path_tmp = infile_path.replace(".txt", "_tmp.txt")

    #reject the bad channels
    data_in = pd.DataFrame(np.genfromtxt(infile_path, usecols=(1,2,3), skip_header=1), columns=["Pad", "Dummy", "Vdep"])
    data_in.to_csv(infile_path_tmp, sep=",")
    with open(infile_path_tmp, "r") as tmp_file:
        tmp_data = tmp_file.read()
    os.remove(infile_path_tmp)
    tmp_data = tmp_data.replace(",", "    ")
    with open(infile_path_tmp, "w") as tmp_file:
        tmp_file.write(tmp_data)    


    lcurr_vis_path = os.path.join(
        thisdir, "%s.pdf" % ID)

    this_cmd = HEXPLOTCOMMAND
    this_cmd = this_cmd.replace("<INPUTFILE>", infile_path_tmp)
    this_cmd = this_cmd.replace("<OUTPUTFILE>", lcurr_vis_path)
    this_cmd = this_cmd.replace("<GEOFILE>", GEOFILE)
    this_cmd = this_cmd.replace("<ZMIN>", "%s" % ZMIN)
    this_cmd = this_cmd.replace("<ZMAX>", "%s" % ZMAX)
    this_cmd = this_cmd.replace("<TITLE>", Title)

    env = {}
    env.update(os.environ)
    p = Popen(this_cmd, stdout=sys.stdout,
            stderr=sys.stderr, shell=True, env=env)
    out, err = p.communicate()
    code = p.returncode
    if code != 0:
        raise Exception("Hexplot plotting failed")