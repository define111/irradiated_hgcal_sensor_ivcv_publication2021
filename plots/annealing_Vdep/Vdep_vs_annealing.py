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

hexplot_geo_file_path = os.path.join(os.environ["HEXPLOT_DIR"], "geo", "hex_positions_HPK_198ch_8inch_edge_ring_testcap.txt")

#load geometry mapping and determine non-full cells
geo_mapping = pd.DataFrame(np.genfromtxt(open(hexplot_geo_file_path, "r"), skip_header=7, usecols=(0, 1, 2, 3), dtype=[("channel", "i4"), ("x", "f8"), ("y", "f8"), ("type", "i4")]))
NONFULLCELLS = []
for CHANNEL in range(1, 199):
    geotype = np.array(geo_mapping.type[geo_mapping.channel==CHANNEL])[0]
    if geotype!=0:  #not a full cell
        NONFULLCELLS.append(CHANNEL)  



name = "annealing_Vdep"
#prepare the canvas
canvas = ROOT.TCanvas("Canvas" + name, "canvas" + name, cm.default_canvas_width, cm.default_canvas_height)
cm.setup_canvas(canvas, cm.default_canvas_width, cm.default_canvas_height)
canvas.Divide(1)
pad = canvas.GetPad(1)
cm.setup_pad(pad)
pad.cd()


# determine per-channel leakage current at common voltage (EVALVOLTAGE)
tmp_data = []

for annealing in [0, 9, 24, 61, 80]:
    postfix = ""
    if annealing > 0:
        postfix = "_%iminAnnealing" % annealing
    measID = _measID+postfix


    infile_path = os.path.join(os.environ["DATA_DIR"], "cv/%s/Vdep/%s/Vdep_serial.txt" % (Campaign, measID))

    #reject the bad channels
    data_in = pd.DataFrame(np.genfromtxt(infile_path, usecols=(1,2,3), skip_header=1), columns=["Pad", "Dummy", "Vdep"])
    data_in = data_in[~data_in.Pad.isin(NONFULLCELLS)]
    data_in = data_in.drop(columns=["Dummy"])
    data_in = data_in.assign(annealingMin=annealing)

    tmp_data.append(data_in)

_df = pd.concat(tmp_data)

legend1 = ROOT.TLegend(*cm.calc_legend_pos(10, x1=0.6, x2=0.9, y2=0.87))
cm.setup_legend(legend1)
legend1.SetNColumns(2)

#create the graphs
graphs = {}
for draw_index, _channel in enumerate(_df.Pad.unique()):
    if (draw_index % 8) != 3:
        continue

    channel_data = _df[_df.Pad==_channel]
    annealingMin = np.array(channel_data.annealingMin)
    Vdep = np.array(channel_data.Vdep)
    graphs[_channel] = ROOT.TGraph()
    NGraphs = len([key for key in graphs])
    for i in range(len(channel_data)):
        if Vdep[i]*1. < 100:
            continue
        graphs[_channel].SetPoint(graphs[_channel].GetN(), annealingMin[i]*1., Vdep[i]*100./Vdep[0])
    cm.setup_graph(graphs[_channel])
    graphs[_channel].SetMarkerStyle(19+NGraphs%11)
    graphs[_channel].SetMarkerColor((NGraphs-1)%9+1)
    graphs[_channel].SetLineColor((NGraphs-1)%9+1)

    xaxis_title = "t = Addtional annealing at +60^{#circ} C (min)"
    cm.setup_x_axis(graphs[_channel].GetXaxis(), pad, {"Title": xaxis_title, "TitleOffset": 0.90*graphs[_channel].GetXaxis().GetTitleOffset()})
    yaxis_title = "U_{dep}/U_{dep}(t=0) [%]"
    cm.setup_y_axis(graphs[_channel].GetYaxis(), pad, {"Title": yaxis_title})

    if NGraphs==1:
        graphs[_channel].GetYaxis().SetRangeUser(59., 101.)
        graphs[_channel].Draw("APL")
    else:
        graphs[_channel].Draw("PLSAME")

    legend1.AddEntry(graphs[_channel], "pad %i" % _channel)


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