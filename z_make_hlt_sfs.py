import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--year",type=str,help="Data-taking year",required=True)
parser.add_argument("--plotdir",type=str,help="Output directory for plots",default="/eos/user/a/amlevin/www/tmp/")

args = parser.parse_args()

import ROOT

ROOT.ROOT.EnableImplicitMT()

rdf_mc=ROOT.RDataFrame("Events","/afs/cern.ch/work/a/amlevin/data/z/"+args.year+"/1June2019/zjets_hlt_sf.root")

if args.year == "2016" or args.year == "2017":
    rdf_data=ROOT.RDataFrame("Events","/afs/cern.ch/work/a/amlevin/data/z/"+args.year+"/1June2019/single_electron_hlt_sf.root")
elif args.year == "2018":
    rdf_data=ROOT.RDataFrame("Events","/afs/cern.ch/work/a/amlevin/data/z/"+args.year+"/1June2019/egamma_hlt_sf.root")
else:
    assert(0)

rinterface_mc=rdf_mc.Filter("((lepton1_passHLT && (event % 2 == 0)) || (lepton2_passHLT && (event % 2 == 1))) && abs(lepton1_pdgid) == 11")

if args.year == "2016" or args.year == "2017":    
    rinterface_mc=rinterface_mc.Define("weight","gen_weight/abs(gen_weight)*puWeight*PrefireWeight")
#    rinterface_mc=rinterface_mc.Define("weight","gen_weight*PrefireWeight")
#    rinterface_mc=rinterface_mc.Define("weight","gen_weight/abs(gen_weight)")
else:    
    rinterface_mc=rinterface_mc.Define("weight","gen_weight/abs(gen_weight)*puWeight")
#    rinterface_mc=rinterface_mc.Define("weight","gen_weight/abs(gen_weight)")

rinterface_mc=rinterface_mc.Define("probe_passHLT","if (event % 2 == 0) return lepton2_passHLT; else return lepton1_passHLT;")
rinterface_mc=rinterface_mc.Define("probe_eta","if (event % 2 == 0) return lepton2_eta; else return lepton1_eta;")
rinterface_mc=rinterface_mc.Define("probe_pt","if (event % 2 == 0) return lepton2_pt; else return lepton1_pt;")

rinterface_mc_pass=rinterface_mc.Filter("probe_passHLT")
rinterface_mc_fail=rinterface_mc.Filter("!probe_passHLT")

from array import array

if args.year == "2016":
    binning_pt = array('f',[35,50,60,70,100,150,200,500])
    binning_eta = array('f', [-2.5,-2.0,-1.566,-1.444,-0.8,0,0.8,1.444,1.566,2.0,2.5]) 
elif args.year == "2017":
    binning_pt = array('f',[35,50,60,70,100,150,200,500])
    binning_eta = array('f', [-2.5,-2.0,-1.566,-1.444,-0.8,0,0.8,1.444,1.566,2.0,2.5]) 
elif args.year == "2018":
    binning_pt = array('f',[35,50,60,70,100,150,200,500])
    binning_eta = array('f', [-2.5,-2.0,-1.566,-1.444,-0.8,0,0.8,1.444,1.566,2.0,2.5]) 
else:
    assert(0)

th1dmodel_eta=ROOT.RDF.TH1DModel("", "", len(binning_eta)-1, binning_eta)
th1dmodel_pt=ROOT.RDF.TH1DModel("", "", len(binning_pt)-1, binning_pt)
th2dmodel_etapt=ROOT.RDF.TH2DModel("", "", len(binning_eta)-1, binning_eta, len(binning_pt)-1,binning_pt)

