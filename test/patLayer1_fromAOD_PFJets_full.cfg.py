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
     fileNames = cms.untracked.vstring('file:/afs/cern.ch/cms/PRS/top/cmssw-data/relval200-for-pat-testing/FullSimTTBar-2_1_X_2008-07-08_STARTUP_V4-AODSIM.100.root')
)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )


# PAT Layer 0+1
process.load("PhysicsTools.PatAlgos.patLayer0_cff")
process.load("PhysicsTools.PatAlgos.patLayer1_cff")


## Load additional RECO config
# Magnetic field now needs to be in the high-level py
process.load("Configuration.StandardSequences.MagneticField_cff")

# define the jet collection we want to use

# Additional code
process.load("RecoParticleFlow.PFProducer.particleFlow_cff")
process.load("RecoJets.JetAssociationProducers.j2tParametersVX_cfi")
process.ic5PFJetTracksAssociatorAtVertex = cms.EDFilter("JetTracksAssociatorAtVertex", process.j2tParametersVX, jets = cms.InputTag("iterativeCone5PFJets") )
# MC match
process.jetPartonMatch.src        = cms.InputTag("allLayer0PFJets")
process.jetGenJetMatch.src        = cms.InputTag("allLayer0PFJets")
process.jetPartonAssociation.jets = cms.InputTag("allLayer0PFJets")
# Trigger match
process.jetTrigMatchHLT1ElectronRelaxed.src = cms.InputTag("allLayer0PFJets")
process.jetTrigMatchHLT2jet.src             = cms.InputTag("allLayer0PFJets")
# Jet Tracks Association
process.patAODJetTracksAssociator.src        = cms.InputTag("iterativeCone5PFJets")
process.patAODJetTracksAssociator.tracks     = cms.InputTag("ic5PFJetTracksAssociatorAtVertex")
process.layer0JetTracksAssociator.collection = cms.InputTag("allLayer0PFJets")
process.layer0JetTracksAssociator.backrefs   = cms.InputTag("allLayer0PFJets")
process.layer0JetCharge.src                  = cms.InputTag("allLayer0PFJets")
# Layer 1 pat::Jets
process.allLayer1Jets.jetSource = cms.InputTag("allLayer0PFJets")
process.allLayer1Jets.embedCaloTowers   = False
process.allLayer1Jets.addBTagInfo       = False
process.allLayer1Jets.addResolutions    = False
process.allLayer1Jets.addJetCorrFactors = False

# Now we break up process.patLayer0
process.p = cms.Path(
                process.patBeforeLevel0Reco *
                process.ic5PFJetTracksAssociatorAtVertex *
                process.patLayer0Cleaners *
                process.allLayer0PFJets *
                process.patHighLevelReco *
                process.patMCTruth *
                process.patTrigMatch
                + process.patLayer1
            )

# Output module configuration
process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('PATLayer1_Output.fromAOD_PFJets_full.root'),
    # save only events passing the full path
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    outputCommands = cms.untracked.vstring('drop *')
)
process.outpath = cms.EndPath(process.out)
# save PAT Layer 1 output
process.load("PhysicsTools.PatAlgos.patLayer1_EventContent_cff")
process.out.outputCommands.extend(process.patLayer1EventContent.outputCommands)

