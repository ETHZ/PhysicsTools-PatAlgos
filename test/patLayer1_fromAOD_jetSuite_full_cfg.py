# import skeleton process
from PhysicsTools.PatAlgos.patTemplate_cfg import *


# PAT Layer 0+1
process.load("PhysicsTools.PatAlgos.patSequences_cff")

from PhysicsTools.PatAlgos.tools.jetTools import *

# Taking away BasicJets because RecoJets/JetProducers/python/BasicJetIcone5_cfi.py in 2.2.X is wrong
## FIXME ### make also some basic jets for testing
## FIXME from RecoJets.JetProducers.BasicJetIcone5_cfi import iterativeCone5BasicJets
## FIXME process.iterativeCone5BasicJets = iterativeCone5BasicJets.clone(src = cms.InputTag("towerMaker"))


addJetCollection(process,cms.InputTag('sisCone5CaloJets'),'SC5',
                        doJTA=True,doBTagging=True,jetCorrLabel=('SC5','Calo'),doType1MET=True,doL1Counters=False,
                        genJetCollection=cms.InputTag("sisCone5GenJets"))
##addJetCollection(process,cms.InputTag('sisCone7CaloJets'),'SC7',
##                        doJTA=True,doBTagging=False,jetCorrLabel=None,doType1MET=True,doL1Counters=False,
##                        genJetCollection=cms.InputTag("sisCone5GenJets"))
##addJetCollection(process,cms.InputTag('kt4CaloJets'),'KT4',
##                        doJTA=True,doBTagging=True,jetCorrLabel=('KT4','Calo'),doType1MET=True,doL1Counters=False,
##                        genJetCollection=cms.InputTag("kt4GenJets"))
##addJetCollection(process,cms.InputTag('kt6CaloJets'),'KT6',
##                        doJTA=True,doBTagging=False,jetCorrLabel=None,doType1MET=True,doL1Counters=False,
##                        genJetCollection=cms.InputTag("kt6GenJets"))
## FIXME addJetCollection(process,cms.InputTag('iterativeCone5BasicJets'), 'BJ5',
## FIXME                        doJTA=True,doBTagging=True,jetCorrLabel=('MC5','Calo'),doType1MET=True,doL1Counters=False)
##addJetCollection(process,cms.InputTag('iterativeCone5PFJets'), 'PFc',
##                        doJTA=True,doBTagging=True,jetCorrLabel=None,doType1MET=True,doL1Counters=False,
##                        genJetCollection=cms.InputTag("iterativeCone5GenJets"))
##addJetCollection(process,cms.InputTag('iterativeCone5PFJets'), 'PFr',
##                        doJTA=True,doBTagging=True,jetCorrLabel=None,doType1MET=True,doL1Counters=False,
##                        genJetCollection=cms.InputTag("iterativeCone5GenJets"))

process.p = cms.Path(
                process.patDefaultSequence  
            )


process.out.outputCommands += ["keep *_selectedLayer1Jets*_*_*", "keep *_layer1METs*_*_*"]

#### Dump the python config
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
