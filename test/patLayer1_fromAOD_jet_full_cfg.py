# This is an example PAT configuration showing the workflow for jets

# Starting with a skeleton process which gets imported with the following line
from PhysicsTools.PatAlgos.patTemplate_cfg import *

# extraction of jet sequences
process.load("PhysicsTools.PatAlgos.recoLayer0.bTagging_cff")         ## empty
process.load("PhysicsTools.PatAlgos.recoLayer0.jetTracksCharge_cff")
process.load("PhysicsTools.PatAlgos.recoLayer0.jetMETCorrections_cff")
process.load("PhysicsTools.PatAlgos.mcMatchLayer0.mcMatchSequences_cff")
process.load("PhysicsTools.PatAlgos.producersLayer1.jetProducer_cfi")

process.p = cms.Path(
     process.patJetCharge *  
     process.patJetCorrections *
     process.jetPartonMatch *
     process.jetGenJetMatch *
     process.jetFlavourId *  
     process.allLayer1Jets
)

# In addition you usually want to change the following parameters:
#
#   process.GlobalTag.globaltag =  ...      (according to https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideFrontierConditions)
#   process.source.fileNames = [ ... ]      (e.g. 'file:AOD.root')
#   process.maxEvents.input = ...           (e.g. -1 to run on all events)
#   process.out.outputCommands = [ ... ]    (e.g. taken from PhysicsTools/PatAlgos/python/patEventContent_cff.py)
#   process.out.fileName = ...              (e.g. 'myTuple.root')
#   process.options.wantSummary = False     (to suppress the long output at the end of the job)
