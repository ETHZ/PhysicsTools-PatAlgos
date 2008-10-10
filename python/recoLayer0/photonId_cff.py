import FWCore.ParameterSet.Config as cms

patPhotonID = cms.EDFilter("PhotonIDConverter",
    src = cms.InputTag("photons"),
    photonID = cms.InputTag("PhotonIDProd","PhotonAssociatedID")
)
