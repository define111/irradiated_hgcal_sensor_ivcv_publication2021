# Author: Thorben Quast, thorben.quast@cern.ch
# Date: 08 September 2021



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
    "N4790_7": {
        "MeasID": "HPK_8in_198ch_2019_N4790_7_neg40degC_BackSideBiased_80minsAnnealing",
        "Campaign": "RINSC_May2022_ALPS_BacksideBias", 
        "SensorType": "LD",
        "zmax": 6.0,
        "Title": "after additional annealing"
    },
    "N4792_6": {
        "MeasID": "8in_198ch_2019_N4792_6_neg40degC_BackSideBiased_80minsAnnealing",
        "Campaign": "RINSC_May2022_ALPS_BacksideBias", 
        "SensorType": "LD",
        "zmax": 6.0,
        "Title": "after additional annealing"
    },
    
    "N4790_19": {
        "MeasID": "8in_198ch_2019_N4790_19_neg40degC_BackSideBiased_80minsAnnealing",
        "Campaign": "RINSC_May2022_ALPS_BacksideBias", 
        "SensorType": "LD",
        "zmax": 6.0,
        "Title": "after additional annealing"
    },
    
    "N4790_5": {
        "MeasID": "8in_198ch_2019_N4790_05_neg40degC_80minsAnnealing_BackSideBias",
        "Campaign": "RINSC_May2022_ALPS_BacksideBias", 
        "SensorType": "LD",
        "zmax": 4.0,
        "Title": "after additional annealing"
    },
    "N4791_10": {
        "MeasID": "8in_198ch_2019_N4791_10_neg40degC_BackSideBiased_80minsAnnealing",
        "Campaign": "RINSC_May2022_ALPS_BacksideBias", 
        "SensorType": "LD",
        "zmax": 4.0,
        "Title": "after additional annealing"
    },
    
    "N4790_16": {
        "MeasID": "8in_198ch_2019_N4790_16_neg40degC_BackSideBias_115minsAnnealing",
        "Campaign": "RINSC_May2022_ALPS_BacksideBias", 
        "SensorType": "LD",
        "zmax": 4.0,
        "Title": "after additional annealing"
    },
    
    "N4790_09": {
        "MeasID": "HPK_8in_198ch_2019_N4790_9_neg40degC_BackSideBiased_80minsAnnealing",
        "Campaign": "RINSC_May2022_ALPS_BacksideBias", 
        "SensorType": "LD",
        "zmax": 6.5,
        "Title": "after additional annealing"
    },
    "N4790_21": {
        "MeasID": "HPK_8in_198ch_2019_N479021_neg40degC_BackSideBiased_115minsAnnealing",
        "Campaign": "RINSC_May2022_ALPS_BacksideBias", 
        "SensorType": "LD",
        "zmax": 6.5,
        "Title": "after additional annealing"
    },
    "N4792_7": {
        "MeasID": "HPK_8in_198ch_2019_N4792_7_neg40degC_BackSideBiased_80minsAnnealing",
        "Campaign": "RINSC_May2022_ALPS_BacksideBias", 
        "SensorType": "LD",
        "zmax": 6.5,
        "Title": "after additional annealing"
    },

    "N4790_8": {
        "MeasID": "8in_198ch_2019_N4790_8_neg40degC",
        "Campaign": "RINSC_March2022_ALPS", 
        "SensorType": "LD",
        "zmax": 5.0,
        "Title": "after additional annealing"
    },
    "N4792_09": {
        "MeasID": "8in_198ch_2019_N4792_09_neg40degC_noAnnealing",
        "Campaign": "RINSC_March2022_ALPS", 
        "SensorType": "LD",
        "zmax": 5.0,
        "Title": "after additional annealing"
    },
    "N4792_20": {
        "MeasID": "8in_198ch_2019_N4792_20_neg40degC_noAnnealing",
        "Campaign": "RINSC_March2022_ALPS", 
        "SensorType": "LD",
        "zmax": 5.0,
        "Title": "after additional annealing"
    },
    "1013_annealed": {
        "MeasID": "8in_198ch_2019_1013_1E15_neg40_post80minAnnealing_chucktempcorrected",
        "Campaign": "June2021_ALPS", 
        "SensorType": "LD",
        "zmax": 1.62,
        "Title": "after additional annealing"
    },
    "0541_04_annealed": {
        "MeasID": "8in_198ch_2019_N0541_04_25E14_neg40_post80minAnnealing_chucktempcorrected",
        "Campaign": "June2021_ALPS", 
        "SensorType": "LD",
        "zmax": 3.25,
        "Title": "after additional annealing"
    },
    "3009": {
        "MeasID": "8in_432_3009_5E15_neg40_chucktempcorrected",
        "Campaign": "June2021_ALPS", 
        "SensorType": "HD",
        "zmax": 2.12,
        "Title": "120 #mum, ~5.0#times10^{15} neq/cm^{2}"
    },
    "1013": {
        "MeasID": "8in_198ch_2019_1013_1E15_neg40_chucktempcorrected",
        "Campaign": "June2021_ALPS", 
        "SensorType": "LD",
        "zmax": 1.62,
        "Title": "300 #mum, ~0.8#times10^{15} neq/cm^{2}"
    },
    "0541_04": {
        "MeasID": "8in_198ch_2019_N0541_04_25E14_neg40_chucktempcorrected",
        "Campaign": "June2021_ALPS", 
        "SensorType": "LD",
        "zmax": 3.25,
        "Title": "200 #mum, ~1.9#times10^{15} neq/cm^{2}"
    },
    "1105": {
        "MeasID": "8in_198ch_2019_1105_15E14_neg40_postAnnealing_TTU",
        "Campaign": "TTU_October2021",
        "SensorType": "LD",
        "zmax": 2.0,
        "Title": ""
    },
    "1003": {
        "MeasID": "8in_198ch_2019_1003_15E14_neg40_postAnnealing_TTU",
        "Campaign": "TTU_October2021",
        "SensorType": "LD",
        "zmax": 2.0,
        "Title": ""
    },
    "1113": {
        "MeasID": "8in_198ch_2019_1113_15E14_neg40_postAnnealing_TTU",
        "Campaign": "TTU_October2021",
        "SensorType": "LD",
        "zmax": 2.0,
        "Title": ""
    },
    "N0541_17": {
        "MeasID": "8in_198ch_2019_N0541_17_15E14_neg40_postAnnealing_TTU",
        "Campaign": "TTU_October2021",
        "SensorType": "LD",
        "zmax": 2.0,
        "Title": ""
    }    
}


