# This is an example PAT configuration showing the usage of PAT with PF2PAT on its input

# Starting with a skeleton process which gets imported with the following line
from PhysicsTools.PatAlgos.patTemplate_cfg import *

# the source is already defined in patTemplate_cfg.
# overriding source and various other things
process.source.fileNames = cms.untracked.vstring('file:PF2PAT.root')

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )


process.out.fileName = cms.untracked.string('patLayer1_fromPF2PAT.root')

# load the PAT config
process.load("PhysicsTools.PatAlgos.patSequences_cff")

# Configure PAT to use PF2PAT instead of AOD sources
# this function will modify the PAT sequences. It is currently 
# not possible to run PF2PAT+PAT and standart PAT at the same time
from PhysicsTools.PatAlgos.tools.pfTools import *
tauTypeInPF2PAT(process,"fixedConePFTau")# which tau type is used by PF2PAT (impossible to deduce from configuration)
usePF2PAT(process,runPF2PAT=False)

# Let it run
process.p = cms.Path(
    process.patDefaultSequence  
)

process.patElectrons.embedGenMatch = True
process.patMuons.embedGenMatch = True

# Add PF2PAT output to the created file
from PhysicsTools.PatAlgos.patEventContent_cff import patEventContentNoCleaning
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

process.MessageLogger.cerr.FwkReport.reportEvery = 10
