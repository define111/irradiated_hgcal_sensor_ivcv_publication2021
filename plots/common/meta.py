import ROOT
import os



GEOFILES = {
    "LD": "hex_positions_HPK_198ch_8inch_edge_ring_testcap_paper.txt",
    "HD": "hex_positions_HPK_432ch_8inch_edge_ring_testcap_paper.txt"
}

MEASUREMENTS = {}
MEASUREMENTS["1002"] = {
    "Campaign": "October2020_ALPS",
    "Design": "LD",
    "Cells": [159, 171, 172],
    "ID": "8in_198ch_2019_1002_65E13_neg40_annealed68min_October2020_chucktempcorrected",
    "p-stop": "ind.",
    "thickness": 300,
    "Vfb": -2,
    "fluence": 7.1,                 #round 1, c.f. https://indico.cern.ch/event/1085830/contributions/4565317/attachments/2343669/3995999/11-12-2021_RINSC_Irradiation_Validation_and_Status.pdf
    "annealing": 80.5
}
MEASUREMENTS["1102"] = {
    "Campaign": "October2020_ALPS",
    "Design": "LD",
    "Cells": [159, 171, 172],
    "ID": "8in_198ch_2019_1102_65E13_neg40_annealed68min_October2020_chucktempcorrected",
    "p-stop": "comm.",
    "thickness": 300,
    "Vfb": -2,
    "fluence": 7.1,                 #round 1, c.f. https://indico.cern.ch/event/1085830/contributions/4565317/attachments/2343669/3995999/11-12-2021_RINSC_Irradiation_Validation_and_Status.pdf
    "annealing": 76.7
}
MEASUREMENTS["1101"] = {
    "Campaign": "October2020_ALPS",
    "Design": "LD",
    "Cells": [159, 171, 172],
    "ID": "8in_198ch_2019_1101_65E13_neg40_annealed68min_October2020_chucktempcorrected",
    "p-stop": "comm.",
    "thickness": 300,
    "Vfb": -5,
    "fluence": 7.1,                 #round 1, c.f. https://indico.cern.ch/event/1085830/contributions/4565317/attachments/2343669/3995999/11-12-2021_RINSC_Irradiation_Validation_and_Status.pdf
    "annealing": 76.0
}
MEASUREMENTS["2002"] = {
    "Campaign": "Spring2021_ALPS",
    "Design": "LD",
    "Cells": [78, 92, 93],
    "ID": "8in_198ch_2019_2002_25E14_neg40_80minAnnealing_chucktempcorrected",
    "p-stop": "ind.",
    "thickness": 200,
    "Vfb": -2, 
    "fluence": 23.5,                  #round 5, c.f. https://indico.cern.ch/event/1085830/contributions/4565317/attachments/2343669/3995999/11-12-2021_RINSC_Irradiation_Validation_and_Status.pdf
    "annealing": 79.9
}
MEASUREMENTS["2114"] = {
    "Campaign": "Spring2021_ALPS",
    "Design": "LD",
    "Cells": [78, 92, 93],
    "ID": "8in_198ch_2019_2114_25E14_neg40_80minAnnealing_chucktempcorrected",
    "p-stop": "comm.",
    "thickness": 200,
    "Vfb": -2, 
    "fluence": 23.5,                  #round 5, c.f. https://indico.cern.ch/event/1085830/contributions/4565317/attachments/2343669/3995999/11-12-2021_RINSC_Irradiation_Validation_and_Status.pdf
    "annealing": 79.9
}
MEASUREMENTS["2105"] = {
    "Campaign": "Spring2021_ALPS",
    "Design": "LD",
    "Cells": [78, 92, 93],
    "ID": "8in_198ch_2019_2105_25E14_neg40_80minAnnealing_chucktempcorrected",
    "p-stop": "comm.",
    "thickness": 200,
    "Vfb": -5, 
    "fluence": 23.5,                  #round 5, c.f. https://indico.cern.ch/event/1085830/contributions/4565317/attachments/2343669/3995999/11-12-2021_RINSC_Irradiation_Validation_and_Status.pdf
    "annealing": 79.9
}
MEASUREMENTS["2004"] = {
    "Campaign": "Spring2021_ALPS",
    "Design": "LD",
    "Cells": [78, 92, 93],
    "ID": "8in_198ch_2019_2004_25E14_neg40_80minAnnealing_chucktempcorrected",
    "p-stop": "ind.",
    "thickness": 200,
    "Vfb": -5, 
    "fluence": 23.5,                  #round 5, c.f. https://indico.cern.ch/event/1085830/contributions/4565317/attachments/2343669/3995999/11-12-2021_RINSC_Irradiation_Validation_and_Status.pdf
    "annealing": 79.9
}
MEASUREMENTS["3003"] = {
    "Campaign": "Winter2021",
    "Design": "HD",
    "Cells": [103, 104, 121, 122, 140, 141, 142],
    "ID": "8in_432_3003_1E16_neg40deg_new_picoammeter_Winter2021_chucktempcorrected",
    "p-stop": "ind.",
    "thickness": 120,
    "Vfb": -2, 
    "fluence": 110,                 #round 3, c.f. https://indico.cern.ch/event/1085830/contributions/4565317/attachments/2343669/3995999/11-12-2021_RINSC_Irradiation_Validation_and_Status.pdf                 
    "annealing": 400
}
MEASUREMENTS["3103"] = {
    "Campaign": "Winter2021",
    "Design": "HD",
    "Cells": [103, 104, 121, 122, 140, 141, 142],
    "ID": "8in_432_3103_1E16_neg40deg_new_picoammeter_Winter2021_chucktempcorrected",
    "p-stop": "comm.",
    "thickness": 120,
    "Vfb": -2, 
    "fluence": 110,                 #round 3, c.f. https://indico.cern.ch/event/1085830/contributions/4565317/attachments/2343669/3995999/11-12-2021_RINSC_Irradiation_Validation_and_Status.pdf
    "annealing": 400
}
MEASUREMENTS["3009"] = {
    "Campaign": "June2021_ALPS",
    "Design": "HD",
    "Cells": [166, 167, 187, 188, 189, 211, 212],
    "ID": "8in_432_3009_5E15_neg40_post80minAnnealing_chucktempcorrected",
    "p-stop": "ind.",
    "thickness": 120,
    "Vfb": -2, 
    "fluence": 50,                  #round 8
    "annealing": 80
}
MEASUREMENTS["3010"] = {
    "Campaign": "June2021_ALPS",
    "Design": "HD",
    "Cells": [166, 167, 187, 188, 189, 211, 212],
    "ID": "8in_432_3010_5E15_neg40_post80minAnnealing_chucktempcorrected",
    "p-stop": "ind.",
    "thickness": 120,
    "Vfb": -2, 
    "fluence": 50,                  #round 8
    "annealing": 80
}
MEASUREMENTS["3109"] = {
    "Campaign": "June2021_ALPS",
    "Design": "HD",
    "Cells": [166, 167, 187, 188, 189, 211, 212],
    "ID": "8in_432_3109_5E15_neg40_post80minAnnealing_chucktempcorrected",
    "p-stop": "comm.",
    "thickness": 120,
    "Vfb": -2, 
    "fluence": 50,                  #round 8
    "annealing": 80
}
MEASUREMENTS["3110"] = {
    "Campaign": "June2021_ALPS",
    "Design": "HD",
    "Cells": [166, 167, 187, 188, 189, 211, 212],
    "ID": "8in_432_3110_5E15_neg40_post80minAnnealing_chucktempcorrected",
    "p-stop": "comm.",
    "thickness": 120,
    "Vfb": -2, 
    "fluence": 50,                  #round 8
    "annealing": 80
}
MEASUREMENTS["1013"] = {
    "Campaign": "June2021_ALPS",
    "Design": "LD",
    "Cells": [164, 165, 175],
    "ID": "8in_198ch_2019_1013_1E15_neg40_post80minAnnealing_chucktempcorrected",
    "p-stop": "ind.",
    "thickness": 300,
    "Vfb": -2, 
    "fluence": 8.2,                  #round 10               
    "annealing": 80.
}
MEASUREMENTS["1114"] = {
    "Campaign": "June2021_ALPS",
    "Design": "LD",
    "Cells": [164, 165, 175],
    "ID": "8in_198ch_2019_1114_1E15_neg40_post80minAnnealing_chucktempcorrected",
    "p-stop": "comm.",
    "thickness": 300,
    "Vfb": -2, 
    "fluence": 8.2,                  #round 10               
    "annealing": 80.
}
MEASUREMENTS["5414"] = {
    "Campaign": "June2021_ALPS",
    "Design": "LD",
    "Cells": [164, 165, 175],
    "ID": "8in_198ch_2019_N0541_04_25E14_neg40_post80minAnnealing_chucktempcorrected",
    "p-stop": "ind.",
    "thickness": 200,
    "Vfb": -5, 
    "fluence": 19,                  #round 11
    "annealing": 100.
}

