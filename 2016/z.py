data_driven = True

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

from math import hypot, pi, sqrt

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

f_pu_weights = ROOT.TFile("/afs/cern.ch/user/a/amlevin/PileupWeights2016.root")

pu_weight_hist = f_pu_weights.Get("ratio")

from z_labels import labels

mll_index = 3

variables = ["met","lepton1_pt","lepton1_eta","mll","lepton1_phi","mt","npvs"]
variables_labels = ["met","lepton1_pt","lepton1_eta","mll","lepton1_phi","mt","npvs"]

assert(len(variables) == len(variables_labels))

from array import array

histogram_templates = [ROOT.TH1F("met", "", 15 , 0., 300 ), ROOT.TH1F('lepton_pt', '', 8, 20., 180 ), ROOT.TH1F('lepton_eta', '', 10, -2.5, 2.5 ), ROOT.TH1F("mll","",60,60,120),ROOT.TH1F("lepton_phi","",14,-3.5,3.5), ROOT.TH1F("mt","",20,0,200), ROOT.TH1F("npvs","",51,-0.5,50.5)] 

assert(len(variables) == len(histogram_templates))

def getVariable(varname, tree):
    if varname == "mll":
        return tree.mll
    elif varname == "mt":
        return tree.mt
    elif varname == "npvs":
        return float(tree.npvs)
    elif varname == "met":
        return tree.met
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
    elif varname == "mt":
        return "m_{t} (GeV)"
    elif varname == "mll":
        return "m_{ll} (GeV)"
    elif varname == "met":
        return "MET (GeV)"
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

    if tree.mll > 80:
        pass_mll = False
    else:
        pass_mll = True


#    if tree.met > 35:
    if tree.met > 70:
#    if tree.met > 0:
        pass_met = True
    else:
        pass_met = False

    if tree.mt > 30:
#    if tree.mt > 0:
        pass_mt = True
    else:
        pass_mt = False


    if pass_lepton_pt and pass_lepton_selection and  pass_mll and pass_lepton_flavor and pass_met and pass_mt:
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
    data_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/z/2016/double_muon.root")
elif lepton_name == "electron":
#    data_file = ROOT.TFile.Open("/afs/cern.ch/project/afs/var/ABS/recover/R.1935065321.08020759/data/wg/single_electron.root")
    data_file = ROOT.TFile.Open("/afs/cern.ch/work/a/amlevin/data/z/2016/double_electron.root")
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

def fillHistogramMC(label,sample):

    print "Running over sample " + str(sample["filename"])
    print "sample[\"tree\"].GetEntries() = " + str(sample["tree"].GetEntries())

    for i in range(sample["tree"].GetEntries()):

        if i > 0 and i % 100000 == 0:
            print "Processed " + str(i) + " out of " + str(sample["tree"].GetEntries()) + " events"

        sample["tree"].GetEntry(i)

        if sample["tree"].met < 70 or sample["tree"].mt < 30:
            continue

        if sample["tree"].is_lepton1_real == '\x01':
            pass_is_lepton_real = True
        else:
            pass_is_lepton_real = False

        weight = sample["xs"] * 1000 * 35.9 / sample["nweightedevents"]
        weight *= pu_weight_hist.GetBinContent(pu_weight_hist.FindFixBin(sample["tree"].npu))    
        weight *= sample["tree"].L1PreFiringWeight 

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

        for j in range(len(variables)):
            fillHistogram(label["hists"][j],getVariable(variables[j],sample["tree"]),weight)    

print "Running over data"
print "data_events_tree.GetEntries() = " + str(data_events_tree.GetEntries())

for i in range(data_events_tree.GetEntries()):
    data_events_tree.GetEntry(i)

    if i > 0 and i % 100000 == 0:
        print "Processed " + str(i) + " out of " + str(data_events_tree.GetEntries()) + " events"

    if data_events_tree.met < 70 or data_events_tree.mt < 30:  
        continue

    if pass_selection(data_events_tree):
        for j in range(len(variables)):
            fillHistogram(data["hists"][j],getVariable(variables[j],data_events_tree))

for label in labels.keys():

    for sample in labels[label]["samples"]:
        fillHistogramMC(labels[label],sample)

    for i in range(len(variables)):    

        if labels[label]["color"] == None:
            continue

        labels[label]["hists"][i].SetFillColor(labels[label]["color"])
        labels[label]["hists"][i].SetFillStyle(1001)
        labels[label]["hists"][i].SetLineColor(labels[label]["color"])

labels["z+jets"]["hists"][mll_index].Print("all")
data["hists"][mll_index].Print("all")

for i in range(len(variables)):

    data["hists"][i].Print("all")

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

    if lepton_name == "electron" or lepton_name == "both": 
        hsum.Add(e_to_p["hists"][i])
        hstack.Add(e_to_p["hists"][i])

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

    if lepton_name == "electron" or lepton_name == "both":
        j=j+1
        draw_legend(xpositions[j],0.84 - ypositions[j]*yoffset,e_to_p["hists"][i],"e->#gamma","f")

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

