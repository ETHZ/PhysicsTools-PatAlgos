from PhysicsTools.PatAlgos.patTemplate_cfg import *

# PAT Layer 0+1
process.load("PhysicsTools.PatAlgos.patSequences_cff")

from PhysicsTools.PatAlgos.tools.jetTools import *

## ==== Example with CaloJets
switchJetCollection(process, 
        cms.InputTag('sisCone5CaloJets'),  # Jet collection; must be already in the event when patDefaultSequence is executed
        doJTA=True,            # Run Jet-Track association & JetCharge
        doBTagging=True,       # Run b-tagging
        jetCorrLabel=('SC5','Calo'), # example jet correction name; set to None for no JEC
        doType1MET=True,       # recompute Type1 MET using these jets
        genJetCollection=cms.InputTag("sisCone5GenJets")) 

## ==== FOR BASIC JETS
### make some basic jets for testing
# from RecoJets.JetProducers.BasicJetIcone5_cfi import iterativeCone5BasicJets
# process.iterativeCone5BasicJets = iterativeCone5BasicJets.clone(src = cms.InputTag("towerMaker"))
#
### configure PAT
# switchJetCollection(process, 
#        cms.InputTag('iterativeCone5BasicJets'), # Jet collection; must be already in the event patLayer0 sequence is executed
#        doJTA=True,
#        doBTagging=True,
#        jetCorrLabel=None,#=('S5','Calo'), # If you have JES corrections, you can apply them even to BasicJets
#        doType1MET=False)                  # Type1MET dows not work on BasicJets :-(


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