MEASUREMENTS["3005"] = {
    "Campaign": "TTU_October2021",
    "Design": "HD",
    "Cells": [203, 204, 227, 228, 229, 251, 252],
    "ID": "8in_432_3005_25E14_neg40_postAnnealing_TTU",
    "p-stop": "ind.",
    "thickness": 120,
    "Vfb": -2,                  #cf. https://docs.google.com/spreadsheets/d/1YQ9Icu-fA5thREVmhuf5KUcIxVmbys7nzgwrs02DT20/edit#gid=928090113
    "fluence": 16.5,             #round 7
    "annealing": 80
}

MEASUREMENTS["3008"] = {
    "Campaign": "TTU_October2021",
    "Design": "HD",
    "Cells": [203, 204, 227, 228, 229, 251, 252],
    "ID": "8in_432_3008_25E14_neg40_postAnnealing_TTU",
    "p-stop": "ind.",
    "thickness": 120,
    "Vfb": -2,                  #https://docs.google.com/spreadsheets/d/1YQ9Icu-fA5thREVmhuf5KUcIxVmbys7nzgwrs02DT20/edit#gid=928090113
    "fluence": 16.5,             #round 7
    "annealing": 80
}

MEASUREMENTS["3104"] = {
    "Campaign": "TTU_October2021",
    "Design": "HD",
    "Cells": [203, 204, 227, 228, 229, 251, 252],
    "ID": "8in_432_3104_25E14_neg40_postAnnealing_TTU",
    "p-stop": "comm.",
    "thickness": 120,
    "Vfb": -2,                  #https://docs.google.com/spreadsheets/d/1YQ9Icu-fA5thREVmhuf5KUcIxVmbys7nzgwrs02DT20/edit#gid=928090113
    "fluence": 16.5,             #round 7
    "annealing": 80
}

