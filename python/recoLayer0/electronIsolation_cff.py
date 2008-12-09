import FWCore.ParameterSet.Config as cms

# define module labels for old (tk-based isodeposit) POG isolation
# WARNING: these labels are used in the functions below.
patAODElectronIsolationLabels = cms.VInputTag(
        cms.InputTag("eleIsoDepositTk"),
        cms.InputTag("eleIsoDepositEcalFromHits"),
        cms.InputTag("eleIsoDepositHcalFromHits"),
)

# read and convert to ValueMap<IsoDeposit> keyed to Candidate
patAODElectronIsolations = cms.EDFilter("MultipleIsoDepositsToValueMaps",
    collection   = cms.InputTag("pixelMatchGsfElectrons"),
    associations = patAODElectronIsolationLabels,
)

# re-key ValueMap<IsoDeposit> to Layer 0 output
layer0ElectronIsolations = cms.EDFilter("CandManyValueMapsSkimmerIsoDeposits",
    collection   = cms.InputTag("allLayer0Electrons"),
    backrefs     = cms.InputTag("allLayer0Electrons"),
    commonLabel  = cms.InputTag("patAODElectronIsolations"),
    associations = patAODElectronIsolationLabels,
)

# sequence to run on AOD before PAT
patAODElectronIsolation = cms.Sequence(patAODElectronIsolations)

# sequence to run after the PAT cleaners
patLayer0ElectronIsolation = cms.Sequence(layer0ElectronIsolations)
