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

#process.content = cms.EDAnalyzer("EventContentAnalyzer")
process.load("PhysicsTools.PatAlgos.cleaningLayer0.caloTauCleaner_cfi")

# replace allLayer0Taus with allLayer0CaloTaus by hand unpacking the patLayer0 sequence
process.p = cms.Path(
        #process.content +             # uncomment to get a dump of the input to PAT
        process.patBeforeLevel0Reco *
        process.allLayer0Muons *
        process.allLayer0Electrons *
        process.allLayer0Photons *
        process.allLayer0CaloTaus *
        process.allLayer0Jets *
        process.allLayer0METs *
        process.patHighLevelReco *
        process.patMCTruth *
        process.patTrigMatch +
        process.patLayer1
)
# reconfigure MC, Trigger match and Layer 1 to use CaloTaus
process.tauMatch.src                 = cms.InputTag('allLayer0CaloTaus')
process.tauTrigMatchHLT1Tau.src      = cms.InputTag('allLayer0CaloTaus')
process.tauTrigMatchHLT2TauPixel.src = cms.InputTag('allLayer0CaloTaus')
process.allLayer1Taus.tauSource      = cms.InputTag('allLayer0CaloTaus')

# Output module configuration
process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('PATLayer1_Output.fromAOD_CaloTau_full.root'),
    # save only events passing the full path
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    outputCommands = cms.untracked.vstring('drop *')
)
process.outpath = cms.EndPath(process.out)
# save PAT Layer 1 output
process.load("PhysicsTools.PatAlgos.patLayer1_EventContent_cff")
process.out.outputCommands.extend(process.patLayer1EventContent.outputCommands)