MEASUREMENTS["3105"] = {
    "Campaign": "TTU_October2021",
    "Design": "HD",
    "Cells": [203, 204, 227, 228, 229, 251, 252],
    "ID": "8in_432_3105_25E14_neg40_postAnnealing_TTU",
    "p-stop": "comm.",
    "thickness": 120,
    "Vfb": -2,                  #https://docs.google.com/spreadsheets/d/1YQ9Icu-fA5thREVmhuf5KUcIxVmbys7nzgwrs02DT20/edit#gid=928090113
    "fluence": 16.5,             #round 7
    "annealing": 80
}

MEASUREMENTS["3101"] = {
    "Campaign": "TTU_October2021",
    "Design": "HD",
    "Cells": [203, 204, 227, 228, 229, 251, 252],
    "ID": "8in_432_3101_1E16_neg40_TTU",
    "p-stop": "comm.",
    "thickness": 120,
    "Vfb": -2,                  #https://docs.google.com/spreadsheets/d/1YQ9Icu-fA5thREVmhuf5KUcIxVmbys7nzgwrs02DT20/edit#gid=928090113
    "fluence": 80.0,             #round 6
    "annealing": 0
}

MEASUREMENTS["3107"] = {
    "Campaign": "TTU_October2021",
    "Design": "HD",
    "Cells": [203, 204, 227, 228, 229, 251, 252],
    "ID": "8in_432_3107_1E16_neg40_TTU",
    "p-stop": "comm.",
    "thickness": 120,
    "Vfb": -5,                  #https://docs.google.com/spreadsheets/d/1YQ9Icu-fA5thREVmhuf5KUcIxVmbys7nzgwrs02DT20/edit#gid=928090113
    "fluence": 80.0,             #round 6
    "annealing": 0
}


MEASUREMENTS["1105"] = {
    "Campaign": "TTU_October2021",
    "Design": "LD",
    "Cells": [88, 103, 104],
    "ID": "8in_198ch_2019_1105_15E14_neg40_postAnnealing_TTU",
    "p-stop": "comm.",
    "thickness": 300,
    "Vfb": -5,                  #https://docs.google.com/spreadsheets/d/1YQ9Icu-fA5thREVmhuf5KUcIxVmbys7nzgwrs02DT20/edit#gid=928090113
    "fluence": 13.5,             #round 9
    "annealing": 80
}

