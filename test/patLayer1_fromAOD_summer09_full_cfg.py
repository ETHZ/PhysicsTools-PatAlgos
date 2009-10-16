from PhysicsTools.PatAlgos.patTemplate_cfg import *

from PhysicsTools.PatAlgos.tools.jetTools import *

from PhysicsTools.PatAlgos.tools.cmsswVersionTools import *

# run the 3.3.x software on Summer 09 MC from 3.1.x:
#   - change the name from "ak" (3.3.x) to "antikt) (3.1.x)
#   - run jet ID (not run in 3.1.x)
run33xOn31xMC( process,
               jetSrc = cms.InputTag("antikt5CaloJets"),
               jetIdTag = "antikt5"
               )

from PhysicsTools.PatAlgos.tools.coreTools import *
#restrictInputToAOD(process)
#removeMCMatching(process, 'Muons')
#removeAllPATObjectsBut(process, ['Muons'])
#removeSpecificPATObjects(process, ['Electrons', 'Muons', 'Taus'])

#addJetID( process, "sisCone5CaloJets", "sc5")
#from PhysicsTools.PatAlgos.tools.jetTools import *
#addJetCollection(process,cms.InputTag('sisCone5CaloJets'),
#                 'SC5',
#                 doJTA        = True,
#                 doBTagging   = True,
#                 jetCorrLabel = ('SC5','Calo'),
#                 doType1MET   = True,
#                 doL1Cleaning = True,                 
#                 doL1Counters = False,
#                 genJetCollection=cms.InputTag("sisCone5GenJets"),
#                 doJetID      = True,
#                 jetIdLabel   = "sc5"
#                 )

process.p = cms.Path(
                process.patDefaultSequence  
            )

# In addition you usually want to change the following parameters:
#
#   process.GlobalTag.globaltag =  ...     ## (according to https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideFrontierConditions)
#   process.source.fileNames = [ ... ]     ## (e.g. 'file:AOD.root')
#   process.out.outputCommands = [ ... ]   ## (e.g. taken from PhysicsTools/PatAlgos/python/patEventContent_cff.py)
#   process.out.fileName = ...             ## (e.g. 'myTuple.root')
process.options.wantSummary = True        ## (to suppress the long output at the end of the job)

process.source.fileNames = [
    '/store/relval/CMSSW_3_1_4/RelValTTbar/GEN-SIM-RECO/MC_31X_V3-v1/0005/901ABD8A-E5B0-DE11-8AE6-000423D98DD4.root'
    ]
process.maxEvents.input = 50         ##  (e.g. -1 to run on all events)
