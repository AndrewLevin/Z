import argparse

parser = argparse.ArgumentParser()

parser.add_argument("--year",type=str,help="Data-taking year",required=True)
parser.add_argument("--plotdir",type=str,help="Output directory for plots",default="/eos/user/a/amlevin/www/tmp/")
parser.add_argument("--outfile",type=str,help="Output root filename",required=True)

args = parser.parse_args()

import ROOT

ROOT.ROOT.EnableImplicitMT()

eff_scale_factor_cpp = '''

TFile electron_id_2016_sf_file("eff_scale_factors/2016/2016LegacyReReco_ElectronMedium_Fall17V2.root","read");
TH2F * electron_id_2016_sf = (TH2F*) electron_id_2016_sf_file.Get("EGamma_SF2D");

TFile electron_id_2017_sf_file("eff_scale_factors/2017/2017_ElectronMedium.root","read");
TH2F * electron_id_2017_sf = (TH2F*)electron_id_2017_sf_file.Get("EGamma_SF2D");

TFile electron_id_2018_sf_file("eff_scale_factors/2018/2018_ElectronMedium.root","read");
TH2F * electron_id_2018_sf = (TH2F*)electron_id_2018_sf_file.Get("EGamma_SF2D");

TFile electron_reco_2016_sf_file("eff_scale_factors/2016/EGM2D_BtoH_GT20GeV_RecoSF_Legacy2016.root","read");
TH2F * electron_reco_2016_sf = (TH2F*) electron_reco_2016_sf_file.Get("EGamma_SF2D");

TFile electron_reco_2017_sf_file("eff_scale_factors/2017/egammaEffi.txt_EGM2D_runBCDEF_passingRECO.root","read");
TH2F * electron_reco_2017_sf = (TH2F*)electron_reco_2017_sf_file.Get("EGamma_SF2D");

TFile electron_reco_2018_sf_file("eff_scale_factors/2018/egammaEffi.txt_EGM2D_updatedAll.root" ,"read");
TH2F * electron_reco_2018_sf = (TH2F*)electron_reco_2018_sf_file.Get("EGamma_SF2D");

float electron_efficiency_scale_factor(float pt, float eta, string year) {
    TH2F * electron_reco_sf = 0;
    TH2F * electron_id_sf = 0;
    if (year == "2016") {
        electron_reco_sf = electron_reco_2016_sf;
        electron_id_sf = electron_id_2016_sf;
    }
    else if (year == "2017"){
        electron_reco_sf = electron_reco_2017_sf;
        electron_id_sf = electron_id_2017_sf;
    }
    else if (year == "2018") {
        electron_reco_sf = electron_reco_2018_sf;
        electron_id_sf = electron_id_2018_sf;
    }
    else
        assert(0);
    int electron_id_sf_xaxisbin = -1;
    int electron_id_sf_yaxisbin = -1;
    if (year == "2016") {    
        electron_id_sf_xaxisbin = electron_id_sf->GetXaxis()->FindFixBin(eta);
        electron_id_sf_yaxisbin = electron_id_sf->GetYaxis()->FindFixBin(TMath::Min(pt,float(electron_id_sf->GetYaxis()->GetBinCenter(electron_id_sf->GetNbinsY()))));
    }
    else if (year == "2017") {
        electron_id_sf_xaxisbin = electron_id_sf->GetXaxis()->FindFixBin(eta);
        electron_id_sf_yaxisbin = electron_id_sf->GetYaxis()->FindFixBin(TMath::Min(pt,float(electron_id_sf->GetYaxis()->GetBinCenter(electron_id_sf->GetNbinsY()))));
    }
    else if (year == "2018") {
        electron_id_sf_xaxisbin = electron_id_sf->GetXaxis()->FindFixBin(eta);
        electron_id_sf_yaxisbin = electron_id_sf->GetYaxis()->FindFixBin(TMath::Min(pt,float(electron_id_sf->GetYaxis()->GetBinCenter(electron_id_sf->GetNbinsY()))));
    }
    else assert(0);

    float sf_id = electron_id_sf->GetBinContent(electron_id_sf_xaxisbin,electron_id_sf_yaxisbin); 
    //the reco 2D histogram is really a 1D histogram
    float sf_reco=electron_reco_sf->GetBinContent(electron_reco_sf->GetXaxis()->FindFixBin(eta),1);
    return sf_id*sf_reco;
}

'''

ROOT.gInterpreter.Declare(eff_scale_factor_cpp)

rdf_mc1=ROOT.RDataFrame("Events","/afs/cern.ch/work/a/amlevin/data/z/"+args.year+"/1June2019/zjetsfxfx_hlt_sf.root")
rdf_mc2=ROOT.RDataFrame("Events","/afs/cern.ch/work/a/amlevin/data/z/"+args.year+"/1June2019/zjetsmlm_hlt_sf.root")
rdf_mc3=ROOT.RDataFrame("Events","/afs/cern.ch/work/a/amlevin/data/z/"+args.year+"/1June2019/zjetsfxfx_hlt_sf.root")
rdf_mc4=ROOT.RDataFrame("Events","/afs/cern.ch/work/a/amlevin/data/z/"+args.year+"/1June2019/zjetsfxfx_hlt_sf.root")

if args.year == "2016" or args.year == "2017":
    rdf_data1=ROOT.RDataFrame("Events","/afs/cern.ch/work/a/amlevin/data/z/"+args.year+"/1June2019/single_electron_hlt_sf.root")
    rdf_data2=ROOT.RDataFrame("Events","/afs/cern.ch/work/a/amlevin/data/z/"+args.year+"/1June2019/single_electron_hlt_sf.root")
    rdf_data3=ROOT.RDataFrame("Events","/afs/cern.ch/work/a/amlevin/data/z/"+args.year+"/1June2019/single_electron_hlt_sf.root")
elif args.year == "2018":
    rdf_data1=ROOT.RDataFrame("Events","/afs/cern.ch/work/a/amlevin/data/z/"+args.year+"/1June2019/egamma_hlt_sf.root")
    rdf_data2=ROOT.RDataFrame("Events","/afs/cern.ch/work/a/amlevin/data/z/"+args.year+"/1June2019/egamma_hlt_sf.root")
    rdf_data3=ROOT.RDataFrame("Events","/afs/cern.ch/work/a/amlevin/data/z/"+args.year+"/1June2019/egamma_hlt_sf.root")
else:
    assert(0)

rinterface_mc1=rdf_mc1.Filter("((lepton1_passHLT && (event % 2 == 0)) || (lepton2_passHLT && (event % 2 == 1))) && abs(lepton1_pdgid) == 11 && mll > 60 && mll < 120")
rinterface_mc2=rdf_mc2.Filter("((lepton1_passHLT && (event % 2 == 0)) || (lepton2_passHLT && (event % 2 == 1))) && abs(lepton1_pdgid) == 11 && mll > 60 && mll < 120")
rinterface_mc3=rdf_mc3.Filter("((lepton1_passHLT && (event % 2 == 0)) || (lepton2_passHLT && (event % 2 == 1))) && abs(lepton1_pdgid) == 11 && mll > 86.18 && mll < 96.18")
rinterface_mc4=rdf_mc4.Filter("((lepton1_passHLT && (event % 2 == 0)) || (lepton2_passHLT && (event % 2 == 1))) && abs(lepton1_pdgid) == 11 && ((mll > 60 && mll < 86.18) || (mll > 96.18 && mll < 120))")



if args.year == "2016" or args.year == "2017":    
    rinterface_mc1=rinterface_mc1.Define("weight","gen_weight/abs(gen_weight)*puWeight*PrefireWeight*electron_efficiency_scale_factor(lepton1_pt,lepton1_eta,\""+args.year+"\")*electron_efficiency_scale_factor(lepton2_pt,lepton2_eta,\""+args.year+"\")")
    rinterface_mc2=rinterface_mc2.Define("weight","gen_weight/abs(gen_weight)*puWeight*PrefireWeight*electron_efficiency_scale_factor(lepton1_pt,lepton1_eta,\""+args.year+"\")*electron_efficiency_scale_factor(lepton2_pt,lepton2_eta,\""+args.year+"\")")
    rinterface_mc3=rinterface_mc3.Define("weight","gen_weight/abs(gen_weight)*puWeight*PrefireWeight*electron_efficiency_scale_factor(lepton1_pt,lepton1_eta,\""+args.year+"\")*electron_efficiency_scale_factor(lepton2_pt,lepton2_eta,\""+args.year+"\")")    
    rinterface_mc4=rinterface_mc4.Define("weight","gen_weight/abs(gen_weight)*puWeight*PrefireWeight*electron_efficiency_scale_factor(lepton1_pt,lepton1_eta,\""+args.year+"\")*electron_efficiency_scale_factor(lepton2_pt,lepton2_eta,\""+args.year+"\")")
