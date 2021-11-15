# Author: Thorben Quast, thorben.quast@cern.ch
# Date: 10 September 2021

import numpy as np

import common as cm
ROOT = cm.ROOT
ROOT.gROOT.SetBatch(True)
cm.setup_style()

import os
thisdir = os.path.dirname(os.path.realpath(__file__))

from common.util import deltaI_relative, scale_graph
from common.meta import FULL_CELL_AREA, MEASUREMENTS

from math import sqrt

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--UREF", type=int, help="Reference voltage", default="600", required=False)
args = parser.parse_args()

UREF = args.UREF

# 1. e.g. 10 percent depletion voltage variation, estimated in main program
# not relevant for fixed voltage reference
DELTAUREF = 0.0 if UREF > 0 else 0.1
def compute_errors(measurement_meta, current):
    fluence = measurement_meta["fluence"]
    Campaign = measurement_meta["Campaign"]
    #2. fluence error is assumed to be 5% up and 20%, c.f. N. Hinton's talk at review on 12 November 2021
    x_err_up =  0.05 * fluence
    x_err_down = 0.20 * fluence 

    # 3. +/- 0.5 deg C temperature variation at CERN, +/- 1.5 deg C at TTU
    DELTAT = 0.5
    if Campaign == "TTU_October2021":
        DELTAT = 1.5
    y_err_down = deltaI_relative(DELTAT, -40.)*current
    y_err_up = deltaI_relative(DELTAT, -40.)*current
    
    # 4. annealing time uncertainty, only underestimate of time possible --> lower currents
    annealing_down = 0.
    if Campaign == "Spring2021_ALPS":
        annealing_up = 0.01
    elif (Campaign == "Winter2021") or (Campaign == "TTU_October2021"):
        annealing_up = 0.2
    else:
        annealing_up = 0.05
    y_err_up = sqrt(y_err_up**2 + (annealing_up*current)**2)
    #y_err_down = sqrt(y_err_down**2 + (annealing_up*current)**2)

    #5. thickness variation
    delta_thickness = 2./measurement_meta["thickness"]
    y_err_up = sqrt(y_err_up**2 + (delta_thickness*current)**2)
    y_err_down = sqrt(y_err_down**2 + (delta_thickness*current)**2)

    return x_err_down, x_err_up, y_err_down, y_err_up

if UREF == -1:
    PAIRS = [["1002", "2002", "3003", "3009", "3010", "1013"], ["1102", "2114", "3103", "3109", "3110", "1114"], ["2004", "5414"], ["1101", "2105"]]
elif UREF <= 600:
    #PAIRS = [["1002", "2002", "3003", "3009", "3010", "1013"], ["1102", "2114", "3103", "3109", "3110", "1114"], ["2004", "5414"], ["1101", "2105"], ["3104", "1003"]]  
    PAIRS = [["1002", "2002", "3003", "3009", "3010", "1013"], ["1102", "2114", "3103", "3109", "3110", "1114"], ["2004", "5414"], ["1101", "2105"]]  
else:
    PAIRS = [["1002", "2002", "3003", "3009", "3010", "1013"], ["1102", "2114", "3103", "3109", "3110", "1114"], ["2004", "5414"]]
iv_vs_fluence_graphs = []

#all points in one, used for fitting
iv_vs_fluence_gr_all = ROOT.TGraphAsymmErrors()

