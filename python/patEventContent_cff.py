# The following comments couldn't be translated into the new config version:

import FWCore.ParameterSet.Config as cms

patEventContent = [
    'keep *_selectedLayer1Photons_*_*', 
    'keep *_selectedLayer1Electrons_*_*', 
    'keep *_selectedLayer1Muons_*_*', 
    'keep *_selectedLayer1Taus_*_*', 
    'keep *_selectedLayer1Jets_*_*', 
    'keep *_selectedLayer1METs_*_*',
    'keep *_selectedLayer1Hemispheres_*_*',
    'keep patPFParticles_*_*_*',
]

patExtraAodEventContent = [
    # GEN
    'keep recoGenParticles_genParticles_*_*',
    'keep *_genEventScale_*_*',
    'keep *_genEventWeight_*_*',
    'keep *_genEventPdfInfo_*_*',
    # RECO
    'keep recoTracks_generalTracks_*_*', 
    'keep *_towerMaker_*_*',
    'keep *_offlineBeamSpot_*_*',
    'keep *_offlinePrimaryVertices_*_*',
    # TRIGGER
    'keep edmTriggerResults_TriggerResults_*_HLT', 
    'keep *_hltTriggerSummaryAOD_*_*',
]
