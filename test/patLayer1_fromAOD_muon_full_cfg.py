# import skeleton process
from PhysicsTools.PatAlgos.patTemplate_cfg import *

# extraction of muon sequences
process.load("PhysicsTools.PatAlgos.producersLayer1.muonProducer_cff")
process.load("PhysicsTools.PatAlgos.selectionLayer1.muonSelector_cfi")

# note that you can use a bunch of core tools of PAT 
# to taylor your PAT configuration; for a few examples
# uncomment the following lines

from PhysicsTools.PatAlgos.tools.coreTools import *
useAODInputFor(process, ['Muons'])

# let it run
process.p = cms.Path(
    process.makeAllLayer1Muons *
    process.selectedLayer1Muons
)

# In addition you usually want to change the following parameters:
#
#   process.GlobalTag.globaltag =  ...      (according to https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideFrontierConditions)
#   process.source.fileNames = [ ... ]      (e.g. 'file:AOD.root')
#   process.maxEvents.input = ...           (e.g. -1 to run on all events)
#   process.out.outputCommands = [ ... ]    (e.g. taken from PhysicsTools/PatAlgos/python/patEventContent_cff.py)
#   process.out.fileName = ...              (e.g. 'myTuple.root')
#   process.options.wantSummary = False     (to suppress the long output at the end of the job)

