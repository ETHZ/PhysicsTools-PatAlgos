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
process.load("RecoJets.JetAssociationProducers.ic5JetTracksAssociatorAtVertex_cfi")
process.load("RecoBTag.Configuration.RecoBTag_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")  ## check this is correct for you!
process.load("Configuration.StandardSequences.MagneticField_cff")

## Redefine sequences
# same as default 'btagging' except without the module 'btagSoftElectrons'
process.btaggingAOD = cms.Sequence(
    process.impactParameterTagInfos *
    process.jetBProbabilityBJetTags +
    process.jetProbabilityBJetTags +
    process.trackCountingHighPurBJetTags +
    process.trackCountingHighEffBJetTags +
    process.impactParameterMVABJetTags *
    process.secondaryVertexTagInfos *
    process.simpleSecondaryVertexBJetTags +
    process.combinedSecondaryVertexBJetTags +
    process.combinedSecondaryVertexMVABJetTags +
    process.softElectronTagInfos *
    process.softElectronBJetTags +
    process.softMuonTagInfos *
    process.softMuonBJetTags +
    process.softMuonNoIPBJetTags )
process.prePATreco = cms.Sequence(
    process.ic5JetTracksAssociatorAtVertex *
    process.btaggingAOD)
# PAT sequence, with 'prePATreco' before
process.p = cms.Path(
                process.prePATreco
                #+ process.content    # uncomment to get a dump of the file before PAT layer 0
                + process.patLayer0  
                + process.patLayer1
            )

# make the L2+L3 correction chain for sisCone, as it's not in L2L3Corrections152_cff.py
process.L2L3JetCorrectorMcone5 = cms.ESSource("JetCorrectionServiceChain",
    correctors = cms.vstring('L2RelativeJetCorrectorScone5', 'L3AbsoluteJetCorrectorScone5'),
    label      = cms.string('L2L3JetCorrectorScone5')
)
## Define variables for new inputs
jets         = 'sisCone5CaloJets'      # not using cms.InputTag as some modules want it as a string :-(
jetCorrector = 'L2L3JetCorrectorScone5'

btagLabels   = ['trackCountingHighEffBJetTags',  'trackCountingHighPurBJetTags', 
                'impactParameterMVABJetTags',    'jetBProbabilityBJetTags',         'jetProbabilityBJetTags', 
                'simpleSecondaryVertexBJetTags', 'combinedSecondaryVertexBJetTags', 'combinedSecondaryVertexMVABJetTags', 
                'softElectronBJetTags',          'softMuonBJetTags',                'softMuonNoIPBJetTags']
## Replace statements
# layer 0 cleaners
process.allLayer0Jets.jetSource               = jets
# JetMET calibrations
process.jetCorrFactors.jetSource              = jets
process.jetCorrFactors.defaultJetCorrector    = jetCorrector
process.corMetType1Icone5.inputUncorJetsLabel = jets
process.corMetType1Icone5.corrector           = jetCorrector
# Jet-Track association & b-tagging
process.ic5JetTracksAssociatorAtVertex.jets = jets
process.softElectronTagInfos.jets           = jets
process.softMuonTagInfos.jets               = jets
process.patAODJetTracksAssociator.src       = jets
process.patAODTagInfos.collection           = jets
process.patAODBTags.collection              = jets
process.patAODBTags.associations            = btagLabels 
process.layer0BTags.associations            = btagLabels 

#process.content = cms.EDAnalyzer("EventContentAnalyzer")
# Output module configuration
process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('PATLayer1_Output.fromAOD_sisCone_full.root'),
    # save only events passing the full path
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    outputCommands = cms.untracked.vstring('drop *')
)
process.outpath = cms.EndPath(process.out)
# save PAT Layer 1 output
process.load("PhysicsTools.PatAlgos.patLayer1_EventContent_cff")
process.out.outputCommands.extend(process.patLayer1EventContent.outputCommands)