MEASUREMENTS["1003"] = {
    "Campaign": "TTU_October2021",
    "Design": "LD",
    "Cells": [88, 103, 104],
    "ID": "8in_198ch_2019_1003_15E14_neg40_postAnnealing_TTU",
    "p-stop": "ind.",
    "thickness": 300,
    "Vfb": -2,                  #https://docs.google.com/spreadsheets/d/1YQ9Icu-fA5thREVmhuf5KUcIxVmbys7nzgwrs02DT20/edit#gid=928090113
    "fluence": 13.5,             #round 9
    "annealing": 80
}


MEASUREMENTS["1113"] = {
    "Campaign": "TTU_October2021",
    "Design": "LD",
    "Cells": [88, 103, 104],
    "ID": "8in_198ch_2019_1113_15E14_neg40_postAnnealing_TTU",
    "p-stop": "comm.",
    "thickness": 300,
    "Vfb": -2,                  #https://docs.google.com/spreadsheets/d/1YQ9Icu-fA5thREVmhuf5KUcIxVmbys7nzgwrs02DT20/edit#gid=928090113
    "fluence": 13.5,             #round 9
    "annealing": 80
}

MEASUREMENTS["54117"] = {
    "Campaign": "TTU_October2021",
    "Design": "LD",
    "Cells": [88, 103, 104],
    "ID": "8in_198ch_2019_N0541_17_15E14_neg40_postAnnealing_TTU",
    "p-stop": "ind.",
    "thickness": 300,
    "Vfb": -5,                  #https://docs.google.com/spreadsheets/d/1YQ9Icu-fA5thREVmhuf5KUcIxVmbys7nzgwrs02DT20/edit#gid=928090113
    "fluence": 13.5,             #round 9
    "annealing": 80
}



class Dataset:
    def __init__(self):
        self.dict = {}
        self.data_file_location = "<MAINDATADIR>"
        self.key = ""

    def add_entry(self, ID, measID, campaign, props=None):
        self.dict[ID] = {"MeasID": measID, "Campaign": campaign, "Priority": 999}
        default_styleprops = {"Color": ROOT.kBlack, "MarkerStyle": 21, "LineStyle": 1, "Label": "-"}
        if props is None:
            props = default_styleprops
        else:
            default_styleprops.update(props)
            props = default_styleprops
        
        self.update(ID, props)
    
    def update(self, ID, props):
        self.dict[ID].update(props)
    
    def SetGraph(self, ID, gr):
        gr.SetLineColor(self.GetLineColor(ID))
        gr.SetMarkerColor(self.GetMarkerColor(ID))
        gr.SetLineStyle(self.GetLineStyle(ID))
        gr.SetMarkerStyle(self.GetMarkerStyle(ID))
        self.update(ID, {"graph": gr})

    def GetPath(self, ID):
        cid = self.dict[ID]["Campaign"]
        mid = self.dict[ID]["MeasID"]
        return self.data_file_location.replace("<MAINDATADIR>", os.environ["DATA_DIR"]).replace("<CAMPAIGN>", cid).replace("<MEASID>", mid)

    def GetKey(self):
        return self.key
    
    def GetGraph(self, ID):
        return self.dict[ID]["graph"]

    def GetLineColor(self, ID):
        return self.dict[ID]["Color"]
    
    def GetMarkerColor(self, ID):
        return self.GetLineColor(ID)

    def GetLineStyle(self, ID):
        return self.dict[ID]["LineStyle"]

    def GetMarkerStyle(self, ID):
        return self.dict[ID]["MarkerStyle"]

    def GetLabel(self, ID):
        return self.dict[ID]["Label"]
    
    def GetIDs(self):
        return [k[0] for k in sorted(self.dict.items(), key = lambda x : x[1]["Priority"])]



