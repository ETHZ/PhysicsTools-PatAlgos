# This is an example PAT configuration showing the usage of generic tracks
# with vertex information

# Starting with a skeleton process which gets imported with the following line
from PhysicsTools.PatAlgos.patTemplate_cfg import *

# add the track candidates to the configuration 
from PhysicsTools.PatAlgos.tools.trackTools import *

makeTrackCandidates(process,
    label        = 'TrackCands',                  
    tracks       = cms.InputTag('generalTracks'), 
    particleType = 'pi+',                         
    preselection = 'pt > 10',                     
    selection    = 'pt > 10',                     
    isolation    = {'tracker':0.3, 'ecalTowers':0.3, 'hcalTowers':0.3},                            
    isoDeposits  = [],                            
    mcAs         = 'muon'           
)                                   

# select best vertex
process.bestVertex = cms.EDFilter(
    "PATSingleVertexSelector",
    mode      = cms.string("nearestToCandidate"),
    fallbacks = cms.vstring("fromCandidate", "beamSpot"),
    vertices              = cms.InputTag("offlinePrimaryVerticesWithBS"),
    vertexPreselection    = cms.vstring("(chi2prob(chi2,ndf) > 0.01) && (trackSize >= 3)"),
    candidates            = cms.VInputTag(cms.InputTag('gsfElectrons'), cms.InputTag('muons')),
    candidatePreselection = cms.string("pt > 5"),
    beamSpot              = cms.InputTag('offlineBeamSpot'),
)

# produce vertex associations
process.patTrackVertexInfo = cms.EDProducer(
    "PATVertexAssociationProducer",
    candidates = cms.VInputTag( 
    cms.InputTag('gsfElectrons'),
    cms.InputTag('muons'),
    cms.InputTag('patAODTrackCands'),
    ),
    useTracks = cms.bool(True), 
    vertices  = cms.InputTag('bestVertex'),
)

# add modules to the default sequence right after the patAODTrackCands 
process.patDefaultSequence.replace(process.patAODTrackCands,
                                   process.patAODTrackCands *
                                   process.bestVertex *
                                   process.patTrackVertexInfo
                                   )

# add it to the GenericParticles (FIXME: add to muons and electrons, too)
process.patTrackCands.vertexing = cms.PSet(
    vertexAssociations = cms.InputTag("patTrackVertexInfo"),
)

process.p = cms.Path(
        process.patDefaultSequence 
)

# add generic tracks to the output file
process.out.outputCommands.append('keep *_selectedLayer1TrackCands_*_*')
process.out.outputCommands.append('keep *_patTrackVertexInfo_*_*')
process.out.outputCommands.append('keep *_bestVertex_*_*')

# In addition you usually want to change the following parameters:
#
#   process.GlobalTag.globaltag =  ...     ## (according to https://twiki.cern.ch/twiki/bin/view/CMS/SWGuideFrontierConditions)
#   process.source.fileNames = [ ... ]     ## (e.g. 'file:AOD.root')
#   process.maxEvents.input = ...          ## (e.g. -1 to run on all events)
#   process.out.outputCommands = [ ... ]   ## (e.g. taken from PhysicsTools/PatAlgos/python/patEventContent_cff.py)
#   process.out.fileName = ...             ## (e.g. 'myTuple.root')
process.options.wantSummary = False        ## (to suppress the long output at the end of the job)
