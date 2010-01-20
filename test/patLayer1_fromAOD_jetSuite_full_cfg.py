# import skeleton process
from PhysicsTools.PatAlgos.patTemplate_cfg import *

# uncomment the following line to add tcMET to the event content
from PhysicsTools.PatAlgos.tools.metTools import *
addTcMET(process, 'TC')
addPfMET(process, 'PF')

# uncomment the following line to add different jet collections
# to the event content
from PhysicsTools.PatAlgos.tools.jetTools import *

# produce jpt corrected calo jets, which are not on AOD per default
process.load("PhysicsTools.PatAlgos.recoLayer0.jetPlusTrack_cff")
process.jpt = cms.Path(
    process.jptCaloJets
)

# uncomment the following lines to add ak7Calo jets to your PAT output
addJetCollection(process,cms.InputTag('ak7CaloJets'),
                 'AK7', 'Calo',
                 doJTA        = True,
                 doBTagging   = False,
                 jetCorrLabel = None,
                 doType1MET   = True,
                 doL1Cleaning = True,                 
                 doL1Counters = False,
                 genJetCollection=cms.InputTag("ak7GenJets"),
                 doJetID      = True,
                 jetIdLabel   = "ak7"
                 )

# uncomment the following lines to add iterativeCone5JPT jets to
# your PAT output
addJetCollection(process,cms.InputTag('JetPlusTrackZSPCorJetIcone5'),
                 'IC5', 'JPT',
                 doJTA        = True,
                 doBTagging   = True,
#                jetCorrLabel = ('IC5','JPT'), ## this still needs completion of correction factors by JetMET
                 jetCorrLabel = None,
                 doType1MET   = False,
                 doL1Cleaning = False,
                 doL1Counters = True,                 
                 genJetCollection = cms.InputTag("iterativeCone5GenJets"),
                 doJetID      = False
                 )

# uncomment the following lines to add sisCone5PF jets to your PAT output
addJetCollection(process,cms.InputTag('sisCone5PFJets'),
                 'SC5', 'PF',
                 doJTA        = True,
                 doBTagging   = True,
                 jetCorrLabel = ('SC5','PF'),
                 doType1MET   = True,
                 doL1Cleaning = True,                 
                 doL1Counters = False,
                 genJetCollection=cms.InputTag("sisCone5GenJets"),
                 doJetID      = True,
                 jetIdLabel   = "sc5"
                 )

# uncomment the following lines to add sisCone7Calo jets to your PAT output
addJetCollection(process,cms.InputTag('sisCone7CaloJets'),
                 'SC7', 'Calo',
                 doJTA        = True,
                 doBTagging   = False,
                 jetCorrLabel = None,
                 doType1MET   = True,
                 doL1Cleaning = True,                 
                 doL1Counters = False,
                 genJetCollection=cms.InputTag("sisCone5GenJets"),
                 doJetID      = True,
                 jetIdLabel   = "sc7"
                 )

# uncomment the following lines to add kt4Calo jets to your PAT output
addJetCollection(process,cms.InputTag('kt4CaloJets'),
                 'KT4', 'Calo',
                 doJTA        = True,
                 doBTagging   = True,
                 jetCorrLabel = ('KT4','Calo'),
                 doType1MET   = True,
                 doL1Cleaning = True,                 
                 doL1Counters = False,
                 genJetCollection=cms.InputTag("kt4GenJets"),
                 doJetID      = True,
                 jetIdLabel   = "kt4"
                 )

# uncomment the following lines to add kt6Calo jets to your PAT output
addJetCollection(process,cms.InputTag('kt6CaloJets'),
                 'KT6', 'Calo',
                 doJTA        = True,
                 doBTagging   = False,
                 jetCorrLabel = None,
                 doType1MET   = True,
                 doL1Cleaning = True,                 
                 doL1Counters = False,
                 genJetCollection=cms.InputTag("kt6GenJets"),
                 doJetID      = True,
                 jetIdLabel   = "kt6"
                 )

# uncomment the following lines to add iterativeCone5Pflow jets to your PAT output
switchJetCollection(process,cms.InputTag('sisCone5PFJets'),
                 doJTA        = True,
                 doBTagging   = True,
                 jetCorrLabel = ('SC5','PF'),
                 doType1MET   = True,
                 genJetCollection=cms.InputTag("iterativeCone5GenJets"),
                 doJetID      = True
                 )

process.p = cms.Path(
    process.patDefaultSequence
)

# In addition you usually want to change the following parameters:
#
#   process.GlobalTag.globaltag =  ...   ## (according to https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideFrontierConditions)
#   process.source.fileNames = [ ... ]   ## (e.g. 'file:AOD.root')
process.maxEvents.input = 10             ## (e.g. -1 to run on all events)
#   process.out.outputCommands = [ ... ] ## (e.g. taken from PhysicsTools/PatAlgos/python/patEventContent_cff.py)
#   process.out.fileName = ...           ## (e.g. 'myTuple.root')
process.options.wantSummary = True       ## (to suppress the long output at the end of the job)    



#### The following lines are meant for debigging only ####

#
#f = open("patLayer1_fromAOD_jetSuite_full.dump.py", "w")
#f.write(process.dumpPython())
#f.close()
#

#### GraphViz dumps of sequences and modules, useful for debugging.
#### WARNING: it's not for the weak-hearted; the output plot is HUGE
#### needs a version of 'dot' that works with png graphics. 
#### in case, you can borrw mine with
####   export LD_LIBRARY_PATH=/afs/cern.ch/user/g/gpetrucc/scratch0/graphviz/lib:${LD_LIBRARY_PATH}
####   export PATH=/afs/cern.ch/user/g/gpetrucc/scratch0/graphviz/bin:${PATH}
#
# from PhysicsTools.PatAlgos.tools.circuitry import *
# plotSequences(   process.p, 'patSequences.png')
# plotModuleInputs(process.p, 'patModules.png'  ,printOuter=False,printLinkNames=True)  # no nodes for non-PAT modules
