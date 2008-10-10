import FWCore.ParameterSet.Config as cms

from PhysicsTools.PatAlgos.recoLayer0.bTagging_cff import *
from PhysicsTools.PatAlgos.recoLayer0.electronId_cff import *
from PhysicsTools.PatAlgos.recoLayer0.electronIsolation_cff import *
from PhysicsTools.PatAlgos.recoLayer0.jetFlavourId_cff import *
from PhysicsTools.PatAlgos.recoLayer0.jetMETCorrections_cff import *
from PhysicsTools.PatAlgos.recoLayer0.jetTracksCharge_cff import *
#from PhysicsTools.PatAlgos.recoLayer0.muonIsolation_cff import *   ## << nothing to do here
from PhysicsTools.PatAlgos.recoLayer0.photonId_cff import *
from PhysicsTools.PatAlgos.recoLayer0.photonIsolation_cff import *

from TrackingTools.TransientTrack.TransientTrackBuilder_cfi import *  # needed for the MET
from TrackingTools.TrackAssociator.DetIdAssociatorESProducer_cff import *

patLayer0Reco = cms.Sequence(
    patElectronId *
    patJetFlavourId *
    patElectronIsolation *
    patPhotonIsolation *
    patPhotonID *
    #patMuonIsolation *    ## << nothing to do here
    patBTagging *
    patJetMETCorrections *
    patJetTracksCharge
)
