pu1data_driven = True

def fillHistogram(hist,value,weight=1):
    if options.overflow:
        if value > hist.GetBinLowEdge(hist.GetNbinsX()):
            value = hist.GetBinCenter(hist.GetNbinsX())
    hist.Fill(value,weight)

import ctypes

import json

import sys
import style

import optparse

from math import hypot, pi, sqrt, cos, sin, atan2

from pprint import pprint

def deltaPhi(phi1,phi2):
    ## Catch if being called with two objects                                                                                                                        
    if type(phi1) != float and type(phi1) != int:
        phi1 = phi1.phi
    if type(phi2) != float and type(phi2) != int:
        phi2 = phi2.phi
    ## Otherwise                                                                                                                                                     
    dphi = (phi1-phi2)
    while dphi >  pi: dphi -= 2*pi
    while dphi < -pi: dphi += 2*pi
    return dphi

def deltaR(eta1,phi1,eta2=None,phi2=None):
    ## catch if called with objects                                                                                                                                  
    if eta2 == None:
        return deltaR(eta1.eta,eta1.phi,phi1.eta,phi1.phi)
    ## otherwise                                                                                                                                                     
    return hypot(eta1-eta2, deltaPhi(phi1,phi2))


parser = optparse.OptionParser()


parser.add_option('--lep',dest='lep',default='both')
parser.add_option('--normalize_mll',dest='normalize_mll',action='store_true',default=False)
parser.add_option('--make_recoil_trees',dest='make_recoil_trees',action='store_true',default=False)
parser.add_option('--apply_recoil_corr',dest='apply_recoil_corr',action='store_true',default=False)
parser.add_option('--make_plots',dest='make_plots',action='store_true',default=False)
parser.add_option('--overflow',dest='overflow',action='store_true',default=False)

parser.add_option('--lumi',dest='lumi')
parser.add_option('--variable',dest='variable')

parser.add_option('-i',dest='inputfile')
parser.add_option('-o',dest='outputdir',default="/eos/user/a/amlevin/www/tmp/")

(options,args) = parser.parse_args()

if options.lep == "muon":
    lepton_name = "muon"
elif options.lep == "electron":
    lepton_name = "electron"
elif options.lep == "both":
    lepton_name = "both"
else:
    assert(0)

import eff_scale_factor

import ROOT

from array import array

if options.make_recoil_trees:

    recoil_outfile = ROOT.TFile("recoil.root",'recreate')

    data_recoil_tree = ROOT.TTree("data_recoil_tree","data recoil tree")

    data_u1= array( 'f', [ 0 ] )
    data_recoil_tree.Branch( 'u1', data_u1, 'u1/F')

    data_u2= array( 'f', [ 0 ] )
    data_recoil_tree.Branch( 'u2', data_u2, 'u2/F')

    data_zpt= array( 'f', [ 0 ] )
    data_recoil_tree.Branch( 'zpt', data_zpt, 'zpt/F')

    data_weight= array( 'f', [ 0 ] )  #will always be 1
    data_recoil_tree.Branch( 'weight', data_weight, 'weight/F')

    mc_recoil_tree = ROOT.TTree("mc_recoil_tree","mc recoil tree")

    mc_u1= array( 'f', [ 0 ] )
    mc_recoil_tree.Branch( 'u1', mc_u1, 'u1/F')

    mc_u2= array( 'f', [ 0 ] )
    mc_recoil_tree.Branch( 'u2', mc_u2, 'u2/F')

    mc_zpt= array( 'f', [ 0 ] )
    mc_recoil_tree.Branch( 'zpt', mc_zpt, 'zpt/F')

    mc_weight= array( 'f', [ 0 ] )
    mc_recoil_tree.Branch( 'weight', mc_weight, 'weight/F')

met_weight_list  = [0,1.04438,1.03441,1.01202,0.97558,0.934234,0.889209,0.859616,0.838646,0.795616,0.838776,0.79236,0.937482,1.38006,1.73772,3.40153,6.16593,20.019,4.56341,4.30805,15.3002,0,33.3087,0,1.49879,0,0,0.688555,0,0,0,0]

recoil_weight_list = [0,1.05308,1.03883,1.01358,0.981316,0.952414,0.929029,0.917159,0.908528,0.90361,0.883288,0.918111,0.944326,0.943427,0.956951,0.905486,0.824449,1.718,1.69566,2.8904,0.123703,0.37997]

zpt_weight_list = [0,1.02548,0.964365,0.975732,0.989607,1.01585,1.08599,1.17429,1.254,1.38018,1.48303,1.49296,1.92722,1.96488,2.64043,3.13321,2.54325,2.40273,4.45963,3.96664,0,7.50793]

