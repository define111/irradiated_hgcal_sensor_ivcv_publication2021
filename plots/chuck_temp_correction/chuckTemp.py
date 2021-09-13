# Author: Thorben Quast, thorben.quast@cern.ch
# Date: 07 May 2021

# -computes leakage current ratios of 8inch LD sensor 1004 with three different orientations
# -the leakage current ratios serve as an estimate for a relative temperature difference
# -hereby, a temperature needs to be assumed for one of the three symmetry sectors of the chuck
# -all three symmetry sectors of the silicon sensor can be used for inference of the temperature ratios
# -they should give comparable results if the leakage current difference is dominated by some chuck temperature profile

import sys
import os
from subprocess import Popen
import numpy as np
import pandas as pd

import common as cm
ROOT = cm.ROOT
ROOT.gROOT.SetBatch(True)
cm.setup_style()

import os
thisdir = os.path.dirname(os.path.realpath(__file__))

from common.meta import rot
from common.util import deltaT

TREF = -40
EVALVOLTAGE = 600
NCHANNELS = 199
CAMPAIGN = "Spring2021_ALPS"
ROT = 120



for chucktemp_corrected in [False, True]:
    postfix = "_chucktempcorrected" if chucktemp_corrected else ""
    MEASUREMENTS = []
    MEASUREMENTS.append(("8in_198ch_2019_2109_25E14_neg40_post80minAnnealing" + postfix, 0))
    MEASUREMENTS.append(("8in_198ch_2019_2109_25E14_neg40_post80minAnnealing_rot120deg_acw" + postfix, 120))
    MEASUREMENTS.append(("8in_198ch_2019_2109_25E14_neg40_post80minAnnealing_rot240deg_acw" + postfix, 240))


    # plotting of ratios with hexplot
    HEXPLOTCOMMAND = "<HEXPLOTDIR>/bin/HexPlot \
                    -g <HEXPLOTDIR>/geo/<GEOFILE> \
                    -i <INPUTFILE> \
                    -o <OUTPUTFILE> \
                    --if <FORMAT> \
                    --CV -p GEO  --colorpalette <COLORPALETTE>\
                    --vn 'Capacitance:<DEF>:<UNIT>' --select <VOLTAGE>\
                    -z <ZMIN>:<ZMAX>".replace("<HEXPLOTDIR>", os.environ["HEXPLOT_DIR"]).replace("<GEOFILE>", "hex_positions_HPK_198ch_8inch_edge_ring_testcap.txt")

    # get geometry mapping
    geofile = "<HEXPLOTDIR>/geo/<GEOFILE>".replace("<HEXPLOTDIR>", os.environ["HEXPLOT_DIR"]).replace("<GEOFILE>", "hex_positions_HPK_198ch_8inch_edge_ring_testcap.txt")
    geomap = pd.DataFrame(np.genfromtxt(geofile, usecols=(0, 1, 2), dtype=[("padnr", int), ("x", float), ("y", float)]))


    tmp_data = []
    for measID, rotation in MEASUREMENTS:
        # retrieve paths of processed files as input
        infile = ROOT.TFile(os.path.join(
            os.environ["DATA_DIR"], "iv/%s/channelIV/%s/TGraphErrors.root" % (CAMPAIGN, measID)), "READ")

        # retrieve information from db

        # determine per-channel leakage current at common voltage (EVALVOLTAGE)
        # not a fit here, but infrastructure in place in case a
        lfti = ROOT.TF1("pol1", "pol1", EVALVOLTAGE-70., EVALVOLTAGE+70.)

        for CHANNEL in range(1, NCHANNELS):
            canvas = ROOT.TCanvas()
            gr = infile.Get("IV_uncorrected_channel%i" % CHANNEL)
            gr.Fit(lfti, "RQ")

            # compute ratios and save as file
            lcurr = lfti.Eval(EVALVOLTAGE)


            # rotation not really useful because coordinate system center not quite in center
            tmp_data.append((CHANNEL, EVALVOLTAGE, lcurr, rotation))

    _df = pd.DataFrame(tmp_data, columns=[
        "channel", "U", "I", "rot"])

    ratios = []



    # input ratios
    for _index in range(len(rot[0])):
        _ch_rot0 = rot[0][_index]
        _ch_rot120 = rot[120][_index]
        _ch_rot240 = rot[240][_index]

        x_ch_rot0, y_ch_rot0 = (geomap[geomap.padnr ==
                    _ch_rot0].x.iloc[0], geomap[geomap.padnr == _ch_rot0].y.iloc[0])
        x_ch_rot120, y_ch_rot120 = (geomap[geomap.padnr ==
                                        _ch_rot120].x.iloc[0], geomap[geomap.padnr == _ch_rot120].y.iloc[0])
        x_ch_rot240, y_ch_rot240 = (geomap[geomap.padnr ==
                                        _ch_rot240].x.iloc[0], geomap[geomap.padnr == _ch_rot240].y.iloc[0])

        I_rot0 = np.array(
            _df.loc[(_df.U == EVALVOLTAGE) & (_df.channel == _ch_rot0) & (_df.rot == ROT)].I)[0]
        I_rot120 = np.array(
            _df.loc[(_df.U == EVALVOLTAGE) & (_df.channel == _ch_rot120) & (_df.rot == (ROT+120) % 360)].I)[0]
        I_rot240 = np.array(
            _df.loc[(_df.U == EVALVOLTAGE) & (_df.channel == _ch_rot240) & (_df.rot == (ROT+240) % 360)].I)[0]

        #left-most sector is the reference
        I_ref = I_rot120
        ch_ref = _ch_rot120
        x_ref = x_ch_rot120
        y_ref = y_ch_rot120
            
        ratios.append((_ch_rot0, EVALVOLTAGE, 100. *
                        (I_rot0-I_ref)/I_ref, deltaT(I_rot0, I_ref), ROT, x_ch_rot0, y_ch_rot0, ch_ref, x_ref, y_ref))
        ratios.append((_ch_rot120, EVALVOLTAGE, 100. *
                        (I_rot120-I_ref)/I_ref, deltaT(I_rot120, I_ref), ROT, x_ch_rot120, y_ch_rot120, ch_ref, x_ref, y_ref))
        ratios.append((_ch_rot240, EVALVOLTAGE, 100. *
                        (I_rot240-I_ref)/I_ref, deltaT(I_rot240, I_ref), ROT, x_ch_rot240, y_ch_rot240, ch_ref, x_ref, y_ref))

    ratio_vis_path = os.path.join(thisdir, CAMPAIGN+postfix+".pdf")
    tmp_file_path = ratio_vis_path.replace(".pdf", ".txt")
    _ratio_df = pd.DataFrame(ratios, columns=["channel", "U", "ratio", "dT", "ROT", "x", "y", "channel_ref", "x_ref", "y_ref"])
    _ratio_df[_ratio_df.ROT == ROT].to_csv(tmp_file_path, sep=" ", header=None)

    this_cmd = HEXPLOTCOMMAND
    this_cmd = this_cmd.replace("<INPUTFILE>", tmp_file_path)
    this_cmd = this_cmd.replace("<OUTPUTFILE>", ratio_vis_path)
    this_cmd = this_cmd.replace("<VOLTAGE>", str(EVALVOLTAGE))
    this_cmd = this_cmd.replace("<COLORPALETTE>", "104")
    this_cmd = this_cmd.replace("<UNIT>", "^{#circ}C")
    this_cmd = this_cmd.replace("<FORMAT>", "null:PADNUM:SELECTOR:null:VAL:null:null:null")
    this_cmd = this_cmd.replace("<DEF>", "#DeltaT (T_{ref}=-40^{#circ}C)")
    this_cmd = this_cmd.replace("<ZMIN>", "-1.2")
    this_cmd = this_cmd.replace("<ZMAX>", "1.2")

    env = {}
    env.update(os.environ)
    p = Popen(this_cmd, stdout=sys.stdout,
                stderr=sys.stderr, shell=True, env=env)
    out, err = p.communicate()
    code = p.returncode
    if code != 0:
        raise Exception("Hexplot plotting failed")
    os.remove(tmp_file_path)
