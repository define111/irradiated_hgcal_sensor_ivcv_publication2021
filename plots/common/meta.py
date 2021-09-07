import ROOT
import os

class Dataset:
    def __init__(self):
        self.dict = {}
        self.data_file_location = "<MAINDATADIR>"
        self.key = ""

    def add_entry(self, ID, measID, campaign, props=None):
        self.dict[ID] = {"MeasID": measID, "Campaign": campaign, "Priority": 999}
        props = {"Color": ROOT.kBlack, "MarkerStyle": 21, "LineStyle": 1, "Label": "-"} if props is None else props
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
    def __init__(self):
        super().__init__()
        self.data_file_location = "<MAINDATADIR>/iv/<CAMPAIGN>/totalIV/<MEASID>/total_current_IV.root"
        self.key = "total_current_IV"

        # specify which data 
        self.add_entry(1002, "8in_198ch_2019_1002_65E13_neg40_annealed68min_October2020", "October2020_ALPS")
        self.add_entry(3003, "8in_432_3003_1E16_neg40deg_new_picoammeter_Winter2021", "Winter2021")
        self.add_entry(2004, "8in_198ch_2019_2004_25E14_neg40_80minAnnealing", "Spring2021_ALPS")
        self.add_entry(3009, "8in_432_3009_5E15_neg40_post80minAnnealing", "June2021_ALPS")
        self.add_entry(1013, "8in_198ch_2019_1013_1E15_neg40_post80minAnnealing", "June2021_ALPS")
        self.add_entry(541, "8in_198ch_2019_N0541_04_25E14_neg40_post80minAnnealing", "June2021_ALPS")
    
        # specify style
        self.update(3003, {"Color": ROOT.kGray+1, "LineStyle": 1, "MarkerStyle": 20, "Label": "HD, 120 #mum, 1E16 neq/cm^{2}", "Priority": 1})
        self.update(3009, {"Color": ROOT.kBlue+1, "LineStyle": 2, "MarkerStyle": 21, "Label": "HD, 120 #mum, 5E15 neq/cm^{2}", "Priority": 2})
        self.update(541, {"Color": ROOT.kCyan+1, "LineStyle": 3, "MarkerStyle": 22, "Label": "LD, 200 #mum, 2.5E15 neq/cm^{2}", "Priority": 3})
        self.update(2004, {"Color": ROOT.kRed+1, "LineStyle": 2, "MarkerStyle": 20, "Label": "LD, 200 #mum, 2.5E15 neq/cm^{2}", "Priority": 4})
        self.update(1013, {"Color": ROOT.kGreen+1, "LineStyle": 3, "MarkerStyle": 21, "Label": "LD, 300 #mum, 1E15 neq/cm^{2}", "Priority": 5})
        self.update(1002, {"Color": ROOT.kBlack, "LineStyle": 1, "MarkerStyle": 22, "Label": "LD, 300 #mum, 6.5E14 neq/cm^{2}", "Priority": 6})