recoil_zpt_weight_list = [0,1.05216,1.03766,1.01483,0.984147,0.956141,0.92989,0.911838,0.892875,0.872895,0.835284,0.842361,0.840118,0.806624,0.753405,0.719853,0.583694,1.18084,0.79967,1.09567,0.10118,0.0992985]

zpt_weight_hist = ROOT.TH1F("zpt weight hist", "", 20, 0., 200 )
met_weight_hist = ROOT.TH1F("met weight hist", "", 30 , 0., 300 )
recoil_weight_hist = ROOT.TH1F("recoil weight hist", "", 20 , 0., 200 )
recoil_zpt_weight_hist = ROOT.TH1F("recoil post zpt weight hist", "", 20 , 0., 200 )

for i in range(met_weight_hist.GetNbinsX()+2):
    met_weight_hist.SetBinContent(i,met_weight_list[i])

for i in range(recoil_weight_hist.GetNbinsX()+2):
    recoil_weight_hist.SetBinContent(i,recoil_weight_list[i])

for i in range(zpt_weight_hist.GetNbinsX()+2):
    zpt_weight_hist.SetBinContent(i,zpt_weight_list[i])

for i in range(recoil_zpt_weight_hist.GetNbinsX()+2):
    recoil_zpt_weight_hist.SetBinContent(i,recoil_zpt_weight_list[i])

met_weight_hist.Print("all")
recoil_weight_hist.Print("all")
recoil_zpt_weight_hist.Print("all")
zpt_weight_hist.Print("all")

f_pu_weights = ROOT.TFile("/afs/cern.ch/user/a/amlevin/PileupWeights2016.root")

pu_weight_hist = f_pu_weights.Get("ratio")

from z_labels import labels

mll_index = 4

#variables = []
#variables_labels = []

if options.make_plots:    
    variables = ["dphill","met","lepton1_pt","lepton1_eta","mll","lepton1_phi","mt","mt1","mt2","npvs","njets40","metmrawmet","rawmet","recoil","z_pt","corrmet","recoil1","recoil2","corrrecoil1","corrrecoil2"]
    variables_labels = ["dphill","met","lepton1_pt","lepton1_eta","mll","lepton1_phi","mt","mt1","mt2","npvs","njets40","metmrawmet","rawmet","recoil","z_pt","corrmet","recoil1","recoil2","corrrecoil1","corrrecoil2"]
else:
    variables = []
    variables_labels = []

assert(len(variables) == len(variables_labels))

from array import array


if options.make_plots: 
    histogram_templates = [ROOT.TH1D('dphill','',16,0,pi),ROOT.TH1F("met", "", 40 , 0., 200 ), ROOT.TH1F('lepton_pt', '', 8, 20., 180 ), ROOT.TH1F('lepton_eta', '', 10, -2.5, 2.5 ), ROOT.TH1F("mll","",60,60,120),ROOT.TH1F("lepton_phi","",14,-3.5,3.5),ROOT.TH1F("mt","",20,0,200),ROOT.TH1F("mt1","",20,0,200),ROOT.TH1F("mt2","",20,0,200),ROOT.TH1F("npvs","",51,-0.5,50.5),ROOT.TH1D("njets40","",7,-0.5,6.5),ROOT.TH1F("metmrawmet", "", 20 , -50., 50 ),ROOT.TH1F("rawmet", "", 30 , 0.,  300 ),ROOT.TH1F("recoil","",20,0,200),ROOT.TH1F('z_pt', '', 20, 0., 200 ),ROOT.TH1F("corrmet", "", 40 , 0., 200 ),ROOT.TH1F("recoil1","",20,-100,100),ROOT.TH1F("recoil2","",20,-100,100),ROOT.TH1F("corrrecoil1","",20,-100,100),ROOT.TH1F("corrrecoil2","",20,0-100,100)] 
else:
    histogram_templates = []

#histogram_templates = []

assert(len(variables) == len(histogram_templates))

