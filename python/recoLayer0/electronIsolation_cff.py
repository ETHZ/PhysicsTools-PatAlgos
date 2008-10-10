import FWCore.ParameterSet.Config as cms

from RecoEgamma.EgammaIsolationAlgos.eleIsoDeposits_cff import *
from RecoEgamma.EgammaIsolationAlgos.egammaSuperClusterMerger_cfi import *
from RecoEgamma.EgammaIsolationAlgos.egammaBasicClusterMerger_cfi import *

egammaSuperClusterMerger.src = cms.VInputTag(
    cms.InputTag('hybridSuperClusters'), 
   #cms.InputTag('correctedHybridSuperClusters'), 
    cms.InputTag('multi5x5SuperClusters', 'multi5x5EndcapSuperClusters'),
   #cms.InputTag('multi5x5SuperClustersWithPreshower'),
   #cms.InputTag('correctedMulti5x5SuperClustersWithPreshower')
)
egammaBasicClusterMerger.src = cms.VInputTag(
    cms.InputTag('hybridSuperClusters',  'hybridBarrelBasicClusters'), 
    cms.InputTag('multi5x5BasicClusters','multi5x5EndcapBasicClusters')
)

from RecoEgamma.EgammaIsolationAlgos.eleEcalExtractorBlocks_cff import *
from RecoEgamma.EgammaIsolationAlgos.eleHcalExtractorBlocks_cff import *

eleIsoDepositTk.ExtractorPSet.ComponentName = cms.string('TrackExtractor')
eleIsoDepositEcalSCVetoFromClusts = cms.EDProducer("CandIsoDepositProducer",
    src = cms.InputTag("pixelMatchGsfElectrons"),
    MultipleDepositsFlag = cms.bool(False),
    trackType = cms.string('candidate'),
    ExtractorPSet = cms.PSet( EleIsoEcalSCVetoFromClustsExtractorBlock )
)
eleIsoDepositEcalFromClusts = cms.EDProducer("CandIsoDepositProducer",
    src = cms.InputTag("pixelMatchGsfElectrons"),
    MultipleDepositsFlag = cms.bool(False),
    trackType = cms.string('candidate'),
    ExtractorPSet = cms.PSet( EleIsoEcalFromClustsExtractorBlock )
)
eleIsoDepositHcalFromTowers = cms.EDProducer("CandIsoDepositProducer",
    src = cms.InputTag("pixelMatchGsfElectrons"),
    MultipleDepositsFlag = cms.bool(False),
    trackType = cms.string('candidate'),
    ExtractorPSet = cms.PSet( EleIsoHcalFromTowersExtractorBlock )
)

# define module labels for old (tk-based isodeposit) POG isolation
patElectronIsolationLabels = cms.VInputTag(
        cms.InputTag("eleIsoDepositTk"),
      #  cms.InputTag("eleIsoDepositEcalFromHits"),
      #  cms.InputTag("eleIsoDepositHcalFromHits"),
        cms.InputTag("eleIsoDepositEcalFromClusts"),       # try these two if you want to compute them from AOD
        cms.InputTag("eleIsoDepositHcalFromTowers"),       # instead of reading the values computed in RECO
      # cms.InputTag("eleIsoDepositEcalSCVetoFromClust"), # somebody might want this one for ECAL instead
)

# read and convert to ValueMap<IsoDeposit> keyed to Candidate
# FIXME: no longer needed?
patElectronIsolations = cms.EDFilter("MultipleIsoDepositsToValueMaps",
    collection   = cms.InputTag("pixelMatchGsfElectrons"),
    associations = patElectronIsolationLabels,
)

# selecting POG modules that can run on top of AOD
eleIsoDepositAOD = cms.Sequence( eleIsoDepositTk * eleIsoDepositEcalFromClusts * eleIsoDepositHcalFromTowers)

