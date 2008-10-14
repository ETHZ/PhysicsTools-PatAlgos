import FWCore.ParameterSet.Config as cms

isolatedCaloTaus = cms.EDFilter("IsolatedCaloTauSelector",
    tauSource              = cms.InputTag("caloRecoTauProducer"),
    tauDiscriminatorSource = cms.InputTag("caloRecoTauDiscriminationByIsolation"),
)