def getVariable(varname, tree, corrmet = None, corrmetphi = None):
    if varname == "mll":
        return tree.mll
    elif varname == "dphill":
        return abs(deltaPhi(tree.lepton1_phi,tree.lepton2_phi))
    elif varname == "njets40":
        return float(tree.njets40)
    elif varname == "mt":
        return tree.mt
    elif varname == "z_pt":
        return sqrt(pow(tree.lepton1_pt*cos(tree.lepton1_phi) + tree.lepton2_pt*cos(tree.lepton2_phi),2)+pow(tree.lepton1_pt*sin(tree.lepton1_phi) + tree.lepton2_pt*sin(tree.lepton2_phi),2))
    elif varname == "z_phi":
        return atan2(tree.lepton1_pt*sin(tree.lepton1_phi) + tree.lepton2_pt*sin(tree.lepton2_phi),tree.lepton1_pt*cos(tree.lepton1_phi) + tree.lepton2_pt*cos(tree.lepton2_phi))
    elif varname == "recoil":
        return sqrt(pow(tree.met*cos(tree.metphi) + tree.lepton1_pt*cos(tree.lepton1_phi) + tree.lepton2_pt*cos(tree.lepton2_phi),2)+pow(tree.met*sin(tree.metphi) + tree.lepton1_pt*sin(tree.lepton1_phi) + tree.lepton2_pt*sin(tree.lepton2_phi),2))
    elif varname == "corrrecoil":
        return sqrt(pow(corrmet*cos(corrmetphi) + tree.lepton1_pt*cos(tree.lepton1_phi) + tree.lepton2_pt*cos(tree.lepton2_phi),2)+pow(corrmet*sin(corrmetphi) + tree.lepton1_pt*sin(tree.lepton1_phi) + tree.lepton2_pt*sin(tree.lepton2_phi),2))
    elif varname == "recoil1":
        z_phi = atan2(tree.lepton1_pt*sin(tree.lepton1_phi) + tree.lepton2_pt*sin(tree.lepton2_phi),tree.lepton1_pt*cos(tree.lepton1_phi) + tree.lepton2_pt*cos(tree.lepton2_phi))
        return cos(z_phi)*(-tree.met*cos(tree.metphi) - tree.lepton1_pt*cos(tree.lepton1_phi) - tree.lepton2_pt*cos(tree.lepton2_phi)) + sin(z_phi)*(-tree.met*sin(tree.metphi) - tree.lepton1_pt*sin(tree.lepton1_phi) - tree.lepton2_pt*sin(tree.lepton2_phi))
    elif varname == "recoil2":
        z_phi = atan2(tree.lepton1_pt*sin(tree.lepton1_phi) + tree.lepton2_pt*sin(tree.lepton2_phi),tree.lepton1_pt*cos(tree.lepton1_phi) + tree.lepton2_pt*cos(tree.lepton2_phi))
        return -sin(z_phi)*(-tree.met*cos(tree.metphi) - tree.lepton1_pt*cos(tree.lepton1_phi) - tree.lepton2_pt*cos(tree.lepton2_phi)) + cos(z_phi)*(-tree.met*sin(tree.metphi) - tree.lepton1_pt*sin(tree.lepton1_phi) - tree.lepton2_pt*sin(tree.lepton2_phi))
    elif varname == "corrrecoil1":
        z_phi = atan2(tree.lepton1_pt*sin(tree.lepton1_phi) + tree.lepton2_pt*sin(tree.lepton2_phi),tree.lepton1_pt*cos(tree.lepton1_phi) + tree.lepton2_pt*cos(tree.lepton2_phi))
        return cos(z_phi)*(-corrmet*cos(corrmetphi) - tree.lepton1_pt*cos(tree.lepton1_phi) - tree.lepton2_pt*cos(tree.lepton2_phi)) + sin(z_phi)*(-corrmet*sin(corrmetphi) - tree.lepton1_pt*sin(tree.lepton1_phi) - tree.lepton2_pt*sin(tree.lepton2_phi))
    elif varname == "corrrecoil2":
        z_phi = atan2(tree.lepton1_pt*sin(tree.lepton1_phi) + tree.lepton2_pt*sin(tree.lepton2_phi),tree.lepton1_pt*cos(tree.lepton1_phi) + tree.lepton2_pt*cos(tree.lepton2_phi))
        return -sin(z_phi)*(-corrmet*cos(corrmetphi) - tree.lepton1_pt*cos(tree.lepton1_phi) - tree.lepton2_pt*cos(tree.lepton2_phi)) + cos(z_phi)*(-corrmet*sin(corrmetphi) - tree.lepton1_pt*sin(tree.lepton1_phi) - tree.lepton2_pt*sin(tree.lepton2_phi))
    elif varname == "recoil_x":
        return -tree.met*cos(tree.metphi) - tree.lepton1_pt*cos(tree.lepton1_phi) - tree.lepton2_pt*cos(tree.lepton2_phi)
    elif varname == "recoil_y":
        return -tree.met*sin(tree.metphi) - tree.lepton1_pt*sin(tree.lepton1_phi) - tree.lepton2_pt*sin(tree.lepton2_phi)
    elif varname == "mt1":
        return tree.mt1
    elif varname == "mt2":
        return tree.mt2
    elif varname == "npvs":
        return float(tree.npvs)
    elif varname == "met":
        if tree.met > 200:
            return 199.99
        else:
            return tree.met
    elif varname == "corrmet":
        if corrmet > 200:
            return 199.99
        else:
            return corrmet
    elif varname == "rawmet":
        return tree.rawmet
    elif varname == "metmrawmet":
        return tree.met-tree.rawmet
    elif varname == "lepton1_pt":
        return tree.lepton1_pt
    elif varname == "lepton2_pt":
        return tree.lepton2_pt
    elif varname == "lepton1_eta":
        return tree.lepton1_eta
    elif varname == "lepton2_eta":
        return tree.lepton2_eat
    elif varname == "lepton1_phi":
        return tree.lepton1_phi
    elif varname == "lepton2_phi":
        return tree.lepton2_phi
    else:
        assert(0)

