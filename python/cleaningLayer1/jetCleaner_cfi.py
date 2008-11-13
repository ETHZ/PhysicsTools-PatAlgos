import FWCore.ParameterSet.Config as cms

cleanLayer1Jets = cms.EDFilter("PATJetCleaner",
    ## uncalibrated reco jet input source
    src = cms.InputTag("allLayer1Jets"), 

    # preselection (any string-based cut on pat::Jet)
    preselection = cms.string(''),

    # selection (e.g. ID)
    selection = cms.PSet(
        type = cms.string('none')
    ),

    removeOverlaps = cms.PSet(
        ## Flag or discard jets that match with clean electrons
        electrons = cms.PSet( 
            collection = cms.InputTag("cleanLayer1Electrons"), ## 
            deltaR = cms.double(0.3), ##
            cut = cms.string('pt > 10'),              ## as in LeptonJetIsolationAngle
            #flags = cms.vstring('Isolation/Tracker'), ## request the item to be marked as isolated in the tracker
            #                                          ## by the PATElectronCleaner
        ),
        ## Flag or discard jets that match with Taus. Off, as it was not there in TQAF
        #taus = cms.PSet(     
        #    collection = cms.InputTag("allLayer0Taus")
        #    deltaR     = cms.double(0.3)
        #)
        ## flag or discard jets that match with Photons. Off, as it was not there in TQAF
        #photons = cms.PSet(
        #    collection = cms.InputTag("allLayer0Photons")
        #    deltaR     = cms.double(0.3)
        #)
        #muons = cms.PSet( ... ) // supported, but it's not likely you want it
        #jets  = cms.PSet( ... ) // same as above   
        user = cms.VPSet()
    ),
)
