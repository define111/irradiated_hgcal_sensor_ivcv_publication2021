# Author: Thorben Quast, thorben.quast@cern.ch
# Date: 06 May 2021
#

import numpy as np
import pandas as pd

import common as cm
ROOT = cm.ROOT
ROOT.gROOT.SetBatch(True)
cm.setup_style()
ROOT.gStyle.SetPalette(ROOT.kBird)

import os
thisdir = os.path.dirname(os.path.realpath(__file__))

from common.meta import MEASUREMENTS
from math import sqrt, cos, sin


from common.meta import *

EVALVOLTAGE = 600


tmp_data = []
outfile = ROOT.TFile(os.path.join(thisdir, "fits.root"), "RECREATE")
outfile.Close()

XMINMAX = {
    "5414": (1.94, 2.55),
    "1002": (0.861, 1.12)
}

YMINMAX = {
    "5414": (238., 280.),
    "1002": (350., 420.)
}


for _ID in ["5414", "1002"]:
    Campaign = MEASUREMENTS[_ID]["Campaign"]
    Geometry = MEASUREMENTS[_ID]["Design"]
    measID = MEASUREMENTS[_ID]["ID"]

    xmin, xmax = XMINMAX[_ID]
    ymin, ymax = YMINMAX[_ID]

    # retrieve leakage currents
    infile_1 = ROOT.TFile(os.path.join(
        os.environ["DATA_DIR"], "iv/%s/channelIV/%s/TGraphErrors.root" % (Campaign, measID)), "READ")

    # retrieve depletion voltage 
    datapath = os.path.join(os.environ["DATA_DIR"], "cv/%s/Vdep/%s/Vdep_serial.txt" % (Campaign, measID.replace("_chucktempcorrected", "")))
    VdepData = np.genfromtxt(datapath, skip_header=1, usecols=(1, 3))

    #retrieve information from db
    hexplot_geo_file_path = os.path.join(os.environ["HEXPLOT_DIR"], "geo", "hex_positions_HPK_198ch_8inch_edge_ring_testcap.txt")

    #load geometry mapping
    geo_mapping = pd.DataFrame(np.genfromtxt(open(hexplot_geo_file_path, "r"), skip_header=7, usecols=(0, 1, 2, 3), dtype=[("channel", "i4"), ("x", "f8"), ("y", "f8"), ("type", "i4")]))

    #determine per-channel leakage current at common voltage (EVALVOLTAGE)
    lin_fit_1 = ROOT.TF1("pol0_1", "pol0", EVALVOLTAGE-50., EVALVOLTAGE+50.)				#not a fit here, but infrastructure in place in case a


    h2_ = ROOT.TH2F("h2_%s"%measID, "h2_%s"%measID, int((xmax-xmin)*100), xmin, xmax, int(ymax-ymin), ymin, ymax)

    for _entry in VdepData:
        _ch = int(_entry[0])
        _geotype = np.array(geo_mapping.type[geo_mapping.channel==_ch])[0]
        if _geotype != 0:
            continue
        _Vdep = _entry[1]

        graph_1 = infile_1.Get("IV_uncorrected_channel%i" % _ch)
        graph_1.Fit(lin_fit_1, "RQ")
        #interpolate to EVALVOLTAGE
        I_1 = lin_fit_1.Eval(EVALVOLTAGE)

        h2_.Fill(I_1, _Vdep)



    name = "Vdep_vs_current_%s" %  _ID
    #prepare the canvas
    canvas = ROOT.TCanvas("Canvas" + name, "canvas" + name, cm.default_canvas_width, cm.default_canvas_height)
    cm.setup_canvas(canvas, cm.default_canvas_width, cm.default_canvas_height)
    canvas.Divide(1)
    pad = canvas.GetPad(1)
    cm.setup_pad(pad)
    pad.cd()

    cm.setup_graph(h2_)
    cm.setup_x_axis(h2_.GetXaxis(), pad, {"Title": "I_{pad, -40^{#circ}C}(600 V) (#muA)"})
    cm.setup_y_axis(h2_.GetYaxis(), pad, {"Title": "U_{dep} estimate (V)"})	

    h2_.Draw("COL")

    profile_x = h2_.ProfileX()
    cm.setup_graph(profile_x, {"MarkerColor": ROOT.kBlack, "MarkerStyle": 20, "MarkerSize": 2})
    profile_x.Draw("SAME")

    f1_linfit = ROOT.TF1("f1", "pol1", xmin, xmax)
    cm.setup_graph(f1_linfit, {"LineColor": ROOT.kRed+1, "LineWidth": 3, "LineStyle": 2})
    profile_x.Fit(f1_linfit, "RQN")
    f1_linfit.Draw("SAME")


    legend = ROOT.TLegend(*cm.calc_legend_pos(3, x1=0.13, x2=0.65, y2=0.9))
    cm.setup_legend(legend)
    legend.AddEntry(profile_x, "Data", "pl")
    legend.AddEntry(f1_linfit, "Fit: #DeltaU_{dep}/#DeltaI_{pad, -40^{#circ}C} = %.1f V/#muA" % f1_linfit.GetParameter(1))
    legend.Draw()

    canvas.cd()
    # cms label
    cms_labels = cm.create_cms_labels()
    cms_labels.Draw()

    # campaign label
    campaign_label = cm.create_campaign_label()
    campaign_label.Draw()

    textlabel = {"5414": "LD, 200 #mum, 2.5E15 neq", "1002": "LD, 300 #mum, 6.5E14 neq"}[_ID]
    label = ROOT.TLatex(0.45, 0.9, textlabel)
    cm.setup_label(label, {"TextAlign": 31, "TextFont": 73})
    label.Draw()

    pad.SetGrid(True)
    #save pdf
    canvas.Print(os.path.join(thisdir, "{}.pdf".format(name)))


