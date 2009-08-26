


# This is an example PAT configuration showing the usage of PF2PAT

# Starting with a skeleton process which gets imported with the following line
from PhysicsTools.PatAlgos.patTemplate_cfg import *

# overriding source and various other things
#process.load("PhysicsTools.PFCandProducer.Sources.source_ZtoEles_DBS_312_cfi")
process.load("PhysicsTools.PFCandProducer.Sources.source_ZtoMus_DBS_cfi")
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False))

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.out.fileName = cms.untracked.string('patLayer1_fromAOD_PF2PAT_full.root')

# load the standard PAT config
process.load("PhysicsTools.PatAlgos.patSequences_cff")

# load the PF to PAT config
process.load("PhysicsTools.PFCandProducer.PF2PAT_cff")

# Configure PAT to use PF2PAT instead of AOD sources
from PhysicsTools.PatAlgos.tools.pfTools import *
usePF2PAT(process,runPF2PAT=True, addElectrons=True)  # or you can leave this to the default, False, and run PF2PAT before patDefaultSequence

# Let it run
process.p = cms.Path(
    process.patDefaultSequence  
)

process.allLayer1Electrons.embedGenMatch = True
process.allLayer1Muons.embedGenMatch = True

# Add PF2PAT output to the created file
from PhysicsTools.PatAlgos.patEventContent_cff import patEventContentNoLayer1Cleaning
process.load("PhysicsTools.PFCandProducer.PF2PAT_EventContent_cff")
process.out.outputCommands =  cms.untracked.vstring('drop *')
process.out.outputCommands.extend( process.PATEventContent.outputCommands)


# In addition you usually want to change the following parameters:
#
#   process.GlobalTag.globaltag =  ...      (according to https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideFrontierConditions)
#   process.source.fileNames = [ ... ]      (e.g. 'file:AOD.root')
#   process.maxEvents.input = ...           (e.g. -1 to run on all events)
#   process.out.outputCommands = [ ... ]    (e.g. taken from PhysicsTools/PatAlgos/python/patEventContent_cff.py)
#   process.out.fileName = ...              (e.g. 'myTuple.root')
#   process.options.wantSummary = False     (to suppress the long output at the end of the job)

process.MessageLogger.cerr.FwkReport.reportEvery = 100
