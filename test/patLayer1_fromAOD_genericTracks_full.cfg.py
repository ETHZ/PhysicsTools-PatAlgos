import FWCore.ParameterSet.Config as cms

process = cms.Process("PAT")

# initialize MessageLogger and output report
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.categories.append('PATLayer0Summary')
process.MessageLogger.cerr.INFO = cms.untracked.PSet(
    default          = cms.untracked.PSet( limit = cms.untracked.int32(0)  ),
    PATLayer0Summary = cms.untracked.PSet( limit = cms.untracked.int32(-1) )
)
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

# source
process.source = cms.Source("PoolSource", 
     fileNames = cms.untracked.vstring('file:/afs/cern.ch/cms/PRS/top/cmssw-data/relval200-for-pat-testing/FullSimTTbar-210p5.1-AODSIM.100.root')
)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )


# Magnetic field now needs to be in the high-level py
process.load("Configuration.StandardSequences.MagneticField_cff")

# PAT Layer 0+1
process.load("PhysicsTools.PatAlgos.patLayer0_cff")
process.load("PhysicsTools.PatAlgos.patLayer1_cff")

# Additionl modules
process.load("PhysicsTools.PatAlgos.recoLayer0.genericTrackCandidates_cff")
process.load("PhysicsTools.PatAlgos.cleaningLayer0.genericTrackCleaner_cfi")
## MC match
from PhysicsTools.PatAlgos.mcMatchLayer0.muonMatch_cfi import muonMatch
process.trackMuMatch = muonMatch.clone()
process.trackMuMatch.src = 'allLayer0TrackCands'
## Layer 1
from PhysicsTools.PatAlgos.producersLayer1.genericParticleProducer_cfi import allLayer1GenericParticles
process.allLayer1TrackCands = allLayer1GenericParticles.clone()
process.allLayer1TrackCands.src = 'allLayer0TrackCands'
process.allLayer1TrackCands.addGenMatch           = True
process.allLayer1TrackCands.genParticleMatch      = 'trackMuMatch'
process.allLayer1TrackCands.isolation.tracker.src = 'layer0TrackIsolations:patAODTrackIsoDepositCtfTk'
process.allLayer1TrackCands.isolation.ecal.src    = 'layer0TrackIsolations:patAODTrackIsoDepositCalByAssociatorTowersecal'
process.allLayer1TrackCands.isolation.hcal.src    = 'layer0TrackIsolations:patAODTrackIsoDepositCalByAssociatorTowershcal'
process.allLayer1TrackCands.isoDeposits.tracker   = 'layer0TrackIsolations:patAODTrackIsoDepositCtfTk'
process.allLayer1TrackCands.isoDeposits.ecal      = 'layer0TrackIsolations:patAODTrackIsoDepositCalByAssociatorTowersecal'
process.allLayer1TrackCands.isoDeposits.hcal      = 'layer0TrackIsolations:patAODTrackIsoDepositCalByAssociatorTowershcal'
## Filter
process.selectedLayer1TrackCands = cms.EDFilter("PATGenericParticleSelector",
    src = cms.InputTag("allLayer1TrackCands"),
    cut = cms.string('(pt > 15.) && (caloIso < 10.)')
)

process.p = cms.Path(
        # before-cleaner reconstruction
        process.patBeforeLevel0Reco *
        process.patAODTrackCandSequence *
        # all the cleaners
        process.allLayer0Muons *
        process.allLayer0Electrons *
        process.allLayer0Photons *
        process.allLayer0Taus *
        process.allLayer0TrackCands *
        process.allLayer0Jets *
        process.allLayer0METs *
        # high level reco
        process.patHighLevelReco *
        process.patLayer0TrackCandSequence *
        # matching with MC and trigger
        process.patTrigMatch *
        process.patMCTruth *
        process.trackMuMatch *
        # layer 1
        process.patLayer1 *
        process.allLayer1TrackCands *
        process.selectedLayer1TrackCands
)

# Output module configuration
process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('PATLayer1_Output.fromAOD_genericTracks_full.root'),
    # save only events passing the full path
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    outputCommands = cms.untracked.vstring('drop *')
)
process.outpath = cms.EndPath(process.out)
# save PAT Layer 1 output
process.load("PhysicsTools.PatAlgos.patLayer1_EventContent_cff")
process.out.outputCommands.extend(process.patLayer1EventContent.outputCommands)
process.out.outputCommands.append('keep *_selectedLayer1TrackCands_*_*')