#    rinterface_mc=rinterface_mc.Define("weight","gen_weight*PrefireWeight")
#    rinterface_mc=rinterface_mc.Define("weight","gen_weight/abs(gen_weight)")
else:    
    rinterface_mc1=rinterface_mc1.Define("weight","gen_weight/abs(gen_weight)*puWeight*electron_efficiency_scale_factor(lepton1_pt,lepton1_eta,\""+args.year+"\")*electron_efficiency_scale_factor(lepton2_pt,lepton2_eta,\""+args.year+"\")")
    rinterface_mc2=rinterface_mc2.Define("weight","gen_weight/abs(gen_weight)*puWeight*electron_efficiency_scale_factor(lepton1_pt,lepton1_eta,\""+args.year+"\")*electron_efficiency_scale_factor(lepton2_pt,lepton2_eta,\""+args.year+"\")")
    rinterface_mc3=rinterface_mc3.Define("weight","gen_weight/abs(gen_weight)*puWeight*electron_efficiency_scale_factor(lepton1_pt,lepton1_eta,\""+args.year+"\")*electron_efficiency_scale_factor(lepton2_pt,lepton2_eta,\""+args.year+"\")")
    rinterface_mc4=rinterface_mc4.Define("weight","gen_weight/abs(gen_weight)*puWeight*electron_efficiency_scale_factor(lepton1_pt,lepton1_eta,\""+args.year+"\")*electron_efficiency_scale_factor(lepton2_pt,lepton2_eta,\""+args.year+"\")")
#    rinterface_mc=rinterface_mc.Define("weight","gen_weight/abs(gen_weight)")

rinterface_mc1=rinterface_mc1.Define("probe_passHLT","if (event % 2 == 0) return lepton2_passHLT; else return lepton1_passHLT;")
rinterface_mc1=rinterface_mc1.Define("probe_eta","if (event % 2 == 0) return lepton2_eta; else return lepton1_eta;")
rinterface_mc1=rinterface_mc1.Define("probe_pt","if (event % 2 == 0) return lepton2_pt; else return lepton1_pt;")

rinterface_mc1_pass=rinterface_mc1.Filter("probe_passHLT")
rinterface_mc1_fail=rinterface_mc1.Filter("!probe_passHLT")

rinterface_mc2=rinterface_mc2.Define("probe_passHLT","if (event % 2 == 0) return lepton2_passHLT; else return lepton1_passHLT;")
rinterface_mc2=rinterface_mc2.Define("probe_eta","if (event % 2 == 0) return lepton2_eta; else return lepton1_eta;")
rinterface_mc2=rinterface_mc2.Define("probe_pt","if (event % 2 == 0) return lepton2_pt; else return lepton1_pt;")

rinterface_mc2_pass=rinterface_mc2.Filter("probe_passHLT")
rinterface_mc2_fail=rinterface_mc2.Filter("!probe_passHLT")

rinterface_mc3=rinterface_mc3.Define("probe_passHLT","if (event % 2 == 0) return lepton2_passHLT; else return lepton1_passHLT;")
rinterface_mc3=rinterface_mc3.Define("probe_eta","if (event % 2 == 0) return lepton2_eta; else return lepton1_eta;")
rinterface_mc3=rinterface_mc3.Define("probe_pt","if (event % 2 == 0) return lepton2_pt; else return lepton1_pt;")

rinterface_mc3_pass=rinterface_mc3.Filter("probe_passHLT")
rinterface_mc3_fail=rinterface_mc3.Filter("!probe_passHLT")

rinterface_mc4=rinterface_mc4.Define("probe_passHLT","if (event % 2 == 0) return lepton2_passHLT; else return lepton1_passHLT;")
rinterface_mc4=rinterface_mc4.Define("probe_eta","if (event % 2 == 0) return lepton2_eta; else return lepton1_eta;")
rinterface_mc4=rinterface_mc4.Define("probe_pt","if (event % 2 == 0) return lepton2_pt; else return lepton1_pt;")

rinterface_mc4_pass=rinterface_mc4.Filter("probe_passHLT")
rinterface_mc4_fail=rinterface_mc4.Filter("!probe_passHLT")

from array import array

if args.year == "2016":
    binning_pt = array('f',[30,40,50,60,70,100,150,200,500])
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

rresultptr_mc1_pass_etapt=rinterface_mc1_pass.Histo2D(th2dmodel_etapt,"probe_eta","probe_pt","weight")
rresultptr_mc1_fail_etapt=rinterface_mc1_fail.Histo2D(th2dmodel_etapt,"probe_eta","probe_pt","weight")
rresultptr_mc1_pass_eta=rinterface_mc1_pass.Histo1D(th1dmodel_eta,"probe_eta","weight")
rresultptr_mc1_fail_eta=rinterface_mc1_fail.Histo1D(th1dmodel_eta,"probe_eta","weight")
rresultptr_mc1_pass_pt=rinterface_mc1_pass.Histo1D(th1dmodel_pt,"probe_pt","weight")
rresultptr_mc1_fail_pt=rinterface_mc1_fail.Histo1D(th1dmodel_pt,"probe_pt","weight")

h_mc1_pass_etapt=rresultptr_mc1_pass_etapt.GetValue()
h_mc1_fail_etapt=rresultptr_mc1_fail_etapt.GetValue()
h_mc1_pass_eta=rresultptr_mc1_pass_eta.GetValue()
h_mc1_fail_eta=rresultptr_mc1_fail_eta.GetValue()
h_mc1_pass_pt=rresultptr_mc1_pass_pt.GetValue()
h_mc1_fail_pt=rresultptr_mc1_fail_pt.GetValue()

rresultptr_mc2_pass_etapt=rinterface_mc2_pass.Histo2D(th2dmodel_etapt,"probe_eta","probe_pt","weight")
rresultptr_mc2_fail_etapt=rinterface_mc2_fail.Histo2D(th2dmodel_etapt,"probe_eta","probe_pt","weight")
rresultptr_mc2_pass_eta=rinterface_mc2_pass.Histo1D(th1dmodel_eta,"probe_eta","weight")
rresultptr_mc2_fail_eta=rinterface_mc2_fail.Histo1D(th1dmodel_eta,"probe_eta","weight")
rresultptr_mc2_pass_pt=rinterface_mc2_pass.Histo1D(th1dmodel_pt,"probe_pt","weight")
rresultptr_mc2_fail_pt=rinterface_mc2_fail.Histo1D(th1dmodel_pt,"probe_pt","weight")

h_mc2_pass_etapt=rresultptr_mc2_pass_etapt.GetValue()
h_mc2_fail_etapt=rresultptr_mc2_fail_etapt.GetValue()
h_mc2_pass_eta=rresultptr_mc2_pass_eta.GetValue()
h_mc2_fail_eta=rresultptr_mc2_fail_eta.GetValue()
h_mc2_pass_pt=rresultptr_mc2_pass_pt.GetValue()
h_mc2_fail_pt=rresultptr_mc2_fail_pt.GetValue()

rresultptr_mc3_pass_etapt=rinterface_mc3_pass.Histo2D(th2dmodel_etapt,"probe_eta","probe_pt","weight")
rresultptr_mc3_fail_etapt=rinterface_mc3_fail.Histo2D(th2dmodel_etapt,"probe_eta","probe_pt","weight")
rresultptr_mc3_pass_eta=rinterface_mc3_pass.Histo1D(th1dmodel_eta,"probe_eta","weight")
rresultptr_mc3_fail_eta=rinterface_mc3_fail.Histo1D(th1dmodel_eta,"probe_eta","weight")
rresultptr_mc3_pass_pt=rinterface_mc3_pass.Histo1D(th1dmodel_pt,"probe_pt","weight")
rresultptr_mc3_fail_pt=rinterface_mc3_fail.Histo1D(th1dmodel_pt,"probe_pt","weight")

h_mc3_pass_etapt=rresultptr_mc3_pass_etapt.GetValue()
h_mc3_fail_etapt=rresultptr_mc3_fail_etapt.GetValue()
h_mc3_pass_eta=rresultptr_mc3_pass_eta.GetValue()
h_mc3_fail_eta=rresultptr_mc3_fail_eta.GetValue()
h_mc3_pass_pt=rresultptr_mc3_pass_pt.GetValue()
h_mc3_fail_pt=rresultptr_mc3_fail_pt.GetValue()

