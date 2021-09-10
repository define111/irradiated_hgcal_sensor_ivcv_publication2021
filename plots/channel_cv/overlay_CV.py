# Author: Thorben Quast, thorben.quast@cern.ch
# Date: 08 September 2021

#
import common as cm
ROOT = cm.ROOT
ROOT.gROOT.SetBatch(True)
cm.setup_style()

import os
thisdir = os.path.dirname(os.path.realpath(__file__))

from copy import deepcopy
from common.util import *
from common.meta import ChannelCV

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--type", type=str, help="", default="sensors", required=False)
args = parser.parse_args()

Dataset = ChannelCV(args.type)
name = "channel_CV_sensors_%s" %  args.type

#prepare the canvas

canvas = ROOT.TCanvas("Canvas" + name, "canvas" + name, cm.default_canvas_width, cm.default_canvas_height)
cm.setup_canvas(canvas, cm.default_canvas_width, cm.default_canvas_height)
canvas.Divide(1)
pad = canvas.GetPad(1)
cm.setup_pad(pad)
pad.cd()

#prepare the legend
if args.type == "channels":
    legend = ROOT.TLegend(*cm.calc_legend_pos(len(Dataset.GetIDs()), x1=0.48, x2=0.87, y2=0.89))
else:
    legend = ROOT.TLegend(*cm.calc_legend_pos(len(Dataset.GetIDs()), x1=0.48, x2=0.93, y2=0.92))
cm.setup_legend(legend)

# load the graphs

for draw_index, _id in enumerate(Dataset.GetIDs()):
    infile = ROOT.TFile(Dataset.GetPath(_id), "READ")
    gr = deepcopy(infile.Get(Dataset.GetKey(_id)))
    Dataset.SetGraph(_id, gr)

    cm.setup_graph(gr)
    cm.setup_x_axis(gr.GetXaxis(), pad, {"Title": "U_{bias} (V)"})
    cm.setup_y_axis(gr.GetYaxis(), pad, {"Title": "C_{pad} (pF)"})	
    gr.SetMinimum(0.0)
    gr.SetMaximum(125.0)
    gr.GetXaxis().SetLimits(0., 900.)

    legend.AddEntry(gr, Dataset.GetLabel(_id), "pl")
    
    if draw_index == 0:
        gr.Draw("ALP")
    else:
        gr.Draw("LP")
legend.Draw()


canvas.cd()
# cms label
cms_labels = cm.create_cms_labels()
cms_labels.Draw()

# campaign label
campaign_label = cm.create_campaign_label()
campaign_label.Draw()

if args.type == "channels":
    label = ROOT.TLatex(0.83, 0.89, "LD, 200 #mum, 2.5E15 neq")
    cm.setup_label(label, {"TextAlign": 31, "TextFont": 73})
    label.Draw()


frequency_label = ROOT.TLatex(0.15, 0.87, "f_{LCR} = 2 kHz")
cm.setup_label(frequency_label, {"TextFont": 73, "TextColor": ROOT.kViolet+1})
frequency_label.Draw()

pad.SetGrid(True)
#save pdf
canvas.Print(os.path.join(thisdir, "{}.pdf".format(name)))