# Author: Thorben Quast, thorben.quast@cern.ch
# Date: 13 September 2021

import common as cm
ROOT = cm.ROOT
ROOT.gROOT.SetBatch(True)
cm.setup_style()

import os
thisdir = os.path.dirname(os.path.realpath(__file__))

from copy import deepcopy
from common.util import TemperatureScaling, scale_graph

MEASUREMENTS = []
MEASUREMENTS.append(("8in_198ch_2019_1004_65E13_neg30_BlackCover_October2020", -30))
MEASUREMENTS.append(("8in_198ch_2019_1004_65E13_neg35_BlackCover_October2020", -35))
MEASUREMENTS.append(("8in_198ch_2019_1004_65E13_neg40_BlackCover_October2020", -40))

output_directory = os.path.dirname(os.path.realpath(__file__))
CHANNEL = 24
colors = [ROOT.kRed, ROOT.kBlack, ROOT.kBlue]

name = "iv_overlay_ch%i" % CHANNEL
canvas_width = 1600
canvas_height = 900
canvas = ROOT.TCanvas("Canvas" + name, "canvas" + name, canvas_width, canvas_height)
cm.setup_canvas(canvas, canvas_width, canvas_height)
canvas.Divide(1)
pad = canvas.GetPad(1)
cm.setup_pad(pad)
pad.cd()


graphs = []

#prepare the legend
legend = ROOT.TLegend(*cm.calc_legend_pos(3, x1=0.18, x2=0.7, y2=0.88))
cm.setup_legend(legend)
legend.SetNColumns(2)

for drawindex, (measID, temp) in enumerate(MEASUREMENTS):
    # retrieve paths of processed files as input
    infile = ROOT.TFile(os.path.join(
        os.environ["DATA_DIR"], "iv/October2020_ALPS/channelIV/%s/TGraphErrors.root" % measID), "READ")

    # determine per-channel leakage current at common voltage (EVALVOLTAGE)
    # not a fit here, but infrastructure in place in case a

    gr_uncorrected = deepcopy(infile.Get("IV_uncorrected_channel%i" % CHANNEL))
    infile.Close()
    gr = deepcopy(gr_uncorrected)
    gr.SetName("IV_tempcorrected_channel%i" % CHANNEL)

    scale_graph(gr, TemperatureScaling(temp, -35.))

    cm.setup_graph(gr_uncorrected, {"MarkerColor": colors[drawindex], "LineColor": colors[drawindex], "MarkerSize": 3, "LineWidth": 3, "LineStyle": 2 , "MarkerStyle": 21+drawindex})
    cm.setup_x_axis(gr_uncorrected.GetXaxis(), pad , {"Title": "U_{bias} (V)"})
    cm.setup_y_axis(gr_uncorrected.GetYaxis(), pad , {"Title": "I_{pad, T} (#muA)"})
    cm.setup_graph(gr, {"MarkerColor": colors[drawindex]+1, "LineColor": colors[drawindex]+1, "MarkerSize": 3, "LineWidth": 3, "LineStyle": 1, "MarkerStyle": 21+drawindex})
    
    if drawindex==0:
        gr_uncorrected.GetYaxis().SetRangeUser(0., 3.)
        gr_uncorrected.Draw("APL")
    else:
        gr_uncorrected.Draw("PLSAME")
    
    legend.AddEntry(gr_uncorrected, "T = %i^{#circ}C" % temp, "pl")
    
    if temp!=-35:
        gr.Draw("PLSAME")
        legend.AddEntry(gr, "T #rightarrow T' = -35^{#circ}C", "pl")
    else:
        legend.AddEntry(ROOT.nullptr, "", "p")

    graphs.append(gr)
    graphs.append(gr_uncorrected)
    drawindex+=1
legend.Draw()


canvas.cd()

# cms label
cms_labels = cm.create_cms_labels()
cms_labels.Draw()

# campaign label
campaign_label = cm.create_campaign_label()
campaign_label.Draw()

pad.SetGrid(True)

label = ROOT.TLatex(0.40, 0.89, "LD, 300 #mum, 0.9#times10^{15} neq/cm^{2}")
cm.setup_label(label, {"TextAlign": 31, "TextFont": 73})
label.Draw()

canvas.Print(os.path.join(thisdir, "{}.pdf".format(name)))
