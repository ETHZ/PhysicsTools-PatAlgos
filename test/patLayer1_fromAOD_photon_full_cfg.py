# import skeleton process
from PhysicsTools.PatAlgos.patTemplate_cfg import *

# extraction of photon sequences
process.load("PhysicsTools.PatAlgos.producersLayer1.photonProducer_cff")
process.load("PhysicsTools.PatAlgos.selectionLayer1.photonSelector_cfi")

process.p = cms.Path(
    process.makePatPhotons *
    process.selectedPatPhotons    
)

# In addition you usually want to change the following parameters:
#
#   process.GlobalTag.globaltag =  ...      (according to https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideFrontierConditions)
#   process.source.fileNames = [ ... ]      (e.g. 'file:AOD.root')
#   process.maxEvents.input = ...           (e.g. -1 to run on all events)
#   process.out.outputCommands = [ ... ]    (e.g. taken from PhysicsTools/PatAlgos/python/patEventContent_cff.py)
#   process.out.fileName = ...              (e.g. 'myTuple.root')
#   process.options.wantSummary = False     (to suppress the long output at the end of the job)

