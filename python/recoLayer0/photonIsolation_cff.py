import FWCore.ParameterSet.Config as cms

# load E/gamma POG config
from RecoEgamma.EgammaIsolationAlgos.gamIsoDeposits_cff import *
from RecoEgamma.EgammaIsolationAlgos.gamEcalExtractorBlocks_cff import *
from RecoEgamma.EgammaIsolationAlgos.gamHcalExtractorBlocks_cff import *

gamIsoDepositTk.ExtractorPSet.ComponentName = cms.string('TrackExtractor')
gamIsoDepositEcalSCVetoFromClusts = cms.EDProducer("CandIsoDepositProducer",
    src = cms.InputTag("photons"),
    MultipleDepositsFlag = cms.bool(False),
    trackType = cms.string('candidate'),
    ExtractorPSet = cms.PSet( GamIsoEcalSCVetoFromClustsExtractorBlock )
)
gamIsoDepositEcalFromClusts = cms.EDProducer("CandIsoDepositProducer",
    src = cms.InputTag("photons"),
    MultipleDepositsFlag = cms.bool(False),
    trackType = cms.string('candidate'),
    ExtractorPSet = cms.PSet( GamIsoEcalFromClustsExtractorBlock )
)
gamIsoDepositHcalFromTowers = cms.EDProducer("CandIsoDepositProducer",
    src = cms.InputTag("photons"),
    MultipleDepositsFlag = cms.bool(False),
    trackType = cms.string('candidate'),
    ExtractorPSet = cms.PSet( GamIsoHcalFromTowersExtractorBlock )
)

# selecting POG modules that can run on top of AOD
gamIsoDepositAOD = cms.Sequence(gamIsoDepositTk * gamIsoDepositEcalFromClusts * gamIsoDepositHcalFromTowers)

# sequence to run on AOD before PAT 
patPhotonIsolation = cms.Sequence(gamIsoDepositAOD)
