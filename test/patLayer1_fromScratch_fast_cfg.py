import FWCore.ParameterSet.Config as cms

process = cms.Process("PAT")

# initialize MessageLogger and output report
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

# FAMOS source
process.load("FastSimulation.Configuration.ttbar_cfi")
# some FAMOS setup (FIXME maybe this should go)
process.load("PhysicsTools.PatAlgos.famos.boostrapWithFamos_cff")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

## Standard PAT Configuration File
process.load("PhysicsTools.PatAlgos.patSequences_cff")

from PhysicsTools.PatAlgos.tools.jetTools import *
print "*********************************************************************"
print "Switching all processes to use the anti-kT algorithm by default."
print "Switch the jet collection to your desired algorithm if this is not"
print "what you want to use. Note that L7Parton correction are taken from"
print "SC5 instead of AK5. This is an intermediate solution for the time "
print "being."
print "*********************************************************************"
switchJetCollection(process, 
                    cms.InputTag('ak5CaloJets'),   
                    doJTA            = True,            
                    doBTagging       = True,            
                    jetCorrLabel     = ('AK5','Calo'),  
                    doType1MET       = True,            
                    genJetCollection = cms.InputTag("ak5GenJets")
                    ) 

## Load additional RECO config
# Magnetic field now needs to be in the high-level py
# process.load("Configuration.StandardSequences.MagneticField_cff")

#process.content = cms.EDAnalyzer("EventContentAnalyzer")
process.p = cms.Path(
                process.famosWithEverything        +    # run full FAMOS (ttbar events)
                #process.content                   +    # to get a dump of the output of FAMOS
                process.patDefaultSequence
            )


# Output module configuration
from PhysicsTools.PatAlgos.patEventContent_cff import patEventContent
process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('PATLayer1_Output.fromScratch_fast.root'),
    # save only events passing the full path
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    # save PAT Layer 1 output
    outputCommands = cms.untracked.vstring('drop *', *patEventContent ) # you need a '*' to unpack the list of commands 'patEventContent'
)
process.outpath = cms.EndPath(process.out)

