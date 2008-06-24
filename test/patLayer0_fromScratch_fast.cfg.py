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

# FAMOS source
process.load("PhysicsTools.PatAlgos.famos.famosSequences_cff")
process.load("PhysicsTools.PatAlgos.famos.boostrapWithFamos_cff")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

# PAT Layer 0
process.load("PhysicsTools.PatAlgos.patLayer0_cff")
#process.content = cms.EDAnalyzer("EventContentAnalyzer")
process.p = cms.Path(
                process.famosWithEverythingPAT +     # run full FAMOS (ttbar events)
                #process.content               +     # to get a dump of the output of FAMOS
                process.patLayer0_withoutTrigMatch # PAT Layer 0, no trigger matching
            )

from PhysicsTools.PatAlgos.famos import patLayer0_FamosSetup_cff
patLayer0_FamosSetup_cff.setup(process) # apply 'replace' statements for Layer 0

# Output module configuration
process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('PATLayer0_Output.fromScratch_fast.root'),
    # save only events passing the full path
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    outputCommands = cms.untracked.vstring('drop *')
)
process.outpath = cms.EndPath(process.out)
# save PAT Layer 0 output
process.load("PhysicsTools.PatAlgos.patLayer0_EventContent_cff")
process.out.outputCommands.extend(process.patLayer0EventContent.outputCommands)

