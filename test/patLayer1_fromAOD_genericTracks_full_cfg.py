import FWCore.ParameterSet.Config as cms

process = cms.Process("PAT")

# initialize MessageLogger and output report
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

# source
process.source = cms.Source("PoolSource", 
     fileNames = cms.untracked.vstring('/store/relval/CMSSW_3_1_0_pre6/RelValTTbar/GEN-SIM-RECO/IDEAL_31X_v1/0002/50D4BADB-FA32-DE11-BA01-000423D98DC4.root')
)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )


process.load("Configuration.StandardSequences.Geometry_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.GlobalTag.globaltag = cms.string('IDEAL_31X::All')
process.load("Configuration.StandardSequences.MagneticField_cff")

# PAT Layer 0+1
process.load("PhysicsTools.PatAlgos.patSequences_cff")

from PhysicsTools.PatAlgos.tools.trackTools import *
makeTrackCandidates(process, 
        label='TrackCands',                   # output collection will be 'allLayer0TrackCands', 'allLayer1TrackCands', 'selectedLayer1TrackCands'
        tracks=cms.InputTag('generalTracks'), # input track collection
        particleType="pi+",                   # particle type (for assigning a mass)
        preselection='pt > 10',               # preselection cut on candidates. Only methods of 'reco::Candidate' are available
        selection='pt > 10',                  # Selection on PAT Layer 1 objects ('selectedLayer1TrackCands')
        isolation={'tracker':0.3,             # Isolations to use ('source':deltaR; set to {} for None)
                   'ecalTowers':0.3,          # 'tracker' => as muon track iso
                   'hcalTowers':0.3},         # 'ecalTowers', 'hcalTowers' => as muon iso from calo towers.
        isodeposits=[],                       # examples: 'tracker','ecalTowers','hcalTowers'; [] = empty list = none   
        mcAs=cms.InputTag("muons")            # Replicate MC match as the one used by PAT on this AOD collection (None = no mc match)
        );                                    #  you can specify more than one collection for this

process.p = cms.Path(
        process.patDefaultSequence 
)

# Output module configuration
process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('PATLayer1_Output.fromAOD_genericTracks_full.root'),
    # save only events passing the full path
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    outputCommands = cms.untracked.vstring('drop *')
)
process.outpath = cms.EndPath(process.out)
# save PAT Layer 1 output
from PhysicsTools.PatAlgos.patEventContent_cff import *
process.out.outputCommands += patEventContent 
process.out.outputCommands.append('keep *_selectedLayer1TrackCands_*_*')

#### Dump the python config
#
# f = open("patLayer1_fromAOD_genericTracks_full.dump.py", "w")
# f.write(process.dumpPython())
# f.close()
#
 
