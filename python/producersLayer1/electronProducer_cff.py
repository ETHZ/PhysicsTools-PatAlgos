import FWCore.ParameterSet.Config as cms

# add PAT specifics
from PhysicsTools.PatAlgos.mcMatchLayer0.electronMatch_cfi import *

# produce object
from PhysicsTools.PatAlgos.producersLayer1.electronProducer_cfi import *

makePatElectrons = cms.Sequence(
    electronMatch *
    patElectrons
    )