rresultptr_mc_pass_etapt=rinterface_mc_pass.Histo2D(th2dmodel_etapt,"probe_eta","probe_pt","weight")
rresultptr_mc_fail_etapt=rinterface_mc_fail.Histo2D(th2dmodel_etapt,"probe_eta","probe_pt","weight")
rresultptr_mc_pass_eta=rinterface_mc_pass.Histo1D(th1dmodel_eta,"probe_eta","weight")
rresultptr_mc_fail_eta=rinterface_mc_fail.Histo1D(th1dmodel_eta,"probe_eta","weight")
rresultptr_mc_pass_pt=rinterface_mc_pass.Histo1D(th1dmodel_pt,"probe_pt","weight")
rresultptr_mc_fail_pt=rinterface_mc_fail.Histo1D(th1dmodel_pt,"probe_pt","weight")

h_mc_pass_etapt=rresultptr_mc_pass_etapt.GetValue()
h_mc_fail_etapt=rresultptr_mc_fail_etapt.GetValue()
h_mc_pass_eta=rresultptr_mc_pass_eta.GetValue()
h_mc_fail_eta=rresultptr_mc_fail_eta.GetValue()
h_mc_pass_pt=rresultptr_mc_pass_pt.GetValue()
h_mc_fail_pt=rresultptr_mc_fail_pt.GetValue()

for i in range(h_mc_pass_eta.GetNbinsX()+2):
    if h_mc_pass_eta.GetBinContent(i) < 0:
        h_mc_pass_eta.SetBinContent(i,0)
    if h_mc_fail_eta.GetBinContent(i) < 0:
        h_mc_fail_eta.SetBinContent(i,0)

for i in range(h_mc_pass_pt.GetNbinsX()+2):
    if h_mc_pass_pt.GetBinContent(i) < 0:
        h_mc_pass_pt.SetBinContent(i,0)
    if h_mc_fail_pt.GetBinContent(i) < 0:
        h_mc_fail_pt.SetBinContent(i,0)

for i in range(h_mc_pass_etapt.GetNbinsX()+2):
    for j in range(h_mc_pass_etapt.GetNbinsY()+2):
        if h_mc_pass_etapt.GetBinContent(i,j) < 0:
            h_mc_pass_etapt.SetBinContent(i,j,0)
        if h_mc_fail_etapt.GetBinContent(i,j) < 0:
            h_mc_fail_etapt.SetBinContent(i,j,0)

h_mc_etapt_den=th2dmodel_etapt.GetHistogram().Clone()
h_mc_etapt_eff=th2dmodel_etapt.GetHistogram().Clone()
h_mc_etapt_den.Sumw2()
h_mc_etapt_eff.Sumw2()
h_mc_eta_den=th1dmodel_eta.GetHistogram().Clone()
h_mc_eta_eff=th1dmodel_eta.GetHistogram().Clone()
h_mc_eta_den.Sumw2()
h_mc_eta_eff.Sumw2()
h_mc_pt_den=th1dmodel_pt.GetHistogram().Clone()
h_mc_pt_eff=th1dmodel_pt.GetHistogram().Clone()
h_mc_pt_den.Sumw2()
h_mc_pt_eff.Sumw2()

h_etapt_sf=th2dmodel_etapt.GetHistogram().Clone()
h_eta_sf=th1dmodel_eta.GetHistogram().Clone()
h_pt_sf=th1dmodel_pt.GetHistogram().Clone()

h_mc_etapt_den.Add(h_mc_pass_etapt)
h_mc_etapt_den.Add(h_mc_fail_etapt)
h_mc_etapt_eff.Add(h_mc_pass_etapt)
h_mc_etapt_eff.Divide(h_mc_etapt_den)
teff_mc_etapt=ROOT.TEfficiency(h_mc_pass_etapt,h_mc_etapt_den)
h_mc_eta_den.Add(h_mc_pass_eta)
h_mc_eta_den.Add(h_mc_fail_eta)
h_mc_eta_eff.Add(h_mc_pass_eta)
h_mc_eta_eff.Divide(h_mc_eta_den)
teff_mc_eta=ROOT.TEfficiency(h_mc_pass_eta,h_mc_eta_den)
h_mc_pt_den.Add(h_mc_pass_pt)
h_mc_pt_den.Add(h_mc_fail_pt)
h_mc_pt_eff.Add(h_mc_pass_pt)
h_mc_pt_eff.Divide(h_mc_pt_den)
teff_mc_pt=ROOT.TEfficiency(h_mc_pass_pt,h_mc_pt_den)


