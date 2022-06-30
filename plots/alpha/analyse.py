# Author: Thorben Quast, thorben.quast@cern.ch
# Date: 10 September 2021
 
import numpy as np
 
import common as cm
ROOT = cm.ROOT
ROOT.gROOT.SetBatch(True)
cm.setup_style()
 
import os
thisdir = os.path.dirname(os.path.realpath(__file__))
 
from common.util import deltaI_relative, TemperatureScaling, scale_graph
from common.meta import FULL_CELL_AREA, MEASUREMENTS
 
from math import sqrt
import math
 
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
   #2. fluence uncertainty is assumed to be 15% for Si diodes, 25% for Fe foils
   if fluence < 30:
       x_err_up =  0.2 * fluence
       x_err_down = 0.2 * fluence
   else:
       x_err_up =  0.2 * fluence
       x_err_down = 0.2 * fluence
 
   # 3. +/- 0.5 deg C temperature variation at CERN, +/- 1.5 deg C at TTU
   DELTAT = 0.5
   if Campaign == "TTU_October2021":
       DELTAT = 1.0
   y_err_down = deltaI_relative(DELTAT, -40.)*current
   y_err_up = deltaI_relative(DELTAT, -40.)*current
  
   # 4. annealing time uncertainty, only underestimate of time possible --> lower currents
   annealing_down = 0.
   if Campaign == "Spring2021_ALPS":
       annealing_up = 0.05
   elif (Campaign == "Winter2021") or (Campaign == "TTU_October2021"):
       annealing_up = 0.3
   else:
       annealing_up = 0.10
   y_err_up = sqrt(y_err_up**2 + (annealing_up*current)**2)
   y_err_down = sqrt(y_err_down**2 + (annealing_down*current)**2)
 
   #5. thickness variation
   delta_thickness = 2./measurement_meta["thickness"]
   y_err_up = sqrt(y_err_up**2 + (delta_thickness*current)**2)
   y_err_down = sqrt(y_err_down**2 + (delta_thickness*current)**2)
 
   return x_err_down, x_err_up, y_err_down, y_err_up

if UREF == -1:    
    PAIRS = [["1002", "2002", "3002", "3009", "3010", "1013"], ["1102", "2114", "3102", "3109", "3110", "1114"], ["2004", "5414"], ["1101", "2105"]]
    lengthOfV1 = 4
elif UREF <= 600:
    PAIRS = [["1002", "2002", "3002", "3009", "3010", "1013", "3008", "1003_xcheck"], ["1102", "2114", "3102", "3109", "3110", "1114", "3104"], ["2004", "5414"], ["1101", "2105", "1105_xcheck"]]
    lengthOfV1 = 4
else:
    PAIRS = [["1002", "2002", "3002", "3009", "3010", "1013"], ["1102", "2114", "3102", "3109", "3110", "1114"], ["2004", "5414"]]
    lengthOfV1 = 3    
PAIRS_V2_B = [measurement for measurement in MEASUREMENTS if (MEASUREMENTS[measurement]["version"] == 2) & (MEASUREMENTS[measurement]["oxideType"]=="B") & (MEASUREMENTS[measurement]["Annealing_stage"]=="Final") & (MEASUREMENTS[measurement]["Frequency"] == "1kHz")]
PAIRS.append(PAIRS_V2_B)
PAIRS_V2_C = [measurement for measurement in MEASUREMENTS if (MEASUREMENTS[measurement]["version"] == 2) & (MEASUREMENTS[measurement]["oxideType"]=="C") & (MEASUREMENTS[measurement]["Annealing_stage"]=="Final") & (MEASUREMENTS[measurement]["Frequency"] == "1kHz")]
PAIRS.append(PAIRS_V2_C)
PAIRS_V2_D = [measurement for measurement in MEASUREMENTS if (MEASUREMENTS[measurement]["version"] == 2) & (MEASUREMENTS[measurement]["oxideType"]=="D") & (MEASUREMENTS[measurement]["Annealing_stage"]=="Final") & (MEASUREMENTS[measurement]["Frequency"] == "1kHz")]
PAIRS.append(PAIRS_V2_D)
  
iv_vs_fluence_graphs = []
 
campaign_Lables = []
campaign_Fluences = []
numberOfOxides= len(PAIRS) - lengthOfV1
 
