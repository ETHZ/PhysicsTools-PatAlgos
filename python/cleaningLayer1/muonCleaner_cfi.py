import FWCore.ParameterSet.Config as cms

cleanLayer1Muons = cms.EDFilter("PATMuonCleaner",
    src = cms.InputTag("allLayer1Muons"), 

    # preselection (any string-based cut for pat::Muon)
    preselection = cms.string(''),

    # selection (e.g. ID)
    selection = cms.PSet(
        type = cms.string('none')
    ),
    # Other possible selections:
    ## Reco-based muon selection)
    # selection = cms.PSet( type = cms.string("globalMuons") ) # pick only globalMuons
    ## ID-based selection (maybe only tracker muons?)
    # selection = cms.PSet(                                   
    #     type = cms.string("muonPOG")
    #     flag = cms.string("TMLastStationLoose")     # flag for the muon id algorithm
    #                      # "TMLastStationLoose", "TMLastStationTight"  
    #                      # "TM2DCompatibilityLoose", "TM2DCompatibilityTight" 
    #     minCaloCompatibility    = cms.double(0.0)     # cut on calo compatibility
    #     minSegmentCompatibility = cms.double(0.0)     # cut on muon segment match to tracker
    # )
    ## Custom cut-based selection (from SusyAnalyzer))
    # selection = cms.PSet( type = cms.string("custom")  
    #                       dPbyPmax = cms.double(0.5)
    #                       chi2max  = cms.double(3.0)
    #                       nHitsMin = cms.double(13) )

    ## Duplicate removal configurables
    ## Usually not needed
    #
    #removeOverlaps = cms.PSet(
    #    # muons = cms.PSet(
    #    #    collection = cms.InputTag("allLayer0Muons")
    #    #    deltaR     = cms.double(0.3)
    #    # )
    #),

)
