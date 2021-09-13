# Author: Thorben Quast, thorben.quast@cern.ch
# Date: 10 September 2021

import pandas as pd
import numpy as np

import common as cm
ROOT = cm.ROOT
ROOT.gROOT.SetBatch(True)
cm.setup_style()

import os
thisdir = os.path.dirname(os.path.realpath(__file__))

from copy import deepcopy
from common.util import *


#measurement specifics
_measID = "8in_198ch_2019_2004_25E14_neg40"
Campaign = "Spring2021_ALPS"
name = "annealing_current"

EVALVOLTAGE = 600

hexplot_geo_file_path = os.path.join(os.environ["HEXPLOT_DIR"], "geo", "hex_positions_HPK_198ch_8inch_edge_ring_testcap.txt")
#load geometry mapping
geo_mapping = pd.DataFrame(np.genfromtxt(open(hexplot_geo_file_path, "r"), skip_header=7, usecols=(0, 1, 2, 3), dtype=[("channel", "i4"), ("x", "f8"), ("y", "f8"), ("type", "i4")]))


#prepare the canvas
canvas = ROOT.TCanvas("Canvas" + name, "canvas" + name, cm.default_canvas_width, cm.default_canvas_height)
cm.setup_canvas(canvas, cm.default_canvas_width, cm.default_canvas_height)
canvas.Divide(1)
pad = canvas.GetPad(1)
cm.setup_pad(pad)
pad.cd()


# determine per-channel leakage current at common voltage (EVALVOLTAGE)
lfti = ROOT.TF1("pol1", "pol1", EVALVOLTAGE-120., EVALVOLTAGE+70.)
tmp_data = []

for annealing in [0, 9, 24, 61, 80]:
    postfix = ""
    if annealing > 0:
        postfix = "_%iminAnnealing" % annealing
    measID = _measID+postfix+"_chucktempcorrected"

    # retrieve paths of processed files as input
    infile = ROOT.TFile(os.path.join(
        os.environ["DATA_DIR"], "iv/%s/channelIV/%s/TGraphErrors.root" % (Campaign, measID)), "READ")

    for CHANNEL in range(1, 199):
        geotype = np.array(geo_mapping.type[geo_mapping.channel==CHANNEL])[0]
        if geotype!=0:  #not a full cell
            continue            
        try:
            gr = infile.Get("IV_uncorrected_channel%i" % CHANNEL)
            gr.GetXaxis().SetTitle(
                "Effective bias voltage (HV resistance-corrected) [V]")
        except:
            continue

        gr.Fit(lfti, "RQ")

        # compute ratios and save as file
        lcurr = lfti.Eval(EVALVOLTAGE)

        # position not really useful because coordinate system center not quite in center
        tmp_data.append((annealing, CHANNEL, EVALVOLTAGE, lcurr))

_df = pd.DataFrame(tmp_data, columns=["annealingMin", "channel", "U", "I"])

legend1 = ROOT.TLegend(*cm.calc_legend_pos(10, x1=0.6, x2=0.9, y2=0.87))
cm.setup_legend(legend1)
legend1.SetNColumns(2)

#create the graphs
graphs = {}
for draw_index, _channel in enumerate(_df.channel.unique()):
    if (draw_index % 8) != 3:
        continue

    channel_data = _df[_df.channel==_channel]
    annealingMin = np.array(channel_data.annealingMin)
    I = np.array(channel_data.I)
    I = I/I[0]*100.
    graphs[_channel] = ROOT.TGraph()
    NGraphs = len([key for key in graphs])
    for i in range(len(channel_data)):
        graphs[_channel].SetPoint(graphs[_channel].GetN(), annealingMin[i]*1., I[i]*1.)
    
    cm.setup_graph(graphs[_channel])
    graphs[_channel].SetMarkerStyle(19+NGraphs%11)
    graphs[_channel].SetMarkerColor((NGraphs-1)%9+1)
    graphs[_channel].SetLineColor((NGraphs-1)%9+1)

    graphs[_channel].GetYaxis().SetRangeUser(72., 101.)
    xaxis_title = "t = Addtional annealing at +60^{#circ} C (min)"
    cm.setup_x_axis(graphs[_channel].GetXaxis(), pad, {"Title": xaxis_title, "TitleOffset": 0.90*graphs[_channel].GetXaxis().GetTitleOffset()})
    yaxis_title = "I_{pad, -40^{#circ}C}(t, %i V)/I_{pad, -40^{#circ}C}(t=0, %i V)" % (EVALVOLTAGE, EVALVOLTAGE)+"[%]"
    cm.setup_y_axis(graphs[_channel].GetYaxis(), pad, {"Title": yaxis_title})
        
    if NGraphs==1:
        graphs[_channel].Draw("APL")
    else:
        graphs[_channel].Draw("PLSAME")
    
    legend1.AddEntry(graphs[_channel], "pad %i" % _channel)

    if NGraphs == 20:
        break
    
    

canvas.cd()
# cms label
cms_labels = cm.create_cms_labels()
cms_labels.Draw()

# campaign label
campaign_label = cm.create_campaign_label()
campaign_label.Draw()

label = ROOT.TLatex(0.6, 0.88, "LD, 200 #mum, 2.5E15 neq")
cm.setup_label(label, {"TextFont": 73})
label.Draw()

legend1.Draw()

pad.SetGrid(True)
#save pdf
canvas.Print(os.path.join(thisdir, "{}.pdf".format(name)))

