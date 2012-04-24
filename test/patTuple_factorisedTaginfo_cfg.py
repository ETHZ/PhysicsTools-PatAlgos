## import skeleton process
from PhysicsTools.PatAlgos.patTemplate_cfg import *

#from PhysicsTools.PatAlgos.tools.jetTools_taginfo_AddSwitch import *
#from PhysicsTools.PatAlgos.tools.jetTools_taginfo import * 
#from PhysicsTools.PatAlgos.tools.jetTools_factor import *
from PhysicsTools.PatAlgos.tools.jetTools import *



addJetCollection(process,cms.InputTag('ak7CaloJets'),
                 'AK7', 'Calo',
                 doJTA        = True,
#                 doBTagging   = False,
                 doBTagging   = True,
#                 jetCorrLabel = ('AK7CaloJets', ['L2Relative', 'L3Absolute']),
                 doType1MET   = True,
                 doL1Cleaning = True,
                 doL1Counters = False,
                 genJetCollection=cms.InputTag("ak7GenJets"),

                 doJetID      = True,
                 jetIdLabel   = "ak7"


#		 ,btagInfo    = ['impactParameterTagInfos','secondaryVertexTagInfos','softMuonTagInfos']



#######		  ,btagInfo = ['impactParameterTagInfos']
#                 ,btagInfo = ['softMuonTagInfos']
#                 ,btagInfo = ['impactParameterTagInfos','secondaryVertexTagInfos']
#   		 ,btagInfo = ['impactParameterTagInfos','secondaryVertexTagInfos','secondaryVertexNegativeTagInfos']                               


#		 ,btagdiscriminators=['jetBProbabilityBJetTags', 'jetProbabilityBJetTags', 'trackCountingHighPurBJetTags','trackCountingHighEffBJetTags', 
#	'simpleSecondaryVertexHighEffBJetTags','simpleSecondaryVertexHighPurBJetTags','combinedSecondaryVertexBJetTags','combinedSecondaryVertexMVABJetTags','softMuonBJetTags','softMuonByPtBJetTags','softMuonByIP3dBJetTags']
               
#		,btagdiscriminators=['softMuonBJetTags','softMuonByPtBJetTags','jetBProbabilityBJetTags', 'jetProbabilityBJetTags', 'trackCountingHighPurBJetTags','trackCountingHighEffBJetTags']


#                ,btagdiscriminators=['jetBProbabilityBJetTags','jetProbabilityBJetTags','trackCountingHighPurBJetTags','trackCountingHighEffBJetTags']
#                ,btagdiscriminators=['softMuonBJetTags','softMuonByPtBJetTags','softMuonByIP3dBJetTags']
#                ,btagdiscriminators=['combinedSecondaryVertexBJetTags','combinedSecondaryVertexMVABJetTags']
###                ,btagdiscriminators=['simpleSecondaryVertexHighEffBJetTags','simpleSecondaryVertexHighPurBJetTags']
##                ,btagdiscriminators=['simpleSecondaryVertexNegativeHighEffBJetTags','simpleSecondaryVertexNegativeHighPurBJetTags','negativeTrackCountingHighEffJetTags','negativeTrackCountingHighPurJetTags']
#		 ,btagdiscriminators=['negativeTrackCountingHighEffJetTags','negativeTrackCountingHighPurJetTags']


	)

## uncomment the following lines to switch the jet
## collection from a 35X input sample
#switchJetCollection35X(process,cms.InputTag('ak5PFJets'),
#                 doJTA        = True,
#                 doBTagging   = True,
#                 jetCorrLabel = None,
#                 doType1MET   = True,
#                 genJetCollection=cms.InputTag("ak5GenJets"),
#                 doJetID      = True
#                 )

##from PhysicsTools.PatAlgos.tools.jetTools import *

switchJetCollection(process,cms.InputTag('ak5PFJets'),
                 doJTA        = True,
#                 doBTagging   = False,
                 doBTagging   = True,
#                 jetCorrLabel = None,
                 doType1MET   = True,
                 genJetCollection=cms.InputTag("ak5GenJets"),
                 doJetID      = True

#                ,btagInfo    = ['impactParameterTagInfos','secondaryVertexTagInfos','softMuonTagInfos']

#######                 ,btagInfo = ['impactParameterTagInfos']
###                 ,btagInfo = ['softMuonTagInfos']
#                 ,btagInfo = ['impactParameterTagInfos','secondaryVertexTagInfos']
#                 ,btagInfo = ['impactParameterTagInfos','secondaryVertexTagInfos','secondaryVertexNegativeTagInfos']



#                ,btagdiscriminators=['jetBProbabilityBJetTags', 'jetProbabilityBJetTags', 'trackCountingHighPurBJetTags','trackCountingHighEffBJetTags',
#       'simpleSecondaryVertexHighEffBJetTags','simpleSecondaryVertexHighPurBJetTags','combinedSecondaryVertexBJetTags','combinedSecondaryVertexMVABJetTags','softMuonBJetTags','softMuonByPtBJetTags','softMuonByIP3dBJetTags']

#               ,btagdiscriminators=['softMuonBJetTags','softMuonByPtBJetTags','jetBProbabilityBJetTags', 'jetProbabilityBJetTags', 'trackCountingHighPurBJetTags','trackCountingHighEffBJetTags']


#                ,btagdiscriminators=['jetBProbabilityBJetTags','jetProbabilityBJetTags','trackCountingHighPurBJetTags','trackCountingHighEffBJetTags']
###                ,btagdiscriminators=['softMuonBJetTags','softMuonByPtBJetTags','softMuonByIP3dBJetTags']
#                ,btagdiscriminators=['combinedSecondaryVertexBJetTags','combinedSecondaryVertexMVABJetTags']
#                ,btagdiscriminators=['simpleSecondaryVertexHighEffBJetTags','simpleSecondaryVertexHighPurBJetTags']
#                ,btagdiscriminators=['simpleSecondaryVertexNegativeHighEffBJetTags','simpleSecondaryVertexNegativeHighPurBJetTags','negativeTrackCountingHighEffJetTags','negativeTrackCountingHighPurJetTags']
#                ,btagdiscriminators=['negativeTrackCountingHighEffJetTags','negativeTrackCountingHighPurJetTags']                
#

                 )



#process.patJetsAK7Calo.addTagInfos = True
#process.patJets.addTagInfos = False

process.p = cms.Path(
    process.patDefaultSequence
    )

#process.source.fileNames = ['file:/afs/cern.ch/cms/Tutorials/TWIKI_DATA/CMSDataAnaSch//CMSDataAnaSch_RelValZMM428.root']
process.source.fileNames = ['/store/relval/CMSSW_5_2_0_pre6/RelValProdTTbar/AODSIM/START52_V2-v3/0112/DE997D18-B360-E111-A5C5-003048678B12.root']
process.out.fileName = 'patTuple_TESTFACTORISATION.root'            ##  (e.g. 'patTuple_disc.root')
process.options.wantSummary = True        ##  (to suppress the long output at the end of the job)