def getXaxisLabel(varname):
    if varname == "npvs":
        return "number of PVs"
    elif varname == "njets40":
        return "number of jets with pt > 40 GeV"
    elif varname == "recoil":
        return "recoil"
    elif varname == "recoil1":
        return "recoil1"
    elif varname == "recoil2":
        return "recoil2"
    elif varname == "corrrecoil1":
        return "corrected recoil1"
    elif varname == "corrrecoil2":
        return "corrected recoil2"
    elif varname == "z_pt":
        return "Z p_{t} (GeV)"
    elif varname == "mt":
        return "m_{t} (GeV)"
    elif varname == "mt1":
        return "m_{t1} (GeV)"
    elif varname == "mt2":
        return "m_{t2} (GeV)"
    elif varname == "mll":
        return "m_{ll} (GeV)"
    elif varname == "met":
        return "MET (GeV)"
    elif varname == "corrmet":
        return "corrected MET (GeV)"
    elif varname == "rawmet":
        return "Raw MET (GeV)"
    elif varname == "metmrawmet":
        return "MET - Raw MET(GeV)"
    elif varname == "lepton1_pt":
        return "lepton 1 p_{T} (GeV)"
    elif varname == "lepton1_eta":
        return "lepton 1 #eta"
    elif varname == "lepton1_phi":
        return "lepton 1 #phi"
    elif varname == "lepton2_pt":
        return "lepton 2 p_{T} (GeV)"
    elif varname == "lepton2_eta":
        return "lepton 2 #eta"
    elif varname == "lepton2_phi":
        return "lepton 2 #phi"
    elif varname == "dphill":
         return "#Delta#phi(l,l)"
    else:
        assert(0)

def pass_selection(tree):

    if tree.lepton1_pt > 20:
        pass_lepton_pt = True
    else:
        pass_lepton_pt = False

    if tree.is_lepton1_tight == '\x01':
        pass_lepton_selection = True
    else:
        pass_lepton_selection = False    

    if lepton_name == "electron":
        if abs(tree.lepton1_pdgid) == 11:
            pass_lepton_flavor = True
        else:
            pass_lepton_flavor = False
    elif lepton_name == "muon":
        if abs(tree.lepton1_pdgid) == 13:
            pass_lepton_flavor = True
        else:
            pass_lepton_flavor = False
    elif lepton_name == "both":
        assert(abs(tree.lepton1_pdgid) == 11 or abs(tree.lepton1_pdgid) == 13)
        pass_lepton_flavor = True
    else:
        assert(0)

    if lepton_name == "electron":    
        if True:
            pass_mll = True
        else:
            pass_mll = False
    elif lepton_name == "muon":        
        if True:
            pass_mll = True
        else:
            pass_mll = False
    elif lepton_name == "both":
        if True:
            pass_mll = True
        else:
            pass_mll = False
    else:
        assert(0)

#    if tree.mll > 80:
#        pass_mll = False
#    else:
#        pass_mll = True

#    if tree.met > 35:
    if tree.met > 0:
#    if tree.met > 0:
        pass_met = True
    else:
        pass_met = False

    if tree.puppimt > 0:
#    if tree.mt > 0:
        pass_mt = True
    else:
        pass_mt = False


#    if pass_lepton_pt and pass_lepton_selection and  pass_mll and pass_lepton_flavor and (pass_met and pass_mt) and tree.njets15 == 1 and tree.njets20 == 0 and abs((tree.met-tree.rawmet)/tree.rawmet) > 0.001:
    if pass_lepton_pt and pass_lepton_selection and  pass_mll and pass_lepton_flavor and (pass_met and pass_mt) and tree.njets40 == 0:
        return True
    else:
        return False

#def fillHistograms(tree,hists):

xoffsetstart = 0.0;
yoffsetstart = 0.0;
xoffset = 0.20;
yoffset = 0.05;

xpositions = [0.68,0.68,0.68,0.68,0.445,0.445,0.445,0.445,0.21,0.21,0.21,0.21]
ypositions = [0,1,2,3,0,1,2,3,0,1,2,3]

#xpositions = [0.68,0.68,0.68,0.68,0.68,0.68,0.68,0.445,0.445,0.445,0.445,0.445,0.445,0.445,0.21,0.21,0.21,0.21,0.21,0.21,0.21]
#ypositions = [0,1,2,3,4,5,6,0,1,2,3,4,5,6,0,1,2,3,4,5,6]