# sequence to run on AOD before PAT
patElectronIsolation = cms.Sequence(
        egammaSuperClusterMerger *  ## 
        egammaBasicClusterMerger *  ## 
        eleIsoDepositAOD *          ## 
        patElectronIsolations)

####    def useElectronAODIsolation(process,layers=(0,1,)):
####        if (layers.__contains__(0)):
####            print "Switching to isolation computed from AOD info for Electrons in PAT Layer 0"
####            patElectronIsolationLabels = cms.VInputTag(
####                cms.InputTag("eleIsoDepositTk"),
####                cms.InputTag("eleIsoDepositEcalFromClusts"),
####                cms.InputTag("eleIsoDepositHcalFromTowers"),
####            )
####            process.patElectronIsolations.associations = patElectronIsolationLabels
####            process.layer0ElectronIsolations.associations = patElectronIsolationLabels
####            #This does not work yet :-(
####            # process.patElectronIsolation = cms.Sequence(
####            #    egammaSuperClusterMerger * egammaBasicClusterMerger +  
####            #    eleIsoDepositAOD +
####            #    patElectronIsolations
####            # )
####            process.allLayer0Electrons.isolation.ecal.src = cms.InputTag("patElectronIsolations","eleIsoDepositEcalFromClusts")
####            process.allLayer0Electrons.isolation.hcal.src = cms.InputTag("patElectronIsolations","eleIsoDepositHcalFromTowers")
####        if (layers.__contains__(1)):
####            print "Switching to isolation computed from AOD info for Electrons in PAT Layer 1"
####            process.allLayer1Electrons.isolation.ecal.src = cms.InputTag("layer0ElectronIsolations","eleIsoDepositEcalFromClusts")
####            process.allLayer1Electrons.isolation.hcal.src = cms.InputTag("layer0ElectronIsolations","eleIsoDepositHcalFromTowers")
####            process.allLayer1Electrons.isoDeposits.ecal   = cms.InputTag("layer0ElectronIsolations","eleIsoDepositEcalFromClusts")
####            process.allLayer1Electrons.isoDeposits.hcal   = cms.InputTag("layer0ElectronIsolations","eleIsoDepositHcalFromTowers")
####    
####    def useElectronRecHitIsolation(process,layers=(0,1,)):
####        if (layers.__contains__(0)):
####            print "Switching to RecHit isolation for Electrons in PAT Layer 0"
####            patElectronIsolationLabels = cms.VInputTag(
####                cms.InputTag("eleIsoDepositTk"),
####                cms.InputTag("eleIsoDepositEcalFromHits"),
####                cms.InputTag("eleIsoDepositHcalFromHits"),
####            )
####            process.patElectronIsolations.associations = patElectronIsolationLabels
####            process.layer0ElectronIsolations.associations = patElectronIsolationLabels
####            #This does not work yet :-(
####            # process.patElectronIsolation = cms.Sequence( patElectronIsolations )
####            process.allLayer0Electrons.isolation.ecal.src = cms.InputTag("patElectronIsolations","eleIsoDepositEcalFromHits")
####            process.allLayer0Electrons.isolation.hcal.src = cms.InputTag("patElectronIsolations","eleIsoDepositHcalFromHits")
####        if (layers.__contains__(1)):
####            print "Switching to RecHit isolation for Electrons in PAT Layer 1"
####            process.allLayer1Electrons.isolation.ecal.src = cms.InputTag("layer0ElectronIsolations","eleIsoDepositEcalFromHits")
####            process.allLayer1Electrons.isolation.hcal.src = cms.InputTag("layer0ElectronIsolations","eleIsoDepositHcalFromHits")
####            process.allLayer1Electrons.isoDeposits.ecal   = cms.InputTag("layer0ElectronIsolations","eleIsoDepositEcalFromHits")
####            process.allLayer1Electrons.isoDeposits.hcal   = cms.InputTag("layer0ElectronIsolations","eleIsoDepositHcalFromHits")
####    
