import ROOT
import os

class Dataset:
    def __init__(self):
        self.dict = {}
        self.data_file_location = "<MAINDATADIR>"
        self.key = ""

    def add_entry(self, ID, measID, campaign, priority, props=None):
        self.dict[ID] = {"MeasID": measID, "Campaign": campaign, "Priority": priority}
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
        self.add_entry(1002, "8in_198ch_2019_1002_65E13_neg40_annealed68min_October2020", "October2020_ALPS", 0)
        self.add_entry(3003, "8in_432_3003_1E16_neg40deg_new_picoammeter_Winter2021", "Winter2021", 1)
    
        # specify style
        self.update(1002, {"Color": ROOT.kBlack, "LineStyle": 1, "MarkerStyle": 18, "Label": "LD, 300#mum, 6.5E14 neq/cm^{2}"})
        self.update(3003, {"Color": ROOT.kRed, "LineStyle": 2, "MarkerStyle": 23, "Label": "HD, 120#mum, 1E16 neq/cm^{2}"})