style.GoodStyle().cd()

def set_axis_fonts(thstack, coordinate, title):

    if coordinate == "x":
        axis = thstack.GetXaxis();
    elif coordinate == "y":
        axis = thstack.GetYaxis();
    else:
        assert(0)
    
    axis.SetLabelFont  (   42)
    axis.SetLabelOffset(0.015)
    axis.SetLabelSize  (0.050)
    axis.SetNdivisions (  505)
    axis.SetTitleFont  (   42)
    axis.SetTitleOffset(  1.5)
    axis.SetTitleSize  (0.050)
    if (coordinate == "y"):
        axis.SetTitleOffset(1.6)
    axis.SetTitle(title)    

def draw_legend(x1,y1,hist,label,options):

    legend = ROOT.TLegend(x1+xoffsetstart,y1+yoffsetstart,x1+xoffsetstart + xoffset,y1+yoffsetstart + yoffset)

    legend.SetBorderSize(     0)
    legend.SetFillColor (     0)
    legend.SetTextAlign (    12)
    legend.SetTextFont  (    42)
    legend.SetTextSize  ( 0.040)

    legend.AddEntry(hist,label,options)

    legend.Draw("same")

    #otherwise the legend goes out of scope and is deleted once the function finishes
    hist.label = legend

if lepton_name == "muon":
#    data_file = ROOT.TFile.Open("/afs/cern.ch/project/afs/var/ABS/recover/R.1935065321.08020759/data/wg/single_muon.root")
#    data_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/z/2016/double_muon.root")
    data_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/z/2016/1June2019/double_muon.root")
elif lepton_name == "electron":
#    data_file = ROOT.TFile.Open("/afs/cern.ch/project/afs/var/ABS/recover/R.1935065321.08020759/data/wg/single_electron.root")
#    data_file = ROOT.TFile.Open("/afs/cern.ch/user/a/amlevin/2016_nanoaodsim_data/CMSSW_9_4_4/src/Merged.root") 
#    data_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/z/2016/double_electron.root.bak")
#    data_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/z/2016/double_eg.root")
    data_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/z/2016/1June2019/double_eg.root")
#    data_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/tmp/double_electron.root")
#    data_file = ROOT.TFile.Open("/eos/user/a/amlevin/tmp/double_electron.root")
#    data_file = ROOT.TFile.Open("/afs/cern.ch/user/a/amlevin/z/2016/Merged_Skim.root")
elif lepton_name == "both":
    data_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/z/2016/double_lepton.root")
else:
    assert(0)

for label in labels.keys():

    labels[label]["hists"] = []

    for i in range(len(variables)):    

        labels[label]["hists"].append(histogram_templates[i].Clone(label + " " + variables[i]))
        labels[label]["hists"][i].Sumw2()

    for sample in labels[label]["samples"]:
        sample["file"] = ROOT.TFile.Open(sample["filename"])
        sample["tree"] = sample["file"].Get("Events")
        sample["nweightedevents"] = sample["file"].Get("nWeightedEvents").GetBinContent(1)

data = {}

data["hists"] = []

for i in range(len(variables)):
    data["hists"].append(histogram_templates[i].Clone("data " + variables[i]))

for i in range(len(variables)):
    data["hists"][i].Sumw2()

data_events_tree = data_file.Get("Events")

c1 = ROOT.TCanvas("c1", "c1",5,50,500,500);

ROOT.gROOT.cd()

ROOT.gROOT.ProcessLine("#include \"/afs/cern.ch/user/a/amlevin/recoil_corrections/MetTools/RecoilCorrections/RecoilCorrector.hh\"")

