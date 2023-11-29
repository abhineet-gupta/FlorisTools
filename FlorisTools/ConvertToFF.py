# from floris.tools.floris_interface import FlorisInterface
import json
from pyFAST.fastfarm.TurbSimCaseCreation import TSCaseCreation



def read_input(file):
    with open(file) as f:
        inputdata = json.load(f)
    return inputdata

def generate_turbsim(inputdata)
    
    Case = TSCaseCreation(D, HubHt, Vhub, TI, PLExp, x=xlocs, y=ylocs, zbot=zbot, cmax=cmax, fmax=fmax, Cmeander=Cmeander)
    # Rewrite TurbSim Input File
    Case.writeTSFile(OldTSFile, NewTSFile, tmax=5, turb=1)