for pair_index, _pair in enumerate(PAIRS):
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
      
       #load the IV curves\
 
       infile = ROOT.TFile(os.path.join(os.environ["DATA_DIR"], "iv/%s/channelIV/%s/TGraphErrors.root" % (Campaign, MEASID)), "READ")
       lcurr_average = []
       lcurr_rel_up_average = []
       lcurr_rel_down_average = []
       for _channel in CELLS:
           if UREF == -1:
               Uref = loaded_Vdep[loaded_channels==_channel][0]
           else:
               Uref = UREF
           gr = infile.Get("IV_uncorrected_channel%i" % _channel)
           scale_graph(gr, 1E-3 * TemperatureScaling(-40., -20.))
 
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
      
       campaign_Lables.append(Campaign)
       campaign_Fluences.append(fluence)
       lcurr_average = np.mean(lcurr_average)
       lcurr_rel_up_average = np.mean(lcurr_rel_up_average)
       lcurr_rel_down_average = np.mean(lcurr_rel_down_average)   
       np_gr = iv_vs_fluence_gr.GetN()
       iv_vs_fluence_gr.SetPoint(np_gr, fluence, lcurr_average)
      
       #error calculation
       x_err_down, x_err_up, y_err_down, y_err_up = compute_errors(MEASUREMENTS[ID], lcurr_average)                
      
       #add reference voltage variation, only if Udep is taken
       if UREF == -1:
           y_err_down = sqrt(y_err_down**2+(lcurr_average*lcurr_rel_down_average)**2)
           y_err_up = sqrt(y_err_up**2+(lcurr_average*lcurr_rel_up_average)**2)
 
       iv_vs_fluence_gr.SetPointError(np_gr, x_err_down, x_err_up, y_err_down, y_err_up)
  
   if pair_index<lengthOfV1:
       iv_vs_fluence_gr.SetName("%s p-stop, U_{fb}=%i V" % (MEASUREMENTS[ID]["p-stop"], MEASUREMENTS[ID]["Vfb"]))
       iv_vs_fluence_graphs.append(iv_vs_fluence_gr)
   else:
       iv_vs_fluence_gr.SetName("%s p-stop, U_{fb}=%i V, oxide %s" % (MEASUREMENTS[ID]["p-stop"], MEASUREMENTS[ID]["Vfb"], MEASUREMENTS[ID]["oxideType"]))
       iv_vs_fluence_graphs.append(iv_vs_fluence_gr)
  
#prepare the canvas
if UREF > 0:
   name = "alpha_%iV" % UREF
else:
   name = "alpha_Udep"
canvas_width = 1600
canvas_height = 900
canvas = ROOT.TCanvas("Canvas" + name, "canvas" + name, canvas_width, canvas_height)
cm.setup_canvas(canvas, canvas_width, canvas_height)
canvas.Divide(1)
pad = canvas.GetPad(1)
cm.setup_pad(pad)
pad.cd()
 
pol1_fits = []
legend_graphs = ROOT.TLegend(*cm.calc_legend_pos(len(PAIRS)+1, x1=0.15, x2=0.45, y2=0.94))
 
cm.setup_legend(legend_graphs)
 
legend_fits = ROOT.TLegend(*cm.calc_legend_pos(2.35, x1=0.450, x2=0.93, y2=0.245))
cm.setup_legend(legend_fits)
legend_fits.SetTextSize(35)
 
legend_graphs_V2 = ROOT.TLegend(*cm.calc_legend_pos(numberOfOxides+1, x1=0.6, x2=0.94, y2=0.5))
cm.setup_legend(legend_graphs_V2)
 
pol1_fits = []
for draw_index, iv_vs_fluence_gr in enumerate(iv_vs_fluence_graphs):
  
   if UREF == 800:
       cm.setup_graph(iv_vs_fluence_gr, {"MarkerStyle": [20, 25, 22, 20, 25, 22][draw_index], "LineStyle": 1, "MarkerSize": 4})
   else:
       cm.setup_graph(iv_vs_fluence_gr, {"MarkerStyle": [20, 25, 22, 32, 20, 25, 22][draw_index], "LineStyle": 1, "MarkerSize": 4})
   iv_vs_fluence_gr.GetYaxis().SetRangeUser(250.*1E-3, 8200.*1E-3)
   cm.setup_x_axis(iv_vs_fluence_gr.GetXaxis(), pad, {"Title": "Irradiation fluence (10^{14} neq/cm^{2})"})
   y_title = "I_{pad, -20^{#circ}C}(U=%i) / V (mA/cm^{3})" % UREF
   if UREF < 0:
       y_title = "I_{pad, -20^{#circ}C}(U=U_{dep}) / V (mA/cm^{3})"
   cm.setup_y_axis(iv_vs_fluence_gr.GetYaxis(), pad, {"Title": y_title})
   if UREF == 800:
       iv_vs_fluence_gr.SetLineColor([ROOT.kBlack, ROOT.kBlack, ROOT.kBlack, ROOT.kBlue, ROOT.kGreen, ROOT.kMagenta][draw_index])
       iv_vs_fluence_gr.SetMarkerColor([ROOT.kBlack, ROOT.kBlack, ROOT.kBlack , ROOT.kBlue, ROOT.kGreen, ROOT.kMagenta][draw_index])
   else:
       iv_vs_fluence_gr.SetLineColor([ROOT.kBlack, ROOT.kBlack, ROOT.kBlack, ROOT.kBlack, ROOT.kBlue, ROOT.kGreen, ROOT.kMagenta][draw_index])
       iv_vs_fluence_gr.SetMarkerColor([ROOT.kBlack, ROOT.kBlack, ROOT.kBlack, ROOT.kBlack, ROOT.kBlue, ROOT.kGreen, ROOT.kMagenta][draw_index])
  
   if draw_index == 0:
       iv_vs_fluence_gr.Draw("AP")
       iv_vs_fluence_gr.GetXaxis().SetLimits(4., 130.)
       iv_vs_fluence_gr.Draw("AP")
   else:
       iv_vs_fluence_gr.Draw("PSAME")
 
   pol1_fit = ROOT.TF1("pol1_%i", "pol1", 0., 120.)
   pol1_fit.FixParameter(0, 0)
   iv_vs_fluence_gr.Fit(pol1_fit, "N")
   pol1_fits.append(pol1_fit)
   if draw_index<lengthOfV1:
       legend_graphs.AddEntry(iv_vs_fluence_gr, iv_vs_fluence_gr.GetName(), "p")
   else:
       legend_graphs_V2.AddEntry(iv_vs_fluence_gr, iv_vs_fluence_gr.GetName(), "p")
 
 