#recoilCorrector = ROOT.RecoilCorrector("/afs/cern.ch/user/a/amlevin/recoil_corrections/MetTools/RecoilCorrections/mc/fits_pf.root","fcnPF") 
#recoilCorrector = ROOT.RecoilCorrector("/afs/cern.ch/user/a/amlevin/recoil_corrections/MetTools/RecoilCorrections/mc/fits_pf.root","grPF") 
#recoilCorrector = ROOT.RecoilCorrector("/afs/cern.ch/user/a/amlevin/recoil_corrections/MetTools/RecoilCorrections/mcmyptbinning/fits_pf.root","grPF") 
recoilCorrector = ROOT.RecoilCorrector("/afs/cern.ch/user/a/amlevin/recoil_corrections/MetTools/RecoilCorrections/mcweightsmyptbinning/fits_pf.root","grPF") 
#recoilCorrector.addDataFile("/afs/cern.ch/user/a/amlevin/recoil_corrections/MetTools/RecoilCorrections/data/fits_pf.root")
recoilCorrector.addDataFile("/afs/cern.ch/user/a/amlevin/recoil_corrections/MetTools/RecoilCorrections/datamyptbinning/fits_pf.root")
recoilCorrector.addMCFile("/afs/cern.ch/user/a/amlevin/recoil_corrections/MetTools/RecoilCorrections/mcweightsmyptbinning/fits_pf.root")
#recoilCorrector.addMCFile("/afs/cern.ch/user/a/amlevin/recoil_corrections/MetTools/RecoilCorrections/data/fits_pf.root")
#recoilCorrector.addDataFile("/afs/cern.ch/user/a/amlevin/recoil_corrections/MetTools/RecoilCorrections/mc/fits_pf.root")
#recoilCorrector.addFileWithGraph("/afs/cern.ch/user/a/amlevin/recoil_corrections/MetTools/RecoilCorrections/mc/fits_pf.root")
recoilCorrector.addFileWithGraph("/afs/cern.ch/user/a/amlevin/recoil_corrections/MetTools/RecoilCorrections/datamyptbinning/fits_pf.root")

def fillHistogramMC(label,sample):

    print "Running over sample " + str(sample["filename"])
    print "sample[\"tree\"].GetEntries() = " + str(sample["tree"].GetEntries())

    for i in range(sample["tree"].GetEntries()):

        if i > 0 and i % 100000 == 0:
            print "Processed " + str(i) + " out of " + str(sample["tree"].GetEntries()) + " events"

        sample["tree"].GetEntry(i)

#        if abs(sample["tree"].genzpt - 129.183) > 0.001:
#            continue
        
        corrMet = sample["tree"].met
        corrMetPhi = sample["tree"].metphi

        if options.apply_recoil_corr:

#            corrMet = ROOT.Double()
#            corrMetPhi = ROOT.Double()
            corrMet = ROOT.Double(sample["tree"].met)
            corrMetPhi = ROOT.Double(sample["tree"].metphi)
            genVPt = ROOT.Double(getVariable("z_pt",sample["tree"]))
            genVPhi = ROOT.Double(getVariable("z_phi",sample["tree"]))
#            genVPt = ROOT.Double(sample["tree"].genzpt)
#            genVPhi = ROOT.Double(sample["tree"].genzphi)
            dileptonPt = ROOT.Double(getVariable("z_pt",sample["tree"]))
            dileptonPhi = ROOT.Double(getVariable("z_phi",sample["tree"]))
#            dileptonPt = ROOT.Double(sample["tree"].genzpt)
#            dileptonPhi = ROOT.Double(sample["tree"].genzphi)
            pu1= ROOT.Double()
            pu2= ROOT.Double()

#            recoilCorrector.CorrectType2(corrMet,corrMetPhi,genVPt,genVPhi,dileptonPt,dileptonPhi,pu1,pu2,-1)
            recoilCorrector.CorrectType2FromGraph(corrMet,corrMetPhi,genVPt,genVPhi,dileptonPt,dileptonPhi,pu1,pu2,0,0)
#            recoilCorrector.CorrectType0(corrMet,corrMetPhi,genVPt,genVPhi,dileptonPt,dileptonPhi,pu1,pu2,0)

#        print corrMet

#            if corrMet > 70:
#                print str(getVariable("z_pt",sample["tree"])) + " " + str(sample["tree"].met) + " " + str(corrMet)


#        if (sample["tree"].puppimet < 0 or sample["tree"].puppimt < 0) or not (sample["tree"].njets15 == 1 and sample["tree"].njets20 == 0) or abs((sample["tree"].met-sample["tree"].rawmet)/sample["tree"].rawmet) < 0.001:
#        if (sample["tree"].met < 0 or sample["tree"].puppimt < 0 or sample["tree"].njets40 != 0):
#        if (corrMet < 60 or sample["tree"].puppimt < 0 or sample["tree"].njets40 != 0 or getVariable("z_pt",sample["tree"]) > 10 or getVariable("z_pt",sample["tree"]) < 9):
#        if (corrMet < 60 or sample["tree"].puppimt < 0 or sample["tree"].njets40 != 0):
#        if (sample["tree"].met < 60 or sample["tree"].puppimt < 0 or sample["tree"].njets40 != 0):
#        if (abs(getVariable("corrrecoil1",sample["tree"],corrMet,corrMetPhi)) < 60 or sample["tree"].puppimt < 0 or sample["tree"].njets40 != 0 or getVariable("z_pt",sample["tree"]) > 10 or getVariable("z_pt",sample["tree"]) < 9):
#        if (sample["tree"].met < 70 or sample["tree"].puppimt < 0 or sample["tree"].njets40 != 0 or getVariable("z_pt",sample["tree"]) > 10 or getVariable("z_pt",sample["tree"]) < 9):
#        if (sample["tree"].met < 70 or sample["tree"].puppimt < 0 or sample["tree"].njets40 != 0 or getVariable("z_pt",sample["tree"]) > 2):
#        if (corrMet < 70 or sample["tree"].puppimt < 0 or sample["tree"].njets40 != 0):
#        if (sample["tree"].met < 70 or sample["tree"].puppimt < 0 or sample["tree"].njets40 != 0):
#        if (sample["tree"].met < 0 or sample["tree"].puppimt < 0 or sample["tree"].njets40 != 0):
        if False:
           continue


        if sample["tree"].is_lepton1_real == '\x01':
            pass_is_lepton_real = True
        else:
            pass_is_lepton_real = False

        weight = sample["xs"] * 1000 * 35.9 / sample["nweightedevents"]
        weight *= pu_weight_hist.GetBinContent(pu_weight_hist.FindFixBin(sample["tree"].npu))    
