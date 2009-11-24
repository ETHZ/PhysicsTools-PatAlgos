# This is an example PAT configuration showing the usage of PAT on minbias data

# Starting with a skeleton process which gets imported with the following line
from PhysicsTools.PatAlgos.patTemplate_cfg import *

from PhysicsTools.PatAlgos.tools.coreTools import *


#switch off new tau features introduced in 33X to restore 31X defaults
# new feaures: - shrinkingConeTaus instead of fixedCone ones
#              - TaNC discriminants attached for shrinkingConeTaus
#              - default preselection on cleaningLayer1
from PhysicsTools.PatAlgos.tools.tauTools import *
switchTo31Xdefaults(process)

# turn off MC matching for the process
removeMCMatching(process, 'All')

# let it run
process.p = cms.Path(
    process.patDefaultSequence
    )


# Add the files for run 122314
readFiles = cms.untracked.vstring()
secFiles = cms.untracked.vstring()

readFiles.extend( [
       '/store/data/BeamCommissioning09/MinimumBias/RECO/v2/000/122/314/F62B040F-6CD8-DE11-9007-001D09F24664.root',
       '/store/data/BeamCommissioning09/MinimumBias/RECO/v2/000/122/314/F4387297-74D8-DE11-996C-001D09F24F1F.root',
       '/store/data/BeamCommissioning09/MinimumBias/RECO/v2/000/122/314/EE7B1AC4-6CD8-DE11-97BB-0030487A1FEC.root',
       '/store/data/BeamCommissioning09/MinimumBias/RECO/v2/000/122/314/9264A28F-87D8-DE11-83A1-001D09F24763.root',
       '/store/data/BeamCommissioning09/MinimumBias/RECO/v2/000/122/314/7C7495C2-71D8-DE11-ACF2-001D09F248F8.root',
       '/store/data/BeamCommissioning09/MinimumBias/RECO/v2/000/122/314/4CAB3B6C-6BD8-DE11-845C-000423D9890C.root',
       '/store/data/BeamCommissioning09/MinimumBias/RECO/v2/000/122/314/02E8544C-70D8-DE11-85CF-001617C3B66C.root' ] );
process.source.fileNames = readFiles
process.source.firstRun = cms.untracked.uint32(122314)

# process all the events
process.maxEvents.input = -1
process.options.wantSummary = True        ##  (to suppress the long output at the end of the job)    