'''
MEASUREMENTS = {
    "3005": {
        "MeasID": "8in_432_3005_25E14_neg40_postAnnealing_TTU",
        "Campaign": "TTU_October2021", 
        "SensorType": "HD",
        "zmax": 1.15,
        "Title": "HD, 120 #mum, 1.65#times10^{15} neq/cm^{2}"
    },
    "3008": {
        "MeasID": "8in_432_3008_25E14_neg40_postAnnealing_TTU",
        "Campaign": "TTU_October2021", 
        "SensorType": "HD",
        "zmax": 1.15,
        "Title": "HD, 120 #mum, 1.65#times10^{15} neq/cm^{2}"
    },
    "3104": {
        "MeasID": "8in_432_3104_25E14_neg40_postAnnealing_TTU",
        "Campaign": "TTU_October2021", 
        "SensorType": "HD",
        "zmax": 1.15,
        "Title": "HD, 120 #mum, 1.65#times10^{15} neq/cm^{2}"
    },
    "3105": {
        "MeasID": "8in_432_3105_25E14_neg40_postAnnealing_TTU",
        "Campaign": "TTU_October2021", 
        "SensorType": "HD",
        "zmax": 1.15,
        "Title": "HD, 120 #mum, 1.65#times10^{15} neq/cm^{2}"
    }  
}
'''  
EVALVOLTAGE = 600

