import FWCore.ParameterSet.Config as cms

from PhysicsTools.PatAlgos.recoLayer0.duplicatedElectrons_cfi import *
from PhysicsTools.PatAlgos.recoLayer0.duplicatedPhotons_cfi import *
from PhysicsTools.PatAlgos.recoLayer0.isolatedCaloTauSelector_cfi import *
from PhysicsTools.PatAlgos.recoLayer0.isolatedPFTauSelector_cfi import *

# additional high level reco tasks
from PhysicsTools.PatAlgos.recoLayer0.layer0Reco_cff import *

# MC matching
from PhysicsTools.PatAlgos.mcMatchLayer0.mcMatchSequences_cff   import  *

# trigger matching
from PhysicsTools.PatAlgos.triggerLayer0.trigMatchSequences_cff import  *

patLayer0_withoutTrigMatch = cms.Sequence(
        photonsNoDuplicates * electronsNoDuplicates * isolatedCaloTaus * isolatedPFTaus *
        patLayer0Reco *
        patMCTruth
)

# Layer 0 default sequence 
patLayer0 = cms.Sequence(
        patLayer0_withoutTrigMatch *
        patTrigMatch
)