for _pair in PAIRS:
    iv_vs_fluence_gr = ROOT.TGraphAsymmErrors()
    for ID in _pair:
        # compute the datapoints
        Campaign = MEASUREMENTS[ID]["Campaign"]
        Design = MEASUREMENTS[ID]["Design"]
        MEASID = MEASUREMENTS[ID]["ID"]
        CELLS = MEASUREMENTS[ID]["Cells"]

        #load Vdep_data
        Vdep_path = os.path.join(os.environ["DATA_DIR"], "cv/%s/Vdep/%s/Vdep_serial.txt" % (Campaign, MEASID.replace("_chucktempcorrected", "")))
        if UREF == -1:
            loaded_channels, loaded_Vdep = np.genfromtxt(Vdep_path, skip_header=1, usecols=(1, 3), unpack=True)
        
        #load the IV curves
        infile = ROOT.TFile(os.path.join(os.environ["DATA_DIR"], "iv/%s/channelIV/%s/TGraphErrors.root" % (Campaign, MEASID)), "READ")

        lcurr_average = []
        lcurr_rel_up_average = []
        lcurr_rel_down_average = []
        for _channel in CELLS:
            if UREF == -1:
                Uref = loaded_Vdep[loaded_channels==_channel][0]
            else:
                Uref = UREF 
            gr = infile.Get("IV_tempcorrected_channel%i" % _channel)

            lfti_up = ROOT.TF1("pol1_up", "pol1", (1.+DELTAUREF)*Uref-105., (1.+DELTAUREF)*Uref+105.)
            lfti_down = ROOT.TF1("pol1_down", "pol1", (1.-DELTAUREF)*Uref-105., (1.-DELTAUREF)*Uref+105.)
            lfti = ROOT.TF1("pol1", "pol1", Uref-105., Uref+105.)
            gr.Fit(lfti_up, "RQ")
            gr.Fit(lfti_down, "RQ")
            gr.Fit(lfti, "RQ")
            gr.Draw()
           
            lcurr_up = lfti_up.Eval((1.+DELTAUREF)*Uref)
            lcurr_down = lfti_down.Eval((1.-DELTAUREF)*Uref)
            lcurr = lfti.Eval(Uref)
            if lcurr == 0:
                print("Skipping", _channel, "of", MEASID)
                continue
            thickness = MEASUREMENTS[ID]["thickness"]
            lcurr_per_cm3 = lcurr / (FULL_CELL_AREA[Design]*thickness*pow(10, -12))
            lcurr_average.append(lcurr_per_cm3)
            lcurr_rel_up_average.append(1.-lcurr_up/lcurr)
            lcurr_rel_down_average.append(1.-lcurr_down/lcurr)



        fluence = MEASUREMENTS[ID]["fluence"]
        lcurr_average = np.mean(lcurr_average)
        lcurr_rel_up_average = np.mean(lcurr_rel_up_average)
        lcurr_rel_down_average = np.mean(lcurr_rel_down_average)
        if Campaign == "TTU_October2021":
            lcurr_average = lcurr_average * 0.75                #scale down by expected annealing improvement           
            lcurr_rel_up_average = lcurr_rel_up_average * 0.75                #scale down by expected annealing improvement           
            lcurr_rel_down_average = lcurr_rel_down_average * 0.75                #scale down by expected annealing improvement           
        np_gr = iv_vs_fluence_gr.GetN()
        iv_vs_fluence_gr.SetPoint(np_gr, fluence, lcurr_average)
        
        #error calculation
        x_err_down, x_err_up, y_err_down, y_err_up = compute_errors(MEASUREMENTS[ID], lcurr_average)                 
        
        #add reference voltage variation, only if Udep is taken
        if UREF == -1:
            y_err_down = sqrt(y_err_down**2+(lcurr_average*lcurr_rel_down_average)**2)
            y_err_up = sqrt(y_err_up**2+(lcurr_average*lcurr_rel_up_average)**2)

        iv_vs_fluence_gr.SetPointError(np_gr, x_err_down, x_err_up, y_err_down, y_err_up)
        
        if Campaign != "TTU_October2021":
            np_gr_all = iv_vs_fluence_gr_all.GetN()
            iv_vs_fluence_gr_all.SetPoint(np_gr_all, fluence, lcurr_average)
            iv_vs_fluence_gr_all.SetPointError(np_gr_all, x_err_down, x_err_up, y_err_down, y_err_up)

    if Campaign != "TTU_October2021":
        iv_vs_fluence_gr.SetName("STD. oxide, %s p-stop, U_{fb}=%i V" % (MEASUREMENTS[ID]["p-stop"], MEASUREMENTS[ID]["Vfb"]))
    else:
        iv_vs_fluence_gr.SetName("non-annealed sensors @ TTU [x0.75]")

    iv_vs_fluence_graphs.append(iv_vs_fluence_gr)


