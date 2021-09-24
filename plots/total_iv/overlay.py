# Author: Thorben Quast, thorben.quast@cern.ch
# Date: 07 September 2021

#
import common as cm
ROOT = cm.ROOT
ROOT.gROOT.SetBatch(True)
cm.setup_style()

import os
thisdir = os.path.dirname(os.path.realpath(__file__))

from copy import deepcopy
from common.util import *
from common.meta import TotalIV

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--type", type=str, help="", default="good", required=False)
args = parser.parse_args()


#prepare the canvas
if args.type == "bad":
    Dataset = TotalIV("bad")
    name = "total_current_IV_bad"
else:
    Dataset = TotalIV("good")
    name = "total_current_IV"

canvas = ROOT.TCanvas("Canvas" + name, "canvas" + name, cm.default_canvas_width, cm.default_canvas_height)
cm.setup_canvas(canvas, cm.default_canvas_width, cm.default_canvas_height)
canvas.Divide(1)
pad = canvas.GetPad(1)
cm.setup_pad(pad)
pad.cd()

#prepare the legend
X2 = 0.9
if args.type == "bad":
    X2 = 0.99
legend = ROOT.TLegend(*cm.calc_legend_pos(len(Dataset.GetIDs())+1, x1=0.12, x2=X2, y2=0.38))
cm.setup_legend(legend)

compliance_line = ROOT.TF1("compliance", "2000", 0., 900.)
cm.setup_graph(compliance_line, {"LineWidth": 3, "LineStyle": 3, "LineColor": ROOT.kRed+1})
legend.AddEntry(compliance_line, "2 mA I_{tot} compliance", "l")

# load the graphs
for draw_index, _id in enumerate(Dataset.GetIDs()):
    infile = ROOT.TFile(Dataset.GetPath(_id), "READ")
    gr = deepcopy(infile.Get(Dataset.GetKey()))
    Dataset.SetGraph(_id, gr)

    cm.setup_graph(gr)
    cm.setup_x_axis(gr.GetXaxis(), pad, {"Title": "U_{bias} (V)"})
    cm.setup_y_axis(gr.GetYaxis(), pad, {"Title": "I_{tot, -40^{#circ}C} (#muA)"})	
    gr.SetMinimum(4.0)
    gr.SetMaximum(3000.0)
    gr.GetXaxis().SetLimits(0., 900.)

    legend.AddEntry(gr, Dataset.GetLabel(_id), "pl")
    
    if draw_index == 0:
        gr.Draw("ALP")
    else:
        gr.Draw("LP")

compliance_line.Draw("SAME")
legend.Draw()

canvas.cd()
# cms label
cms_labels = cm.create_cms_labels()
cms_labels.Draw()

# campaign label
campaign_label = cm.create_campaign_label()
campaign_label.Draw()

pad.SetLogy(True)
#pad.SetGrid(True)
#save pdf
canvas.Print(os.path.join(thisdir, "{}.pdf".format(name)))