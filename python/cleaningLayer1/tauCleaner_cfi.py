import FWCore.ParameterSet.Config as cms

cleanLayer1Taus = cms.EDFilter("PATTauCleaner",
    ## uncalibrated reco tau input source
    src = cms.InputTag("allLayer1Taus"), 

    # preselection (any string-based cut on pat::Tau)
    preselection = cms.string(''),

    # selection (e.g. ID)
    selection = cms.PSet(
        type = cms.string('none')
    ),

    removeOverlaps = cms.PSet(
        ## Flag or discard jets that match with clean electrons
        #electrons = cms.PSet( 
        #    collection = cms.InputTag("cleanLayer1Electrons"), ## 
        #    deltaR = cms.double(0.3), ##
        #    #cut = cms.string('pt > 10'),              ## as in LeptonTauIsolationAngle
        #    #flags = cms.vstring('Isolation/Tracker'), ## request the item to be marked as isolated in the tracker
        #    #                                          ## by the PATElectronCleaner
        #),
    ),
)
