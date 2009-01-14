import FWCore.ParameterSet.Config as cms

# module to filter on the minimal number of Electrons
minLayer1Electrons = cms.EDFilter("PATElectronMinFilter",
    src = cms.InputTag("cleanLayer1Electrons"),
    minNumber = cms.uint32(0)
)