rinterface_data=rdf_data.Filter("((lepton1_passHLT && (event % 2 == 0)) || (lepton2_passHLT && (event % 2 == 1))) && abs(lepton1_pdgid) == 11")

rinterface_data=rinterface_data.Define("probe_passHLT","if (event % 2 == 0) return lepton2_passHLT; else return lepton1_passHLT;")
rinterface_data=rinterface_data.Define("probe_eta","if (event % 2 == 0) return lepton2_eta; else return lepton1_eta;")
rinterface_data=rinterface_data.Define("probe_pt","if (event % 2 == 0) return lepton2_pt; else return lepton1_pt;")

rinterface_data_pass=rinterface_data.Filter("probe_passHLT")
rinterface_data_fail=rinterface_data.Filter("!probe_passHLT")

rresultptr_data_pass_etapt=rinterface_data_pass.Histo2D(th2dmodel_etapt,"probe_eta","probe_pt")
rresultptr_data_fail_etapt=rinterface_data_fail.Histo2D(th2dmodel_etapt,"probe_eta","probe_pt")
rresultptr_data_pass_eta=rinterface_data_pass.Histo1D(th1dmodel_eta,"probe_eta")
rresultptr_data_fail_eta=rinterface_data_fail.Histo1D(th1dmodel_eta,"probe_eta")
rresultptr_data_pass_pt=rinterface_data_pass.Histo1D(th1dmodel_pt,"probe_pt")
rresultptr_data_fail_pt=rinterface_data_fail.Histo1D(th1dmodel_pt,"probe_pt")

rresultptr_data_pass_etapt.Sumw2()
rresultptr_data_fail_etapt.Sumw2()
rresultptr_data_pass_eta.Sumw2()
rresultptr_data_fail_eta.Sumw2()
rresultptr_data_pass_pt.Sumw2()
rresultptr_data_fail_pt.Sumw2()

h_data_pass_etapt=rresultptr_data_pass_etapt.GetValue()
h_data_fail_etapt=rresultptr_data_fail_etapt.GetValue()
h_data_pass_eta=rresultptr_data_pass_eta.GetValue()
h_data_fail_eta=rresultptr_data_fail_eta.GetValue()
h_data_pass_pt=rresultptr_data_pass_pt.GetValue()
h_data_fail_pt=rresultptr_data_fail_pt.GetValue()

h_data_etapt_den=th2dmodel_etapt.GetHistogram().Clone()
h_data_etapt_eff=th2dmodel_etapt.GetHistogram().Clone()
h_data_etapt_den.Sumw2()
h_data_etapt_eff.Sumw2()
h_data_eta_den=th1dmodel_eta.GetHistogram().Clone()
h_data_eta_eff=th1dmodel_eta.GetHistogram().Clone()
h_data_eta_den.Sumw2()
h_data_eta_eff.Sumw2()
h_data_pt_den=th1dmodel_pt.GetHistogram().Clone()
h_data_pt_eff=th1dmodel_pt.GetHistogram().Clone()
h_data_pt_den.Sumw2()
h_data_pt_eff.Sumw2()

h_data_etapt_den.Add(h_data_pass_etapt)
h_data_etapt_den.Add(h_data_fail_etapt)
h_data_etapt_eff.Add(h_data_pass_etapt)
h_data_etapt_eff.Divide(h_data_etapt_den)
teff_data_etapt=ROOT.TEfficiency(h_data_pass_etapt,h_data_etapt_den)
h_data_eta_den.Add(h_data_pass_eta)
h_data_eta_den.Add(h_data_fail_eta)
h_data_eta_eff.Add(h_data_pass_eta)
h_data_eta_eff.Divide(h_data_eta_den)
teff_data_eta=ROOT.TEfficiency(h_data_pass_eta,h_data_eta_den)
h_data_pt_den.Add(h_data_pass_pt)
h_data_pt_den.Add(h_data_fail_pt)
h_data_pt_eff.Add(h_data_pass_pt)
h_data_pt_eff.Divide(h_data_pt_den)
teff_data_pt=ROOT.TEfficiency(h_data_pass_pt,h_data_pt_den)

