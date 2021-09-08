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

MEASUREMENTS = {
    "1002": {
        "MeasID": "8in_198ch_2019_1002_65E13_neg40_annealed68min_October2020_chucktempcorrected",
        "Campaign": "October2020_ALPS", 
        "SensorType": "LD",
        "zmax": 1.15,
        "Title": "LD, 300 #mum, 6.5E14 neq/cm^{2}"
    },
    "3003": {
        "MeasID": "8in_432_3003_1E16_neg40deg_new_picoammeter_Winter2021_chucktempcorrected",
        "Campaign": "Winter2021", 
        "SensorType": "HD",
        "zmax": 2.85,
        "Title": "HD, 120 #mum, 1E16 neq/cm^{2}"
    },
    "2004": {
        "MeasID": "8in_198ch_2019_2004_25E14_neg40_80minAnnealing_chucktempcorrected",
        "Campaign": "Spring2021_ALPS", 
        "SensorType": "LD",
        "zmax": 2.75,
        "Title": "LD, 200 #mum, 2.5E15 neq/cm^{2}"
    },
    "3009": {
        "MeasID": "8in_432_3009_5E15_neg40_post80minAnnealing_chucktempcorrected",
        "Campaign": "June2021_ALPS", 
        "SensorType": "HD",
        "zmax": 1.7,
        "Title": "HD, 120 #mum, 5E15 neq/cm^{2}"
    },
    "1013": {
        "MeasID": "8in_198ch_2019_1013_1E15_neg40_post80minAnnealing_chucktempcorrected",
        "Campaign": "June2021_ALPS", 
        "SensorType": "LD",
        "zmax": 1.4,
        "Title": "LD, 300 #mum, 1E15 neq/cm^{2}"
    },
    "0541_04": {
        "MeasID": "8in_198ch_2019_N0541_04_25E14_neg40_post80minAnnealing_chucktempcorrected",
        "Campaign": "June2021_ALPS", 
        "SensorType": "LD",
        "zmax": 2.5,
        "Title": "LD, 200 #mum, 2.5E15 neq/cm^{2}"
    }
}
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
HEXPLOTCOMMAND = HEXPLOTCOMMAND.replace("<ZMIN>", "0.5")


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

    GEOFILE = "hex_positions_HPK_198ch_8inch_edge_ring_testcap.txt" if SensorType == "LD" else "hex_positions_HPK_432ch_8inch_edge_ring_testcap.txt"
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
        thisdir, "%s.pdf" % ID)
    tmp_file_path = lcurr_vis_path.replace(".pdf", ".txt")
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