import FWCore.ParameterSet.Config as cms

from PhysicsTools.PatAlgos.tools.helpers import *
   
def switchToCaloTau(process,pfTauLabel=cms.InputTag('pfRecoTauProducer'), caloTauLabel=cms.InputTag('caloRecoTauProducer')):
    # swap the discriminators we compute # FIXME: remove if they're already on AOD
    process.patAODReco.replace(process.patPFTauDiscrimination, process.patCaloTauDiscrimination)
    massSearchReplaceParam(process.patTrigMatch, 'src', pfTauLabel, caloTauLabel)
    massSearchReplaceParam(process.patMCTruth,   'src', pfTauLabel, caloTauLabel)
    process.allLayer1Taus.tauSource      = caloTauLabel
    process.allLayer1Taus.tauIDSources = cms.PSet(  ## FIXME: get this list from process.patCaloTauDiscrimination
            leadingTrackFinding = cms.InputTag("caloRecoTauDiscriminationByLeadingTrackFinding"),
            leadingTrackPtCut   = cms.InputTag("caloRecoTauDiscriminationByLeadingTrackPtCut"),
            byIsolation         = cms.InputTag("caloRecoTauDiscriminationByIsolation"),
           #againstElectron     = cms.InputTag("caloRecoTauDiscriminationAgainstElectron"),  # Not on AOD
    )
    if pfTauLabel in process.aodSummary.candidates:
        process.aodSummary.candidates[process.aodSummary.candidates.index(pfTauLabel)] = caloTauLabel
    else:
        process.aodSummary.candidates += [caloTauLabel]
