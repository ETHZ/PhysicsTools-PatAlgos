import FWCore.ParameterSet.Config as cms

allLayer1Muons = cms.EDProducer("PATMuonProducer",

    # General configurables
    muonSource = cms.InputTag("muons"),
    
 

    # user data to add
    userData = cms.PSet(
      # add custom classes here
      userClasses = cms.PSet(
        src = cms.VInputTag('')
      ),
      # add doubles here
      userFloats = cms.PSet(
        src = cms.VInputTag('')
      ),
      # add ints here
      userInts = cms.PSet(
        src = cms.VInputTag('')
      ),
      # add "inline" functions here
      userFunctions = cms.vstring(""),
      userFunctionLabels = cms.vstring("")
    ),
                                
    embedTrack          = cms.bool(False), ## whether to embed in AOD externally stored tracker track
    embedCombinedMuon   = cms.bool(True), ## whether to embed in AOD externally stored combined muon track
    embedStandAloneMuon = cms.bool(True), ## whether to embed in AOD externally stored standalone muon track
    embedPickyMuon      = cms.bool(True), ## whether to embed in AOD externally stored TeV-refit picky muon track
    embedTpfmsMuon      = cms.bool(True), ## whether to embed in AOD externally stored TeV-refit TPFMS muon track
 

# resolution configurables
    addResolutions   = cms.bool(False),
# pflow specific
    pfMuonSource = cms.InputTag("pfMuons"),
    useParticleFlow =  cms.bool( False ),
    embedPFCandidate = cms.bool(False),

# Store isolation values
    isolation = cms.PSet(
        tracker = cms.PSet(
            src = cms.InputTag("muIsoFromDepsTk"),
        ),
        ecal = cms.PSet(
            src = cms.InputTag("muIsoFromDepsEcalFromHits"),
        ),
        hcal = cms.PSet(
            src = cms.InputTag("muIsoFromDepsHcalFromTowers"),
        ),
        user = cms.VPSet(),
    ),
    # Store IsoDeposits
    isoDeposits = cms.PSet(
        tracker = cms.InputTag("muIsoDepositTk"),
        ecal    = cms.InputTag("muIsoDepositEcalFromHits"),
        hcal    = cms.InputTag("muIsoDepositHcalFromTowers"),
    ),

    

    # Trigger matching configurables
    addTrigMatch = cms.bool(True),
    trigPrimMatch = cms.VInputTag(cms.InputTag("muonTrigMatchHLT1MuonNonIso"), cms.InputTag("muonTrigMatchHLT1MET65")),

    # MC matching configurables
    addGenMatch = cms.bool(True),
    embedGenMatch = cms.bool(False),
    genParticleMatch = cms.InputTag("muonMatch"), ## particles source to be used for the matching

    # Efficiencies
    addEfficiencies = cms.bool(False),
    efficiencies    = cms.PSet(),
                                
    # TeV refit tracks
    addTeVRefits = cms.bool(True),
    pickySrc = cms.InputTag("tevMuons", "picky"),
    tpfmsSrc = cms.InputTag("tevMuons", "firstHit"),
)


