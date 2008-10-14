import FWCore.ParameterSet.Config as cms

isolatedPFTaus = cms.EDFilter("IsolatedPFTauSelector",
    tauSource              = cms.InputTag("pfRecoTauProducer"),
    tauDiscriminatorSource = cms.InputTag("pfRecoTauDiscriminationByIsolation"),
)
