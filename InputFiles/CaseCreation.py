import os
import numpy as np
import matplotlib.pyplot as plt
import json
from pyFAST.fastfarm.TurbSimCaseCreation import TSCaseCreation
from pyFAST.fastfarm.FASTFarmCaseCreation import FFCaseCreation

inputfile = os.path.join('InputFiles','input_KingPlains.json')
ThisDir=os.path.dirname(__file__)

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
plt.plot(xlocs,ylocs,'*')

""" 
Setup a FAST.Farm suite of cases based on input parameters.

The extent of the high res and low res domain are setup according to the guidelines:
    https://openfast.readthedocs.io/en/dev/source/user/fast.farm/ModelGuidance.html

NOTE: If driving FAST.Farm using TurbSim inflow, the resulting boxes are necessary to
      build the final FAST.Farm case and are not provided as part of this repository. 
      If driving FAST.Farm using LES inflow, the VTK boxes are not necessary to exist.

"""


# -----------------------------------------------------------------------------
# USER INPUT: Modify these
#             For the d{t,s}_{high,low}_les paramters, use AMRWindSimulation.py
# -----------------------------------------------------------------------------

# ----------- Case absolute path
path = './Test'

# ----------- General hard-coded parameters
cmax     = 5      # maximum blade chord (m)
fmax     = 10/6   # maximum excitation frequency (Hz)
Cmeander = 1.9    # Meandering constant (-)

# ----------- Wind farm
# D = 240
zhub = HubHt
wts = {}
for i in np.arange(len(xlocs)):
    wts[i] = {'x':xlocs[i],'y':ylocs[i],'z':0.0,'D':D, 'zhub':zhub,'cmax':cmax,'fmax':fmax,'Cmeander':Cmeander}

# wts  = {
#             0 :{'x':0.0,     'y':0,       'z':0.0,  'D':D,  'zhub':zhub,  'cmax':cmax,  'fmax':fmax,  'Cmeander':Cmeander},
#             1 :{'x':1852.0,  'y':0,       'z':0.0,  'D':D,  'zhub':zhub,  'cmax':cmax,  'fmax':fmax,  'Cmeander':Cmeander},
#             2 :{'x':3704.0,  'y':0,       'z':0.0,  'D':D,  'zhub':zhub,  'cmax':cmax,  'fmax':fmax,  'Cmeander':Cmeander},
#             3 :{'x':5556.0,  'y':0,       'z':0.0,  'D':D,  'zhub':zhub,  'cmax':cmax,  'fmax':fmax,  'Cmeander':Cmeander},
#             4 :{'x':7408.0,  'y':0,       'z':0.0,  'D':D,  'zhub':zhub,  'cmax':cmax,  'fmax':fmax,  'Cmeander':Cmeander},
#             5 :{'x':1852.0,  'y':1852.0,  'z':0.0,  'D':D,  'zhub':zhub,  'cmax':cmax,  'fmax':fmax,  'Cmeander':Cmeander},
#             6 :{'x':3704.0,  'y':1852.0,  'z':0.0,  'D':D,  'zhub':zhub,  'cmax':cmax,  'fmax':fmax,  'Cmeander':Cmeander},
#             7 :{'x':5556.0,  'y':1852.0,  'z':0.0,  'D':D,  'zhub':zhub,  'cmax':cmax,  'fmax':fmax,  'Cmeander':Cmeander},
#             8 :{'x':7408.0,  'y':1852.0,  'z':0.0,  'D':D,  'zhub':zhub,  'cmax':cmax,  'fmax':fmax,  'Cmeander':Cmeander},
#             9 :{'x':3704.0,  'y':3704.0,  'z':0.0,  'D':D,  'zhub':zhub,  'cmax':cmax,  'fmax':fmax,  'Cmeander':Cmeander},
#             10:{'x':5556.0,  'y':3704.0,  'z':0.0,  'D':D,  'zhub':zhub,  'cmax':cmax,  'fmax':fmax,  'Cmeander':Cmeander},
#             11:{'x':7408.0,  'y':3704.0,  'z':0.0,  'D':D,  'zhub':zhub,  'cmax':cmax,  'fmax':fmax,  'Cmeander':Cmeander},
#         }
refTurb_rot = 0

# ----------- Additional variables
tmax = 10     # Total simulation time
nSeeds = 1      # Number of different seeds
zbot = 1        # Bottom of your domain
mod_wake = 1    # Wake model. 1: Polar, 2: Curl, 3: Cartesian

# ----------- Desired sweeps
vhub       = [10]
shear      = [0.2]
TIvalue    = [10]
inflow_deg = [0]

# ----------- Turbine parameters
# Set the yaw of each turbine for wind dir. One row for each wind direction.
yaw_init = np.array([[0,0,0,0,0,0,0,0,0,0,0,0]])
print(yaw_init)
# yaw_init = np.transpose(yaw_init)
print(yaw_init)
# ----------- Low- and high-res boxes parameters
# Should match LES if comparisons are to be made; otherwise, set desired values
# For an automatic computation of such parameters, omit them from the call to FFCaseCreation
# High-res boxes settings
dt_high_les = 0.05                # sampling frequency of high-res files
ds_high_les = 2.0               # dx, dy, dz that you want these high-res files at
extent_high = 1.2               # high-res box extent in y and x for each turbine, in D.
# Low-res boxes settings
dt_low_les  = 3                  # sampling frequency of low-res files
ds_low_les  = 5.0               # dx, dy, dz of low-res files
# extent_low  = [3, 80, 3, 80, 20]   # extent in xmin, xmax, ymin, ymax, zmax, in D
extent_low = None


