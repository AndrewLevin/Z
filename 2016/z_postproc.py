#!/usr/bin/env python
import os, sys
import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
from importlib import import_module
from PhysicsTools.NanoAODTools.postprocessing.framework.postprocessor import PostProcessor

from  zModule import *

from countHistogramsModule import *
#from countHistogramsPDFModule import *
#from countHistogramsQCDScaleModule import *
#from countHistogramsLHEAndGenSelectionsModule import *

from PhysicsTools.NanoAODTools.postprocessing.framework.crabhelper import inputFiles,runsAndLumis

#p=PostProcessor(".",["root://cms-xrd-global.cern.ch//store/mc/RunIISummer16NanoAOD/TTJets_TuneCUETP8M1_13TeV-madgraphMLM-pythia8/NANOAODSIM/PUMoriond17_05Feb2018_94X_mcRun2_asymptotic_v2-v1/40000/1EA786F7-D312-E811-9ED3-001E67460991.root"],"event == 2303072","keep_and_drop.txt",[countHistogramsModule(),exampleModule()],provenance=True,justcount=False,noOut=False,fwkJobReport=True, outputbranchsel = "output_branch_selection.txt")

p=PostProcessor(".",inputFiles(),None,"keep_and_drop.txt",[countHistogramsModule(),exampleModule()],provenance=True,justcount=False,fwkJobReport=True,jsonInput=runsAndLumis(),noOut=False,outputbranchsel = "output_branch_selection.txt")

#p=PostProcessor(".",["/eos/user/a/amlevin/data/nano/unmerged/zjets.100.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.102.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.103.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.104.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.105.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.106.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.107.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.108.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.109.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.10.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.110.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.111.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.112.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.113.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.114.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.115.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.116.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.117.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.118.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.119.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.11.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.120.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.121.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.122.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.123.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.124.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.125.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.126.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.127.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.128.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.129.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.12.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.130.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.131.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.132.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.133.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.134.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.135.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.136.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.137.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.138.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.139.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.13.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.140.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.141.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.142.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.143.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.144.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.145.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.146.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.147.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.148.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.149.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.14.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.150.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.151.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.152.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.154.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.155.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.156.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.157.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.158.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.159.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.160.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.161.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.162.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.163.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.164.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.165.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.166.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.167.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.168.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.169.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.16.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.170.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.171.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.172.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.173.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.174.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.175.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.176.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.177.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.178.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.179.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.17.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.180.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.181.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.182.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.183.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.184.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.185.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.186.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.187.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.188.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.189.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.18.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.190.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.191.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.192.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.193.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.194.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.195.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.196.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.197.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.198.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.199.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.19.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.1.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.200.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.201.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.202.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.203.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.204.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.205.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.206.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.207.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.208.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.209.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.20.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.210.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.211.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.212.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.213.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.214.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.215.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.216.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.217.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.218.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.219.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.21.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.220.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.221.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.222.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.223.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.224.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.225.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.226.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.227.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.228.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.229.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.22.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.230.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.231.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.232.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.233.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.234.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.235.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.236.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.237.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.238.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.239.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.23.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.240.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.241.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.242.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.243.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.244.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.245.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.246.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.247.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.248.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.249.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.24.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.250.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.251.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.252.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.253.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.254.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.255.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.256.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.257.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.258.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.259.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.25.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.260.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.261.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.262.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.263.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.264.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.265.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.266.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.267.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.268.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.269.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.270.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.271.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.272.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.273.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.274.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.275.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.276.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.277.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.278.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.279.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.27.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.280.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.281.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.282.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.283.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.284.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.285.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.286.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.287.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.288.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.289.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.28.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.290.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.291.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.292.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.293.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.294.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.295.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.296.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.297.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.298.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.299.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.29.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.2.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.300.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.301.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.302.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.303.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.304.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.305.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.306.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.307.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.308.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.309.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.30.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.310.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.311.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.312.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.313.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.314.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.315.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.316.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.317.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.318.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.319.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.31.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.320.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.321.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.322.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.323.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.324.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.325.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.326.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.327.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.328.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.329.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.32.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.330.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.331.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.332.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.333.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.334.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.335.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.336.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.337.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.338.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.339.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.33.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.340.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.341.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.342.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.343.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.344.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.345.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.346.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.347.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.348.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.349.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.34.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.350.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.351.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.352.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.353.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.355.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.356.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.357.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.358.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.359.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.35.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.360.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.361.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.362.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.363.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.364.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.365.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.366.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.367.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.368.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.369.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.36.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.370.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.371.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.372.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.373.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.374.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.375.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.376.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.377.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.378.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.379.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.37.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.380.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.381.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.382.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.383.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.384.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.385.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.386.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.387.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.388.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.389.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.38.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.390.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.391.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.392.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.393.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.394.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.395.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.396.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.397.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.398.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.399.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.39.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.3.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.400.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.401.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.402.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.403.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.404.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.405.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.406.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.407.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.408.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.409.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.40.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.410.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.411.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.412.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.413.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.414.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.415.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.416.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.417.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.418.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.419.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.41.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.420.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.421.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.422.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.423.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.424.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.425.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.426.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.427.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.428.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.429.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.42.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.430.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.431.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.433.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.434.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.436.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.437.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.438.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.439.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.43.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.440.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.441.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.442.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.443.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.444.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.445.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.446.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.447.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.448.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.449.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.44.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.450.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.451.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.452.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.453.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.455.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.456.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.457.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.458.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.459.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.45.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.460.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.461.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.462.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.463.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.464.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.465.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.466.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.467.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.469.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.46.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.470.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.471.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.472.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.473.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.474.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.475.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.476.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.477.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.47.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.48.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.49.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.4.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.50.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.51.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.52.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.53.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.54.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.55.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.56.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.57.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.58.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.59.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.5.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.60.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.61.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.62.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.63.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.64.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.65.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.66.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.67.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.68.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.69.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.6.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.70.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.71.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.72.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.73.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.74.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.75.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.76.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.77.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.78.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.79.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.7.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.80.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.81.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.82.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.83.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.84.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.85.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.86.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.87.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.88.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.89.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.8.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.90.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.91.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.92.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.93.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.94.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.95.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.96.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.97.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.98.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.99.root","/eos/user/a/amlevin/data/nano/unmerged/zjets.9.root"],None,"keep_and_drop.txt",[countHistogramsModule(),exampleModule()],provenance=True,justcount=False,noOut=False,fwkJobReport=True, outputbranchsel = "output_branch_selection.txt")

p.run()

#print "DONE"
#os.system("ls -lR")
