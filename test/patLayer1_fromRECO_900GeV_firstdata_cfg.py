# This is an example PAT configuration showing the usage of PAT on minbias data

# Starting with a skeleton process which gets imported with the following line
from PhysicsTools.PatAlgos.patTemplate_cfg import *

from PhysicsTools.PatAlgos.tools.coreTools import *

## global tag for data
process.GlobalTag.globaltag = cms.string('GR09_P_V8_34X::All')

# turn off MC matching for the process
removeMCMatching(process, ['All'])

# get the 900 GeV jet corrections
from PhysicsTools.PatAlgos.tools.jetTools import *
switchJECSet( process, "900GeV")

# remove the tag infos
process.allLayer1Jets.addTagInfos = False
# require jet pt > 20 (L2+L3 corrected)
process.selectedLayer1Jets.cut = cms.string('pt > 10')
# look for at least one jet
process.countLayer1Jets.minNumber = 0



# Add the files for runs 123575 and 123596
readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring()

readFiles.extend( [
        '/store/data/BeamCommissioning09/MinimumBias/RAW-RECO/SD_InterestingEvents-Dec19thSkim_341_v1/0006/5A5773A3-B9ED-DE11-A99A-0026189437F8.root',
        '/store/data/BeamCommissioning09/MinimumBias/RAW-RECO/SD_InterestingEvents-Dec19thSkim_341_v1/0006/CA156CCC-B9ED-DE11-B022-00261894390B.root'
        ] );
process.source.fileNames = readFiles

# let it run
process.p = cms.Path(
    process.patDefaultSequence
    )

# rename output file
process.out.fileName = cms.untracked.string('rereco_900GeV_firstdata_pat.root')

# reduce verbosity
process.MessageLogger.cerr.FwkReport.reportEvery = cms.untracked.int32(1000)

# process all the events
process.maxEvents.input = 1000
process.options.wantSummary = True


from Configuration.EventContent.EventContent_cff import RECOEventContent
from PhysicsTools.PatAlgos.patEventContent_cff import *
process.out.outputCommands += (['drop *_*_*_*'])
process.out.outputCommands += RECOEventContent.outputCommands
process.out.outputCommands += patEventContent
process.out.outputCommands += patEventContentNoLayer1Cleaning