rresultptr_mc4_pass_etapt=rinterface_mc4_pass.Histo2D(th2dmodel_etapt,"probe_eta","probe_pt","weight")
rresultptr_mc4_fail_etapt=rinterface_mc4_fail.Histo2D(th2dmodel_etapt,"probe_eta","probe_pt","weight")
rresultptr_mc4_pass_eta=rinterface_mc4_pass.Histo1D(th1dmodel_eta,"probe_eta","weight")
rresultptr_mc4_fail_eta=rinterface_mc4_fail.Histo1D(th1dmodel_eta,"probe_eta","weight")
rresultptr_mc4_pass_pt=rinterface_mc4_pass.Histo1D(th1dmodel_pt,"probe_pt","weight")
rresultptr_mc4_fail_pt=rinterface_mc4_fail.Histo1D(th1dmodel_pt,"probe_pt","weight")

h_mc4_pass_etapt=rresultptr_mc4_pass_etapt.GetValue()
h_mc4_fail_etapt=rresultptr_mc4_fail_etapt.GetValue()
h_mc4_pass_eta=rresultptr_mc4_pass_eta.GetValue()
h_mc4_fail_eta=rresultptr_mc4_fail_eta.GetValue()
h_mc4_pass_pt=rresultptr_mc4_pass_pt.GetValue()
h_mc4_fail_pt=rresultptr_mc4_fail_pt.GetValue()

for i in range(h_mc1_pass_eta.GetNbinsX()+2):
    if h_mc1_pass_eta.GetBinContent(i) < 0:
        h_mc1_pass_eta.SetBinContent(i,0)
    if h_mc1_fail_eta.GetBinContent(i) < 0:
        h_mc1_fail_eta.SetBinContent(i,0)

for i in range(h_mc1_pass_pt.GetNbinsX()+2):
    if h_mc1_pass_pt.GetBinContent(i) < 0:
        h_mc1_pass_pt.SetBinContent(i,0)
    if h_mc1_fail_pt.GetBinContent(i) < 0:
        h_mc1_fail_pt.SetBinContent(i,0)

for i in range(h_mc1_pass_etapt.GetNbinsX()+2):
    for j in range(h_mc1_pass_etapt.GetNbinsY()+2):
        if h_mc1_pass_etapt.GetBinContent(i,j) < 0:
            h_mc1_pass_etapt.SetBinContent(i,j,0)
        if h_mc1_fail_etapt.GetBinContent(i,j) < 0:
            h_mc1_fail_etapt.SetBinContent(i,j,0)

for i in range(h_mc2_pass_eta.GetNbinsX()+2):
    if h_mc2_pass_eta.GetBinContent(i) < 0:
        h_mc2_pass_eta.SetBinContent(i,0)
    if h_mc2_fail_eta.GetBinContent(i) < 0:
        h_mc2_fail_eta.SetBinContent(i,0)

for i in range(h_mc2_pass_pt.GetNbinsX()+2):
    if h_mc2_pass_pt.GetBinContent(i) < 0:
        h_mc2_pass_pt.SetBinContent(i,0)
    if h_mc2_fail_pt.GetBinContent(i) < 0:
        h_mc2_fail_pt.SetBinContent(i,0)

for i in range(h_mc2_pass_etapt.GetNbinsX()+2):
    for j in range(h_mc2_pass_etapt.GetNbinsY()+2):
        if h_mc2_pass_etapt.GetBinContent(i,j) < 0:
            h_mc2_pass_etapt.SetBinContent(i,j,0)
        if h_mc2_fail_etapt.GetBinContent(i,j) < 0:
            h_mc2_fail_etapt.SetBinContent(i,j,0)

for i in range(h_mc3_pass_eta.GetNbinsX()+2):
    if h_mc3_pass_eta.GetBinContent(i) < 0:
        h_mc3_pass_eta.SetBinContent(i,0)
    if h_mc3_fail_eta.GetBinContent(i) < 0:
        h_mc3_fail_eta.SetBinContent(i,0)

for i in range(h_mc3_pass_pt.GetNbinsX()+2):
    if h_mc3_pass_pt.GetBinContent(i) < 0:
        h_mc3_pass_pt.SetBinContent(i,0)
    if h_mc3_fail_pt.GetBinContent(i) < 0:
        h_mc3_fail_pt.SetBinContent(i,0)

for i in range(h_mc3_pass_etapt.GetNbinsX()+2):
    for j in range(h_mc3_pass_etapt.GetNbinsY()+2):
        if h_mc3_pass_etapt.GetBinContent(i,j) < 0:
            h_mc3_pass_etapt.SetBinContent(i,j,0)
        if h_mc3_fail_etapt.GetBinContent(i,j) < 0:
            h_mc3_fail_etapt.SetBinContent(i,j,0)

for i in range(h_mc4_pass_eta.GetNbinsX()+2):
    if h_mc4_pass_eta.GetBinContent(i) < 0:
        h_mc4_pass_eta.SetBinContent(i,0)
    if h_mc4_fail_eta.GetBinContent(i) < 0:
        h_mc4_fail_eta.SetBinContent(i,0)

for i in range(h_mc4_pass_pt.GetNbinsX()+2):
    if h_mc4_pass_pt.GetBinContent(i) < 0:
        h_mc4_pass_pt.SetBinContent(i,0)
    if h_mc4_fail_pt.GetBinContent(i) < 0:
        h_mc4_fail_pt.SetBinContent(i,0)

for i in range(h_mc4_pass_etapt.GetNbinsX()+2):
    for j in range(h_mc4_pass_etapt.GetNbinsY()+2):
        if h_mc4_pass_etapt.GetBinContent(i,j) < 0:
            h_mc4_pass_etapt.SetBinContent(i,j,0)
        if h_mc4_fail_etapt.GetBinContent(i,j) < 0:
            h_mc4_fail_etapt.SetBinContent(i,j,0)

h_mc1_etapt_den=th2dmodel_etapt.GetHistogram().Clone()
h_mc1_etapt_eff=th2dmodel_etapt.GetHistogram().Clone()
h_mc1_etapt_den.Sumw2()
h_mc1_etapt_eff.Sumw2()
h_mc1_eta_den=th1dmodel_eta.GetHistogram().Clone()
h_mc1_eta_eff=th1dmodel_eta.GetHistogram().Clone()
h_mc1_eta_den.Sumw2()
h_mc1_eta_eff.Sumw2()
h_mc1_pt_den=th1dmodel_pt.GetHistogram().Clone()
h_mc1_pt_eff=th1dmodel_pt.GetHistogram().Clone()
h_mc1_pt_den.Sumw2()
h_mc1_pt_eff.Sumw2()

h_mc2_etapt_den=th2dmodel_etapt.GetHistogram().Clone()
h_mc2_etapt_eff=th2dmodel_etapt.GetHistogram().Clone()
h_mc2_etapt_den.Sumw2()
h_mc2_etapt_eff.Sumw2()
h_mc2_eta_den=th1dmodel_eta.GetHistogram().Clone()
h_mc2_eta_eff=th1dmodel_eta.GetHistogram().Clone()
h_mc2_eta_den.Sumw2()
h_mc2_eta_eff.Sumw2()
h_mc2_pt_den=th1dmodel_pt.GetHistogram().Clone()
h_mc2_pt_eff=th1dmodel_pt.GetHistogram().Clone()
h_mc2_pt_den.Sumw2()
h_mc2_pt_eff.Sumw2()

h_mc3_etapt_den=th2dmodel_etapt.GetHistogram().Clone()
h_mc3_etapt_eff=th2dmodel_etapt.GetHistogram().Clone()
h_mc3_etapt_den.Sumw2()
h_mc3_etapt_eff.Sumw2()
h_mc3_eta_den=th1dmodel_eta.GetHistogram().Clone()
h_mc3_eta_eff=th1dmodel_eta.GetHistogram().Clone()
h_mc3_eta_den.Sumw2()
h_mc3_eta_eff.Sumw2()
h_mc3_pt_den=th1dmodel_pt.GetHistogram().Clone()
h_mc3_pt_eff=th1dmodel_pt.GetHistogram().Clone()
h_mc3_pt_den.Sumw2()
h_mc3_pt_eff.Sumw2()

h_mc4_etapt_den=th2dmodel_etapt.GetHistogram().Clone()
h_mc4_etapt_eff=th2dmodel_etapt.GetHistogram().Clone()
h_mc4_etapt_den.Sumw2()
h_mc4_etapt_eff.Sumw2()
h_mc4_eta_den=th1dmodel_eta.GetHistogram().Clone()
h_mc4_eta_eff=th1dmodel_eta.GetHistogram().Clone()
h_mc4_eta_den.Sumw2()
h_mc4_eta_eff.Sumw2()
h_mc4_pt_den=th1dmodel_pt.GetHistogram().Clone()
h_mc4_pt_eff=th1dmodel_pt.GetHistogram().Clone()
h_mc4_pt_den.Sumw2()
h_mc4_pt_eff.Sumw2()