#prepare the canvas
if UREF > 0:
    name = "alpha_%iV" % UREF
else:
    name = "alpha_Udep"
canvas_width = cm.default_canvas_width
canvas_height = cm.default_canvas_height
canvas = ROOT.TCanvas("Canvas" + name, "canvas" + name, canvas_width, canvas_height)
cm.setup_canvas(canvas, canvas_width, canvas_height)
canvas.Divide(1)
pad = canvas.GetPad(1)
cm.setup_pad(pad)
pad.cd()


pol1_fits = []
legend_graphs = ROOT.TLegend(*cm.calc_legend_pos(len(PAIRS), x1=0.15, x2=0.76, y2=0.94))
cm.setup_legend(legend_graphs)

legend_fits = ROOT.TLegend(*cm.calc_legend_pos(1.5, x1=0.28, x2=0.98, y2=0.185))
cm.setup_legend(legend_fits)
legend_fits.SetTextSize(50)

for draw_index, iv_vs_fluence_gr in enumerate(iv_vs_fluence_graphs):
    cm.setup_graph(iv_vs_fluence_gr, {"MarkerStyle": [20, 25, 22, 32, 28][draw_index], "LineStyle": 1, "MarkerSize": 4})
    iv_vs_fluence_gr.GetYaxis().SetRangeUser(150., 15000.)
    cm.setup_x_axis(iv_vs_fluence_gr.GetXaxis(), pad, {"Title": "Irradiation fluence (1E14 neq/cm^{2})"})
    y_title = "I_{pad, -20^{#circ}C}(U=%i) / V (#muA/cm^{3})" % UREF
    if UREF < 0:
        y_title = "I_{pad, -20^{#circ}C}(U=U_{dep}) / V (#muA/cm^{3})"
    cm.setup_y_axis(iv_vs_fluence_gr.GetYaxis(), pad, {"Title": y_title})

    iv_vs_fluence_gr.SetLineColor([ROOT.kBlue+1, ROOT.kOrange+1, ROOT.kBlack, ROOT.kGreen+2, ROOT.kGray][draw_index])
    iv_vs_fluence_gr.SetMarkerColor([ROOT.kBlue+1, ROOT.kOrange+1, ROOT.kBlack, ROOT.kGreen+2, ROOT.kGray][draw_index])
    
    if draw_index == 0:
        iv_vs_fluence_gr.Draw("AP")
        iv_vs_fluence_gr.GetXaxis().SetLimits(4., 130.)
        iv_vs_fluence_gr.Draw("AP")
    else:
        iv_vs_fluence_gr.Draw("PSAME")


    legend_graphs.AddEntry(iv_vs_fluence_gr, iv_vs_fluence_gr.GetName(), "p")


#perform alpha fit
pol1_fit = ROOT.TF1("pol1", "pol1", 0., 120.)
pol1_fit.FixParameter(0, 0)
pol1_fit.SetParameter(1, 5.)
iv_vs_fluence_gr_all.Fit(pol1_fit, "RN")
pol1_fit.SetLineColor(ROOT.kRed)
pol1_fit.SetLineStyle(2)
pol1_fit.SetLineWidth(4)    
pol1_fit.Draw("SAME")
legend_fits.AddEntry(pol1_fit, "#alpha(-20^{#circ}C)=(%.1f#pm%.1f)x10^{-19} A/cm" % (pol1_fit.GetParameter(1)*0.1, pol1_fit.GetParError(1)*0.1), "l")

legend_graphs.Draw()
legend_fits.Draw()

canvas.cd()
# cms label
cms_labels = cm.create_cms_labels()
cms_labels.Draw()

# campaign label
campaign_label = cm.create_campaign_label()
campaign_label.Draw()

pad.SetLogx(True)
pad.SetLogy(True)
pad.SetGrid(True)

#save pdf
canvas.Print(os.path.join(thisdir, "{}.pdf".format(name)))