class TotalIV(Dataset):
    def __init__(self, _type="good"):
        super().__init__()
        self.data_file_location = "<MAINDATADIR>/iv/<CAMPAIGN>/totalIV/<MEASID>/total_current_IV.root"
        self.key = "total_current_IV"

        if _type == "good":
            # specify which data 
            self.add_entry("1002", "8in_198ch_2019_1002_65E13_neg40_October2020", "October2020_ALPS")
            self.add_entry("3003", "8in_432_3003_1E16_neg40deg_new_picoammeter_Winter2021", "Winter2021")
            #self.add_entry("2004", "8in_198ch_2019_2004_25E14_neg40_80minAnnealing", "Spring2021_ALPS")
            #self.add_entry("1013", "8in_198ch_2019_1013_1E15_neg40_post80minAnnealing", "June2021_ALPS")
            ##self.add_entry("3009", "8in_432_3009_5E15_neg40_post80minAnnealing", "June2021_ALPS")
            #self.add_entry("0541_04", "8in_198ch_2019_N0541_04_25E14_neg40_post80minAnnealing", "June2021_ALPS")
        
            # specify style
            self.update("3003", {"Color": ROOT.kBlack, "LineStyle": 2, "MarkerStyle": 20, "Label": "HD, 120 #mum, ~11.0E15 neq/cm^{2}", "Priority": 1})
            #self.update("3009", {"Color": ROOT.kBlack, "LineStyle": 1, "MarkerStyle": 28, "Label": "HD, 120 #mum, 4.2E15 neq, after annealing", "Priority": 2})
            #self.update("0541_04", {"Color": ROOT.kCyan+1, "LineStyle": 1, "MarkerStyle": 21, "Label": "LD, 200 #mum, 1.5E15 neq", "Priority": 3})
            #self.update("2004", {"Color": ROOT.kBlue+1, "LineStyle": 2, "MarkerStyle": 27, "Label": "LD, 200 #mum, 2.3E15 neq", "Priority": 4})
            #self.update("1013", {"Color": ROOT.kBlue+1, "LineStyle": 1, "MarkerStyle": 21, "Label": "LD, 300 #mum, 0.8E15 neq, after annealing", "Priority": 5})
            self.update("1002", {"Color": ROOT.kBlue+1, "LineStyle": 2, "MarkerStyle": 23, "Label": "LD,  300 #mum, ~0.7E15 neq/cm^{2}", "Priority": 2})

        else:
            #self.add_entry("2002", "8in_198ch_2019_2002_25E14_neg40_80minAnnealing", "Spring2021_ALPS")
            #self.add_entry("2002_unannealed", "8in_198ch_2019_2002_25E14_neg40", "Spring2021_ALPS")
            self.add_entry("3110", "8in_432_3110_5E15_neg40_post80minAnnealing", "June2021_ALPS")
            self.add_entry("3110_afterCV", "8in_432_3110_5E15_neg40_post80minAnnealing_afterDischarge", "June2021_ALPS")
            self.add_entry("0538_03", "8in_198ch_2019_N0538_3_1E15_neg40_post80minAnnealing", "June2021_ALPS")
            self.add_entry("0538_03_unannealed", "8in_198ch_2019_N0538_3_1E15_neg40", "June2021_ALPS")
            

            self.update("3110", {"Color": ROOT.kBlack, "LineStyle": 1, "MarkerStyle": 28, "Label": "HD, 120 #mum, 4.2E15 neq, after annealing, #font[22]{before discharge}", "Priority": 1})
            self.update("3110_afterCV", {"Color": ROOT.kOrange+1, "LineStyle": 2, "MarkerStyle": 22, "Label": "HD, 120 #mum, 4.2E15 neq, after annealing, #font[22]{after discharge}", "Priority": 2})
            #self.update("2002", {"Color": ROOT.kGray+1, "LineStyle": 1, "MarkerStyle": 20, "Label": "HD, 200 #mum, 2.9E15 neq", "Priority": 3})
            #self.update("2002_unannealed", {"Color": ROOT.kGray+1, "LineStyle": 3, "MarkerStyle": 22, "Label": " ... no annealing", "Priority": 4})
            self.update("0538_03_unannealed", {"Color": ROOT.kGray+1, "LineStyle": 2, "MarkerStyle": 27, "Label": "LD, 300 #mum, 0.8E15 neq, #font[22]{before annealing}, after discharge", "Priority": 3})
            self.update("0538_03", {"Color": ROOT.kBlue+1, "LineStyle": 1, "MarkerStyle": 21, "Label": "LD, 300 #mum, 0.8E15 neq, #font[22]{after annealing}, after discharge", "Priority": 4})
            

A_FULLPAD_LD = 122105993.42116399       #mum2
A_FULLPAD_HD = 55510000.0       #mum2
A_OUTERCALIB_LD = 92339686.33005302
A_INNERCALIB_LD = 26947138.189286005
A_EDGELARGE_LD = 127001525.27368101
A_EDGESMALL_LD = 85040178.32025799

FULL_CELL_AREA = {
    "LD": A_FULLPAD_LD,      #unit: mum
    "HD": A_FULLPAD_HD,      #unit: mum
}

