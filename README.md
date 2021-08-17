# Electrical characteristics of silicon pad sensor prototypes for the CMS endcap calorimeter upgrade

* [![build status](https://gitlab.cern.ch/CLICdp/HGCAL/hgcal_sensor_characterisation_publication2020/badges/master/pipeline.svg)](https://gitlab.cern.ch/CLICdp/HGCAL/hgcal_sensor_characterisation_publication2020/commits/master)
* [Latest pdf of the paper](https://gitlab.cern.ch/CLICdp/HGCAL/hgcal_sensor_characterisation_publication2020/builds/artifacts/master/raw/main.pdf?job=compile%20PDF)
* [Latest builds of the paper draft](https://gitlab.cern.ch/CLICdp/HGCAL/hgcal_sensor_characterisation_publication2020/pipelines) 

## Download & Compilation: 
```
git clone https://gitlab.cern.ch/CLICdp/HGCAL/hgcal_sensor_characterisation_publication2020.git
cd hgcal_sensor_characterisation_publication2020
. build.sh
```

## Contributing:
- push directly to the master branch if you are only editing the files corresponding to your chapter
- otherwise use merge requests

## Text:
- text files = one per subsection & section
- stored in ```\content```

## Figures and Plots:
- please use .pdf or .png files
- static figures are in ```/figures```
- result plots are to be stored in ```/plots```, important: please provide plotting script with the appropriate execution command in ```/plots/run.sh```
- ROOT-based style is defined in ```/plot/common/__init__.py```, style will be applied by the corresponding authors but please use ROOT (if possible)

## References:
- bib file defined in ```\bib\bib.bib```

## Setup:
- packages defined in ```\setup\packages.tex```
- commands defined in ```\setup\commands.tex```
 
