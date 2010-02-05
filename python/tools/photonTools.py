import FWCore.ParameterSet.Config as cms


def addPhotonUserIsolation(process,
             isolationTypes = ['All']):
    """
    ------------------------------------------------------------------
    add userIsolation to patPhoton:

    process        : process
    isolationTypes : list of predefined userIsolation types to be
                     added; possible values are ['Tracker', 'Ecal',
                     'Hcal', 'All'] 
    ------------------------------------------------------------------
    """
    from RecoEgamma.EgammaIsolationAlgos.gamIsoDeposits_cff import gamIsoDepositTk, gamIsoDepositEcalFromHits, gamIsoDepositHcalFromTowers
    from RecoEgamma.EgammaIsolationAlgos.gamIsoFromDepsModules_cff import gamIsoFromDepsTk, gamIsoFromDepsEcalFromHits, gamIsoFromDepsHcalFromTowers

    gamIsoDepositEcalFromHits.ExtractorPSet.barrelEcalHits = cms.InputTag("reducedEcalRecHitsEB")
    gamIsoDepositEcalFromHits.ExtractorPSet.endcapEcalHits = cms.InputTag("reducedEcalRecHitsEE")
    
    # key to define the parameter sets
    isolationKey=0
    # add pre-requisits to the photon
    for obj in range(len(isolationTypes)):
        if ( isolationTypes[obj] == 'Tracker' or isolationTypes[obj] == 'All'):
            print "adding predefined userIsolation to pat::Photon for Tracker"
            print " -> to access this information call pat::Photon::userIsolation(pat::TrackIso) in your analysis code <-"
            isolationKey=isolationKey+1
            from PhysicsTools.PatAlgos.recoLayer0.photonIsolation_cff import patPhotonTrackIsolation
            process.patPhotonTrackIsolation
            process.patDefaultSequence.replace( process.allLayer1Photons, process.patPhotonTrackIsolation*process.allLayer1Photons )

        if ( isolationTypes[obj] == 'Ecal'    or isolationTypes[obj] == 'All'):
            print "adding predefined userIsolation to pat::Photon for Ecal"
            print " -> to access this information call pat::Photon::userIsolation(pat::EcalIso ) in your analysis code <-"
            isolationKey=isolationKey+10
            from PhysicsTools.PatAlgos.recoLayer0.photonIsolation_cff import patPhotonEcalIsolation
            process.patPhotonEcalIsolation            
            process.patDefaultSequence.replace( process.allLayer1Photons, process.patPhotonEcalIsolation*process.allLayer1Photons )

        if ( isolationTypes[obj] == 'Hcal'    or isolationTypes[obj] == 'All'):
            print "adding predefined userIsolation to pat::Photon for Hcal"
            print " -> to access this information call pat::Photon::userIsolation(pat::HcalIso ) in your analysis code <-"
            isolationKey=isolationKey+100
            from PhysicsTools.PatAlgos.recoLayer0.photonIsolation_cff import patPhotonHcalIsolation            
            process.patPhotonHcalIsolation = patPhotonHcalIsolation
            process.patDefaultSequence.replace( process.allLayer1Photons, process.patPhotonHcalIsolation*process.allLayer1Photons )  

    # do the corresponding replacements in the pat photon
    if ( isolationKey ==   1 ):
        # tracker
        process.allLayer1Photons.isoDeposits = cms.PSet(
            tracker = cms.InputTag("gamIsoDepositTk"),
        )
        process.allLayer1Photons.userIsolation = cms.PSet(
            tracker = cms.PSet(
            src = cms.InputTag("gamIsoFromDepsTk"),
            ),
        )
    if ( isolationKey ==  10 ):
        # ecal
        process.allLayer1Photons.isoDeposits = cms.PSet(
            ecal    = cms.InputTag("gamIsoDepositEcalFromHits"),
        )
        process.allLayer1Photons.userIsolation = cms.PSet(
            ecal = cms.PSet(
            src = cms.InputTag("gamIsoFromDepsEcalFromHits"),
            ),
        )
    if ( isolationKey == 100 ):
        # hcal
        process.allLayer1Photons.isoDeposits = cms.PSet(
            hcal    = cms.InputTag("gamIsoDepositHcalFromTowers"),
        )
        process.allLayer1Photons.userIsolation = cms.PSet(
            hcal = cms.PSet(
            src = cms.InputTag("gamIsoFromDepsHcalFromTowers"),
            ),
        )
    if ( isolationKey ==  11 ):
        # ecal + tracker
        process.allLayer1Photons.isoDeposits = cms.PSet(
            tracker = cms.InputTag("gamIsoDepositTk"),
            ecal    = cms.InputTag("gamIsoDepositEcalFromHits"),
        )
        process.allLayer1Photons.userIsolation = cms.PSet(
            tracker = cms.PSet(
            src = cms.InputTag("gamIsoFromDepsTk"),
            ),
            ecal = cms.PSet(
            src = cms.InputTag("gamIsoFromDepsEcalFromHits"),
            ),
        )
    if ( isolationKey == 101 ):
        # hcal + tracker
        process.allLayer1Photons.isoDeposits = cms.PSet(
            tracker = cms.InputTag("gamIsoDepositTk"),
            hcal    = cms.InputTag("gamIsoDepositHcalFromTowers"),
        )
        process.allLayer1Photons.userIsolation = cms.PSet(
            tracker = cms.PSet(
            src = cms.InputTag("gamIsoFromDepsTk"),
            ),
            hcal = cms.PSet(
            src = cms.InputTag("gamIsoFromDepsHcalFromTowers"),
            ),
        )
    if ( isolationKey == 110 ):
        # hcal + ecal
        process.allLayer1Photons.isoDeposits = cms.PSet(
            ecal    = cms.InputTag("gamIsoDepositEcalFromHits"),
            hcal    = cms.InputTag("gamIsoDepositHcalFromTowers"),
        )
        process.allLayer1Photons.userIsolation = cms.PSet(
            ecal = cms.PSet(
            src = cms.InputTag("gamIsoFromDepsEcalFromHits"),
            ),
            hcal = cms.PSet(
            src = cms.InputTag("gamIsoFromDepsHcalFromTowers"),
            ),
        )
    if ( isolationKey == 111 ):
        # hcal + ecal + tracker
        process.allLayer1Photons.isoDeposits = cms.PSet(
            tracker = cms.InputTag("gamIsoDepositTk"),
            ecal    = cms.InputTag("gamIsoDepositEcalFromHits"),
            hcal    = cms.InputTag("gamIsoDepositHcalFromTowers"),
        )
        process.allLayer1Photons.userIsolation = cms.PSet(
            tracker = cms.PSet(
            src = cms.InputTag("gamIsoFromDepsTk"),
            ),
            ecal = cms.PSet(
            src = cms.InputTag("gamIsoFromDepsEcalFromHits"),
            ),
            hcal = cms.PSet(
            src = cms.InputTag("gamIsoFromDepsHcalFromTowers"),
            ),
            user = cms.VPSet(),
        )

