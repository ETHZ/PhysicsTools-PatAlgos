from PhysicsTools.PatAlgos.patTemplate_cfg import *

# load the standard PAT config 
process.load("PhysicsTools.PatAlgos.patSequences_cff")

from PhysicsTools.PatAlgos.tools.jetTools import *

# uncomment the following lines to switch the standard jet collection
# in PAT (iterativeCone5) to ak5 (anti-kt cone = 0.5)
switchJetCollection(process, 
                    cms.InputTag('antikt5CaloJets'),   
                    doJTA            = True,            
                    doBTagging       = True,            
                    jetCorrLabel     = ('AK5','Calo'),  
                    doType1MET       = True,            
                    genJetCollection = cms.InputTag("antikt5GenJets")
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
process.options.wantSummary = False        ## (to suppress the long output at the end of the job)

