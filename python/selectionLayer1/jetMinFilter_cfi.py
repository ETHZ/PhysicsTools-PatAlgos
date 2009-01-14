import FWCore.ParameterSet.Config as cms

# module to filter on the minimal number of Jets
minLayer1Jets = cms.EDFilter("PATJetMinFilter",
    src = cms.InputTag("cleanLayer1Jets"),
    minNumber = cms.uint32(0)
)