c1 = ROOT.TCanvas("c1","c1")

#h_data_pass.SetStats(0)
#h_data_pass.Draw("colz")
#h_data_eta_eff.SetStats(0)
#h_data_eta_eff.Draw()
teff_data_eta.Draw()

c1.SaveAs(args.plotdir+"/data_"+args.year+"_eta.png")

c2 = ROOT.TCanvas("c2","c2")

#h_data_pass.SetStats(0)
#h_data_pass.Draw("colz")
#h_data_pt_eff.SetStats(0)
#h_data_pt_eff.Draw()

teff_data_pt.Draw()

c2.SaveAs(args.plotdir+"/data_"+args.year+"_pt.png")

c3 = ROOT.TCanvas("c3","c3")

#h_data_pass.SetStats(0)
#h_data_pass.Draw("colz")
#h_data_etapt_eff.SetStats(0)
#h_data_etapt_eff.Draw("zcol")
teff_data_etapt.Draw("zcol")

c3.SaveAs(args.plotdir+"/data_"+args.year+"_etapt.png")

c4 = ROOT.TCanvas("c4","c4")

#h_mc_pass.SetStats(0)
#h_mc_pass.Draw("colz")
#h_mc_eta_eff.SetStats(0)
#h_mc_eta_eff.Draw()

teff_mc_eta.Draw()

c4.SaveAs(args.plotdir+"/mc_"+args.year+"_eta.png")

c5 = ROOT.TCanvas("c5","c5")

#h_mc_pass.SetStats(0)
#h_mc_pass.Draw("colz")
#h_mc_pt_eff.SetStats(0)
#h_mc_pt_eff.Draw()

teff_mc_pt.Draw()

c5.SaveAs(args.plotdir+"/mc_"+args.year+"_pt.png")

c6 = ROOT.TCanvas("c6","c6")

#h_mc_pass.SetStats(0)
#h_mc_pass.Draw("colz")
#h_mc_etapt_eff.SetStats(0)
#h_mc_etapt_eff.Draw("zcol")

teff_mc_etapt.Draw()

c6.SaveAs(args.plotdir+"/mc_"+args.year+"_etapt.png")

for i in range(h_mc_pass_etapt.GetNbinsX()+2):
    for j in range(h_mc_pass_etapt.GetNbinsY()+2):
        h_mc_etapt_eff.SetBinContent(i,j,teff_mc_etapt.GetEfficiency(teff_mc_etapt.GetGlobalBin(i,j)))
        h_mc_etapt_eff.SetBinError(i,j,max(teff_mc_etapt.GetEfficiency(teff_mc_etapt.GetGlobalBin(i,j)),teff_mc_etapt.GetEfficiency(teff_mc_etapt.GetGlobalBin(i,j))))
    for j in range(h_data_pass_etapt.GetNbinsY()+2):
        h_data_etapt_eff.SetBinContent(i,j,teff_data_etapt.GetEfficiency(teff_data_etapt.GetGlobalBin(i,j)))
        h_data_etapt_eff.SetBinError(i,j,max(teff_data_etapt.GetEfficiency(teff_data_etapt.GetGlobalBin(i,j)),teff_data_etapt.GetEfficiency(teff_data_etapt.GetGlobalBin(i,j))))

h_etapt_sf.Add(h_data_etapt_eff)
h_etapt_sf.Divide(h_mc_etapt_eff)

c7 = ROOT.TCanvas("c7","c7")

h_etapt_sf.SetStats(0)
h_etapt_sf.Draw("colz")

c7.SaveAs(args.plotdir+"/sf_"+args.year+"_etapt.png")

