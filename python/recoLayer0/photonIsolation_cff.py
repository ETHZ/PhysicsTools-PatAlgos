import FWCore.ParameterSet.Config as cms

# definee   module labels for POG isolation
patAODPhotonIsolationLabels = cms.VInputTag(
        cms.InputTag("gamIsoDepositTk"),
        cms.InputTag("gamIsoDepositEcalFromHits"),
        cms.InputTag("gamIsoDepositHcalFromHits"),     
)

# read and convert to ValueMap<IsoDeposit> keyed to Candidate
patAODPhotonIsolations = cms.EDFilter("MultipleIsoDepositsToValueMaps",
    collection   = cms.InputTag("photons"),
    associations =  patAODPhotonIsolationLabels,
)

# re-key ValueMap<IsoDeposit> to Layer 0 output
layer0PhotonIsolations = cms.EDFilter("CandManyValueMapsSkimmerIsoDeposits",
    collection   = cms.InputTag("allLayer0Photons"),
    backrefs     = cms.InputTag("allLayer0Photons"),
    commonLabel  = cms.InputTag("patAODPhotonIsolations"),
    associations =  patAODPhotonIsolationLabels,
)

# sequence to run on AOD before PAT 
patAODPhotonIsolation = cms.Sequence(patAODPhotonIsolations)

# sequence to run after PAT cleaners
patLayer0PhotonIsolation = cms.Sequence(layer0PhotonIsolations)

