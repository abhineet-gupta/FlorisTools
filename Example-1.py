import os
import numpy as np
import json
from pyFAST.fastfarm.TurbSimCaseCreation import TSCaseCreation


inputfile = os.path.join('InputFiles','input_KingPlains.json')
ThisDir=os.path.dirname(__file__)

# --- Define parameters necessary for this script
OldTSFile = os.path.join(ThisDir, 'SampleFiles/template_Low_InflowXX_SeedY.inp'     )   # Template file used for TurbSim, need to exist
NewTSFile = os.path.join(ThisDir, 'SampleFiles/High1.inp')   # New file that will be written

with open(inputfile) as f:
    inputdata = json.load(f)

D = inputdata['turbine']['properties']['rotor_diameter']                                      # Turbine diameter (m)
HubHt = inputdata['turbine']['properties']['hub_height']                                              # Hub Height (m)
Vhub  = 6                                                   # mean wind speed at hub height (m/s)
TI    = 10                                                  # turbulence intensity at hub height
PLExp = 0.2                                                 # power law exponent for shear (-)
xlocs = np.array(inputdata['farm']['properties']['layout_x'])  # x positions of turbines
ylocs = np.array(inputdata['farm']['properties']['layout_y'])  # y postitions of turbines

ind_12 = np.array([65,66,67,53,54,55,46,47,48,39,40,41])
xlocs = xlocs[ind_12]
ylocs = ylocs[ind_12]

Case = TSCaseCreation(D, HubHt, Vhub, TI, PLExp, x=xlocs, y=ylocs, boxType='highres',ds_low=25)
# # # Rewrite TurbSim Input File
Case.writeTSFile(OldTSFile, NewTSFile, tmax=700, turb=1)
run_turbsim_cmd = '/Users/agupta/Projects/Tools/AG_openfast/build_v3p5p1_double/modules/turbsim/turbsim ' + NewTSFile
os.system(run_turbsim_cmd)


