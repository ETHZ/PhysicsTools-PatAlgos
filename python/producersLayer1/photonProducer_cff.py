import FWCore.ParameterSet.Config as cms

# add PAT specifics
from PhysicsTools.PatAlgos.mcMatchLayer0.photonMatch_cfi import *

# produce object
from PhysicsTools.PatAlgos.producersLayer1.photonProducer_cfi import *

makePatPhotons = cms.Sequence(
    photonMatch *
    patPhotons
    )
