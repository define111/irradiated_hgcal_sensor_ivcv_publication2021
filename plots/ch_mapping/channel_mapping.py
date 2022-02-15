#Author: Thorben Quast, thorben.quast@cern.ch
#Date: 15 February 2022
#Description: 
#produces the hexplot channel numbering visualisation

import os, sys
import ROOT
thisdir = os.path.dirname(os.path.realpath(__file__))
from subprocess import Popen
import numpy as np
import pandas as pd
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--geometry", type=str, help="Sensor geometry.", default="LD", required=True)
args = parser.parse_args()

#read DB information
hexplot_geo_file = {
	"LD": "hex_positions_HPK_198ch_8inch_edge_ring_testcap_paper.txt",
	"HD": "hex_positions_HPK_432ch_8inch_edge_ring_testcap_paper.txt"
}[args.geometry]

tmp_file_path = os.path.join(thisdir, "%s.txt" % args.geometry)

hexplot_geo_filepath = "<HEXPLOTDIR>/geo/<GEOFILE>".replace("<HEXPLOTDIR>", os.environ["HEXPLOT_DIR"]).replace("<GEOFILE>", hexplot_geo_file)

geo_mapping = np.genfromtxt(hexplot_geo_filepath, skip_header=9, usecols=(0, 3), dtype=[np.int, np.float, np.float, np.int])
geo_mapping = pd.DataFrame(geo_mapping)
geo_mapping = geo_mapping[geo_mapping.f0<={"LD": 199, "HD": 445}[args.geometry]]
geo_mapping.f3 = geo_mapping.f3.map({
	0: -1,
	1: 0,
	4: 1,
	11: 2,
	12: 3,
	14: 4,
	41: 5,
	42: 6,
	43: 7,
	44: 8
})
geo_mapping = geo_mapping.assign(dummy=0)
geo_mapping = geo_mapping.set_index("f0")
geo_mapping.to_csv(tmp_file_path, sep=",")
with open(tmp_file_path, "r") as tmp_file:
	tmp_data = tmp_file.read()
os.remove(tmp_file_path)
tmp_data = tmp_data.replace(",", "    ")
with open(tmp_file_path, "w") as tmp_file:
	tmp_file.write(tmp_data)    


HEXPLOTCOMMAND = "<HEXPLOTDIR>/bin/HexPlot \
                -g <HEXPLOTDIR>/geo/<GEOFILE> \
                -i <INPUTFILE> \
                -o <OUTPUTFILE> \
                --if <FORMAT> \
                --nd 0 \
                --pn 0 \
                --noinfo \
                --noaxis \
                --CV -p GEO  --colorpalette <COLORPALETTE>\
                --vn 'Capacitance:<DEF>:<UNIT>' --select <VOLTAGE>\
                --addLabel '<TITLE>'\
                -z <ZMIN>:<ZMAX>"
                
HEXPLOTCOMMAND = HEXPLOTCOMMAND.replace("<HEXPLOTDIR>", os.environ["HEXPLOT_DIR"])
HEXPLOTCOMMAND = HEXPLOTCOMMAND.replace("<VOLTAGE>", "0")
HEXPLOTCOMMAND = HEXPLOTCOMMAND.replace("<COLORPALETTE>", "%s" % ROOT.kCMYK)
HEXPLOTCOMMAND = HEXPLOTCOMMAND.replace("<UNIT>", "a.u.")
HEXPLOTCOMMAND = HEXPLOTCOMMAND.replace("<FORMAT>", "PADNUM:VAL:SELECTOR")
HEXPLOTCOMMAND = HEXPLOTCOMMAND.replace("<DEF>", "Channel type")


this_cmd = HEXPLOTCOMMAND
this_cmd = this_cmd.replace("<INPUTFILE>", tmp_file_path)
this_cmd = this_cmd.replace("<OUTPUTFILE>", tmp_file_path.replace(".txt", ".pdf"))
this_cmd = this_cmd.replace("<GEOFILE>", hexplot_geo_file)
this_cmd = this_cmd.replace("<ZMIN>", "-1")
this_cmd = this_cmd.replace("<ZMAX>", "9")
this_cmd = this_cmd.replace("<TITLE>", {"LD": "Low density", "HD": "High density"}[args.geometry])

env = {}
env.update(os.environ)
p = Popen(this_cmd, stdout=sys.stdout,
		stderr=sys.stderr, shell=True, env=env)
out, err = p.communicate()
code = p.returncode
if code != 0:
	raise Exception("Hexplot plotting failed")

os.remove(tmp_file_path)