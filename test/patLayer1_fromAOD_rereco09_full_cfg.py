from PhysicsTools.PatAlgos.patTemplate_cfg import *

from PhysicsTools.PatAlgos.tools.jetTools import *

from PhysicsTools.PatAlgos.tools.cmsswVersionTools import *

# run the 3.3.x software on Summer 09 MC from 3.1.x,
#   re-recoed with 3.3.2:
#     - Run GenJets for process in question
run33xOnReRecoMC( process, "ak5GenJets" )

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
    '/store/mc/Summer09/QCDDiJet_Pt2600to3000/GEN-SIM-RECO/MC_31X_V9_7TeV-v1/0001/F8C20DCD-5FCA-DE11-AFF0-001E0BE922E2.root'
    ]
process.maxEvents.input = 50         ##  (e.g. -1 to run on all events)
