import FWCore.ParameterSet.Config as cms

patJetTracksAssociator = cms.EDFilter("JetTracksAssociationValueMap",
    src    = cms.InputTag("iterativeCone5CaloJets"),         ## the AOD jets given as input to the PAT jet cleaner
    tracks = cms.InputTag("ic5JetTracksAssociatorAtVertex"), ## any JetTracksAssociation
    cut = cms.string('') # e.g. normalizedChi2 < 5
)

## Compute JET Charge
patJetCharge = cms.EDFilter("JetChargeValueMap",
    src                  = cms.InputTag("iterativeCone5CaloJets"),             ## The Jets
    jetTracksAssociation = cms.InputTag("patJetTracksAssociator"), ## NOTE: must be something from JetTracksAssociationValueMap
    # -- JetCharge parameters --
    var = cms.string('Pt'),
    exp = cms.double(1.0)
)

patJetTracksCharge = cms.Sequence(patJetTracksAssociator * patJetCharge)
