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
    '/store/mc/Summer09/TTbar/GEN-SIM-RECO/MC_31X_V3-v1/0025/48AC6C31-AA88-DE11-B02C-0030487C6F54.root',
    '/store/mc/Summer09/TTbar/GEN-SIM-RECO/MC_31X_V3-v1/0025/9E80A46A-AA88-DE11-94BD-001E682F882A.root',
    '/store/mc/Summer09/TTbar/GEN-SIM-RECO/MC_31X_V3-v1/0025/6004FF4C-AA88-DE11-B0BF-001E68A9941C.root',
    '/store/mc/Summer09/TTbar/GEN-SIM-RECO/MC_31X_V3-v1/0025/129A0B85-AA88-DE11-B08A-001E6837DFEA.root'
    ]
process.maxEvents.input = 50         ##  (e.g. -1 to run on all events)