h_etapt_sf1=th2dmodel_etapt.GetHistogram().Clone()
h_eta_sf1=th1dmodel_eta.GetHistogram().Clone()
h_pt_sf1=th1dmodel_pt.GetHistogram().Clone()

h_etapt_sf2=th2dmodel_etapt.GetHistogram().Clone()
h_eta_sf2=th1dmodel_eta.GetHistogram().Clone()
h_pt_sf2=th1dmodel_pt.GetHistogram().Clone()

h_etapt_sf3=th2dmodel_etapt.GetHistogram().Clone()
h_eta_sf3=th1dmodel_eta.GetHistogram().Clone()
h_pt_sf3=th1dmodel_pt.GetHistogram().Clone()

h_etapt_sf4=th2dmodel_etapt.GetHistogram().Clone()
h_eta_sf4=th1dmodel_eta.GetHistogram().Clone()
h_pt_sf4=th1dmodel_pt.GetHistogram().Clone()

h_etapt_sf5=th2dmodel_etapt.GetHistogram().Clone()
h_eta_sf5=th1dmodel_eta.GetHistogram().Clone()
h_pt_sf5=th1dmodel_pt.GetHistogram().Clone()

h_mc1_etapt_den.Add(h_mc1_pass_etapt)
h_mc1_etapt_den.Add(h_mc1_fail_etapt)
h_mc1_etapt_eff.Add(h_mc1_pass_etapt)
h_mc1_etapt_eff.Divide(h_mc1_etapt_den)
h_mc1_pass_etapt.GetYaxis().SetTitle("p_{T} (GeV)")
h_mc1_pass_etapt.GetXaxis().SetTitle("\eta")
h_mc1_etapt_den.GetYaxis().SetTitle("p_{T} (GeV)")
h_mc1_etapt_den.GetXaxis().SetTitle("\eta")
teff_mc1_etapt=ROOT.TEfficiency(h_mc1_pass_etapt,h_mc1_etapt_den)
h_mc1_eta_den.Add(h_mc1_pass_eta)
h_mc1_eta_den.Add(h_mc1_fail_eta)
h_mc1_eta_eff.Add(h_mc1_pass_eta)
h_mc1_eta_eff.Divide(h_mc1_eta_den)
teff_mc1_eta=ROOT.TEfficiency(h_mc1_pass_eta,h_mc1_eta_den)
h_mc1_pt_den.Add(h_mc1_pass_pt)
h_mc1_pt_den.Add(h_mc1_fail_pt)
h_mc1_pt_eff.Add(h_mc1_pass_pt)
h_mc1_pt_eff.Divide(h_mc1_pt_den)
teff_mc1_pt=ROOT.TEfficiency(h_mc1_pass_pt,h_mc1_pt_den)

h_mc2_etapt_den.Add(h_mc2_pass_etapt)
h_mc2_etapt_den.Add(h_mc2_fail_etapt)
h_mc2_etapt_eff.Add(h_mc2_pass_etapt)
h_mc2_etapt_eff.Divide(h_mc2_etapt_den)
h_mc2_pass_etapt.GetYaxis().SetTitle("p_{T} (GeV)")
h_mc2_pass_etapt.GetXaxis().SetTitle("\eta")
h_mc2_etapt_den.GetYaxis().SetTitle("p_{T} (GeV)")
h_mc2_etapt_den.GetXaxis().SetTitle("\eta")
teff_mc2_etapt=ROOT.TEfficiency(h_mc2_pass_etapt,h_mc2_etapt_den)
h_mc2_eta_den.Add(h_mc2_pass_eta)
h_mc2_eta_den.Add(h_mc2_fail_eta)
h_mc2_eta_eff.Add(h_mc2_pass_eta)
h_mc2_eta_eff.Divide(h_mc2_eta_den)
teff_mc2_eta=ROOT.TEfficiency(h_mc2_pass_eta,h_mc2_eta_den)
h_mc2_pt_den.Add(h_mc2_pass_pt)
h_mc2_pt_den.Add(h_mc2_fail_pt)
h_mc2_pt_eff.Add(h_mc2_pass_pt)
h_mc2_pt_eff.Divide(h_mc2_pt_den)
teff_mc2_pt=ROOT.TEfficiency(h_mc2_pass_pt,h_mc2_pt_den)

h_mc3_etapt_den.Add(h_mc3_pass_etapt)
h_mc3_etapt_den.Add(h_mc3_fail_etapt)
h_mc3_etapt_eff.Add(h_mc3_pass_etapt)
h_mc3_etapt_eff.Divide(h_mc3_etapt_den)
h_mc3_pass_etapt.GetYaxis().SetTitle("p_{T} (GeV)")
h_mc3_pass_etapt.GetXaxis().SetTitle("\eta")
h_mc3_etapt_den.GetYaxis().SetTitle("p_{T} (GeV)")
h_mc3_etapt_den.GetXaxis().SetTitle("\eta")
teff_mc3_etapt=ROOT.TEfficiency(h_mc3_pass_etapt,h_mc3_etapt_den)
h_mc3_eta_den.Add(h_mc3_pass_eta)
h_mc3_eta_den.Add(h_mc3_fail_eta)
h_mc3_eta_eff.Add(h_mc3_pass_eta)
h_mc3_eta_eff.Divide(h_mc3_eta_den)
teff_mc3_eta=ROOT.TEfficiency(h_mc3_pass_eta,h_mc3_eta_den)
h_mc3_pt_den.Add(h_mc3_pass_pt)
h_mc3_pt_den.Add(h_mc3_fail_pt)
h_mc3_pt_eff.Add(h_mc3_pass_pt)
h_mc3_pt_eff.Divide(h_mc3_pt_den)
teff_mc3_pt=ROOT.TEfficiency(h_mc3_pass_pt,h_mc3_pt_den)

h_mc4_etapt_den.Add(h_mc4_pass_etapt)
h_mc4_etapt_den.Add(h_mc4_fail_etapt)
h_mc4_etapt_eff.Add(h_mc4_pass_etapt)
h_mc4_etapt_eff.Divide(h_mc4_etapt_den)
h_mc4_pass_etapt.GetYaxis().SetTitle("p_{T} (GeV)")
h_mc4_pass_etapt.GetXaxis().SetTitle("\eta")
h_mc4_etapt_den.GetYaxis().SetTitle("p_{T} (GeV)")
h_mc4_etapt_den.GetXaxis().SetTitle("\eta")
teff_mc4_etapt=ROOT.TEfficiency(h_mc4_pass_etapt,h_mc4_etapt_den)
h_mc4_eta_den.Add(h_mc4_pass_eta)
h_mc4_eta_den.Add(h_mc4_fail_eta)
h_mc4_eta_eff.Add(h_mc4_pass_eta)
h_mc4_eta_eff.Divide(h_mc4_eta_den)
teff_mc4_eta=ROOT.TEfficiency(h_mc4_pass_eta,h_mc4_eta_den)
h_mc4_pt_den.Add(h_mc4_pass_pt)
h_mc4_pt_den.Add(h_mc4_fail_pt)
h_mc4_pt_eff.Add(h_mc4_pass_pt)
h_mc4_pt_eff.Divide(h_mc4_pt_den)
teff_mc4_pt=ROOT.TEfficiency(h_mc4_pass_pt,h_mc4_pt_den)

rinterface_data1=rdf_data1.Filter("((lepton1_passHLT && (event % 2 == 0)) || (lepton2_passHLT && (event % 2 == 1))) && abs(lepton1_pdgid) == 11 && mll < 120 && mll > 60")
rinterface_data2=rdf_data2.Filter("((lepton1_passHLT && (event % 2 == 0)) || (lepton2_passHLT && (event % 2 == 1))) && abs(lepton1_pdgid) == 11 && mll < 96.18 && mll > 86.18")
rinterface_data3=rdf_data3.Filter("((lepton1_passHLT && (event % 2 == 0)) || (lepton2_passHLT && (event % 2 == 1))) && abs(lepton1_pdgid) == 11 && ((mll > 60 && mll < 86.18) || (mll > 96.18 && mll < 120))")


rinterface_data1=rinterface_data1.Define("probe_passHLT","if (event % 2 == 0) return lepton2_passHLT; else return lepton1_passHLT;")
rinterface_data1=rinterface_data1.Define("probe_eta","if (event % 2 == 0) return lepton2_eta; else return lepton1_eta;")
rinterface_data1=rinterface_data1.Define("probe_pt","if (event % 2 == 0) return lepton2_pt; else return lepton1_pt;")

