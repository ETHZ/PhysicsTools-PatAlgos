## import skeleton process
from PhysicsTools.PatAlgos.patTemplate_cfg import *

## ------------------------------------------------------
#  NOTE: you can use a bunch of core tools of PAT to
#  taylor your PAT configuration; for a few examples
#  uncomment the lines below
## ------------------------------------------------------
#from PhysicsTools.PatAlgos.tools.coreTools import *

## remove MC matching from the default sequence
#removeMCMatching(process, ['All'])

## remove certain objects from the default sequence
# removeAllPATObjectsBut(process, ['Muons'])
# removeSpecificPATObjects(process, ['Electrons', 'Muons', 'Taus'])

## ------------------------------------------------------
#  NOTE: to run PAT on CMSSW_3_8_X AOD please switch the 
#  use and embedding of bTagInfos for patJets off. These 
#  are not part of the AOD anymore. The bTagDosciminators 
#  supported by the BTag POG are still available and will
#  be embedded.
## ------------------------------------------------------
#process.patJets.addBTagInfo = False
#process.patJets.tagInfoSources = []


## let it run
process.p = cms.Path(
    process.patDefaultSequence
    )


## ------------------------------------------------------
#  In addition you usually want to change the following
#  parameters:
## ------------------------------------------------------
#
#   process.GlobalTag.globaltag = 'GR_R_38X_V15::All' ##  (according to https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideFrontierConditions)
#                                         ##
#   process.source.fileNames = [          ##
#    '/store/data/Run2010B/Mu/AOD/Nov4ReReco_v1/0010/8E202869-33EC-DF11-AD37-485B39800B8A.root'
#   ]                                     ##  (e.g. 'file:AOD.root')
#                                         ##
#   process.maxEvents.input = ...         ##  (e.g. -1 to run on all events)
#                                         ##
#   process.out.outputCommands = [ ... ]  ##  (e.g. taken from PhysicsTools/PatAlgos/python/patEventContent_cff.py)
#                                         ##
#   process.out.fileName = ...            ##  (e.g. 'myTuple.root')
#                                         ##
#   process.options.wantSummary = True    ##  (to suppress the long output at the end of the job)    