#combine all alpha values
alphas = np.array([g.GetParameter(1) for g in pol1_fits])
alpha_errors = np.array([g.GetParError(1) for g in pol1_fits])
alpha_mean = np.average(alphas, weights=alpha_errors**(-2))
alpha_error = sqrt(1/np.sum(alpha_errors**(-2)))
 
 
#perform alpha fit
pol1_fit = ROOT.TF1("pol1", "pol1", 0., 120.)
pol1_fit.FixParameter(0, 0)
pol1_fit.SetParameter(1, alpha_mean)
pol1_fit.SetLineColor(ROOT.kGray+1)
pol1_fit.SetLineStyle(2)
pol1_fit.SetLineWidth(4)   
pol1_fit.Draw("SAME")
alpha_error_temp = alpha_mean*deltaI_relative(0.5, -40)
if UREF == 600:
   legend_fits.AddEntry(pol1_fit, "#alpha_{600V}(-20^{#circ}C)=(%.1f#pm%.1f#pm%.1f)x10^{-19} A/cm" % (alpha_mean*(1E2), alpha_error*(1E2), alpha_error_temp*(1E2)), "l")
elif UREF == 800:
   legend_fits.AddEntry(pol1_fit, "#alpha_{800V}(-20^{#circ}C)=(%.1f#pm%.1f#pm%.1f)x10^{-19} A/cm" % (alpha_mean*(1E2), alpha_error*(1E2), alpha_error_temp*(1E2)), "l")
 
# line300_200 = ROOT.TLine(15., 85.*1E-3, 15., 2400.*1E-3)
# line200_120 = ROOT.TLine(35., 85.*1E-3, 35., 2400.*1E-3)
# line300_200.Draw()
# line200_120.Draw()
legend_graphs.SetHeader("V1 Prototypes")
legend_graphs.Draw()
legend_fits.SetHeader("After 80min at +60^{#circ}C:")
legend_fits.Draw()
legend_graphs_V2.SetHeader("V2 Prototypes")
legend_graphs_V2.Draw()
 
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
 
if UREF == 600:
   location_label_text = ROOT.TText()
   location_label_text.SetTextColor(ROOT.kBlack)
   location_label_text.SetTextSize(0.03)
   #location_label_text.DrawText(0.23, 0.24, "CERN")
   #location_label_text.DrawText(0.3, 0.29, "CERN")
   location_label_text.DrawText(0.45, 0.34, "TTU")
   # location_label_text.DrawText(0.6, 0.75, "Round 7")
   # location_label_text.DrawText(0.71, 0.34, "Round 6")
   # location_label_text.DrawText(0.75, 0.6, "1st from the reactor core")
   # location_label_text.DrawText(0.4, 0.58, "1st from the reactor core")
   # location_label_text.DrawText(0.4, 0.54, "2nd from the reactor core")
   # location_label_text.DrawText(0.75, 0.65, "2nd from the reactor core")
   # location_label_text.DrawText(0.75, 0.56, "3rd from the reactor core")
   # for index, lable in enumerate(campaign_Lables):
   #     print(lable)
   #     new_lable = lable.replace('_ALPS', '')
   #     print(new_lable)
   #     print(campaign_Fluences[index])
   #     print(math.log10(campaign_Fluences[index]/4)/math.log10(120/4))
   #     location_label_text.DrawText(math.log10(campaign_Fluences[index]/4)/math.log10(170/4), 0.34, new_lable)
   #location_label_text.DrawText(0.44, 0.38, "CERN")
   #location_label_text.DrawText(0.49, 0.48, "CERN")
   #location_label_text.DrawText(0.57, 0.54, "CERN")
   #location_label_text.DrawText(0.65, 0.76, "CERN")
   location_label_text.DrawText(0.855, 0.765, "0.5x p-stop")
 
   type_label_text = ROOT.TLatex()
   type_label_text.SetTextColor(ROOT.kViolet+1)
   type_label_text.SetTextSize(0.04)
   # type_label_text.DrawLatex(0.25, 0.56, "300 #mum, LD")
   # type_label_text.DrawLatex(0.48, 0.56, "200 #mum, LD")
   # type_label_text.DrawLatex(0.74, 0.56, "120 #mum, HD")
 
#save pdf
canvas.Print(os.path.join(thisdir, "{}.pdf".format(name)))

