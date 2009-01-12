import FWCore.ParameterSet.Config as cms

patPhotonIDs = cms.EDFilter("PhotonIDConverter",
    src = cms.InputTag("photons"),
    photonID = cms.InputTag("PhotonIDProd","PhotonAssociatedID")
)

## define the sequence, so we have consistent naming conventions
patPhotonID = cms.Sequence( patPhotonIDs )