HEXPLOTCOMMAND = "<HEXPLOTDIR>/bin/HexPlot \
                -g <HEXPLOTDIR>/geo/<GEOFILE> \
                -i <INPUTFILE> \
                -o <OUTPUTFILE> \
                --if <FORMAT> \
                --CV -p GEO  --colorpalette <COLORPALETTE>\
                --vn 'Capacitance:<DEF>:<UNIT>' --select <VOLTAGE>\
                --addLabel '<TITLE>'\
                -z <ZMIN>:<ZMAX>"
                
HEXPLOTCOMMAND = HEXPLOTCOMMAND.replace("<HEXPLOTDIR>", os.environ["HEXPLOT_DIR"])
HEXPLOTCOMMAND = HEXPLOTCOMMAND.replace("<VOLTAGE>", str(EVALVOLTAGE))
HEXPLOTCOMMAND = HEXPLOTCOMMAND.replace("<COLORPALETTE>", "57")
HEXPLOTCOMMAND = HEXPLOTCOMMAND.replace("<UNIT>", "#muA")
HEXPLOTCOMMAND = HEXPLOTCOMMAND.replace("<FORMAT>", "PADNUM:SELECTOR:VAL")
HEXPLOTCOMMAND = HEXPLOTCOMMAND.replace("<DEF>", "I_{pad, -40^{#circ} C}")
HEXPLOTCOMMAND = HEXPLOTCOMMAND.replace("<ZMIN>", "0.25")


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
    print(os.environ["DATA_DIR"])
    infile = ROOT.TFile(infilepath, "READ")


    # retrieve sensor information

    GEOFILE = GEOFILES[SensorType]
    NCHANNELS = 199 if SensorType == "LD" else 444
    ZMAX = measurement["zmax"]
    
    # determine per-channel leakage current at common voltage (EVALVOLTAGE)
    # not a fit here, but infrastructure in place in case a
    lfti = ROOT.TF1("pol1", "pol1", EVALVOLTAGE-120., EVALVOLTAGE+70.)

    tmp_data = []
    for CHANNEL in range(1, NCHANNELS):
        canvas = ROOT.TCanvas()
        try:
            gr = infile.Get("IV_uncorrected_channel%i" % CHANNEL)
            gr.GetXaxis().SetTitle(

                "Effective bias voltage (HV resistance-corrected) [V]")
        except:
            continue
        gr.GetYaxis().SetTitle(
            "Leakage current at -40^{#circ}C [#muA]")
        gr.GetXaxis().SetTitleSize(1.5*gr.GetXaxis().GetTitleSize())
        gr.GetXaxis().SetLabelSize(1.5*gr.GetXaxis().GetLabelSize())
        gr.GetYaxis().SetTitleSize(1.5*gr.GetYaxis().GetTitleSize())
        gr.GetYaxis().SetLabelSize(1.5*gr.GetYaxis().GetLabelSize())
        gr.SetMarkerColor(ROOT.kBlue+2)
        gr.SetMarkerSize(2)
        gr.SetLineWidth(2)
        gr.SetLineColor(ROOT.kBlue+2)
        lfti.SetLineColor(ROOT.kBlue+2)
        gr.Fit(lfti, "RQ")

        # compute ratios and save as file
        lcurr = lfti.Eval(EVALVOLTAGE)

        # position not really useful because coordinate system center not quite in center
        tmp_data.append((CHANNEL, EVALVOLTAGE, lcurr))

    _df = pd.DataFrame(tmp_data, columns=[
        "channel", "U", "I"])

    lcurr_vis_path = os.path.join(
        thisdir, "%s.png" % ID)
    tmp_file_path = lcurr_vis_path.replace(".png", ".txt")
    np.savetxt(tmp_file_path, _df)

    this_cmd = HEXPLOTCOMMAND
    this_cmd = this_cmd.replace("<INPUTFILE>", tmp_file_path)
    this_cmd = this_cmd.replace("<OUTPUTFILE>", lcurr_vis_path)
    this_cmd = this_cmd.replace("<GEOFILE>", GEOFILE)
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
    os.remove(tmp_file_path)