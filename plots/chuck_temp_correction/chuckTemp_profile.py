# Author: Thorben Quast, thorben.quast@cern.ch
# Date: 07 May 2021

# -computes leakage current ratios of 8inch LD sensor 1004 with three different orientations
# -the leakage current ratios serve as an estimate for a relative temperature difference
# -hereby, a temperature needs to be assumed for one of the three symmetry sectors of the chuck
# -all three symmetry sectors of the silicon sensor can be used for inference of the temperature ratios
# -they should give comparable results if the leakage current difference is dominated by some chuck temperature profile

import sys
import os
from subprocess import Popen
import numpy as np
import pandas as pd

import common as cm
ROOT = cm.ROOT
ROOT.gROOT.SetBatch(True)
cm.setup_style()

import os
thisdir = os.path.dirname(os.path.realpath(__file__))


def twoD_Gaussian(_x,  variation=1.0, xo=5.450162034899229, yo=4.934790580919085, sigma_x=10.404935645994943, sigma_y=4.618399296699615, phi=0.006608356781303635):
    x = _x[0]
    y = _x[1]

    a = (np.cos(phi)**2)/(2*sigma_x**2) + (np.sin(phi)**2)/(2*sigma_y**2)
    b = -(np.sin(2*phi))/(4*sigma_x**2) + (np.sin(2*phi))/(4*sigma_y**2)
    c = (np.sin(phi)**2)/(2*sigma_x**2) + (np.cos(phi)**2)/(2*sigma_y**2)
    g = variation*(0.5-np.exp( - (a*((x-xo)**2) + 2*b*(x-xo)*(y-yo) 
                            + c*((y-yo)**2))))
    return g.ravel()

CAMPAIGN = "Spring2021_ALPS"

# plotting of ratios with hexplot
HEXPLOTCOMMAND = "<HEXPLOTDIR>/bin/HexPlot \
                -g <HEXPLOTDIR>/geo/<GEOFILE> \
                -i <INPUTFILE> \
                --noinfo \
                -o <OUTPUTFILE> \
                --if <FORMAT> \
                --CV -p GEO  --colorpalette <COLORPALETTE>\
                --vn 'Capacitance:<DEF>:<UNIT>' --select <SELECTORVAL>\
                -z <ZMIN>:<ZMAX>".replace("<HEXPLOTDIR>", os.environ["HEXPLOT_DIR"]).replace("<GEOFILE>", "hex_positions_HPK_198ch_8inch_edge_ring_testcap.txt")

# get geometry mapping
geofile = "<HEXPLOTDIR>/geo/<GEOFILE>".replace("<HEXPLOTDIR>", os.environ["HEXPLOT_DIR"]).replace("<GEOFILE>", "hex_positions_HPK_198ch_8inch_edge_ring_testcap.txt")
geomap = pd.DataFrame(np.genfromtxt(geofile, usecols=(0, 1, 2), dtype=[("padnr", int), ("x", float), ("y", float)]))
temperatures = []
dummy = np.zeros(len(geomap))
for _index in range(len(geomap)):
    _x = geomap.iloc[_index].x
    _y = geomap.iloc[_index].y
    temperatures.append(twoD_Gaussian((_x, _y))[0])

geomap = geomap.assign(deltaT = np.array(temperatures))
geomap = geomap.assign(dummy = dummy)

geomap = geomap[geomap.padnr<199]





ratio_vis_path = os.path.join(thisdir, CAMPAIGN+"_deltaT.pdf")
tmp_file_path = ratio_vis_path.replace(".pdf", ".txt")
geomap.to_csv(tmp_file_path, sep=" ", header=None)

this_cmd = HEXPLOTCOMMAND
this_cmd = this_cmd.replace("<INPUTFILE>", tmp_file_path)
this_cmd = this_cmd.replace("<OUTPUTFILE>", ratio_vis_path)
this_cmd = this_cmd.replace("<COLORPALETTE>", "104")
this_cmd = this_cmd.replace("<UNIT>", "^{#circ}C")
this_cmd = this_cmd.replace("<FORMAT>", "null:PADNUM:null:null:VAL:SELECTOR")
this_cmd = this_cmd.replace("<DEF>", "#DeltaT (T_{ref}=-40^{#circ}C)")
this_cmd = this_cmd.replace("<ZMIN>", "-0.5")
this_cmd = this_cmd.replace("<ZMAX>", "0.5")
this_cmd = this_cmd.replace("<SELECTORVAL>", str(0))

env = {}
env.update(os.environ)
p = Popen(this_cmd, stdout=sys.stdout,
            stderr=sys.stderr, shell=True, env=env)
out, err = p.communicate()
code = p.returncode
if code != 0:
    raise Exception("Hexplot plotting failed")
#os.remove(tmp_file_path)
