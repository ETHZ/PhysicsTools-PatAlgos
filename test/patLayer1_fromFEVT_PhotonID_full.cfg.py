import FWCore.ParameterSet.Config as cms

process = cms.Process("PAT")

# initialize MessageLogger and output report
process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.threshold = 'INFO'
process.MessageLogger.categories.append('PATLayer0Summary')
process.MessageLogger.cerr.INFO = cms.untracked.PSet(
    default          = cms.untracked.PSet( limit = cms.untracked.int32(0)  ),
    PATLayer0Summary = cms.untracked.PSet( limit = cms.untracked.int32(-1) )
)
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )

# source
process.source = cms.Source("PoolSource", 
     fileNames = cms.untracked.vstring('file:/afs/cern.ch/cms/PRS/top/cmssw-data/relval200-for-pat-testing/FullSimTTbar-210p5.1-ALL.100.root')
)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )


# PAT Layer 0 and 1
process.load("PhysicsTools.PatAlgos.patLayer0_cff")
process.load("PhysicsTools.PatAlgos.patLayer1_cff")


## Load additional RECO config
# Magnetic field now needs to be in the high-level py
process.load("Configuration.StandardSequences.MagneticField_cff")

# produce PhotonID with POG tool, associate it to layer 0 photons
from RecoEgamma.PhotonIdentification.photonId_cfi import PhotonIDProd
process.patAODphotonID = PhotonIDProd.clone()
process.patAODphotonID.photonProducer           = 'allLayer0Photons'
process.patAODphotonID.photonIDAssociationLabel = 'PhotonAssociatedID'
# convert it to ValueMap<PhotonID>
process.layer0PhotonID = cms.EDFilter("PhotonIDConverter",
    src = cms.InputTag("allLayer0Photons"),
    photonID = cms.InputTag("patAODphotonID","PhotonAssociatedID")
)
# store into Layer 1 objects
process.allLayer1Photons.addPhotonID = True
process.allLayer1Photons.photonIDSource = 'layer0PhotonID'
# define sequence
process.patPhotonID = cms.Sequence(process.patAODphotonID * process.layer0PhotonID)


#process.content = cms.EDAnalyzer("EventContentAnalyzer")
process.p = cms.Path(
                process.patLayer0  
                #+ process.content    # to get a dump of the file before running PhotonID
                + process.patPhotonID # insert PhotonID
                + process.patLayer1
            )

# Output module configuration
process.out = cms.OutputModule("PoolOutputModule",
    fileName = cms.untracked.string('PATLayer1_Output.fromFEVT_PhotonID_full.root'),
    # save only events passing the full path
    SelectEvents   = cms.untracked.PSet( SelectEvents = cms.vstring('p') ),
    outputCommands = cms.untracked.vstring('drop *')
                                    
)
process.outpath = cms.EndPath(process.out)
# save PAT Layer 1 output
process.load("PhysicsTools.PatAlgos.patLayer1_EventContent_cff")
process.out.outputCommands.extend(process.patLayer1EventContent.outputCommands)




