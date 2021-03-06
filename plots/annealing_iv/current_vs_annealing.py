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
from common.meta import MEASUREMENTS

def add_value(dict_obj, key, value):
    ''' Adds a key-value pair to the dictionary.
        If the key already exists in the dictionary, 
        it will associate multiple values with that 
        key instead of overwritting its value'''
    if key not in dict_obj:
        dict_obj[key] = value
    elif isinstance(dict_obj[key], list):
        dict_obj[key].append(value)
    else:
        dict_obj[key] = [dict_obj[key], value]
        
def getAnnealingMinutes(annealingSteps):
    annealingMinutes=[]
    for annealingStep in annealingSteps:
        annealingMinutes.append(int(annealingStep.split("min")[0][1:]))
    return annealingMinutes

unique_Measurements = set(MEASUREMENTS)
measurementForUniqueSensor = {}
for measurement in MEASUREMENTS:
    if (MEASUREMENTS[measurement]["version"] == 2) and MEASUREMENTS[measurement]["Frequency"] == "1kHz":
        add_value(measurementForUniqueSensor, MEASUREMENTS[measurement]["Sensor_name"], MEASUREMENTS[measurement])
#measurement specifics
sensorNames=[]
measurementIDs=[]
Campaigns=[]
annealingSteps=[]
thicknesses=[]
fluences=[]
for sensor in measurementForUniqueSensor:
    if isinstance(measurementForUniqueSensor[sensor], list):
        measurementID = measurementForUniqueSensor[sensor][0]["ID"].split("degC")[0]
        Campaign = measurementForUniqueSensor[sensor][0]["Campaign"]
        thickness = measurementForUniqueSensor[sensor][0]["thickness"]
        fluence = measurementForUniqueSensor[sensor][0]["fluence"]
        annealingStepsSensor=[]
        for annealingStep in measurementForUniqueSensor[sensor]:
            annealingTime=annealingStep['ID'].split("BackSideBiased")[1]
            annealingStepsSensor.append(annealingTime)
        sensorNames.append(sensor)    
        measurementIDs.append(measurementID)
        Campaigns.append(Campaign)
        annealingSteps.append(annealingStepsSensor)
        thicknesses.append(thickness)    
        fluences.append(fluence)

#measurement specifics
# _measID = "8in_198ch_2019_2004_25E14_neg40"
# Campaign = "Spring2021_ALPS"

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--EVALVOLTAGE", type=int, help="", default=600, required=False)
args = parser.parse_args()
EVALVOLTAGE = args.EVALVOLTAGE
    
for sensorIndex,sensor in enumerate(sensorNames):
    _measID = measurementIDs[sensorIndex]
    Campaign = Campaigns[sensorIndex]

    name = "annealing_current_%s" % sensorNames[sensorIndex]
    if EVALVOLTAGE == -1:
        name += "_atUdep"

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

    tmp_data = []
    annealingStepsInMinutes=getAnnealingMinutes(annealingSteps[sensorIndex])
    for annealing in annealingStepsInMinutes:
        if EVALVOLTAGE==-1:

            measID = _measID
            if annealing > 0:
                postfix = "_%iminAnnealing" % annealing
                measID = measID+postfix
            
            infile_path = os.path.join(os.environ["DATA_DIR"], "cv/%s/Vdep/%s/Vdep_serial.txt" % (Campaign, measID))

            #reject the bad channels
            VdepData = pd.DataFrame(np.genfromtxt(infile_path, usecols=(1,2,3), skip_header=1), columns=["Pad", "Dummy", "Vdep"])
            VdepData = VdepData.drop(columns=["Dummy"])

        postfix = ""
        if annealing > 0:
            postfix = "_%iminsAnnealing" % annealing
        measID = _measID+'degC_BackSideBiased'+postfix

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
            if EVALVOLTAGE == -1:
                channel_data = VdepData[VdepData.Pad==CHANNEL]
                Vdep = np.array(channel_data.Vdep)[0]
                _EVALVOLTAGE = Vdep
            else:
                _EVALVOLTAGE = EVALVOLTAGE

            lfti = ROOT.TF1("pol1", "pol1", _EVALVOLTAGE-120., _EVALVOLTAGE+120.)

            gr.Fit(lfti, "RQ")

            # compute ratios and save as file
            lcurr = lfti.Eval(_EVALVOLTAGE)

            # position not really useful because coordinate system center not quite in center
            tmp_data.append((annealing, CHANNEL, EVALVOLTAGE, lcurr))

    _df = pd.DataFrame(tmp_data, columns=["annealingMin", "channel", "U", "I"])
    minCurrent = _df['I'].min()
    legend1 = ROOT.TLegend(*cm.calc_legend_pos(10+1, x1=0.6, x2=0.9, y2=0.92))
    cm.setup_legend(legend1)
    legend1.SetNColumns(2)

    #create the graphs
    graphs = {}
    yAxisLimit=100
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
        print(I)
        cm.setup_graph(graphs[_channel])
        graphs[_channel].SetMarkerStyle(19+NGraphs%11)
        graphs[_channel].SetMarkerColor((NGraphs-1)%9+1)
        graphs[_channel].SetLineColor((NGraphs-1)%9+1)

        if EVALVOLTAGE == -1:
            graphs[_channel].GetYaxis().SetRangeUser(59., 101.)
        else:
            print("beginning")
            print(yAxisLimit)
            if I[1]<yAxisLimit:
                yAxisLimit=I[1]
                print("modfiying")
            print (I[1])
            print(yAxisLimit-5)
            graphs[_channel].GetYaxis().SetRangeUser(yAxisLimit-5, 101.)
        xaxis_title = "t = Duration of annealing at +60^{#circ} C (min)"
        cm.setup_x_axis(graphs[_channel].GetXaxis(), pad, {"Title": xaxis_title, "TitleOffset": 0.90*graphs[_channel].GetXaxis().GetTitleOffset()})
        if EVALVOLTAGE == -1:
            yaxis_title = "I_{pad, -40^{#circ}C}(t, U_{dep})/I_{pad, -40^{#circ}C}(t=0, U_{dep}) [%]"
        else:
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
    
    location_label_text = ROOT.TText()
    location_label_text.SetTextColor(ROOT.kBlack)
    location_label_text.SetTextSize(0.035)
    location_label_text.DrawText(0.5, 0.961, sensor+ ', ')

    # campaign label
    campaign_label = cm.create_campaign_label()
    campaign_label.Draw()
    fluenceE15=fluences[sensorIndex]/10
    sensorType="LD"
    if thicknesses[sensorIndex]==120:
        sensorType="HD" 
    _label_text = "%s, %s #mum, ~%s#times10^{15}neq/cm^{2}" % (sensorType, thicknesses[sensorIndex], fluenceE15)
    label = ROOT.TLatex(0.24, 0.82, _label_text)
    cm.setup_label(label, {"TextFont": 73})

    legend1.SetHeader(_label_text)
    #label.Draw()

    legend1.Draw()

    pad.SetGrid(True)
    #save pdf
    canvas.Print(os.path.join(thisdir, "{}.pdf".format(name)))