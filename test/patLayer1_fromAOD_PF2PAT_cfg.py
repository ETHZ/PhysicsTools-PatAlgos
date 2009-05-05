import FWCore.ParameterSet.Config as cms


process = cms.Process("PAT")

process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string('STARTUP_V7::All')
process.load("Configuration.StandardSequences.MagneticField_cff")
process.load("PhysicsTools.PFCandProducer.PF2PAT_cff")
process.load("PhysicsTools.PatAlgos.patSequences_cff")



##########################################################################

# source: 

process.source = cms.Source("PoolSource", 
                            fileNames = cms.untracked.vstring('file:/afs/cern.ch/cms/PRS/top/cmssw-data/relval200-for-pat-testing/FullSimTTBar-2_2_X_2008-11-03-STARTUP_V7-AODSIM.100.root')
                            # fileNames = cms.untracked.vstring('file:aod.root')
)

# in case you are using fast sim input, please specify it!
# jet corrections are different in the fast sim, and will be
# replaced if needed.
fromFastSim = True

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

# verbosity:

process.pfTopProjection.verbose = False


# output:

outputFile = 'patLayer1_fromAOD_PF2PAT.root'
addPF2PATProducts = False


##########################################################################
# Don't modify anything below this line unless you know what you are doing. 

from PhysicsTools.PatAlgos.tools.jetTools import *
if fromFastSim == True:
    switchJECSet(process,newName='Winter09',oldName='Summer08Redigi') 
  

#process.content = cms.EDAnalyzer("EventContentAnalyzer")

# Configure PAT to use PF2PAT instead of AOD sources
from PhysicsTools.PatAlgos.tools.pfTools import *
usePF2PAT(process,runPF2PAT=True)  # or you can leave this to the default, False, and run PF2PAT before patDefaultSequence
# Switch off old trigger matching
from PhysicsTools.PatAlgos.tools.trigTools import switchOffTriggerMatchingOld
switchOffTriggerMatchingOld( process )

process.p = cms.Path(
    process.patDefaultSequence  
)

# Output module configuration
from PhysicsTools.PatAlgos.patEventContent_cff import patEventContentNoLayer1Cleaning
from PhysicsTools.PFCandProducer.PF2PAT_EventContent_cff import PF2PATEventContent
process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string( outputFile ),
    # save only events passing the full path
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    # save PAT Layer 1 output
    outputCommands = cms.untracked.vstring('drop *', *patEventContentNoLayer1Cleaning ) # you need a '*' to unpack the list of commands 'patEventContentNoLayer1Cleaning'
)

if addPF2PATProducts:
    process.out.outputCommands.extend( PF2PATEventContent.outputCommands )

process.outpath = cms.EndPath(process.out)


# initialize MessageLogger and output report
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.categories.append('PATSummaryTables')
process.MessageLogger.cerr.INFO = cms.untracked.PSet(
    default          = cms.untracked.PSet( limit = cms.untracked.int32(0)  ),
    PATSummaryTables = cms.untracked.PSet( limit = cms.untracked.int32(-1) )
)
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False) )

