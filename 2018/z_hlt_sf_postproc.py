#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from zHLTSFModule import *

from PhysicsTools.NanoAODTools.postprocessing.modules.common.countHistogramsModule import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.PrefireCorr import *
from PhysicsTools.NanoAODTools.postprocessing.modules.common.puWeightProducer import *

from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

#p=PostProcessor(".",inputFiles(),None,"z_hlt_sf_keep_and_drop.txt",[countHistogramsModule(),zHLTSFModule()],provenance=True,justcount=False,fwkJobReport=True,jsonInput=runsAndLumis(),noOut=False,outputbranchsel="z_hlt_sf_output_branch_selection.txt")

p=PostProcessor(".",inputFiles(),None,"z_hlt_sf_keep_and_drop.txt",[countHistogramsModule(),zHLTSFModule(),puWeight_2018()],provenance=True,justcount=False,fwkJobReport=True,jsonInput=runsAndLumis(),noOut=False,outputbranchsel="z_hlt_sf_output_branch_selection.txt")

p.run()

#print "DONE"
#os.system("ls -lR")

