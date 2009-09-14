import FWCore.ParameterSet.Config as cms

process = cms.Process("PAT")


# source
process.source = cms.Source("PoolSource", 
    fileNames = cms.untracked.vstring('file:PF2PAT.root')
)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

# Define output module (needs to be done before using the PAT tools)
from PhysicsTools.PatAlgos.patEventContent_cff import patEventContentNoLayer1Cleaning
from PhysicsTools.PatAlgos.patEventContent_cff import patExtraAodEventContent
process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('patLayer1_fromPF2PAT.root'),
    # save only events passing the full path
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    # save PAT Layer 1 output
    outputCommands = cms.untracked.vstring('drop *',
                                           *(patEventContentNoLayer1Cleaning+patExtraAodEventContent) )
                               # you need a '*' to unpack the list of commands 'patEventContentNoLayer1Cleaning'
)

# Configure PAT to use PF2PAT instead of AOD sources
from PhysicsTools.PatAlgos.tools.pfTools import *

usePF2PAT(process, runPF2PAT=False)


process.p = cms.Path(
    process.patDefaultSequence  
)

process.outpath = cms.EndPath(process.out)


# initialize MessageLogger and output report
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )
process.MessageLogger.cerr.FwkReport.reportEvery = 10

process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string('MC_31X_V1::All')
process.load("Configuration.StandardSequences.MagneticField_cff")
