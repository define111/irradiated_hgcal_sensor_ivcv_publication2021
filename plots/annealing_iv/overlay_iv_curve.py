# Author: Thorben Quast, thorben.quast@cern.ch
# Date: 10 September 2021

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
CHANNEL = 24

name = "annealing_IV_ch%s" %  CHANNEL
#prepare the canvas
canvas = ROOT.TCanvas("Canvas" + name, "canvas" + name, cm.default_canvas_width, cm.default_canvas_height)
cm.setup_canvas(canvas, cm.default_canvas_width, cm.default_canvas_height)
canvas.Divide(1)
pad = canvas.GetPad(1)
cm.setup_pad(pad)
pad.cd()

graphs = []
legend1 = ROOT.TLegend(*cm.calc_legend_pos(1, x1=0.2, x2=0.5, y2=0.8))
legend2 = ROOT.TLegend(*cm.calc_legend_pos(4, x1=0.6, x2=0.9, y2=0.34))
cm.setup_legend(legend1)
cm.setup_legend(legend2)

colors = [ROOT.kBlack, ROOT.kCyan+1, ROOT.kBlue+1, ROOT.kViolet+1, ROOT.kGreen-1]

for drawindex, postfix in enumerate(["", "_9minAnnealing", "_24minAnnealing", "_61minAnnealing", "_80minAnnealing"]):
    measID = _measID+postfix+"_chucktempcorrected"
    label = "no additional annealing" if postfix=="" else postfix.replace("_", "").replace("minAnnealing", " min at 60^{#circ}C")
    # retrieve paths of processed files as input
    infile = ROOT.TFile(os.path.join(
        os.environ["DATA_DIR"], "iv/%s/channelIV/%s/TGraphErrors.root" % (Campaign, measID)), "READ")


    gr = deepcopy(infile.Get("IV_uncorrected_channel%i" % CHANNEL))
    infile.Close()

    #apply scale
    scale = 1.
    scale_graph(gr, 1.)

    cm.setup_graph(gr)
    cm.setup_x_axis(gr.GetXaxis(), pad, {"Title": "U_{bias} (V)"})
    cm.setup_y_axis(gr.GetYaxis(), pad, {"Title": "I_{pad, -40^{#circ}C} (#muA)"})	

    gr.SetMarkerStyle(20+drawindex)
    gr.SetLineStyle(1+drawindex)
    gr.SetLineColor(colors[drawindex])
    gr.SetMarkerColor(colors[drawindex])

    if drawindex==0:
        gr.SetTitle(label + ", pad %i" % CHANNEL)
        gr.GetXaxis().SetLimits(0., 900.)
        gr.Draw("APL")
        gr.GetXaxis().SetLimits(0., 900.)
        gr.GetYaxis().SetRangeUser(0., 5.5)
    else:
        gr.Draw("PLSAME")
    
    if drawindex==0:
        legend1.AddEntry(gr, label, "pl")
    else:
        legend2.AddEntry(gr, label, "pl")

    graphs.append(gr)
    drawindex+=1

legend1.Draw()
legend2.Draw()

canvas.cd()
# cms label
cms_labels = cm.create_cms_labels()
cms_labels.Draw()

# campaign label
campaign_label = cm.create_campaign_label()
campaign_label.Draw()

label = ROOT.TLatex(0.24, 0.82, "LD, 200 #mum, 2.5E15 neq")
cm.setup_label(label, {"TextFont": 73})
label.Draw()

pad.SetGrid(True)
#save pdf
canvas.Print(os.path.join(thisdir, "{}.pdf".format(name)))
