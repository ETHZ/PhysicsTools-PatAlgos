# This is an example PAT configuration showing the usage of PF2PAT+PAT on minbias data

# Starting with a skeleton process which gets imported with the following line
from PhysicsTools.PatAlgos.patTemplate_cfg import *

## global tag for data
process.GlobalTag.globaltag = cms.string('GR09_P_V8_34X::All')

# the source is already defined in patTemplate_cfg.
# overriding source and various other things
# Add the files for runs 123575 and 123596
readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring()

readFiles.extend( [
    '/store/data/BeamCommissioning09/MinimumBias/RAW-RECO/SD_InterestingEvents-Dec19thSkim_341_v1/0006/5A5773A3-B9ED-DE11-A99A-0026189437F8.root',
    '/store/data/BeamCommissioning09/MinimumBias/RAW-RECO/SD_InterestingEvents-Dec19thSkim_341_v1/0006/CA156CCC-B9ED-DE11-B022-00261894390B.root'
    ] );
process.source.fileNames = readFiles

process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(False))

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.out.fileName = cms.untracked.string('patLayer1_fromAOD_PF2PAT_900GeV_firstdata.root')

# load the PAT config
process.load("PhysicsTools.PatAlgos.patSequences_cff")

# Configure PAT to use PF2PAT instead of AOD sources
# this function will modify the PAT sequences. It is currently 
# not possible to run PF2PAT+PAT and standart PAT at the same time
from PhysicsTools.PatAlgos.tools.pfTools import *

usePF2PAT(process,runPF2PAT=True, jetAlgo='IC5') 
# turn off MC matching for the process
process.PF2PAT.remove(process.genForPF2PATSequence)
removeMCMatching(process, 'All' )

# get the 900 GeV jet corrections
from PhysicsTools.PatAlgos.tools.jetTools import *
switchJECSet( process, "900GeV")

# remove the tag infos
process.allLayer1Jets.addTagInfos = False
# require jet pt > 10 (L2+L3 corrected)
process.selectedLayer1Jets.cut = cms.string('pt > 10')
# look for at least one jet
#process.countLayer1Jets.minNumber = 0
# add the trigger information to the configuration
from PhysicsTools.PatAlgos.tools.trigTools import *
switchOnTrigger( process )
# remove the dtrigger matches
process.patTriggerSequence.remove( process.patTriggerMatcher )
process.patTriggerEvent.patTriggerMatches = []

# Let it run
process.p = cms.Path(
    process.patDefaultSequence  
)

# Add PF2PAT output to the created file
from PhysicsTools.PatAlgos.patEventContent_cff import *
process.load("PhysicsTools.PFCandProducer.PF2PAT_EventContent_cff")
process.out.outputCommands =  cms.untracked.vstring('drop *')
process.out.outputCommands.extend( process.PATEventContent.outputCommands)
process.out.outputCommands += patEventContentTriggerMatch
process.out.outputCommands += patTriggerStandAloneEventContent
process.out.outputCommands += patTriggerEventContent

# In addition you usually want to change the following parameters:
#
#   process.GlobalTag.globaltag =  ...      (according to https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideFrontierConditions)
#   process.source.fileNames = [ ... ]      (e.g. 'file:AOD.root')
#   process.maxEvents.input = ...           (e.g. -1 to run on all events)
#   process.out.outputCommands = [ ... ]    (e.g. taken from PhysicsTools/PatAlgos/python/patEventContent_cff.py)
#   process.out.fileName = ...              (e.g. 'myTuple.root')
#   process.options.wantSummary = False     (to suppress the long output at the end of the job)

process.MessageLogger.cerr.FwkReport.reportEvery = 1000
