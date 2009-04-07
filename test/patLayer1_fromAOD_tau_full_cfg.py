import FWCore.ParameterSet.Config as cms

process = cms.Process("PAT")

# initialize MessageLogger and output report
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.categories.append('PATSummaryTables')
process.MessageLogger.cerr.INFO = cms.untracked.PSet(
    default          = cms.untracked.PSet( limit = cms.untracked.int32(0)  ),
    PATSummaryTables = cms.untracked.PSet( limit = cms.untracked.int32(-1) )
)
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

# source
process.source = cms.Source("PoolSource", 
    fileNames = cms.untracked.vstring(
    'rfio:/castor/cern.ch/cms/store/relval/CMSSW_3_1_0_pre4/RelValTTbar/GEN-SIM-RECO/IDEAL_30X_v1/0003/00E48100-3A16-DE11-A693-001617DBCF6A.root'
    )
)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string('IDEAL_30X::All')
process.load("Configuration.StandardSequences.MagneticField_cff")

# extraction of tau sequences
process.load("PhysicsTools.JetMCAlgos.TauGenJets_cfi")
process.load("PhysicsTools.PatAlgos.mcMatchLayer0.tauMatch_cfi")
process.load("PhysicsTools.PatAlgos.recoLayer0.tauIsolation_cff")
process.load("PhysicsTools.PatAlgos.recoLayer0.tauDiscriminators_cff")  ##missing modules and inputs
process.load("PhysicsTools.PatAlgos.producersLayer1.tauProducer_cfi")
#process.content = cms.EDAnalyzer("EventContentAnalyzer")

# replacements to make the taus work
process.allLayer1Taus.addGenJetMatch  = False       ## NAN
process.allLayer1Taus.genJetMatch     = ''          ## NAN
process.allLayer1Taus.isolation       = cms.PSet()  ## NAN
process.allLayer1Taus.isoDeposits     = cms.PSet()  ## NAN

process.p = cms.Path(
#     process.patPFTauIsolation *    ## missing modules and inputs
      process.tauMatch +
      process.tauGenJets *
#     process.tauGenJetMatch         ## missing dictionary for tauGenJet
      process.allLayer1Taus
)

# Output module configuration
from PhysicsTools.PatAlgos.patEventContent_cff import patEventContent
process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('PATLayer1_Output.fromAOD_full.root'),
    # save only events passing the full path
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    # save PAT Layer 1 output
    outputCommands = cms.untracked.vstring('drop *', *patEventContent ) # you need a '*' to unpack the list of commands 'patEventContent'
)
process.outpath = cms.EndPath(process.out)

