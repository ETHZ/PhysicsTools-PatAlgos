import FWCore.ParameterSet.Config as cms

# import Muon POG isolation config
from RecoMuon.MuonIsolationProducers.muIsolation_cff import *

#FIXME is this still necessary?
#vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv
# define module labels for old (tk-based isodeposit) POG isolation
patMuonIsolationLabels = cms.VInputTag(
        cms.InputTag("muIsoDepositCalByAssociatorTowers","ecal"),
        cms.InputTag("muIsoDepositCalByAssociatorTowers","hcal"),
        cms.InputTag("muIsoDepositCalByAssociatorTowers","ho"),
        cms.InputTag("muIsoDepositTk"),
        cms.InputTag("muIsoDepositJets")
)
# read and convert to ValueMap<IsoDeposit> keyed to Candidate
patMuonIsolations = cms.EDFilter("MultipleIsoDepositsToValueMaps",
    collection   = cms.InputTag("muons"),
    associations = patMuonIsolationLabels,
)
#^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

# sequence to run on AOD
patMuonIsolation = cms.Sequence(patMuonIsolations)

