import ROOT
import os

FULL_CELL_AREA = {
    "LD": 125415131,      #unit: mum
    "HD": 55508574,      #unit: mum
}

GEOFILES = {
    "LD": "hex_positions_HPK_198ch_8inch_edge_ring_testcap.txt",
    "HD": "hex_positions_HPK_432ch_8inch_edge_ring_testcap.txt"
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
    "fluence": 8.6,                 #round 1, c.f. e-mail U. Heintz 06 May 2021
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
    "fluence": 8.6,                 #round 1, c.f. e-mail U. Heintz 06 May 2021
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
    "fluence": 8.6,                 #round 1, c.f. e-mail U. Heintz 06 May 2021
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
    "fluence": 29,                  #round 5, c.f. e-mail U. Heintz 06 May 2021
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
    "fluence": 29,                  #round 5, c.f. e-mail U. Heintz 06 May 2021
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
    "fluence": 29,                  #round 5, c.f. e-mail U. Heintz 06 May 2021
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
    "fluence": 29,                  #round 5, c.f. e-mail U. Heintz 06 May 2021
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
    "fluence": 110,                 #round 3, c.f. e-mail U. Heintz 06 May 2021                 
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
    "fluence": 110,                 #round 3, c.f. e-mail U. Heintz 06 May 2021
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
    "fluence": 53,
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
    "fluence": 53,
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
    "fluence": 53,
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
    "fluence": 53,
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
    "fluence": 10,                  
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
    "fluence": 10,                  
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
    "fluence": 25,                  
    "annealing": 100.
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
            self.add_entry("1002", "8in_198ch_2019_1002_65E13_neg40_annealed68min_October2020", "October2020_ALPS")
            self.add_entry("3003", "8in_432_3003_1E16_neg40deg_new_picoammeter_Winter2021", "Winter2021")
            self.add_entry("2004", "8in_198ch_2019_2004_25E14_neg40_80minAnnealing", "Spring2021_ALPS")
            self.add_entry("3009", "8in_432_3009_5E15_neg40_post80minAnnealing", "June2021_ALPS")
            self.add_entry("1013", "8in_198ch_2019_1013_1E15_neg40_post80minAnnealing", "June2021_ALPS")
            self.add_entry("0541_04", "8in_198ch_2019_N0541_04_25E14_neg40_post80minAnnealing", "June2021_ALPS")
        
            # specify style
            self.update("3003", {"Color": ROOT.kGray+1, "LineStyle": 1, "MarkerStyle": 20, "Label": "HD, 120 #mum, 1E16 neq", "Priority": 1})
            self.update("3009", {"Color": ROOT.kBlack, "LineStyle": 2, "MarkerStyle": 20, "Label": "HD, 120 #mum, 5E15 neq", "Priority": 2})
            self.update("0541_04", {"Color": ROOT.kCyan+1, "LineStyle": 1, "MarkerStyle": 21, "Label": "LD, 200 #mum, 2.5E15 neq", "Priority": 3})
            self.update("2004", {"Color": ROOT.kBlue+1, "LineStyle": 2, "MarkerStyle": 21, "Label": "LD, 200 #mum, 2.5E15 neq", "Priority": 4})
            self.update("1013", {"Color": ROOT.kOrange+1, "LineStyle": 1, "MarkerStyle": 22, "Label": "LD, 300 #mum, 1E15 neq", "Priority": 5})
            self.update("1002", {"Color": ROOT.kRed+1, "LineStyle": 2, "MarkerStyle": 22, "Label": "LD, 300 #mum, 6.5E14 neq", "Priority": 6})

        else:
            self.add_entry("2002", "8in_198ch_2019_2002_25E14_neg40_80minAnnealing", "Spring2021_ALPS")
            self.add_entry("2002_unannealed", "8in_198ch_2019_2002_25E14_neg40", "Spring2021_ALPS")
            self.add_entry("3110", "8in_432_3110_5E15_neg40_post80minAnnealing", "June2021_ALPS")
            self.add_entry("3110_afterCV", "8in_432_3110_5E15_neg40_post80minAnnealing_afterDischarge", "June2021_ALPS")
            self.add_entry("0538_03", "8in_198ch_2019_N0538_3_1E15_neg40_post80minAnnealing", "June2021_ALPS")
            self.add_entry("0538_03_unannealed", "8in_198ch_2019_N0538_3_1E15_neg40", "June2021_ALPS")
            

            self.update("3110", {"Color": ROOT.kBlue+1, "LineStyle": 1, "MarkerStyle": 20, "Label": "HD, 120 #mum, 5E15 neq", "Priority": 1})
            self.update("3110_afterCV", {"Color": ROOT.kBlue+1, "LineStyle": 3, "MarkerStyle": 22, "Label": "... after CV characterisation", "Priority": 2})
            self.update("2002", {"Color": ROOT.kGray+1, "LineStyle": 1, "MarkerStyle": 20, "Label": "HD, 200 #mum, 2.5E15 neq", "Priority": 3})
            self.update("2002_unannealed", {"Color": ROOT.kGray+1, "LineStyle": 3, "MarkerStyle": 22, "Label": " ... no annealing", "Priority": 4})
            self.update("0538_03", {"Color": ROOT.kRed+1, "LineStyle": 1, "MarkerStyle": 20, "Label": "LD, 300 #mum, 1E15 neq", "Priority": 5})
            self.update("0538_03_unannealed", {"Color": ROOT.kRed+1, "LineStyle": 3, "MarkerStyle": 22, "Label": "... no annealing", "Priority": 6})
            


class ChannelIV(Dataset):
    def __init__(self, _type="sensors"):
        super().__init__()
        self.data_file_location = "<MAINDATADIR>/iv/<CAMPAIGN>/channelIV/<MEASID>/TGraphErrors.root"
        self.key = "IV_uncorrected_channel<CHANNEL>"

        if _type == "sensors":
            self.add_entry("1002", "8in_198ch_2019_1002_65E13_neg40_annealed68min_October2020", "October2020_ALPS", {"Channel": 24})
            self.add_entry("3003", "8in_432_3003_1E16_neg40deg_new_picoammeter_Winter2021", "Winter2021", {"Channel": 313})
            self.add_entry("2004", "8in_198ch_2019_2004_25E14_neg40_80minAnnealing", "Spring2021_ALPS", {"Channel": 24})
            self.add_entry("3009", "8in_432_3009_5E15_neg40_post80minAnnealing", "June2021_ALPS", {"Channel": 123})
            self.add_entry("1013", "8in_198ch_2019_1013_1E15_neg40_post80minAnnealing", "June2021_ALPS", {"Channel": 24})
            self.add_entry("0541_04", "8in_198ch_2019_N0541_04_25E14_neg40_post80minAnnealing", "June2021_ALPS", {"Channel": 24})

            # specify style
            self.update("3003", {"Color": ROOT.kGray+1, "LineStyle": 1, "MarkerStyle": 20, "Label": "HD, 120 #mum, 1E16 neq", "Priority": 1})
            self.update("3009", {"Color": ROOT.kBlack, "LineStyle": 2, "MarkerStyle": 20, "Label": "HD, 120 #mum, 5E15 neq", "Priority": 2})
            self.update("0541_04", {"Color": ROOT.kCyan+1, "LineStyle": 1, "MarkerStyle": 21, "Label": "LD, 200 #mum, 2.5E15 neq", "Priority": 3})
            self.update("2004", {"Color": ROOT.kBlue+1, "LineStyle": 2, "MarkerStyle": 21, "Label": "LD, 200 #mum, 2.5E15 neq", "Priority": 4})
            self.update("1013", {"Color": ROOT.kOrange+1, "LineStyle": 1, "MarkerStyle": 22, "Label": "LD, 300 #mum, 1E15 neq", "Priority": 5})
            self.update("1002", {"Color": ROOT.kRed+1, "LineStyle": 2, "MarkerStyle": 22, "Label": "LD, 300 #mum, 6.5E14 neq", "Priority": 6})
        
        else:
            self.add_entry("0541_04_24", "8in_198ch_2019_N0541_04_25E14_neg40_post80minAnnealing", "June2021_ALPS", {"Channel": 24})
            self.add_entry("0541_04_166", "8in_198ch_2019_N0541_04_25E14_neg40_post80minAnnealing", "June2021_ALPS", {"Channel": 166})
            self.add_entry("0541_04_194", "8in_198ch_2019_N0541_04_25E14_neg40_post80minAnnealing", "June2021_ALPS", {"Channel": 194})
            self.add_entry("0541_04_156", "8in_198ch_2019_N0541_04_25E14_neg40_post80minAnnealing", "June2021_ALPS", {"Channel": 156})
            self.add_entry("0541_04_162", "8in_198ch_2019_N0541_04_25E14_neg40_post80minAnnealing", "June2021_ALPS", {"Channel": 162})
            self.add_entry("0541_04_163", "8in_198ch_2019_N0541_04_25E14_neg40_post80minAnnealing", "June2021_ALPS", {"Channel": 163})

            self.update("0541_04_24", {"Color": ROOT.kGray+1, "LineStyle": 1, "MarkerStyle": 20, "Label": "Pad 24 (full)", "Priority": 1})
            self.update("0541_04_166", {"Color": ROOT.kBlack, "LineStyle": 2, "MarkerStyle": 21, "Label": "Pad 166 (full)", "Priority": 2})
            self.update("0541_04_194", {"Color": ROOT.kCyan+1, "LineStyle": 3, "MarkerStyle": 22, "Label": "Pad 194 (edge, large)", "Priority": 3})
            self.update("0541_04_162", {"Color": ROOT.kBlue+1, "LineStyle": 3, "MarkerStyle": 20, "Label": "Pad 162 (outer calib.)", "Priority": 3})
            self.update("0541_04_156", {"Color": ROOT.kOrange+1, "LineStyle": 2, "MarkerStyle": 21, "Label": "Pad 156 (edge, small)", "Priority": 5})
            self.update("0541_04_163", {"Color": ROOT.kRed+1, "LineStyle": 1, "MarkerStyle": 22, "Label": "Pad 163 (inner calib.)", "Priority": 6})

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

class ChannelInvCV(ChannelCV):
    def __init__(self, _type="sensors"):
        super().__init__(_type)    
        self.data_file_location = "<MAINDATADIR>/cv/<CAMPAIGN>/Vdep/<MEASID>/ch_<CHANNEL>.root"
        self.key = "Vdep_serial_model_ch<CHANNEL>"