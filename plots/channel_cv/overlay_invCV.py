# Author: Thorben Quast, thorben.quast@cern.ch
# Date: 08 September 2021



def linear(x, par):
	return par[0] + x[0] * par[1]

def fit_function_linearintersection(x, par):  
	# par[0] is the intersection point x0
	# function is a + b*x when x < x0
	# and c + d*x when x > x0
	# par[] contains [x0, a, b, d]
	# c is calculated as (a + b*x0) - d*x0

	par2 = [0.]*2
	par2[0] = linear(par, [par[i] for i in [1, 2]]) - par[3] * par[0]
	par2[1] = par[3]
	value = linear(x, [par[i] for i in [1, 2]]) if x[0] < par[0] else linear(x, par2)
	return value


#
import common as cm
ROOT = cm.ROOT
ROOT.gROOT.SetBatch(True)
cm.setup_style()

import os
thisdir = os.path.dirname(os.path.realpath(__file__))

from copy import deepcopy
from common.util import *
from common.meta import ChannelInvCV

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--type", type=str, help="", default="sensors", required=False)
args = parser.parse_args()

Dataset = ChannelInvCV(args.type)
name = "channel_invCV_sensors_%s" %  args.type

#prepare the canvas

canvas = ROOT.TCanvas("Canvas" + name, "canvas" + name, cm.default_canvas_width, cm.default_canvas_height)
cm.setup_canvas(canvas, cm.default_canvas_width, cm.default_canvas_height)
canvas.Divide(1)
pad = canvas.GetPad(1)
cm.setup_pad(pad)
pad.cd()

#prepare the legend
if args.type == "channels":
    legend = ROOT.TLegend(*cm.calc_legend_pos(len(Dataset.GetIDs()), x1=0.57, x2=0.87, y2=0.42))
else:
    legend = ROOT.TLegend(*cm.calc_legend_pos(len(Dataset.GetIDs()), x1=0.57, x2=1.03, y2=0.45))
cm.setup_legend(legend)

fits = []
# load the graphs
for draw_index, _id in enumerate(Dataset.GetIDs()):
    infile = ROOT.TFile(Dataset.GetPath(_id).replace("<CHANNEL>", str(Dataset.GetChannel(_id))), "READ")
    gr = deepcopy(infile.Get(Dataset.GetKey(_id)))
    scale = 1./ROOT.TMath.MaxElement(gr.GetN(), gr.GetY())
    yshift = 0.075-0.03*draw_index
    scale_graph(gr, scale)
    yshift_graph(gr, yshift)
    gr.SetMinimum(0.70)
    gr.SetMaximum(1.1)
    
    
    fit = deepcopy(infile.Get("fit_func_%s" % Dataset.GetKey(_id)))
    fit_draw = ROOT.TF1("fit_draw_%s" % _id, fit_function_linearintersection, 0., 900., 4)
    fit_draw.SetParameter(0, fit.GetParameter(0))
    fit_draw.SetParameter(1, fit.GetParameter(1)*scale+yshift)
    fit_draw.SetParameter(2, fit.GetParameter(2)*scale)
    fit_draw.SetParameter(4, fit.GetParameter(4))
    Vdep_line = ROOT.TLine(fit.GetParameter(0), 0.7, fit.GetParameter(0), 1+yshift)

    Dataset.SetGraph(_id, fit_draw)
    Dataset.SetGraph(_id, gr)


    cm.setup_graph(gr, {"MarkerSize": 2, "LineWidth": 2})
    cm.setup_graph(fit_draw, {"LineWidth": 2})
    cm.setup_graph(Vdep_line, {"LineWidth": 2, "LineStyle": fit_draw.GetLineStyle(), "LineColor": fit_draw.GetLineColor()})
    
    cm.setup_x_axis(gr.GetXaxis(), pad, {"Title": "U_{bias} (V)"})
    cm.setup_y_axis(gr.GetYaxis(), pad, {"Title": "normalised C_{pad}^{-2} (a.u.)", "TitleOffset": 1.1*gr.GetYaxis().GetTitleOffset()})	
    gr.GetXaxis().SetLimits(0., 900.)

    legend.AddEntry(gr, Dataset.GetLabel(_id), "pl")
    
    if draw_index == 0:
        gr.Draw("AP")
    else:
        gr.Draw("P")
    
    fit_draw.Draw("SAME")
    Vdep_line.Draw("SAME")
    fits.append(fit_draw)
    fits.append(Vdep_line)
legend.Draw()


canvas.cd()
# cms label
cms_labels = cm.create_cms_labels()
cms_labels.Draw()

# campaign label
campaign_label = cm.create_campaign_label()
campaign_label.Draw()

if args.type == "channels":
    label = ROOT.TLatex(0.92, 0.45, "LD, 200 #mum, 2.5E15 neq")
    cm.setup_label(label, {"TextAlign": 31, "TextFont": 73})
    label.Draw()

frequency_label = ROOT.TLatex(0.15, 0.87, "f_{LCR} = 2 kHz")
cm.setup_label(frequency_label, {"TextFont": 73, "TextColor": ROOT.kViolet+1})
frequency_label.Draw()

#pad.SetGrid(True)
#save pdf
canvas.Print(os.path.join(thisdir, "{}.pdf".format(name)))