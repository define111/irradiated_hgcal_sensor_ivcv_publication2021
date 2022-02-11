# Author: Thorben Quast, thorben.quast@cern.ch
# Date: 11 February 2022

import numpy as np

import common as cm
ROOT = cm.ROOT
ROOT.gROOT.SetBatch(True)
cm.setup_style()

import os
thisdir = os.path.dirname(os.path.realpath(__file__))

from copy import deepcopy
from common.util import *


#load the data
#make this a function
def read_graph(_file, cut=-1):
    infile_path = os.path.join(os.environ["DATA_DIR"], "RINSC_temperature/%s.csv" % _file)
    time, T1 = np.genfromtxt(infile_path, unpack=True, usecols=(2, 4), delimiter=";", skip_header=1,dtype=np.str)
    #set points of the graph
    gr = ROOT.TGraph()
    for _n in range(len(time)):
        _t = float(time[_n].replace(",", "."))
        _T1 = float(T1[_n].replace(",", "."))
        if (cut != -1) and (_T1 > cut):
            continue
        gr.SetPoint(gr.GetN(), _t/60., _T1)

    return deepcopy(gr)

#read round 1 data
gr_rd1 = read_graph("Round_1_temp", cut=32)
cm.setup_graph(gr_rd1)

gr_rd10 = read_graph("Round_10_Irradiation_Temp_Profile")
cm.setup_graph(gr_rd10)

gr_rd9 = read_graph("Round_9_Irradiation_Temp_Profile")
cm.setup_graph(gr_rd9)

gr_rd11 = read_graph("Round_11_Temp_Profile")
cm.setup_graph(gr_rd11)

gr_rd8 = read_graph("Round_8_Irradiation_Temp_Profile")
cm.setup_graph(gr_rd8)

gr_rd3 = read_graph("Round_3_Temp_Profile")
cm.setup_graph(gr_rd3)


#prepare the canvas
name = "RINSC_temp"

canvas_width = 1600
canvas_height = 900
canvas = ROOT.TCanvas("Canvas" + name, "canvas" + name, canvas_width, canvas_height)
cm.setup_canvas(canvas, canvas_width, canvas_height)
canvas.Divide(1)
pad = canvas.GetPad(1)
cm.setup_pad(pad)
pad.cd()


cm.setup_x_axis(gr_rd10.GetXaxis(), pad, {"Title": "Time after insertion (h)"})
cm.setup_y_axis(gr_rd10.GetYaxis(), pad, {"Title": "Temperature in puck (#circC)"})
gr_rd10.GetXaxis().SetLimits(0., 8.)
gr_rd10.GetYaxis().SetRangeUser(-70., 55.)

gr_rd1.SetLineColor(cm.colors["black"])
gr_rd10.SetLineColor(cm.colors["blue"])
gr_rd9.SetLineColor(cm.colors["creamblue"])
gr_rd11.SetLineColor(ROOT.kViolet)
gr_rd8.SetLineColor(cm.colors["creamred"])
gr_rd3.SetLineColor(cm.colors["red"])

#gr_rd1.Draw("AL")
gr_rd10.Draw("AL")
#gr_rd9.Draw("LSAME")
#gr_rd11.Draw("LSAME")
gr_rd8.Draw("LSAME")
#gr_rd3.Draw("LSAME")

legend1 = ROOT.TLegend(*cm.calc_legend_pos(3, x1=0.7, x2=0.9, y2=0.67))
cm.setup_legend(legend1)
legend1.SetHeader("Irradiation duration")
legend1.AddEntry(gr_rd10, "15 min", "l")
legend1.AddEntry(gr_rd8, "76 min", "l")
legend1.Draw()

canvas.cd()
# cms label
cms_labels = cm.create_cms_labels()
cms_labels.Draw()

# campaign label
campaign_label = cm.create_campaign_label()
campaign_label.Draw()

# add explanation text
RD10_text = ROOT.TText()
RD10_text.SetTextColor(cm.colors["blue"])
RD10_text.SetTextSize(0.03)
RD10_text.DrawText(0.27, 0.23, "Start")
RD10_text.DrawText(0.30, 0.68, "End")
RD10_text.DrawText(0.45, 0.33, "Dry air evaporated")

RD8_text = ROOT.TText()
RD8_text.SetTextColor(cm.colors["creamred"])
RD8_text.SetTextSize(0.03)
RD8_text.DrawText(0.22, 0.13, "Start")
RD8_text.DrawText(0.34, 0.9, "End")
RD8_text.DrawText(0.4, 0.48, "Dry ice evaporated")


pad.SetGrid(True)
#save pdf
canvas.Print(os.path.join(thisdir, "{}.pdf".format(name)))

