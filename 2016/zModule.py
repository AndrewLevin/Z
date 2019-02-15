import ROOT

from math import cos, sqrt

ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection 
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaPhi

class exampleProducer(Module):
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
        self.out.branch("ntruepu",  "F");
        self.out.branch("lepton1_pdgid",  "I");
        self.out.branch("lepton2_pdgid",  "I");
        self.out.branch("lepton1_pt",  "F");
        self.out.branch("lepton1_phi",  "F");
        self.out.branch("lepton1_eta",  "F");
        self.out.branch("lepton2_pt",  "F");
        self.out.branch("lepton2_phi",  "F");
        self.out.branch("lepton2_eta",  "F");
        self.out.branch("photon_pt",  "F");
        self.out.branch("photon_phi",  "F");
        self.out.branch("photon_eta",  "F");
        self.out.branch("mll",  "F");
        self.out.branch("met",  "F");
        self.out.branch("puppimet",  "F");
        self.out.branch("mt",  "F");
        self.out.branch("puppimt",  "F");
        self.out.branch("npvs","I")
        self.out.branch("is_lepton1_tight",  "B");
        self.out.branch("is_lepton2_tight",  "B");
        self.out.branch("gen_weight",  "F");
        self.out.branch("is_lepton1_real",  "B");
        self.out.branch("is_lepton2_real",  "B");
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        #do this first for processing speed-up
        if not (event.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ or event.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ or event.HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ):
            return False

        electrons = Collection(event, "Electron")
        muons = Collection(event, "Muon")

        try:
            genparts = Collection(event, "GenPart")
            lheparts = Collection(event, "LHEPart")
        except:
            
            pass
            
        tight_muons = []

        loose_but_not_tight_muons = []
        
        tight_electrons = []

        loose_but_not_tight_electrons = []

        for i in range(0,len(muons)):

            if muons[i].pt < 20:
                continue

            if abs(muons[i].eta) > 2.4:
                continue

            if muons[i].tightId and muons[i].pfRelIso04_all < 0.15:
                tight_muons.append(i)
            elif muons[i].pfRelIso04_all < 0.25:
                loose_but_not_tight_muons.append(i)

        #for processing speed-up
        if len(tight_muons) + len(loose_but_not_tight_muons) > 2:
            return False

        for i in range (0,len(electrons)):

            if electrons[i].pt < 20:
                continue
            
            if abs(electrons[i].eta + electrons[i].deltaEtaSC) > 2.5:
                continue

            if (abs(electrons[i].eta + electrons[i].deltaEtaSC) < 1.479 and abs(electrons[i].dz) < 0.1 and abs(electrons[i].dxy) < 0.05) or (abs(electrons[i].eta + electrons[i].deltaEtaSC) > 1.479 and abs(electrons[i].dz) < 0.2 and abs(electrons[i].dxy) < 0.1):
                if electrons[i].cutBased >= 3:
                    tight_electrons.append(i)

                elif electrons[i].cutBased >= 1:
                    loose_but_not_tight_electrons.append(i)

        if len(tight_muons) + len(loose_but_not_tight_muons) +  len(tight_electrons) + len(loose_but_not_tight_electrons) > 2:
            return False

        isprompt_mask = (1 << 0) #isPrompt
        isfromhardprocess_mask = (1 << 8) #isFromHardProcess
        isprompttaudecayproduct_mask = (1 << 4) #isPromptTauDecayProduct

        if len(tight_muons) == 2 and muons[tight_muons[0]].pdgId != muons[tight_muons[1]].pdgId and (muons[tight_muons[0]].p4() + muons[tight_muons[1]].p4()).M() > 60 and (muons[tight_muons[0]].p4() + muons[tight_muons[1]].p4()).M() < 120:

            if not (event.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ or event.HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ):
                return False

            print "selected muon event: " + str(event.event) + " " + str(event.luminosityBlock) + " " + str(event.run)

            is_lepton1_real = 0
        
            try:
                for i in range(0,len(genparts)):
                    if genparts[i].pt > 5 and abs(genparts[i].pdgId) == 13 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isprompttaudecayproduct_mask == isprompttaudecayproduct_mask)) and deltaR(muons[tight_muons[0]].eta,muons[tight_muons[0]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                        is_lepton1_real=1
            except:
                pass

            self.out.fillBranch("mt",sqrt(2*muons[tight_muons[0]].pt*event.MET_pt*(1 - cos(event.MET_phi - muons[tight_muons[0]].phi))))
            self.out.fillBranch("puppimt",sqrt(2*muons[tight_muons[0]].pt*event.PuppiMET_pt*(1 - cos(event.PuppiMET_phi - muons[tight_muons[0]].phi))))
            self.out.fillBranch("is_lepton1_real",is_lepton1_real)
            self.out.fillBranch("lepton1_pdgid",muons[tight_muons[0]].pdgId)
            self.out.fillBranch("lepton2_pdgid",muons[tight_muons[1]].pdgId)
            self.out.fillBranch("lepton1_pt",muons[tight_muons[0]].pt)
            self.out.fillBranch("lepton1_eta",muons[tight_muons[0]].eta)
            self.out.fillBranch("lepton1_phi",muons[tight_muons[0]].phi)
            self.out.fillBranch("lepton2_pt",muons[tight_muons[1]].pt)
            self.out.fillBranch("lepton2_eta",muons[tight_muons[1]].eta)
            self.out.fillBranch("lepton2_phi",muons[tight_muons[1]].phi)
            self.out.fillBranch("mll",(muons[tight_muons[0]].p4() + muons[tight_muons[1]].p4()).M())
            self.out.fillBranch("is_lepton1_tight",1)
            self.out.fillBranch("is_lepton2_tight",1)

        elif len(tight_electrons) == 2 and electrons[tight_electrons[0]] != electrons[tight_electrons[1]] and (electrons[tight_electrons[0]].p4()+electrons[tight_electrons[1]].p4()).M() > 60 and (electrons[tight_electrons[0]].p4()+electrons[tight_electrons[1]].p4()).M() < 120:

            if not event.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ:
                return False

            print "selected electron event: " + str(event.event) + " " + str(event.luminosityBlock) + " " + str(event.run)

            is_lepton1_real = 0    
                
            try:

                for i in range(0,len(genparts)):
                    if genparts[i].pt > 5 and abs(genparts[i].pdgId) == 11 and ((genparts[i].statusFlags & isprompt_mask == isprompt_mask) or (genparts[i].statusFlags & isprompttaudecayproduct_mask == isprompttaudecayproduct_mask)) and deltaR(electrons[tight_electrons[0]].eta,electrons[tight_electrons[0]].phi,genparts[i].eta,genparts[i].phi) < 0.3:
                        is_lepton1_real=1
            except:
                pass

            self.out.fillBranch("mt",sqrt(2*electrons[tight_electrons[0]].pt*event.MET_pt*(1 - cos(event.MET_phi - electrons[tight_electrons[0]].phi))))
            self.out.fillBranch("puppimt",sqrt(2*electrons[tight_electrons[0]].pt*event.PuppiMET_pt*(1 - cos(event.PuppiMET_phi - electrons[tight_electrons[0]].phi))))
            self.out.fillBranch("is_lepton1_real",is_lepton1_real)
            self.out.fillBranch("lepton1_pdgid",electrons[tight_electrons[0]].pdgId)
            self.out.fillBranch("lepton2_pdgid",electrons[tight_electrons[1]].pdgId)
            self.out.fillBranch("lepton1_pt",electrons[tight_electrons[0]].pt)
            self.out.fillBranch("lepton1_eta",electrons[tight_electrons[0]].eta)
            self.out.fillBranch("lepton1_phi",electrons[tight_electrons[0]].phi)
            self.out.fillBranch("lepton2_pt",electrons[tight_electrons[1]].pt)
            self.out.fillBranch("lepton2_eta",electrons[tight_electrons[1]].eta)
            self.out.fillBranch("lepton2_phi",electrons[tight_electrons[1]].phi)
            self.out.fillBranch("mll",(electrons[tight_electrons[0]].p4()+electrons[tight_electrons[1]].p4()).M())
            self.out.fillBranch("is_lepton1_tight",1)
            self.out.fillBranch("is_lepton2_tight",1)
        else:
            return False


        try:
            self.out.fillBranch("gen_weight",event.Generator_weight)
        except:
            pass

        try:
            self.out.fillBranch("npu",event.Pileup_nPU)
        except:
            pass

        self.out.fillBranch("puppimet",event.PuppiMET_pt)
        self.out.fillBranch("met",event.MET_pt)
        self.out.fillBranch("npvs",event.PV_npvs)
        self.out.fillBranch("event",event.event)
        self.out.fillBranch("lumi",event.luminosityBlock)
        self.out.fillBranch("run",event.run)

        return True

exampleModule = lambda : exampleProducer()
