import FWCore.ParameterSet.Config as cms

process = cms.Process("PAT")

# initialize MessageLogger and output report
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

# source
process.source = cms.Source("PoolSource", 
     fileNames = cms.untracked.vstring('/store/relval/CMSSW_3_1_0_pre6/RelValTTbar/GEN-SIM-RECO/IDEAL_31X_v1/0002/50D4BADB-FA32-DE11-BA01-000423D98DC4.root')
)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )


# PAT Layer 0+1
process.load("PhysicsTools.PatAlgos.patSequences_cff")

process.allLayer1Electrons.addElectronShapes = False
process.allLayer1Electrons.addElectronID     = False

## Load additional RECO config
process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string('IDEAL_31X::All')
process.load("Configuration.StandardSequences.MagneticField_cff")

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

process.content = cms.EDAnalyzer("EventContentAnalyzer")
process.p = cms.Path(
                ## FIXME process.iterativeCone5BasicJets +  ## Turn on this to run tests on BasicJets
                process.patDefaultSequence  
                #+ process.content    # uncomment to get a dump 
            )


# Output module configuration
process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('PATLayer1_Output.fromAOD_jetSuite_full.root'),
    # save only events passing the full path
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    outputCommands = cms.untracked.vstring('drop *')
)
process.outpath = cms.EndPath(process.out)
# save PAT Layer 1 output
from PhysicsTools.PatAlgos.patEventContent_cff import *
process.out.outputCommands += patEventContent
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
