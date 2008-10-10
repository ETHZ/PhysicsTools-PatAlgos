import FWCore.ParameterSet.Config as cms

#  Layer 1 default sequence
# build the Objects (Jets, Muons, Electrons, METs, Taus)
from PhysicsTools.PatAlgos.producersLayer1.electronProducer_cff import *
from PhysicsTools.PatAlgos.producersLayer1.muonProducer_cff import *
from PhysicsTools.PatAlgos.producersLayer1.tauProducer_cff import *
from PhysicsTools.PatAlgos.producersLayer1.photonProducer_cff import *
from PhysicsTools.PatAlgos.producersLayer1.jetProducer_cff import *
from PhysicsTools.PatAlgos.producersLayer1.metProducer_cff import *

from PhysicsTools.PatAlgos.producersLayer1.hemisphereProducer_cfi import *
from PhysicsTools.PatAlgos.selectionLayer1.leptonCountFilter_cfi import *


allLayer1Objects = cms.Sequence(
        allLayer1Muons +
        allLayer1Electrons +
        allLayer1Taus +
        allLayer1Photons +
        allLayer1Jets +
        allLayer1METs
)

selectedLayer1Objects = cms.Sequence(
        selectedLayer1Muons +
        selectedLayer1Electrons +
        selectedLayer1Taus +
        selectedLayer1Photons +
        selectedLayer1Jets +
        selectedLayer1METs 
)

countLayer1Objects = cms.Sequence(
        countLayer1Muons +
        countLayer1Electrons +
        countLayer1Taus +
        countLayer1Photons +
        countLayer1Jets +
        countLayer1Leptons    ## << Note that this is not a L1 object collection
)



patLayer1 = cms.Sequence(
    allLayer1Objects +
    selectedLayer1Objects +
    selectedLayer1Hemispheres +
    countLayer1Objects
)
