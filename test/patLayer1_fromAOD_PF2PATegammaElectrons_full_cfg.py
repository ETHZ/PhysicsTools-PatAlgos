# Configuration when electrons by the e/gamma POG are added on top of PF2PAT.
# Collection provided by PF2PAT are cleaned wrt the electrons using the standard PAT cleaning.
# The configuration will be removed when PF2PAT provides PFElectrons.
import FWCore.ParameterSet.Config as cms

process = cms.Process("PAT")


# control flags
localSource = False
addPF2PATOutput = False
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )


# source 
#process.load("PhysicsTools.PFCandProducer.Sources/source_ZtoMus_DBS_cfi")
process.load("PhysicsTools.PFCandProducer.Sources/source_ZtoTaus_DBS_cfi")
if localSource:
    process.source = cms.Source("PoolSource", 
                                fileNames = cms.untracked.vstring('file:aod.root')
                                )


# PF2PAT
process.load("PhysicsTools.PFCandProducer.PF2PAT_cff")
# PAT Layer 0+1
process.load("PhysicsTools.PatAlgos.patSequences_cff")

# Configure PAT to use PF2PAT instead of AOD sources
from PhysicsTools.PatAlgos.tools.pfTools import *

# when 'runPF2PAT' is equal True (default is False) PF2PAT is run within patDefaultSequence, otherwise PF2PAT should be run before patDefaultSequence
# addElectrons=True adds standard electrons to configuration and performs standard PAT cleaning wrt electrons (default is False)
usePF2PAT(process,runPF2PAT=True,addElectrons=True)




process.p = cms.Path(
    process.patDefaultSequence  
)

# Output module configuration

from PhysicsTools.PatAlgos.patEventContent_cff import patEventContentNoLayer1Cleaning
process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('patLayer1_fromAOD_PF2PATegammaElectrons_full.root'),
    # save only events passing the full path
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    # save PAT Layer 1 output
    outputCommands = cms.untracked.vstring('drop *', *patEventContentNoLayer1Cleaning ) # you need a '*' to unpack the list of commands 'patEventContentNoLayer1Cleaning'
)
# save PAT Layer 1 output after cleaning
from PhysicsTools.PatAlgos.patEventContent_cff import patEventContent
process.out.outputCommands += cms.untracked.vstring( *patEventContent )

if addPF2PATOutput:
    process.load("PhysicsTools.PFCandProducer.PF2PAT_EventContent_cff")
    process.out.outputCommands.extend( process.PF2PATEventContent.outputCommands)
    process.out.outputCommands.extend( process.PF2PATStudiesEventContent.outputCommands)
    
process.outpath = cms.EndPath(process.out)

# various necessary stuff
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )
process.MessageLogger.cerr.FwkReport.reportEvery = 10

process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string('MC_31X_V1::All')
process.load("Configuration.StandardSequences.MagneticField_cff")
