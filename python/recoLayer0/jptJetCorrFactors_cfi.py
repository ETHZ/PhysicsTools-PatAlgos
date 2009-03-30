import FWCore.ParameterSet.Config as cms

from JetMETCorrections.Configuration.ZSPJetCorrections219_cff import *
from JetMETCorrections.Configuration.JetPlusTrackCorrections_cfi import *

jptJetCorrFactors = cms.EDProducer(
    "JPTJetCorrFactorsProducer",
    JPTZSPCorrectorICone5,
    tagName = ZSPJetCorrectorIcone5.tagName,
    JetsInputTag = cms.InputTag("iterativeCone5CaloJets"),
    )

# Null values mean use JTA "on-the-fly" mode
jptJetCorrFactors.JetTrackCollectionAtVertex = cms.InputTag("")
jptJetCorrFactors.JetTrackCollectionAtCalo   = cms.InputTag("")

