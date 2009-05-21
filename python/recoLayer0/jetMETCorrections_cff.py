import FWCore.ParameterSet.Config as cms

## produce associated jet correction factors for calo jets 
from PhysicsTools.PatAlgos.recoLayer0.jetCorrFactors_cfi import *

## jet sequence
patJetCorrections = cms.Sequence(jetCorrFactors)

## MET corrections for JES
from JetMETCorrections.Type1MET.MetType1Corrections_cff import *
from JetMETCorrections.Configuration.L2L3Corrections_Summer08Redigi_cff import *
corMetType1Icone5.corrector = cms.string('L2L3JetCorrectorIC5Calo')

## MET corrections for muons:
from JetMETCorrections.Type1MET.MetMuonCorrections_cff import corMetGlobalMuons
corMetType1Icone5Muons = corMetGlobalMuons.clone(uncorMETInputTag = cms.InputTag('corMetType1Icone5'))

## MET sequence
patMETCorrections = cms.Sequence(corMetType1Icone5 *
                                 corMetType1Icone5Muons
                                 )

# JetMET sequence
patJetMETCorrections = cms.Sequence(patJetCorrections +
                                    patMETCorrections
                                    )
