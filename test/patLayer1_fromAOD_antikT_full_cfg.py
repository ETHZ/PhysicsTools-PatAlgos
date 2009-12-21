from PhysicsTools.PatAlgos.patTemplate_cfg import *

from PhysicsTools.PatAlgos.tools.jetTools import *

# uncomment the following lines to switch the standard jet collection
# in PAT (iterativeCone5) to ak5 (anti-kt cone = 0.5)
addJetCollection(process, 
                 cms.InputTag('sisCone5CaloJets'),
                 'SC5',
                 'Calo',
                 doJTA            = True,            
                 doBTagging       = True,            
                 jetCorrLabel     = ('SC5','Calo'),  
                 doType1MET       = True,
                 doL1Cleaning = True,                     
                 doL1Counters = False,                 
                 genJetCollection = cms.InputTag("sisCone5GenJets"),
                 doJetID          = True,
                 jetIdLabel       = "sc5"
                 ) 

process.p = cms.Path(
                process.patDefaultSequence  
            )

# In addition you usually want to change the following parameters:
#
#   process.GlobalTag.globaltag =  ...     ## (according to https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideFrontierConditions)
#   process.source.fileNames = [ ... ]     ## (e.g. 'file:AOD.root')
process.maxEvents.input = 10               ## (e.g. -1 to run on all events)
#   process.out.outputCommands = [ ... ]   ## (e.g. taken from PhysicsTools/PatAlgos/python/patEventContent_cff.py)
#   process.out.fileName = ...             ## (e.g. 'myTuple.root')
process.options.wantSummary = True        ## (to suppress the long output at the end of the job)