#        weight *= met_weight_hist.GetBinContent(met_weight_hist.FindFixBin(sample["tree"].met))    
#        weight *= recoil_weight_hist.GetBinContent(recoil_weight_hist.FindFixBin(getVariable("recoil",sample["tree"])))    
#        weight *= zpt_weight_hist.GetBinContent(zpt_weight_hist.FindFixBin(getVariable("z_pt",sample["tree"])))    
#        weight *= recoil_zpt_weight_hist.GetBinContent(recoil_zpt_weight_hist.FindFixBin(getVariable("recoil",sample["tree"])))    
#        weight *= sample["tree"].L1PreFiringWeight 

        if sample["tree"].gen_weight < 0:
            weight = - weight

        if not pass_selection(sample["tree"]):
            continue

        if abs(sample["tree"].lepton1_pdgid) == 11:
            weight *= eff_scale_factor.electron_efficiency_scale_factor(sample["tree"].lepton1_pt,sample["tree"].lepton1_eta)*eff_scale_factor.electron_efficiency_scale_factor(sample["tree"].lepton2_pt,sample["tree"].lepton2_eta)
        elif abs(sample["tree"].lepton1_pdgid) == 13:
            weight *= eff_scale_factor.muon_efficiency_scale_factor(sample["tree"].lepton1_pt,sample["tree"].lepton1_eta)*eff_scale_factor.muon_efficiency_scale_factor(sample["tree"].lepton2_pt,sample["tree"].lepton2_eta)
        else:
            assert(0)

        if options.make_recoil_trees:
            mc_zpt[0] = getVariable("z_pt",sample["tree"])
            mc_u1[0] = getVariable("recoil1",sample["tree"])
            mc_u2[0] = getVariable("recoil2",sample["tree"])
            mc_weight[0] = weight
            mc_recoil_tree.Fill()

        if options.make_plots:    
            for j in range(len(variables)):
                fillHistogram(label["hists"][j],getVariable(variables[j],sample["tree"],corrMet,corrMetPhi),weight)    

print "Running over data"
print "data_events_tree.GetEntries() = " + str(data_events_tree.GetEntries())

for i in range(data_events_tree.GetEntries()):
    
    data_events_tree.GetEntry(i)

    if i > 0 and i % 100000 == 0:
        print "Processed " + str(i) + " out of " + str(data_events_tree.GetEntries()) + " events"

#    if (data_events_tree.puppimet < 70 or data_events_tree.puppimt < 0) or not (data_events_tree.njets15 == 1 and data_events_tree.njets20 == 0) or abs((data_events_tree.met-data_events_tree.rawmet)/data_events_tree.rawmet) < 0.001:  
#    if (abs(getVariable("corrrecoil1",data_events_tree,data_events_tree.met,data_events_tree.metphi)) < 60 or data_events_tree.puppimt < 0 or data_events_tree.njets40 != 0 or getVariable("z_pt",data_events_tree) > 10 or getVariable("z_pt",data_events_tree) < 9):
#    if (data_events_tree.met < 60 or data_events_tree.puppimt < 0 or data_events_tree.njets40 != 0 or getVariable("z_pt",data_events_tree) > 10 or getVariable("z_pt",data_events_tree) < 9):
#    if (data_events_tree.met < 60 or data_events_tree.puppimt < 0 or data_events_tree.njets40 != 0):
#    if (data_events_tree.met < 0 or data_events_tree.puppimt < 0 or data_events_tree.njets40 != 0):
    if False:
        continue

    if pass_selection(data_events_tree):
