import FWCore.ParameterSet.Config as cms

from PhysicsTools.PatAlgos.recoLayer0.bTagging_cff import *
from PhysicsTools.PatAlgos.recoLayer0.electronId_cff import *
from PhysicsTools.PatAlgos.recoLayer0.electronIsolation_cff import *
from PhysicsTools.PatAlgos.recoLayer0.jetMETCorrections_cff import *
from PhysicsTools.PatAlgos.recoLayer0.jetTracksCharge_cff import *
from PhysicsTools.PatAlgos.recoLayer0.muonIsolation_cff import *
from PhysicsTools.PatAlgos.recoLayer0.photonId_cff import *
from PhysicsTools.PatAlgos.recoLayer0.photonIsolation_cff import *
from PhysicsTools.PatAlgos.recoLayer0.tauDiscriminators_cff import *
from PhysicsTools.PatAlgos.recoLayer0.pfCandidateIsoDepositSelection_cff import *
from PhysicsTools.PatAlgos.recoLayer0.tauIsolation_cff import *

## Needed for the MET corrections and  tcMet
from RecoMET.METProducers.TCMET_cfi import *
from JetMETCorrections.Type1MET.MuonMETValueMapProducer_cff import *
from JetMETCorrections.Type1MET.MuonTCMETValueMapProducer_cff import *

# These duplicate removals are here because they're AOD bugfixes
from PhysicsTools.PatAlgos.recoLayer0.duplicatedElectrons_cfi import *

# Produce jpt corrected calo jets, which are not on AOD per default
from JetMETCorrections.Configuration.ZSPJetCorrections219_cff import *
from JetMETCorrections.Configuration.JetPlusTrackCorrections_cff import *
jptCaloJets = cms.Sequence( ZSPJetCorrections * JetPlusTrackCorrections )

# Sequences needed to deliver besic input objects; you shouldn't
# remove modules from here unless you *know* what you're doing
patAODCoreReco = cms.Sequence(
    muonMETValueMapProducer *
    muonTCMETValueMapProducer *
    tcMet +        ## this may be changed to be done on request only
    jptCaloJets +  ## this may be changed to be done on request only
    electronsNoDuplicates 
)

# Sequences needed to deliver external information for objects
# You can remove modules from here if you don't need these features
patAODExtraReco = cms.Sequence(
    #patBTagging +       # Empty sequences not supported yet
    patElectronId +
    patElectronIsolation +
    patJetMETCorrections +
    patJetTracksCharge +
    #patMuonIsolation +   # Empty sequences not supported yet
    #patPhotonID +        # Empty sequences not supported yet
    patPhotonIsolation +
    #patTauDiscrimination # Empty sequences not supported yet
    patPFCandidateIsoDepositSelection +
    patPFTauIsolation
)

# One module to count some AOD Objects that are usually input to PAT
aodSummary = cms.EDAnalyzer("CandidateSummaryTable",
    logName = cms.untracked.string("aodObjects|PATSummaryTables"),
    candidates = cms.VInputTag(
        cms.InputTag("pixelMatchGsfElectrons"),
        cms.InputTag("electronsNoDuplicates"),
        cms.InputTag("muons"),
        cms.InputTag("caloRecoTauProducer"),
        cms.InputTag("pfRecoTauProducer"),
        cms.InputTag("photons"),
        cms.InputTag("iterativeCone5CaloJets"),
        cms.InputTag("JetPlusTrackZSPCorJetIcone5"),        
        cms.InputTag("met"),
    )
)
#aodContents = cms.EDAnalyzer("EventContentAnalyzer")

# Default PAT reconstruction sequence on top of AOD
patAODReco = cms.Sequence(
    patAODCoreReco +
    patAODExtraReco +
    aodSummary #+aodContents
)