rinterface_data2=rinterface_data2.Define("probe_passHLT","if (event % 2 == 0) return lepton2_passHLT; else return lepton1_passHLT;")
rinterface_data2=rinterface_data2.Define("probe_eta","if (event % 2 == 0) return lepton2_eta; else return lepton1_eta;")
rinterface_data2=rinterface_data2.Define("probe_pt","if (event % 2 == 0) return lepton2_pt; else return lepton1_pt;")

rinterface_data3=rinterface_data3.Define("probe_passHLT","if (event % 2 == 0) return lepton2_passHLT; else return lepton1_passHLT;")
rinterface_data3=rinterface_data3.Define("probe_eta","if (event % 2 == 0) return lepton2_eta; else return lepton1_eta;")
rinterface_data3=rinterface_data3.Define("probe_pt","if (event % 2 == 0) return lepton2_pt; else return lepton1_pt;")

rinterface_data1_pass=rinterface_data1.Filter("probe_passHLT")
rinterface_data1_fail=rinterface_data1.Filter("!probe_passHLT")

rinterface_data2_pass=rinterface_data2.Filter("probe_passHLT")
rinterface_data2_fail=rinterface_data2.Filter("!probe_passHLT")

rinterface_data3_pass=rinterface_data3.Filter("probe_passHLT")
rinterface_data3_fail=rinterface_data3.Filter("!probe_passHLT")

rresultptr_data1_pass_etapt=rinterface_data1_pass.Histo2D(th2dmodel_etapt,"probe_eta","probe_pt")
rresultptr_data1_fail_etapt=rinterface_data1_fail.Histo2D(th2dmodel_etapt,"probe_eta","probe_pt")
rresultptr_data1_pass_eta=rinterface_data1_pass.Histo1D(th1dmodel_eta,"probe_eta")
rresultptr_data1_fail_eta=rinterface_data1_fail.Histo1D(th1dmodel_eta,"probe_eta")
rresultptr_data1_pass_pt=rinterface_data1_pass.Histo1D(th1dmodel_pt,"probe_pt")
rresultptr_data1_fail_pt=rinterface_data1_fail.Histo1D(th1dmodel_pt,"probe_pt")

rresultptr_data1_pass_etapt.Sumw2()
rresultptr_data1_fail_etapt.Sumw2()
rresultptr_data1_pass_eta.Sumw2()
rresultptr_data1_fail_eta.Sumw2()
rresultptr_data1_pass_pt.Sumw2()
rresultptr_data1_fail_pt.Sumw2()

rresultptr_data2_pass_etapt=rinterface_data2_pass.Histo2D(th2dmodel_etapt,"probe_eta","probe_pt")
rresultptr_data2_fail_etapt=rinterface_data2_fail.Histo2D(th2dmodel_etapt,"probe_eta","probe_pt")
rresultptr_data2_pass_eta=rinterface_data2_pass.Histo1D(th1dmodel_eta,"probe_eta")
rresultptr_data2_fail_eta=rinterface_data2_fail.Histo1D(th1dmodel_eta,"probe_eta")
rresultptr_data2_pass_pt=rinterface_data2_pass.Histo1D(th1dmodel_pt,"probe_pt")
rresultptr_data2_fail_pt=rinterface_data2_fail.Histo1D(th1dmodel_pt,"probe_pt")

rresultptr_data2_pass_etapt.Sumw2()
rresultptr_data2_fail_etapt.Sumw2()
rresultptr_data2_pass_eta.Sumw2()
rresultptr_data2_fail_eta.Sumw2()
rresultptr_data2_pass_pt.Sumw2()
rresultptr_data2_fail_pt.Sumw2()

rresultptr_data3_pass_etapt=rinterface_data3_pass.Histo2D(th2dmodel_etapt,"probe_eta","probe_pt")
rresultptr_data3_fail_etapt=rinterface_data3_fail.Histo2D(th2dmodel_etapt,"probe_eta","probe_pt")
rresultptr_data3_pass_eta=rinterface_data3_pass.Histo1D(th1dmodel_eta,"probe_eta")
rresultptr_data3_fail_eta=rinterface_data3_fail.Histo1D(th1dmodel_eta,"probe_eta")
rresultptr_data3_pass_pt=rinterface_data3_pass.Histo1D(th1dmodel_pt,"probe_pt")
rresultptr_data3_fail_pt=rinterface_data3_fail.Histo1D(th1dmodel_pt,"probe_pt")

rresultptr_data3_pass_etapt.Sumw2()
rresultptr_data3_fail_etapt.Sumw2()
rresultptr_data3_pass_eta.Sumw2()
rresultptr_data3_fail_eta.Sumw2()
rresultptr_data3_pass_pt.Sumw2()
rresultptr_data3_fail_pt.Sumw2()

h_data1_pass_etapt=rresultptr_data1_pass_etapt.GetValue()
h_data1_fail_etapt=rresultptr_data1_fail_etapt.GetValue()
h_data1_pass_eta=rresultptr_data1_pass_eta.GetValue()
h_data1_fail_eta=rresultptr_data1_fail_eta.GetValue()
h_data1_pass_pt=rresultptr_data1_pass_pt.GetValue()
h_data1_fail_pt=rresultptr_data1_fail_pt.GetValue()

h_data2_pass_etapt=rresultptr_data2_pass_etapt.GetValue()
h_data2_fail_etapt=rresultptr_data2_fail_etapt.GetValue()
h_data2_pass_eta=rresultptr_data2_pass_eta.GetValue()
h_data2_fail_eta=rresultptr_data2_fail_eta.GetValue()
h_data2_pass_pt=rresultptr_data2_pass_pt.GetValue()
h_data2_fail_pt=rresultptr_data2_fail_pt.GetValue()

h_data3_pass_etapt=rresultptr_data3_pass_etapt.GetValue()
h_data3_fail_etapt=rresultptr_data3_fail_etapt.GetValue()
h_data3_pass_eta=rresultptr_data3_pass_eta.GetValue()
h_data3_fail_eta=rresultptr_data3_fail_eta.GetValue()
h_data3_pass_pt=rresultptr_data3_pass_pt.GetValue()
h_data3_fail_pt=rresultptr_data3_fail_pt.GetValue()

h_data1_etapt_den=th2dmodel_etapt.GetHistogram().Clone()
h_data1_etapt_eff=th2dmodel_etapt.GetHistogram().Clone()
h_data1_etapt_den.Sumw2()
h_data1_etapt_eff.Sumw2()
h_data1_eta_den=th1dmodel_eta.GetHistogram().Clone()
h_data1_eta_eff=th1dmodel_eta.GetHistogram().Clone()
h_data1_eta_den.Sumw2()
h_data1_eta_eff.Sumw2()
h_data1_pt_den=th1dmodel_pt.GetHistogram().Clone()
h_data1_pt_eff=th1dmodel_pt.GetHistogram().Clone()
h_data1_pt_den.Sumw2()
h_data1_pt_eff.Sumw2()

h_data2_etapt_den=th2dmodel_etapt.GetHistogram().Clone()
h_data2_etapt_eff=th2dmodel_etapt.GetHistogram().Clone()
h_data2_etapt_den.Sumw2()
h_data2_etapt_eff.Sumw2()
h_data2_eta_den=th1dmodel_eta.GetHistogram().Clone()
h_data2_eta_eff=th1dmodel_eta.GetHistogram().Clone()
h_data2_eta_den.Sumw2()
h_data2_eta_eff.Sumw2()
h_data2_pt_den=th1dmodel_pt.GetHistogram().Clone()
h_data2_pt_eff=th1dmodel_pt.GetHistogram().Clone()
h_data2_pt_den.Sumw2()
h_data2_pt_eff.Sumw2()

h_data3_etapt_den=th2dmodel_etapt.GetHistogram().Clone()
h_data3_etapt_eff=th2dmodel_etapt.GetHistogram().Clone()
h_data3_etapt_den.Sumw2()
h_data3_etapt_eff.Sumw2()
h_data3_eta_den=th1dmodel_eta.GetHistogram().Clone()
h_data3_eta_eff=th1dmodel_eta.GetHistogram().Clone()
h_data3_eta_den.Sumw2()
h_data3_eta_eff.Sumw2()
h_data3_pt_den=th1dmodel_pt.GetHistogram().Clone()
h_data3_pt_eff=th1dmodel_pt.GetHistogram().Clone()
h_data3_pt_den.Sumw2()
h_data3_pt_eff.Sumw2()

