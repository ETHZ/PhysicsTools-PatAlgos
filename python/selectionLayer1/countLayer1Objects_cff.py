import FWCore.ParameterSet.Config as cms

from PhysicsTools.PatAlgos.selectionLayer1.electronCountFilter_cff import *
from PhysicsTools.PatAlgos.selectionLayer1.muonCountFilter_cff import *
from PhysicsTools.PatAlgos.selectionLayer1.tauCountFilter_cff import *
from PhysicsTools.PatAlgos.selectionLayer1.photonCountFilter_cff import *
from PhysicsTools.PatAlgos.selectionLayer1.jetCountFilter_cff import *

from PhysicsTools.PatAlgos.selectionLayer1.leptonCountFilter_cfi import *

countLayer1Objects = cms.Sequence(
    countLayer1Electrons +
    countLayer1Muons +
    countLayer1Taus +
    countLayer1Leptons +
    countLayer1Photons +
    countLayer1Jets 
)