class ChannelIV(Dataset):
    def __init__(self, _type="sensors"):
        super().__init__()
        self.data_file_location = "<MAINDATADIR>/iv/<CAMPAIGN>/channelIV/<MEASID>/TGraphErrors.root"
        self.key = "IV_uncorrected_channel<CHANNEL>"

        if _type == "sensors":
            #self.add_entry("1002", "8in_198ch_2019_1002_65E13_neg40_October2020_chucktempcorrected", "October2020_ALPS", {"Channel": 24, "RelThickness": 3./2., "RelArea": A_FULLPAD_LD/A_FULLPAD_LD})
            #self.add_entry("3003", "8in_432_3003_1E16_neg40deg_new_picoammeter_Winter2021_chucktempcorrected", "Winter2021", {"Channel": 313, "RelThickness": 1.2/2., "RelArea": A_FULLPAD_HD/A_FULLPAD_LD})
            #self.add_entry("2004", "8in_198ch_2019_2004_25E14_neg40_chucktempcorrected", "Spring2021_ALPS", {"Channel": 24, "RelThickness": 2./2., "RelArea": A_FULLPAD_LD/A_FULLPAD_LD})
            self.add_entry("3009", "8in_432_3009_5E15_neg40_chucktempcorrected", "June2021_ALPS", {"Channel": 123, "RelThickness": 1.2/2., "RelArea": A_FULLPAD_HD/A_FULLPAD_LD})
            self.add_entry("1013", "8in_198ch_2019_1013_1E15_neg40_chucktempcorrected", "June2021_ALPS", {"Channel": 24, "RelThickness": 3./2., "RelArea": A_FULLPAD_LD/A_FULLPAD_LD})
            self.add_entry("0541_04", "8in_198ch_2019_N0541_04_25E14_neg40_chucktempcorrected", "June2021_ALPS", {"Channel": 24, "RelThickness": 2./2., "RelArea": A_FULLPAD_LD/A_FULLPAD_LD})

            # specify style
            #self.update("3003", {"Color": ROOT.kGray+1, "LineStyle": 1, "MarkerStyle": 20, "Label": "HD, 120 #mum, 11.0 E15 neq", "Priority": 1})
            self.update("3009", {"Color": ROOT.kBlack, "LineStyle": 1, "MarkerStyle": 28, "Label": "HD, 120 #mum, ~4.2E15 neq/cm^{2}", "Priority": 2})
            self.update("0541_04", {"Color": ROOT.kOrange+1, "LineStyle": 1, "MarkerStyle": 27  , "Label": "LD, 200 #mum, ~1.9E15 neq/cm^{2}", "Priority": 3})
            #self.update("2004", {"Color": ROOT.kBlue+1, "LineStyle": 2, "MarkerStyle": 27, "Label": "LD, 200 #mum, 2.9E15 neq", "Priority": 4})
            self.update("1013", {"Color": ROOT.kBlue+1, "LineStyle": 1, "MarkerStyle": 21, "Label": "LD, 300 #mum, ~0.8E15 neq/cm^{2}", "Priority": 5})
            #self.update("1002", {"Color": ROOT.kRed+1, "LineStyle": 2, "MarkerStyle": 32, "Label": "LD, 300 #mum, 0.9E15 neq", "Priority": 6})
        
        else:
            self.add_entry("0541_04_24", "8in_198ch_2019_N0541_04_25E14_neg40_chucktempcorrected", "June2021_ALPS", {"Channel": 24, "RelArea": A_FULLPAD_LD/A_FULLPAD_LD})
            self.add_entry("0541_04_25", "8in_198ch_2019_N0541_04_25E14_neg40_chucktempcorrected", "June2021_ALPS", {"Channel": 25, "RelArea": A_FULLPAD_LD/A_FULLPAD_LD})
            self.add_entry("0541_04_18", "8in_198ch_2019_N0541_04_25E14_neg40_chucktempcorrected", "June2021_ALPS", {"Channel": 18, "RelArea": A_EDGELARGE_LD/A_FULLPAD_LD})
            self.add_entry("0541_04_5", "8in_198ch_2019_N0541_04_25E14_neg40_chucktempcorrected", "June2021_ALPS", {"Channel": 5, "RelArea": A_EDGESMALL_LD/A_FULLPAD_LD})
            self.add_entry("0541_04_13", "8in_198ch_2019_N0541_04_25E14_neg40_chucktempcorrected", "June2021_ALPS", {"Channel": 13, "RelArea": A_OUTERCALIB_LD/A_FULLPAD_LD})
            self.add_entry("0541_04_14", "8in_198ch_2019_N0541_04_25E14_neg40_chucktempcorrected", "June2021_ALPS", {"Channel": 14, "RelArea": A_INNERCALIB_LD/A_FULLPAD_LD})

            self.update("0541_04_24", {"Color": ROOT.kCyan+1, "LineStyle": 3, "MarkerStyle": 21, "Label": "full pad (#24)", "Priority": 1})
            self.update("0541_04_25", {"Color": ROOT.kBlack, "LineStyle": 2, "MarkerStyle": 28, "Label": "full pad (#25)", "Priority": 2})
            self.update("0541_04_13", {"Color": ROOT.kGray+1, "LineStyle": 1, "MarkerStyle": 20, "Label": "outer calib. pad (#13)", "Priority": 3})
            self.update("0541_04_14", {"Color": ROOT.kBlue+1, "LineStyle": 1, "MarkerStyle": 27, "Label": "inner calib. pad (#14)", "Priority": 4})
            self.update("0541_04_18", {"Color": ROOT.kOrange+1, "LineStyle": 3, "MarkerStyle": 22, "Label": "large edge pad (#18)", "Priority": 5})
            self.update("0541_04_5", {"Color": ROOT.kRed+1, "LineStyle": 2, "MarkerStyle": 32, "Label": "small edge pad (#5)", "Priority": 6})


    def GetChannel(self, ID):
        return self.dict[ID]["Channel"]

    def GetKey(self, ID):
        _channel = self.GetChannel(ID)
        return self.key.replace("<CHANNEL>", str(_channel))



