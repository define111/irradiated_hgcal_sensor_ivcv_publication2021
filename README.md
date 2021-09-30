# Electrical characteristics of silicon pad sensor prototypes for the CMS endcap calorimeter upgrade

* [![build status](https://gitlab.cern.ch/CLICdp/HGCAL/irradiated_hgcal_sensor_ivcv_publication2021/badges/master/pipeline.svg)](https://gitlab.cern.ch/CLICdp/HGCAL/irradiated_hgcal_sensor_ivcv_publication2021/commits/master)
* [Latest builds of the paper draft](https://gitlab.cern.ch/CLICdp/HGCAL/irradiated_hgcal_sensor_ivcv_publication2021/pipelines) 

## Download & Compilation: 
```
git clone https://gitlab.cern.ch/CLICdp/HGCAL/irradiated_hgcal_sensor_ivcv_publication2021.git
cd irradiated_hgcal_sensor_ivcv_publication2021
. build.sh
```

## Contributing:
- please open, use and push your own branch for the chapter that you are authoring
- instructions on creating and pushing new branches: [here](https://forum.freecodecamp.org/t/push-a-new-local-branch-to-a-remote-git-repository-and-track-it-too/13222)
- once in a reviewable state, please submit a [merge request](https://docs.gitlab.com/ee/user/project/merge_requests/getting_started.html) to the master branch to have your contributions merged with the others

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
 