h_data1_etapt_den.Add(h_data1_pass_etapt)
h_data1_etapt_den.Add(h_data1_fail_etapt)
h_data1_etapt_eff.Add(h_data1_pass_etapt)
h_data1_etapt_eff.Divide(h_data1_etapt_den)
h_data1_pass_etapt.GetYaxis().SetTitle("p_{T} (GeV)")
h_data1_pass_etapt.GetXaxis().SetTitle("\eta")
h_data1_etapt_den.GetYaxis().SetTitle("p_{T} (GeV)")
h_data1_etapt_den.GetXaxis().SetTitle("\eta")
teff_data1_etapt=ROOT.TEfficiency(h_data1_pass_etapt,h_data1_etapt_den)
h_data1_eta_den.Add(h_data1_pass_eta)
h_data1_eta_den.Add(h_data1_fail_eta)
h_data1_eta_eff.Add(h_data1_pass_eta)
h_data1_eta_eff.Divide(h_data1_eta_den)
teff_data1_eta=ROOT.TEfficiency(h_data1_pass_eta,h_data1_eta_den)
h_data1_pt_den.Add(h_data1_pass_pt)
h_data1_pt_den.Add(h_data1_fail_pt)
h_data1_pt_eff.Add(h_data1_pass_pt)
h_data1_pt_eff.Divide(h_data1_pt_den)
teff_data1_pt=ROOT.TEfficiency(h_data1_pass_pt,h_data1_pt_den)

h_data2_etapt_den.Add(h_data2_pass_etapt)
h_data2_etapt_den.Add(h_data2_fail_etapt)
h_data2_etapt_eff.Add(h_data2_pass_etapt)
h_data2_etapt_eff.Divide(h_data2_etapt_den)
h_data2_pass_etapt.GetYaxis().SetTitle("p_{T} (GeV)")
h_data2_pass_etapt.GetXaxis().SetTitle("\eta")
h_data2_etapt_den.GetYaxis().SetTitle("p_{T} (GeV)")
h_data2_etapt_den.GetXaxis().SetTitle("\eta")
teff_data2_etapt=ROOT.TEfficiency(h_data2_pass_etapt,h_data2_etapt_den)
h_data2_eta_den.Add(h_data2_pass_eta)
h_data2_eta_den.Add(h_data2_fail_eta)
h_data2_eta_eff.Add(h_data2_pass_eta)
h_data2_eta_eff.Divide(h_data2_eta_den)
teff_data2_eta=ROOT.TEfficiency(h_data2_pass_eta,h_data2_eta_den)
h_data2_pt_den.Add(h_data2_pass_pt)
h_data2_pt_den.Add(h_data2_fail_pt)
h_data2_pt_eff.Add(h_data2_pass_pt)
h_data2_pt_eff.Divide(h_data2_pt_den)
teff_data2_pt=ROOT.TEfficiency(h_data2_pass_pt,h_data2_pt_den)

h_data3_etapt_den.Add(h_data3_pass_etapt)
h_data3_etapt_den.Add(h_data3_fail_etapt)
h_data3_etapt_eff.Add(h_data3_pass_etapt)
h_data3_etapt_eff.Divide(h_data3_etapt_den)
h_data3_pass_etapt.GetYaxis().SetTitle("p_{T} (GeV)")
h_data3_pass_etapt.GetXaxis().SetTitle("\eta")
h_data3_etapt_den.GetYaxis().SetTitle("p_{T} (GeV)")
h_data3_etapt_den.GetXaxis().SetTitle("\eta")
teff_data3_etapt=ROOT.TEfficiency(h_data3_pass_etapt,h_data3_etapt_den)
h_data3_eta_den.Add(h_data3_pass_eta)
h_data3_eta_den.Add(h_data3_fail_eta)
h_data3_eta_eff.Add(h_data3_pass_eta)
h_data3_eta_eff.Divide(h_data3_eta_den)
teff_data3_eta=ROOT.TEfficiency(h_data3_pass_eta,h_data3_eta_den)
h_data3_pt_den.Add(h_data3_pass_pt)
h_data3_pt_den.Add(h_data3_fail_pt)
h_data3_pt_eff.Add(h_data3_pass_pt)
h_data3_pt_eff.Divide(h_data3_pt_den)
teff_data3_pt=ROOT.TEfficiency(h_data3_pass_pt,h_data3_pt_den)

c1 = ROOT.TCanvas("c1","c1")

#h_data_pass.SetStats(0)
#h_data_pass.Draw("colz")
#h_data_eta_eff.SetStats(0)
#h_data_eta_eff.Draw()
teff_data1_eta.SetTitle("HLT Efficiencies;\eta")
teff_data1_eta.Draw()

c1.SaveAs(args.plotdir+"/eff_data1_"+args.year+"_eta.png")

c2 = ROOT.TCanvas("c2","c2")

#h_data_pass.SetStats(0)
#h_data_pass.Draw("colz")
#h_data_pt_eff.SetStats(0)
#h_data_pt_eff.Draw()
teff_data1_pt.SetTitle("HLT Efficiencies;p_{T} (GeV)")
teff_data1_pt.Draw()

c2.SaveAs(args.plotdir+"/eff_data1_"+args.year+"_pt.png")

c3 = ROOT.TCanvas("c3","c3")

#h_data_pass.SetStats(0)
#h_data_pass.Draw("colz")
#h_data_etapt_eff.SetStats(0)
#h_data_etapt_eff.Draw("zcol")

teff_data1_etapt.SetTitle("HLT Efficiencies in Data")
teff_data1_etapt.Draw("zcol")

c3.SaveAs(args.plotdir+"/eff_data1_"+args.year+"_etapt.png")

c4 = ROOT.TCanvas("c4","c4")

#h_data_pass.SetStats(0)
#h_data_pass.Draw("colz")
#h_data_eta_eff.SetStats(0)
#h_data_eta_eff.Draw()
teff_data2_eta.Draw()

c4.SaveAs(args.plotdir+"/eff_data2_"+args.year+"_eta.png")

c5 = ROOT.TCanvas("c5","c5")

#h_data_pass.SetStats(0)
#h_data_pass.Draw("colz")
#h_data_pt_eff.SetStats(0)
#h_data_pt_eff.Draw()

teff_data2_pt.Draw()

c5.SaveAs(args.plotdir+"/eff_data2_"+args.year+"_pt.png")

c6 = ROOT.TCanvas("c6","c6")

#h_data_pass.SetStats(0)
#h_data_pass.Draw("colz")
#h_data_etapt_eff.SetStats(0)
#h_data_etapt_eff.Draw("zcol")

teff_data2_etapt.SetTitle("HLT Efficiencies in Data")
teff_data2_etapt.Draw("zcol")

c6.SaveAs(args.plotdir+"/eff_data2_"+args.year+"_etapt.png")

c7 = ROOT.TCanvas("c7","c7")

#h_data_pass.SetStats(0)
#h_data_pass.Draw("colz")
#h_data_eta_eff.SetStats(0)
#h_data_eta_eff.Draw()
teff_data3_eta.Draw()

c7.SaveAs(args.plotdir+"/eff_data3_"+args.year+"_eta.png")

c8 = ROOT.TCanvas("c8","c8")

#h_data_pass.SetStats(0)
#h_data_pass.Draw("colz")
#h_data_pt_eff.SetStats(0)
#h_data_pt_eff.Draw()

teff_data3_pt.Draw()

c8.SaveAs(args.plotdir+"/eff_data3_"+args.year+"_pt.png")

c9 = ROOT.TCanvas("c9","c9")

#h_data_pass.SetStats(0)
#h_data_pass.Draw("colz")
#h_data_etapt_eff.SetStats(0)
#h_data_etapt_eff.Draw("zcol")

teff_data3_etapt.SetTitle("HLT Efficiencies in Data")
teff_data3_etapt.Draw("zcol")

c9.SaveAs(args.plotdir+"/eff_data3_"+args.year+"_etapt.png")

c10 = ROOT.TCanvas("c10","c10")

#h_mc_pass.SetStats(0)
#h_mc_pass.Draw("colz")
#h_mc_eta_eff.SetStats(0)
#h_mc_eta_eff.Draw()
teff_mc1_eta.SetTitle("HLT Efficiencies;\eta")
teff_mc1_eta.Draw()

c10.SaveAs(args.plotdir+"/eff_mc1_"+args.year+"_eta.png")

c11 = ROOT.TCanvas("c11","c11")

#h_mc_pass.SetStats(0)
#h_mc_pass.Draw("colz")
#h_mc_pt_eff.SetStats(0)
#h_mc_pt_eff.Draw()
teff_mc1_pt.SetTitle("HLT Efficiencies;p_{T} (GeV)")
teff_mc1_pt.Draw()

c11.SaveAs(args.plotdir+"/eff_mc1_"+args.year+"_pt.png")

c12 = ROOT.TCanvas("c12","c12")

#h_mc_pass.SetStats(0)
#h_mc_pass.Draw("colz")
#h_mc_etapt_eff.SetStats(0)
#h_mc_etapt_eff.Draw("zcol")

