import FWCore.ParameterSet.Config as cms

cleanLayer1Electrons = cms.EDFilter("PATElectronCleaner",
    ## pat electron input source
    src = cms.InputTag("allLayer1Electrons"), 

    # preselection (any string-based cut for pat::Electron)
    preselection = cms.string(''),

    # selection (e.g. ID)
    selection = cms.PSet(
        type = cms.string('none')
    ),

    # duplicate removal configurables
    removeOverlaps = cms.PSet(
        ##  Somebody might want this feature
        # muons = cms.PSet(
        #    collection = cms.InputTag("allLayer0Muons")
        #    deltaR     = cms.double(0.3)
        # )
    ),
)
