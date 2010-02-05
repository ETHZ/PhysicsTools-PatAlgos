import FWCore.ParameterSet.Config as cms


def addMuonUserIsolation(process,
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
    # key to define the parameter sets
    isolationKey=0
    # add pre-requisits to the muon
    for obj in range(len(isolationTypes)):
        if ( isolationTypes[obj] == 'Tracker' or isolationTypes[obj] == 'All'):
            print "adding predefined userIsolation to pat::Muon for Tracker"
            print " -> to access this information call pat::Muon::userIsolation(pat::TrackIso) in your analysis code <-"
            isolationKey=isolationKey+1

        if ( isolationTypes[obj] == 'Ecal'    or isolationTypes[obj] == 'All'):
            print "adding predefined userIsolation to pat::Muon for Ecal"
            print " -> to access this information call pat::Muon::userIsolation(pat::EcalIso ) in your analysis code <-"
            isolationKey=isolationKey+10

        if ( isolationTypes[obj] == 'Hcal'    or isolationTypes[obj] == 'All'):
            print "adding predefined userIsolation to pat::Muon for Hcal"
            print " -> to access this information call pat::Muon::userIsolation(pat::HcalIso ) in your analysis code <-"
            isolationKey=isolationKey+100

    # do the corresponding replacements in the pat muon
    if ( isolationKey ==   1 ):
        # tracker
        process.allLayer1Muons.isoDeposits = cms.PSet(
            tracker = cms.InputTag("muIsoDepositTk"),
        )
        process.allLayer1Muons.userIsolation = cms.PSet(
            tracker = cms.PSet(
            src = cms.InputTag("muIsoDepositTk"),
            deltaR = cms.double(0.3)
            ),
        )
    if ( isolationKey ==  10 ):
        # ecal
        process.allLayer1Muons.isoDeposits = cms.PSet(
            ecal    = cms.InputTag("muIsoDepositCalByAssociatorTowers","ecal"),
        )
        process.allLayer1Muons.userIsolation = cms.PSet(
            ecal = cms.PSet(
            src = cms.InputTag("muIsoDepositCalByAssociatorTowers","ecal"),
            deltaR = cms.double(0.3)
            ),
        )
    if ( isolationKey == 100 ):
        # hcal
        process.allLayer1Muons.isoDeposits = cms.PSet(
            hcal    = cms.InputTag("muIsoDepositCalByAssociatorTowers","hcal"),
        )
        process.allLayer1Muons.userIsolation = cms.PSet(
            hcal = cms.PSet(
            src = cms.InputTag("muIsoDepositCalByAssociatorTowers","hcal"),
            deltaR = cms.double(0.3)
            ),
        )
    if ( isolationKey ==  11 ):
        # ecal + tracker
        process.allLayer1Muons.isoDeposits = cms.PSet(
            tracker = cms.InputTag("muIsoDepositTk"),
            ecal    = cms.InputTag("muIsoDepositCalByAssociatorTowers","ecal"),
        )
        process.allLayer1Muons.userIsolation = cms.PSet(
            tracker = cms.PSet(
            src = cms.InputTag("muIsoDepositTk"),
            deltaR = cms.double(0.3)
            ),
            ecal = cms.PSet(
            src = cms.InputTag("muIsoDepositCalByAssociatorTowers","ecal"),
            deltaR = cms.double(0.3)
            ),
        )
    if ( isolationKey == 101 ):
        # hcal + tracker
        process.allLayer1Muons.isoDeposits = cms.PSet(
            tracker = cms.InputTag("muIsoDepositTk"),
            hcal    = cms.InputTag("muIsoDepositCalByAssociatorTowers","hcal"),
        )
        process.allLayer1Muons.userIsolation = cms.PSet(
            tracker = cms.PSet(
            src = cms.InputTag("muIsoDepositTk"),
            deltaR = cms.double(0.3)
            ),
            hcal = cms.PSet(
            src = cms.InputTag("muIsoDepositCalByAssociatorTowers","hcal"),
            deltaR = cms.double(0.3)
            ),
        )
    if ( isolationKey == 110 ):
        # hcal + ecal
        process.allLayer1Muons.isoDeposits = cms.PSet(
            ecal    = cms.InputTag("muIsoDepositCalByAssociatorTowers","ecal"),
            hcal    = cms.InputTag("muIsoDepositCalByAssociatorTowers","hcal"),
        )
        process.allLayer1Muons.userIsolation = cms.PSet(
            ecal = cms.PSet(
            src = cms.InputTag("gamIsoFromDepsEcalFromHits"),
            ),
            hcal = cms.PSet(
            src = cms.InputTag("gamIsoFromDepsHcalFromTowers"),
            ),
        )
    if ( isolationKey == 111 ):
        # hcal + ecal + tracker
        process.allLayer1Muons.isoDeposits = cms.PSet(
            tracker = cms.InputTag("muIsoDepositTk"),
            ecal    = cms.InputTag("muIsoDepositCalByAssociatorTowers","ecal"),
            hcal    = cms.InputTag("muIsoDepositCalByAssociatorTowers","hcal"),
        )
        process.allLayer1Muons.userIsolation = cms.PSet(
            tracker = cms.PSet(
            src = cms.InputTag("muIsoDepositTk"),
            deltaR = cms.double(0.3)
            ),
            ecal = cms.PSet(
            src = cms.InputTag("muIsoDepositCalByAssociatorTowers","ecal"),
            deltaR = cms.double(0.3)
            ),
            hcal = cms.PSet(
            src = cms.InputTag("muIsoDepositCalByAssociatorTowers","hcal"),
            deltaR = cms.double(0.3)
            ),
        )
        
