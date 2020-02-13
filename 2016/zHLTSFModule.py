import ROOT

from math import sin, cos, sqrt

ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaPhi

class zHLTSFProducer(Module):
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("run",  "i");
        self.out.branch("lumi",  "i");
        self.out.branch("event",  "l");
        self.out.branch("npu",  "I");
        self.out.branch("lepton1_pdgid",  "I");
        self.out.branch("lepton2_pdgid",  "I");
        self.out.branch("lepton1_pt",  "F");
        self.out.branch("lepton1_passHLT",  "B");
        self.out.branch("lepton1_phi",  "F");
        self.out.branch("lepton1_eta",  "F");
        self.out.branch("lepton1_sceta",  "F");
        self.out.branch("lepton2_pt",  "F");
        self.out.branch("lepton2_phi",  "F");
        self.out.branch("lepton2_eta",  "F");
        self.out.branch("lepton2_sceta",  "F");
        self.out.branch("lepton2_passHLT",  "B");
        self.out.branch("mll",  "F");
        self.out.branch("met",  "F");
        self.out.branch("metphi",  "F");
        self.out.branch("metup",  "F");
        self.out.branch("puppimet",  "F");
        self.out.branch("puppimetphi",  "F");
        self.out.branch("npvs","I")
        self.out.branch("gen_weight",  "F");
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        if not (event.HLT_Ele27_WPTight_Gsf or event.HLT_IsoMu24 or event.HLT_IsoTkMu24):
            return False

        jets = Collection(event, "Jet")
        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")
        trigobjs = Collection(event, "TrigObj")

        tight_muons = []

        loose_but_not_tight_muons = []
        
        tight_electrons = []

        loose_but_not_tight_electrons = []

        for i in range(0,len(muons)):

            if muons[i].pt < 25:
                continue

            if abs(muons[i].eta) > 2.4:
                continue

            if muons[i].tightId and muons[i].pfRelIso04_all < 0.15:
                tight_muons.append(i)

        #for processing speed-up
        if len(tight_muons) + len(loose_but_not_tight_muons) > 2:
            return False

        for i in range (0,len(electrons)):

            if electrons[i].pt < 30:
                continue
            
            if abs(electrons[i].eta + electrons[i].deltaEtaSC) > 2.5:
                continue

            if (abs(electrons[i].eta + electrons[i].deltaEtaSC) < 1.479 and abs(electrons[i].dz) < 0.1 and abs(electrons[i].dxy) < 0.05) or (abs(electrons[i].eta + electrons[i].deltaEtaSC) > 1.479 and abs(electrons[i].dz) < 0.2 and abs(electrons[i].dxy) < 0.1):
                if electrons[i].cutBased >= 3:
                    tight_electrons.append(i)

        if len(tight_muons) +  len(tight_electrons) > 2:
            return False

        if len(tight_muons) == 2 and muons[tight_muons[0]].pdgId != muons[tight_muons[1]].pdgId and (muons[tight_muons[0]].p4() + muons[tight_muons[1]].p4()).M() > 60 and (muons[tight_muons[0]].p4() + muons[tight_muons[1]].p4()).M() < 120:

            if not (event.HLT_IsoMu24 or event.HLT_IsoTkMu24):
                return False

            print "selected muon event: " + str(event.event) + " " + str(event.luminosityBlock) + " " + str(event.run)

            self.out.fillBranch("lepton1_pdgid",muons[tight_muons[0]].pdgId)
            self.out.fillBranch("lepton2_pdgid",muons[tight_muons[1]].pdgId)
            self.out.fillBranch("lepton1_pt",muons[tight_muons[0]].pt)
            self.out.fillBranch("lepton1_eta",muons[tight_muons[0]].eta)
            self.out.fillBranch("lepton1_sceta",0)
            self.out.fillBranch("lepton1_phi",muons[tight_muons[0]].phi)
            self.out.fillBranch("lepton2_pt",muons[tight_muons[1]].pt)
            self.out.fillBranch("lepton2_eta",muons[tight_muons[1]].eta)
            self.out.fillBranch("lepton2_sceta",0)
            self.out.fillBranch("lepton2_phi",muons[tight_muons[1]].phi)
            self.out.fillBranch("mll",(muons[tight_muons[0]].p4() + muons[tight_muons[1]].p4()).M())

        elif len(tight_electrons) == 2 and electrons[tight_electrons[0]] != electrons[tight_electrons[1]] and (electrons[tight_electrons[0]].p4()+electrons[tight_electrons[1]].p4()).M() > 60 and (electrons[tight_electrons[0]].p4()+electrons[tight_electrons[1]].p4()).M() < 120:

            if not event.HLT_Ele27_WPTight_Gsf:
                return False

            print "selected electron event: " + str(event.event) + " " + str(event.luminosityBlock) + " " + str(event.run)

            self.out.fillBranch("lepton1_pdgid",electrons[tight_electrons[0]].pdgId)
            self.out.fillBranch("lepton2_pdgid",electrons[tight_electrons[1]].pdgId)
            self.out.fillBranch("lepton1_pt",electrons[tight_electrons[0]].pt)
            self.out.fillBranch("lepton1_eta",electrons[tight_electrons[0]].eta)
            self.out.fillBranch("lepton1_sceta",electrons[tight_electrons[0]].eta+electrons[tight_electrons[0]].deltaEtaSC)
            self.out.fillBranch("lepton1_phi",electrons[tight_electrons[0]].phi)
            self.out.fillBranch("lepton2_pt",electrons[tight_electrons[1]].pt)
            self.out.fillBranch("lepton2_eta",electrons[tight_electrons[1]].eta)
            self.out.fillBranch("lepton2_sceta",electrons[tight_electrons[1]].eta+electrons[tight_electrons[1]].deltaEtaSC)
            self.out.fillBranch("lepton2_phi",electrons[tight_electrons[1]].phi)
            self.out.fillBranch("mll",(electrons[tight_electrons[0]].p4()+electrons[tight_electrons[1]].p4()).M())
            lepton1_passHLT = False
            lepton2_passHLT = False

            for i in range(0,len(trigobjs)):
                if trigobjs[i].id == 11 and (trigobjs[i].filterBits & (1 << 1) == (1 << 1)):
                     if deltaR(electrons[tight_electrons[0]].eta,electrons[tight_electrons[0]].phi,trigobjs[i].eta,trigobjs[i].phi) < 0.3:
                         lepton1_passHLT = True
                     if deltaR(electrons[tight_electrons[1]].eta,electrons[tight_electrons[1]].phi,trigobjs[i].eta,trigobjs[i].phi) < 0.3:
                         lepton2_passHLT = True

            self.out.fillBranch("lepton1_passHLT",int(lepton1_passHLT))
            self.out.fillBranch("lepton2_passHLT",int(lepton2_passHLT))

        else:
            return False

        if hasattr(event,"Generator_weight"):
            self.out.fillBranch("gen_weight",event.Generator_weight)

        if hasattr(event,"npu"):
            self.out.fillBranch("npu",event.Pileup_nPU)

        self.out.fillBranch("puppimet",event.PuppiMET_pt)
        self.out.fillBranch("puppimetphi",event.PuppiMET_phi)
        self.out.fillBranch("met",event.MET_pt)
        self.out.fillBranch("metphi",event.MET_phi)
        self.out.fillBranch("npvs",event.PV_npvs)
        self.out.fillBranch("event",event.event)
        self.out.fillBranch("lumi",event.luminosityBlock)
        self.out.fillBranch("run",event.run)

        return True

zHLTSFModule = lambda : zHLTSFProducer()