# ----------- Execution parameters
ffbin = '/Users/agupta/Projects/Tools/AG_openfast/build_v3p5p0/glue-codes/fast-farm/FAST.Farm'

# ----------- LES parameters. This variable will dictate whether it is a TurbSim-driven or LES-driven case
# LESpath = '/full/path/to/the/LES/case'
LESpath = None # set as None if TurbSim-driven is desired


# -----------------------------------------------------------------------------
# ----------- Template files
templatePath            = 'OF_Template'

# Put 'unused' to any input that is not applicable to your case
# Files should be in templatePath
EDfilename              = 'NREL-2p8-127_ElastoDyn.T'
SEDfilename             = 'unused'
HDfilename              = 'unused'
SrvDfilename            = 'NREL-2p8-127_ServoDyn.T'
ADfilename              = 'NREL-2p8-127_AeroDyn15.dat'
ADskfilename            = 'unused'
SubDfilename            = 'unused'
IWfilename              = 'NREL-2p8-127_InflowFile.dat'
BDfilepath              = 'unused'
bladefilename           = 'NREL-2p8-127_ElastoDyn_blade.dat'
towerfilename           = 'NREL-2p8-127_ElastoDyn_tower.dat'
turbfilename            = 'NREL-2p8-127.T'
libdisconfilepath       = '/Users/agupta/Projects/Tools/FlorisTools/OF_Template/libdiscon.so'
controllerInputfilename = 'NREL-2p8-127_DISCON.IN'
coeffTablefilename      = 'unused'
FFfilename              = 'TestCase.fstf'

# TurbSim setups
turbsimLowfilepath      = './SampleFiles/template_Low_InflowXX_SeedY.inp'
turbsimHighfilepath     = './SampleFiles/template_HighT1_InflowXX_SeedY.inp'

# SLURM scripts
slurm_TS_high           = './SampleFiles/runAllHighBox.sh'
slurm_TS_low            = './SampleFiles/runAllLowBox.sh'
slurm_FF_single         = './SampleFiles/runFASTFarm_cond0_case0_seed0.sh'


# -----------------------------------------------------------------------------
# END OF USER INPUT
# -----------------------------------------------------------------------------


# Initial setup
case = FFCaseCreation(path, wts, tmax, zbot, vhub, shear, TIvalue, inflow_deg,
                        dt_high_les, ds_high_les, extent_high,
                        dt_low_les, ds_low_les, extent_low,
                        ffbin, mod_wake, yaw_init,
                        nSeeds=nSeeds, LESpath=LESpath,
                        verbose=1)

case.setTemplateFilename(templatePath, EDfilename, SEDfilename, HDfilename, SrvDfilename, ADfilename,
                            ADskfilename, SubDfilename, IWfilename, BDfilepath, bladefilename, towerfilename,
                            turbfilename, libdisconfilepath, controllerInputfilename, coeffTablefilename,
                            turbsimLowfilepath, turbsimHighfilepath, FFfilename)

# Get domain paramters
case.getDomainParameters()

# Organize file structure
case.copyTurbineFilesForEachCase()

# TurbSim setup
turbsimexe = '/Users/agupta/Projects/Tools/AG_openfast/build_v3p5p0/modules/turbsim/turbsim'
if LESpath is None:
    case.TS_low_setup()
    case.TS_low_slurm_prepare(slurm_TS_low)
    for cond in range(case.nConditions):
            for seed in range(case.nSeeds):
                seedPath = os.path.join(case.path, case.condDirList[cond], f'Seed_{seed}')
                currentTSLowFile = os.path.join(seedPath, 'Low.inp')
                # os.system(turbsimexe + ' ' + currentTSLowFile)

    case.TS_high_setup()
    case.TS_high_slurm_prepare(slurm_TS_high)
    #case.TS_high_slurm_submit()
    for cond in range(case.nConditions):
        for casei in range(case.nHighBoxCases):
            # Get actual case number given the high-box that need to be saved
            casei = case.allHighBoxCases.isel(case=casei)['case'].values
            for seed in range(case.nSeeds):
                seedPath = os.path.join(case.path, case.condDirList[cond], case.caseDirList[casei], f'Seed_{seed}', 'TurbSim')
                for t in range(case.nTurbines):
                    # os.system(turbsimexe + ' ' + os.path.join(seedPath, f'HighT{t+1}.inp'))
                    pass

# Final setup
case.FF_setup()
case.FF_slurm_prepare(slurm_FF_single)
for cond in range(case.nConditions):
    for casei in range(case.nCases):
        for seed in range(case.nSeeds):
            seedPath = os.path.join(case.path,case.condDirList[cond],case.caseDirList[casei], f'Seed_{seed}')
            os.system(ffbin + ' ' + os.path.join(seedPath, 'FFarm_mod.fstf'))
#case.FF_slurm_submit()

