# This is an example PAT configuration showing what exactly gets run for electrons

# Starting with a skeleton process which gets imported with the following line
from PhysicsTools.PatAlgos.patTemplate_cfg import *

# extract the electron sequences
process.load("PhysicsTools.PatAlgos.recoLayer0.electronId_cff")
process.load("PhysicsTools.PatAlgos.recoLayer0.electronIsolation_cff")
process.load("PhysicsTools.PatAlgos.recoLayer0.duplicatedElectrons_cfi")
process.load("PhysicsTools.PatAlgos.mcMatchLayer0.mcMatchSequences_cff")
process.load("PhysicsTools.PatAlgos.producersLayer1.electronProducer_cfi")

# let it run
process.p = cms.Path(
    process.patElectronId *
    process.patElectronIsolation *
    process.electronMatch *
    process.allLayer1Electrons
)

# In addition you usually want to change the following parameters:
#
#   process.GlobalTag.globaltag =  ...      (according to https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideFrontierConditions)
#   process.source.fileNames = [ ... ]      (e.g. 'file:AOD.root')
#   process.maxEvents.input = ...           (e.g. -1 to run on all events)
#   process.out.outputCommands = [ ... ]    (e.g. taken from PhysicsTools/PatAlgos/python/patEventContent_cff.py)
#   process.out.fileName = ...              (e.g. 'myTuple.root')
#   process.options.wantSummary = False     (to suppress the long output at the end of the job)
