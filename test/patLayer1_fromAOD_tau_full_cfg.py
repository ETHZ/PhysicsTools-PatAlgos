# import skeleton process
from PhysicsTools.PatAlgos.patTemplate_cfg import *

# extraction of tau sequences
process.load("PhysicsTools.JetMCAlgos.TauGenJets_cfi")
process.load("PhysicsTools.PatAlgos.mcMatchLayer0.tauMatch_cfi")
process.load("PhysicsTools.PatAlgos.recoLayer0.pfCandidateIsoDepositSelection_cff")
process.load("PhysicsTools.PatAlgos.recoLayer0.tauIsolation_cff")
process.load("PhysicsTools.PatAlgos.recoLayer0.tauDiscriminators_cff")  ##missing modules and inputs
process.load("PhysicsTools.PatAlgos.producersLayer1.tauProducer_cfi")
process.content = cms.EDAnalyzer("EventContentAnalyzer")

# run it
process.p = cms.Path(
    process.patPFCandidateIsoDepositSelection +
    process.patPFTauIsolation +
    process.tauMatch +
    process.tauGenJets +
    process.tauGenJetMatch +
    process.allLayer1Taus 
)

# In addition you usually want to change the following parameters:
#
#   process.GlobalTag.globaltag =  ...      (according to https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideFrontierConditions)
#   process.source.fileNames = [ ... ]      (e.g. 'file:AOD.root')
#   process.maxEvents.input = ...           (e.g. -1 to run on all events)
#   process.out.outputCommands = [ ... ]    (e.g. taken from PhysicsTools/PatAlgos/python/patEventContent_cff.py)
#   process.out.fileName = ...              (e.g. 'myTuple.root')
#   process.options.wantSummary = False     (to suppress the long output at the end of the job)
