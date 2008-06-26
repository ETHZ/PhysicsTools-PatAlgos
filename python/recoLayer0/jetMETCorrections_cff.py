import FWCore.ParameterSet.Config as cms

# define jet flavour correction services
from JetMETCorrections.Configuration.MCJetCorrections152_cff import *
from JetMETCorrections.Configuration.L5FlavorCorrections_cff import *
# produce associated jet correction factors in a valuemap
from PhysicsTools.PatAlgos.recoLayer0.jetCorrFactors_cfi import *
# default JetMET calibration on IC, KT and MC Jets
from JetMETCorrections.Type1MET.MetType1Corrections_cff import *
import JetMETCorrections.Type1MET.corMetMuons_cfi
# JetMET corrections for muons: input jet-corrected MET
# It would be better to get this config to JetMETCorrections/Type1MET/data/ at some point
corMetType1Icone5Muons = JetMETCorrections.Type1MET.corMetMuons_cfi.corMetMuons.clone()
layer0JetCorrFactors = cms.EDFilter("JetCorrFactorsValueMapSkimmer",
    association = cms.InputTag("jetCorrFactors"),
    collection = cms.InputTag("allLayer0Jets"),
    backrefs = cms.InputTag("allLayer0Jets")
)

# Jet corrections are now done on the fly in the JetProducer
# default PAT sequence for JetMET corrections
patAODJetMETCorrections = cms.Sequence(jetCorrFactors*corMetType1Icone5*corMetType1Icone5Muons)
patLayer0JetMETCorrections = cms.Sequence(layer0JetCorrFactors)
corMetType1Icone5Muons.inputUncorMetLabel = 'corMetType1Icone5'
corMetType1Icone5Muons.TrackAssociatorParameters.useEcal = False ## RecoHits

corMetType1Icone5Muons.TrackAssociatorParameters.useHcal = False ## RecoHits

corMetType1Icone5Muons.TrackAssociatorParameters.useHO = False ## RecoHits

corMetType1Icone5Muons.TrackAssociatorParameters.useCalo = True ## CaloTowers

corMetType1Icone5Muons.TrackAssociatorParameters.useMuon = False ## RecoHits

corMetType1Icone5Muons.TrackAssociatorParameters.truthMatch = False