class ChannelCV(ChannelIV):
    def __init__(self, _type="sensors"):
        super().__init__(_type)    
        self.data_file_location = "<MAINDATADIR>/cv/<CAMPAIGN>/channelCV/<MEASID>/TGraphErrors.root"
        self.key = "CV_serial_open_corrected_channel<CHANNEL>"        
        self.dict = {}

        if _type == "sensors":
            self.add_entry("3009", "8in_432_3009_5E15_neg40_post80minAnnealing_chucktempcorrected", "June2021_ALPS", {"Channel": 123, "RelThickness": 1.2/2., "RelArea": A_FULLPAD_HD/A_FULLPAD_LD})
            self.add_entry("1013", "8in_198ch_2019_1013_1E15_neg40_post80minAnnealing_chucktempcorrected", "June2021_ALPS", {"Channel": 24, "RelThickness": 3./2., "RelArea": A_FULLPAD_LD/A_FULLPAD_LD})
            self.add_entry("0541_04", "8in_198ch_2019_N0541_04_25E14_neg40_post80minAnnealing_chucktempcorrected", "June2021_ALPS", {"Channel": 24, "RelThickness": 2./2., "RelArea": A_FULLPAD_LD/A_FULLPAD_LD})

            # specify style
            self.update("3009", {"Color": ROOT.kCyan+1, "LineStyle": 2, "MarkerStyle": 23, "Label": "HD, 120 #mum, ~4.2E15 neq/cm^{2} + annealing", "Priority": 2})
            self.update("0541_04", {"Color": ROOT.kOrange+1, "LineStyle": 2, "MarkerStyle": 20  , "Label": "LD, 200 #mum, ~1.9E15 neq/cm^{2} + annealing", "Priority": 3})
            self.update("1013", {"Color": ROOT.kBlue+1, "LineStyle": 2, "MarkerStyle": 21, "Label": "LD, 300 #mum, ~0.8E15 neq/cm^{2} + annealing", "Priority": 5})
        
        else:
            self.add_entry("0541_04_24", "8in_198ch_2019_N0541_04_25E14_neg40_post80minAnnealing_chucktempcorrected", "June2021_ALPS", {"Channel": 24, "RelArea": A_FULLPAD_LD/A_FULLPAD_LD})
            self.add_entry("0541_04_25", "8in_198ch_2019_N0541_04_25E14_neg40_post80minAnnealing_chucktempcorrected", "June2021_ALPS", {"Channel": 25, "RelArea": A_FULLPAD_LD/A_FULLPAD_LD})
            self.add_entry("0541_04_18", "8in_198ch_2019_N0541_04_25E14_neg40_post80minAnnealing_chucktempcorrected", "June2021_ALPS", {"Channel": 18, "RelArea": A_EDGELARGE_LD/A_FULLPAD_LD})
            self.add_entry("0541_04_5", "8in_198ch_2019_N0541_04_25E14_neg40_post80minAnnealing_chucktempcorrected", "June2021_ALPS", {"Channel": 5, "RelArea": A_EDGESMALL_LD/A_FULLPAD_LD})
            self.add_entry("0541_04_13", "8in_198ch_2019_N0541_04_25E14_neg40_post80minAnnealing_chucktempcorrected", "June2021_ALPS", {"Channel": 13, "RelArea": A_OUTERCALIB_LD/A_FULLPAD_LD})
            self.add_entry("0541_04_14", "8in_198ch_2019_N0541_04_25E14_neg40_post80minAnnealing_chucktempcorrected", "June2021_ALPS", {"Channel": 14, "RelArea": A_INNERCALIB_LD/A_FULLPAD_LD})

            self.update("0541_04_24", {"Color": ROOT.kCyan+1, "LineStyle": 3, "MarkerStyle": 21, "Label": "full pad (#24)", "Priority": 1})
            self.update("0541_04_25", {"Color": ROOT.kBlack, "LineStyle": 2, "MarkerStyle": 28, "Label": "full pad (#25)", "Priority": 2})
            self.update("0541_04_13", {"Color": ROOT.kGray+1, "LineStyle": 1, "MarkerStyle": 20, "Label": "outer calib. pad (#13)", "Priority": 3})
            self.update("0541_04_14", {"Color": ROOT.kBlue+1, "LineStyle": 1, "MarkerStyle": 27, "Label": "inner calib. pad (#14)", "Priority": 4})
            self.update("0541_04_18", {"Color": ROOT.kOrange+1, "LineStyle": 3, "MarkerStyle": 22, "Label": "large edge pad (#18)", "Priority": 5})
            self.update("0541_04_5", {"Color": ROOT.kRed+1, "LineStyle": 2, "MarkerStyle": 32, "Label": "small edge pad (#5)", "Priority": 6})