teff_mc1_etapt.SetTitle("HLT Efficiencies in MC")
teff_mc1_etapt.Draw("colz")

c12.SaveAs(args.plotdir+"/eff_mc1_"+args.year+"_etapt.png")

c13 = ROOT.TCanvas("c13","c13")

#h_mc_pass.SetStats(0)
#h_mc_pass.Draw("colz")
#h_mc_eta_eff.SetStats(0)
#h_mc_eta_eff.Draw()

teff_mc2_eta.Draw()

c13 .SaveAs(args.plotdir+"/eff_mc2_"+args.year+"_eta.png")

c14 = ROOT.TCanvas("c14","c14")

#h_mc_pass.SetStats(0)
#h_mc_pass.Draw("colz")
#h_mc_pt_eff.SetStats(0)
#h_mc_pt_eff.Draw()

teff_mc2_pt.Draw()

c14.SaveAs(args.plotdir+"/eff_mc2_"+args.year+"_pt.png")

c15 = ROOT.TCanvas("c15","c15")

#h_mc_pass.SetStats(0)
#h_mc_pass.Draw("colz")
#h_mc_etapt_eff.SetStats(0)
#h_mc_etapt_eff.Draw("zcol")

teff_mc2_etapt.SetTitle("HLT Efficiencies in MC")
teff_mc2_etapt.Draw("colz")

c15.SaveAs(args.plotdir+"/eff_mc2_"+args.year+"_etapt.png")

c16 = ROOT.TCanvas("c16","c16")

#h_mc_pass.SetStats(0)
#h_mc_pass.Draw("colz")
#h_mc_eta_eff.SetStats(0)
#h_mc_eta_eff.Draw()

teff_mc3_eta.Draw()

c16 .SaveAs(args.plotdir+"/eff_mc3_"+args.year+"_eta.png")

c17 = ROOT.TCanvas("c17","c17")

#h_mc_pass.SetStats(0)
#h_mc_pass.Draw("colz")
#h_mc_pt_eff.SetStats(0)
#h_mc_pt_eff.Draw()

teff_mc3_pt.Draw()

c17.SaveAs(args.plotdir+"/eff_mc3_"+args.year+"_pt.png")

c18 = ROOT.TCanvas("c18","c18")

#h_mc_pass.SetStats(0)
#h_mc_pass.Draw("colz")
#h_mc_etapt_eff.SetStats(0)
#h_mc_etapt_eff.Draw("zcol")

teff_mc3_etapt.SetTitle("HLT Efficiencies in MC")
teff_mc3_etapt.Draw("colz")

c18.SaveAs(args.plotdir+"/eff_mc3_"+args.year+"_etapt.png")

c19 = ROOT.TCanvas("c19","c19")

#h_mc_pass.SetStats(0)
#h_mc_pass.Draw("colz")
#h_mc_eta_eff.SetStats(0)
#h_mc_eta_eff.Draw()

teff_mc4_eta.Draw()

c19 .SaveAs(args.plotdir+"/eff_mc4_"+args.year+"_eta.png")

c20 = ROOT.TCanvas("c20","c20")

#h_mc_pass.SetStats(0)
#h_mc_pass.Draw("colz")
#h_mc_pt_eff.SetStats(0)
#h_mc_pt_eff.Draw()

teff_mc4_pt.Draw()

c20.SaveAs(args.plotdir+"/eff_mc4_"+args.year+"_pt.png")

c21 = ROOT.TCanvas("c21","c21")

#h_mc_pass.SetStats(0)
#h_mc_pass.Draw("colz")
#h_mc_etapt_eff.SetStats(0)
#h_mc_etapt_eff.Draw("zcol")

teff_mc4_etapt.SetTitle("HLT Efficiencies in MC")
teff_mc4_etapt.Draw("colz")

c21.SaveAs(args.plotdir+"/eff_mc4_"+args.year+"_etapt.png")

for i in range(h_mc1_pass_etapt.GetNbinsX()+2):
    for j in range(h_mc1_pass_etapt.GetNbinsY()+2):
        h_mc1_etapt_eff.SetBinContent(i,j,teff_mc1_etapt.GetEfficiency(teff_mc1_etapt.GetGlobalBin(i,j)))
        h_mc1_etapt_eff.SetBinError(i,j,max(teff_mc1_etapt.GetEfficiencyErrorLow(teff_mc1_etapt.GetGlobalBin(i,j)),teff_mc1_etapt.GetEfficiencyErrorUp(teff_mc1_etapt.GetGlobalBin(i,j))))
    for j in range(h_data1_pass_etapt.GetNbinsY()+2):
        h_data1_etapt_eff.SetBinContent(i,j,teff_data1_etapt.GetEfficiency(teff_data1_etapt.GetGlobalBin(i,j)))
        h_data1_etapt_eff.SetBinError(i,j,max(teff_data1_etapt.GetEfficiencyErrorLow(teff_data1_etapt.GetGlobalBin(i,j)),teff_data1_etapt.GetEfficiencyErrorUp(teff_data1_etapt.GetGlobalBin(i,j))))

h_etapt_sf1.Add(h_data1_etapt_eff)

h_etapt_sf1.Divide(h_mc1_etapt_eff)

c22 = ROOT.TCanvas("c22","c22")

#gStyle.SetPaintTextFormat("4.2f")

h_etapt_sf1.SetTitle("HLT Efficiency Scale Factors")
h_etapt_sf1.SetStats(0)
h_etapt_sf1.GetYaxis().SetTitle("p_{T} (GeV)")
h_etapt_sf1.GetXaxis().SetTitle("\eta")

h_etapt_sf1.Draw("colz")

c22.SaveAs(args.plotdir+"/sf1_"+args.year+"_etapt.png")

for i in range(h_mc1_pass_eta.GetNbinsX()+2):
    for j in range(h_mc1_pass_etapt.GetNbinsY()+2):
        h_mc1_eta_eff.SetBinContent(i,j,teff_mc1_eta.GetEfficiency(teff_mc1_eta.GetGlobalBin(i)))
        h_mc1_eta_eff.SetBinError(i,j,max(teff_mc1_eta.GetEfficiencyErrorLow(teff_mc1_eta.GetGlobalBin(i)),teff_mc1_eta.GetEfficiencyErrorUp(teff_mc1_eta.GetGlobalBin(i))))
    for j in range(h_data1_pass_eta.GetNbinsY()+2):
        h_data1_eta_eff.SetBinContent(i,j,teff_data1_eta.GetEfficiency(teff_data1_eta.GetGlobalBin(i)))
        h_data1_eta_eff.SetBinError(i,j,max(teff_data1_eta.GetEfficiencyErrorLow(teff_data1_eta.GetGlobalBin(i)),teff_data1_eta.GetEfficiencyErrorUp(teff_data1_eta.GetGlobalBin(i))))

h_eta_sf1.Add(h_data1_eta_eff)

h_eta_sf1.Divide(h_mc1_eta_eff)

c23 = ROOT.TCanvas("c23","c23")

#gStyle.SetPaintTextFormat("4.2f")

h_eta_sf1.SetTitle("HLT Efficiency Scale Factors")
h_eta_sf1.SetStats(0)
h_eta_sf1.GetXaxis().SetTitle("\eta")

h_eta_sf1.Draw()

c23.SaveAs(args.plotdir+"/sf1_"+args.year+"_eta.png")

for i in range(h_mc1_pass_pt.GetNbinsX()+2):
        h_mc1_pt_eff.SetBinContent(i,teff_mc1_pt.GetEfficiency(teff_mc1_pt.GetGlobalBin(i)))
        h_mc1_pt_eff.SetBinError(i,max(teff_mc1_pt.GetEfficiencyErrorLow(teff_mc1_pt.GetGlobalBin(i)),teff_mc1_pt.GetEfficiencyErrorUp(teff_mc1_pt.GetGlobalBin(i))))
        h_data1_pt_eff.SetBinContent(i,teff_data1_pt.GetEfficiency(teff_data1_pt.GetGlobalBin(i)))
        h_data1_pt_eff.SetBinError(i,max(teff_data1_pt.GetEfficiencyErrorLow(teff_data1_pt.GetGlobalBin(i)),teff_data1_pt.GetEfficiencyErrorUp(teff_data1_pt.GetGlobalBin(i))))

h_pt_sf1.Add(h_data1_pt_eff)

h_pt_sf1.Divide(h_mc1_pt_eff)

c24 = ROOT.TCanvas("c24","c24")

#gStyle.SetPaintTextFormat("4.2f")

h_pt_sf1.SetTitle("HLT Efficiency Scale Factors")
h_pt_sf1.SetStats(0)
h_pt_sf1.GetXaxis().SetTitle("p_{T} (GeV)")

