# import skeleton process
from PhysicsTools.PatAlgos.patTemplate_cfg import *

# PAT Layer 0+1
process.load("PhysicsTools.PatAlgos.patSequences_cff")
process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi")
process.inFlightMuons = cms.EDProducer("PATGenCandsFromSimTracksProducer",
        src           = cms.InputTag("g4SimHits"), # use "famosSimHits" for FAMOS
        setStatus     = cms.int32(-1),
        particleTypes = cms.vstring("mu+"),       # picks also mu-, of course
        filter        = cms.vstring("pt > 0.5"),  # just for testing
        makeMotherLink = cms.bool(True),
        writeAncestors = cms.bool(True), # save also the intermediate GEANT ancestors of the muons
        genParticles   = cms.InputTag("genParticles"),
)
process.muMatch3 = process.muonMatch.clone(mcStatus = cms.vint32(3))
process.muMatch1 = process.muonMatch.clone(mcStatus = cms.vint32(1))
process.muMatchF = process.muonMatch.clone(mcStatus = cms.vint32(-1),
                                           matched  = cms.InputTag("inFlightMuons"))
process.patDefaultSequence.replace(process.muonMatch, process.muMatch1+process.muMatch3+process.muMatchF)
process.allLayer1Muons.genParticleMatch = cms.VInputTag(
    cms.InputTag("muMatch3"),
    cms.InputTag("muMatch1"), 
    cms.InputTag("muMatchF"),
)

process.p = cms.Path(
    process.inFlightMuons + 
    process.patDefaultSequence  
)

# add the in flight muons to the output
process.out.outputCommands.append('keep *_inFlightMuons_*_*')
