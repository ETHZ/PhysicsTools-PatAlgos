# This is an example PAT configuration showing the usage of PAT on fast sim samples

# Starting with a skeleton process which gets imported with the following line
from PhysicsTools.PatAlgos.patTemplate_cfg import *

# load the standard PAT config
process.load("PhysicsTools.PatAlgos.patSequences_cff")

# use a fastsim file as input
process.source.fileNames = cms.untracked.vstring(
   #'/store/relval/CMSSW_3_6_0_pre5/RelValTTbar/GEN-SIM-RECO/MC_36Y_V3-v1/0010/32F0646B-E43D-DF11-B235-003048D3FC94.root'
   '/store/relval/CMSSW_3_6_0_pre6/RelValTTbar/GEN-SIM-RECO/MC_36Y_V4-v1/0011/060537EE-4E45-DF11-AE40-003048679012.root'
)
process.GlobalTag.globaltag = 'MC_3XY_V14::All'

# need to add jetID here as it seems to be missing on the selected file???
#from PhysicsTools.PatAlgos.tools.jetTools import *
#addJetID(process, cms.InputTag('ak5CaloJets'), 'ak5')

# let it run
process.p = cms.Path(
        process.patDefaultSequence
    )


# In addition you usually want to change the following parameters:
#
#   process.GlobalTag.globaltag =  ...      (according to https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideFrontierConditions)
#   process.source.fileNames = [ ... ]      (e.g. 'file:AOD.root')
#   process.maxEvents.input = ...           (e.g. -1 to run on all events)
#   process.out.outputCommands = [ ... ]    (e.g. taken from PhysicsTools/PatAlgos/python/patEventContent_cff.py)
#   process.out.fileName = ...              (e.g. 'myTuple.root')
#   process.options.wantSummary = False     (to suppress the long output at the end of the job)




