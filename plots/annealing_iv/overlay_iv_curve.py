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
for sensorIndex,sensor in enumerate(sensorNames):
    _measID = measurementIDs[sensorIndex]
    Campaign = Campaigns[sensorIndex]
    CHANNEL = 24

    name = "annealing_IV_ch%s_%s" %  (CHANNEL, sensor)
    #prepare the canvas
    canvas = ROOT.TCanvas("Canvas" + name, "canvas" + name, cm.default_canvas_width, cm.default_canvas_height)
    cm.setup_canvas(canvas, cm.default_canvas_width, cm.default_canvas_height)
    canvas.Divide(1)
    pad = canvas.GetPad(1)
    cm.setup_pad(pad)
    pad.cd()

    graphs = []
    legend1 = ROOT.TLegend(*cm.calc_legend_pos(1+1, x1=0.2, x2=0.5, y2=0.85))
    legend2 = ROOT.TLegend(*cm.calc_legend_pos(4, x1=0.6, x2=0.9, y2=0.34))
    cm.setup_legend(legend1)
    cm.setup_legend(legend2)

    colors = [ROOT.kBlack, ROOT.kCyan+1, ROOT.kBlue+1, ROOT.kViolet+1, ROOT.kGreen-1]

    for drawindex, postfix in enumerate(annealingSteps[sensorIndex]):
        measID = _measID+'degC_BackSideBiased'+postfix
        label = "0 min thermal annealing" if postfix=="" else postfix.replace("_", "").replace("minAnnealing", " min at 60^{#circ}C")
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

        gr.SetMarkerStyle({0: 20, 1: 25, 2: 22, 3: 23, 4: 24, 5: 25}[drawindex])
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
    fluenceE15=fluences[sensorIndex]/10
    sensorType="LD"
    if thicknesses[sensorIndex]==120:
        sensorType="HD" 
    _label_text = "%s, %s #mum, ~%s#times10^{15}neq/cm^{2}, %s" % (sensorType, thicknesses[sensorIndex], fluenceE15, sensor)
    label = ROOT.TLatex(0.24, 0.82, _label_text)
    cm.setup_label(label, {"TextFont": 73})

    legend1.SetHeader(_label_text)
    #label.Draw()

    pad.SetGrid(True)
    #save pdf
    canvas.Print(os.path.join(thisdir, "{}.pdf".format(name)))