#        print str(getVariable("dphill",data_events_tree))+" "+str(data_events_tree.run) + " "+str(data_events_tree.lumi) + " " + str(data_events_tree.event)

        if options.make_recoil_trees:

            data_zpt[0] = getVariable("z_pt",data_events_tree)
            data_u1[0] = getVariable("recoil1",data_events_tree)
            data_u2[0] = getVariable("recoil2",data_events_tree)
            data_weight[0] = float(1)
            data_recoil_tree.Fill()

        if options.make_plots:            

            for j in range(len(variables)):
                fillHistogram(data["hists"][j],getVariable(variables[j],data_events_tree,data_events_tree.met,data_events_tree.metphi))

for label in labels.keys():

    for sample in labels[label]["samples"]:
        fillHistogramMC(labels[label],sample)

    for i in range(len(variables)):    

        if labels[label]["color"] == None:
            continue

        labels[label]["hists"][i].SetFillColor(labels[label]["color"])
        labels[label]["hists"][i].SetFillStyle(1001)
        labels[label]["hists"][i].SetLineColor(labels[label]["color"])

if options.normalize_mll:
    labels["z+jets"]["hists"][mll_index].Scale(data["hists"][mll_index].Integral()/labels["z+jets"]["hists"][mll_index].Integral())

#labels["z+jets"]["hists"][0].Scale(data["hists"][0].Integral()/labels["z+jets"]["hists"][0].Integral())

for i in range(len(variables)):

    data["hists"][i].Print("all")
    labels["z+jets"]["hists"][i].Print("all")

    ratio = data["hists"][i].Clone("ratio_"+variables_labels[i]+"_"+str(i))
    ratio.Scale(labels["z+jets"]["hists"][i].Integral()/ratio.Integral())
    ratio.Divide(labels["z+jets"]["hists"][i])
    ratio.Print("all")

    data["hists"][i].SetMarkerStyle(ROOT.kFullCircle)
    data["hists"][i].SetLineWidth(3)
    data["hists"][i].SetLineColor(ROOT.kBlack)

    s=str(options.lumi)+" fb^{-1} (13 TeV)"
    lumilabel = ROOT.TLatex (0.95, 0.93, s)
    lumilabel.SetNDC ()
    lumilabel.SetTextAlign (30)
    lumilabel.SetTextFont (42)
    lumilabel.SetTextSize (0.040)

    hsum = data["hists"][i].Clone()
    hsum.Scale(0.0)

    hstack = ROOT.THStack()

    for label in labels.keys():
        if labels[label]["color"] == None:
            continue
        hsum.Add(labels[label]["hists"][i])
        hstack.Add(labels[label]["hists"][i])

    if data["hists"][i].GetMaximum() < hsum.GetMaximum():
        data["hists"][i].SetMaximum(hsum.GetMaximum()*1.55)
    else:
        data["hists"][i].SetMaximum(data["hists"][i].GetMaximum()*1.55)
        

    data["hists"][i].SetMinimum(0)
    hstack.SetMinimum(0)
    hsum.SetMinimum(0)

    data["hists"][i].Draw("")

    hstack.Draw("hist same")

    cmslabel = ROOT.TLatex (0.18, 0.93, "")
    cmslabel.SetNDC ()
    cmslabel.SetTextAlign (10)
    cmslabel.SetTextFont (42)
    cmslabel.SetTextSize (0.040)
    cmslabel.Draw ("same") 
    
    lumilabel.Draw("same")

    j=0
    draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,data["hists"][i],"data","lp")

    for label in labels.keys():
        if labels[label]["color"] == None:
            continue
        j=j+1    
#        draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,labels[label]["hists"][i],label,"f")
        if len(label) > 10:
            print "Warning: truncating the legend label "+str(label) + " to "+str(label[0:10]) 
            draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,labels[label]["hists"][i],label[0:10],"f")
        else:    
            draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,labels[label]["hists"][i],label,"f")

    set_axis_fonts(data["hists"][i],"x",getXaxisLabel(variables[i]))
    set_axis_fonts(hstack,"x",getXaxisLabel(variables[i]))

    gstat = ROOT.TGraphAsymmErrors(hsum);

    for j in range(0,gstat.GetN()):
        gstat.SetPointEYlow (j, hsum.GetBinError(j+1));
        gstat.SetPointEYhigh(j, hsum.GetBinError(j+1));

    gstat.SetFillColor(12);
    gstat.SetFillStyle(3345);
    gstat.SetMarkerSize(0);
    gstat.SetLineWidth(0);
    gstat.SetLineColor(ROOT.kWhite);
    gstat.Draw("E2same");

    data["hists"][i].Draw("same")

    c1.Update()
    c1.ForceUpdate()
    c1.Modified()

    c1.SaveAs(options.outputdir + "/" + variables_labels[i] + ".png")

c1.Close()

if options.make_recoil_trees:

    recoil_outfile.cd()
    
    data_recoil_tree.Write()
    mc_recoil_tree.Write()
    
    recoil_outfile.Close()