h_pt_sf1.Draw()

c24.SaveAs(args.plotdir+"/sf1_"+args.year+"_pt.png")

for i in range(h_mc2_pass_etapt.GetNbinsX()+2):
    for j in range(h_mc2_pass_etapt.GetNbinsY()+2):
        h_mc2_etapt_eff.SetBinContent(i,j,teff_mc2_etapt.GetEfficiency(teff_mc2_etapt.GetGlobalBin(i,j)))
        h_mc2_etapt_eff.SetBinError(i,j,max(teff_mc2_etapt.GetEfficiencyErrorLow(teff_mc2_etapt.GetGlobalBin(i,j)),teff_mc2_etapt.GetEfficiencyErrorUp(teff_mc2_etapt.GetGlobalBin(i,j))))
    for j in range(h_data1_pass_etapt.GetNbinsY()+2):
        h_data1_etapt_eff.SetBinContent(i,j,teff_data1_etapt.GetEfficiency(teff_data1_etapt.GetGlobalBin(i,j)))
        h_data1_etapt_eff.SetBinError(i,j,max(teff_data1_etapt.GetEfficiencyErrorLow(teff_data1_etapt.GetGlobalBin(i,j)),teff_data1_etapt.GetEfficiencyErrorUp(teff_data1_etapt.GetGlobalBin(i,j))))

h_etapt_sf2.Add(h_data1_etapt_eff)

h_etapt_sf2.Divide(h_mc2_etapt_eff)

c25 = ROOT.TCanvas("c25","c25")

#gStyle.SetPaintTextFormat("4.2f")

h_etapt_sf2.SetTitle("HLT Efficiency Scale Factors")
h_etapt_sf2.SetStats(0)
h_etapt_sf2.GetYaxis().SetTitle("p_{T} (GeV)")
h_etapt_sf2.GetXaxis().SetTitle("\eta")

h_etapt_sf2.Draw("colz")

c25.SaveAs(args.plotdir+"/sf2_"+args.year+"_etapt.png")

for i in range(h_mc2_pass_etapt.GetNbinsX()+2):
    for j in range(h_mc2_pass_etapt.GetNbinsY()+2):
        h_mc2_etapt_eff.SetBinContent(i,j,teff_mc2_etapt.GetEfficiency(teff_mc2_etapt.GetGlobalBin(i,j)))
        h_mc2_etapt_eff.SetBinError(i,j,max(teff_mc2_etapt.GetEfficiencyErrorLow(teff_mc2_etapt.GetGlobalBin(i,j)),teff_mc2_etapt.GetEfficiencyErrorUp(teff_mc2_etapt.GetGlobalBin(i,j))))
    for j in range(h_data1_pass_etapt.GetNbinsY()+2):
        h_data1_etapt_eff.SetBinContent(i,j,teff_data1_etapt.GetEfficiency(teff_data1_etapt.GetGlobalBin(i,j)))
        h_data1_etapt_eff.SetBinError(i,j,max(teff_data1_etapt.GetEfficiencyErrorLow(teff_data1_etapt.GetGlobalBin(i,j)),teff_data1_etapt.GetEfficiencyErrorUp(teff_data1_etapt.GetGlobalBin(i,j))))

h_etapt_sf2.Add(h_data1_etapt_eff)

h_etapt_sf2.Divide(h_mc2_etapt_eff)

c26 = ROOT.TCanvas("c26","c26")

#gStyle.SetPaintTextFormat("4.2f")

h_etapt_sf3.SetTitle("HLT Efficiency Scale Factors")
h_etapt_sf3.SetStats(0)
h_etapt_sf3.GetYaxis().SetTitle("p_{T} (GeV)")
h_etapt_sf3.GetXaxis().SetTitle("\eta")

h_etapt_sf3.Draw("colz")

c26.SaveAs(args.plotdir+"/sf3_"+args.year+"_etapt.png")
  
for i in range(h_mc4_pass_etapt.GetNbinsX()+2):
    for j in range(h_mc4_pass_etapt.GetNbinsY()+2):
        h_mc4_etapt_eff.SetBinContent(i,j,teff_mc4_etapt.GetEfficiency(teff_mc4_etapt.GetGlobalBin(i,j)))
        h_mc4_etapt_eff.SetBinError(i,j,max(teff_mc4_etapt.GetEfficiencyErrorLow(teff_mc4_etapt.GetGlobalBin(i,j)),teff_mc4_etapt.GetEfficiencyErrorUp(teff_mc4_etapt.GetGlobalBin(i,j))))
    for j in range(h_data3_pass_etapt.GetNbinsY()+2):
        h_data3_etapt_eff.SetBinContent(i,j,teff_data3_etapt.GetEfficiency(teff_data3_etapt.GetGlobalBin(i,j)))
        h_data3_etapt_eff.SetBinError(i,j,max(teff_data3_etapt.GetEfficiencyErrorLow(teff_data3_etapt.GetGlobalBin(i,j)),teff_data3_etapt.GetEfficiencyErrorUp(teff_data3_etapt.GetGlobalBin(i,j))))

h_etapt_sf4.Add(h_data3_etapt_eff)

h_etapt_sf4.Divide(h_mc4_etapt_eff)

c27 = ROOT.TCanvas("c27","c27")

#gStyle.SetPaintTextFormat("4.2f")

h_etapt_sf4.SetTitle("HLT Efficiency Scale Factors")
h_etapt_sf4.SetStats(0)
h_etapt_sf4.GetYaxis().SetTitle("p_{T} (GeV)")
h_etapt_sf4.GetXaxis().SetTitle("\eta")

h_etapt_sf4.Draw("colz")

c27.SaveAs(args.plotdir+"/sf4_"+args.year+"_etapt.png")

from math import sqrt

for i in range(h_etapt_sf5.GetNbinsX()+2):
    for j in range(h_etapt_sf5.GetNbinsY()+2):
        h_etapt_sf5.SetBinContent(i,j,sqrt(h_etapt_sf1.GetBinError(i,j)*h_etapt_sf1.GetBinError(i,j)+(h_etapt_sf1.GetBinContent(i,j)-h_etapt_sf2.GetBinContent(i,j))*(h_etapt_sf1.GetBinContent(i,j)-h_etapt_sf2.GetBinContent(i,j))+(h_etapt_sf3.GetBinContent(i,j)-h_etapt_sf4.GetBinContent(i,j))*(h_etapt_sf3.GetBinContent(i,j)-h_etapt_sf4.GetBinContent(i,j))   ))
        h_etapt_sf5.SetBinError(i,j,0)
        h_etapt_sf1.SetBinError(i,j,sqrt(h_etapt_sf1.GetBinError(i,j)*h_etapt_sf1.GetBinError(i,j)+(h_etapt_sf1.GetBinContent(i,j)-h_etapt_sf2.GetBinContent(i,j))*(h_etapt_sf1.GetBinContent(i,j)-h_etapt_sf2.GetBinContent(i,j))+(h_etapt_sf3.GetBinContent(i,j)-h_etapt_sf4.GetBinContent(i,j))*(h_etapt_sf3.GetBinContent(i,j)-h_etapt_sf4.GetBinContent(i,j))   ))
#        h_etapt_sf5.SetBinContent(i,j,sqrt(h_etapt_sf1.GetBinError(i,j)*h_etapt_sf1.GetBinError(i,j)))
#        h_etapt_sf5.SetBinContent(i,j,sqrt((h_etapt_sf1.GetBinContent(i,j)-h_etapt_sf2.GetBinContent(i,j))*(h_etapt_sf1.GetBinContent(i,j)-h_etapt_sf2.GetBinContent(i,j))))
#        h_etapt_sf5.SetBinContent(i,j,sqrt((h_etapt_sf1.GetBinContent(i,j)-h_etapt_sf3.GetBinContent(i,j))*(h_etapt_sf1.GetBinContent(i,j)-h_etapt_sf3.GetBinContent(i,j))))


c27 = ROOT.TCanvas("c27","c27")

#gStyle.SetPaintTextFormat("4.2f")

h_etapt_sf5.SetTitle("HLT Efficiency Scale Factor Errors")
h_etapt_sf5.SetStats(0)
h_etapt_sf5.GetYaxis().SetTitle("p_{T} (GeV)")
h_etapt_sf5.GetXaxis().SetTitle("\eta")

h_etapt_sf5.Draw("colz")

c27.SaveAs(args.plotdir+"/sf5_"+args.year+"_etapt.png")

outfile=ROOT.TFile(args.outfile,"recreate")
outfile.cd()
h_etapt_sf1.Write("hlt_sfs_etapt")
outfile.Close()
