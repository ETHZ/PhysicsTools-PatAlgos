import FWCore.ParameterSet.Config as cms

cleanLayer1Photons = cms.EDFilter("PATPhotonCleaner",
    ## Input collection of Photons
    src = cms.InputTag("allLayer1Photons"),

    # preselection (any string-based cut for pat::Photon)
    preselection = cms.string(''),

    ## Remove or flag photons that overlap with electrons (same superCluster seed or same superCluster)
    removeElectrons = cms.string('bySeed'),  # 'bySeed', 'bySuperCluster' or none
    electrons       = cms.InputTag("cleanLayer1Electrons"),

    # duplicate removal configurables
    removeOverlaps = cms.PSet(
        ##  Somebody might want this feature
        # muons = cms.PSet(
        #    collection = cms.InputTag("allLayer0Muons")
        #    deltaR     = cms.double(0.3)
        # )
    ),

)


