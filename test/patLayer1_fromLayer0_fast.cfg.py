import FWCore.ParameterSet.Config as cms

process = cms.Process("PATLayer1")

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
     fileNames = cms.untracked.vstring('file:PATLayer0_Output.fromAOD_fast.root')
)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )


# PAT Layer 1
process.load("PhysicsTools.PatAlgos.patLayer0_cff") # need to load this too
process.load("PhysicsTools.PatAlgos.patLayer1_cff") # even if we run only layer 1

## Load additional RECO config
# Magnetic field now needs to be in the high-level py
process.load("Configuration.StandardSequences.MagneticField_cff")



#process.content = cms.EDAnalyzer("EventContentAnalyzer")
process.p = cms.Path(
#                process.content   +  # to get a dump of the event content
                process.patLayer1    # PAT Layer 1
            )

from PhysicsTools.PatAlgos.famos import patLayer1_FamosSetup_cff
patLayer1_FamosSetup_cff.setup(process) # apply 'replace' statements for Layer 1

# Output module configuration
process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('PATLayer1_Output.fromLayer0_fast.root'),
    # save only events passing the full path
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    outputCommands = cms.untracked.vstring('drop *')
)
process.outpath = cms.EndPath(process.out)
# save PAT Layer 1 output
process.load("PhysicsTools.PatAlgos.patLayer1_EventContent_cff")
process.out.outputCommands.extend(process.patLayer1EventContent.outputCommands)