class ChannelInvCV(ChannelCV):
    def __init__(self, _type="sensors"):
        super().__init__(_type)    
        self.data_file_location = "<MAINDATADIR>/cv/<CAMPAIGN>/Vdep/<MEASID>/ch_<CHANNEL>.root"
        self.key = "Vdep_serial_model_ch<CHANNEL>"




# creating the mapping
rot = {}
#this is the mapping without double counting!
#corrected on 09 August 2021
rot[0] = [1, 10, 21, 32, 44, 57, 73, 88]
rot[0] += [2, 11, 22, 33, 45, 58, 74, 89]
rot[0] += [3, 12, 23, 34, 46, 59, 75, 90]
rot[0] += [4, 13, 14, 24, 35, 47, 60, 76, 91]
rot[0] += [5, 15, 25, 36, 48, 61, 62, 77, 92]
rot[0] += [6, 16, 26, 37, 49, 63, 78, 93]
rot[0] += [7, 17, 27, 38, 50, 64, 79, 94]
rot[0] += [8, 18, 28, 39, 51, 65, 80, 95]

rot[120] = [190, 181, 171, 159, 146, 132, 119, 103]
rot[120] += [180, 170, 158, 145, 131, 117, 102, 87]
rot[120] += [169, 157, 144, 130, 116, 101, 86, 72]
rot[120] += [156, 142, 143, 129, 115, 100, 85, 71, 56]
rot[120] += [141, 128, 114, 99, 84, 69, 70, 55, 43]
rot[120] += [127, 113, 98, 83, 68, 54, 42, 31]
rot[120] += [112, 97, 82, 67, 53, 41, 30, 20]
rot[120] += [96, 81, 66, 52, 40, 29, 19, 9]

rot[240] = [111, 110, 109, 108, 107, 106, 105, 104]
rot[240] += [126, 125, 124, 123, 122, 121, 120, 119]
rot[240] += [140, 139, 138, 137, 136, 135, 134, 133]
rot[240] += [155, 153, 154, 152, 151, 150, 149, 148, 147]
rot[240] += [168, 167, 166, 165, 164, 162, 163, 161, 160]
rot[240] += [179, 178, 177, 176, 175, 174, 173, 172]
rot[240] += [189, 188, 187, 186, 185, 184, 183, 182]
rot[240] += [198, 197, 196, 195, 194, 193, 192, 191]
