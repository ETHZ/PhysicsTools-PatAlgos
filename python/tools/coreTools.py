from FWCore.GuiBrowsers.ConfigToolBase import *

from PhysicsTools.PatAlgos.tools.helpers import *

#this we need to reimplement:
# - RestrictInputToAOD

class RemoveMCMatching(ConfigToolBase):

    """ Remove monte carlo matching from a given collection or all PAT
    candidate collections:
    """
    _label='removeMCMatching'
    _defaultParameters=dicttypes.SortedKeysDict()
    def __init__(self):
        ConfigToolBase.__init__(self)
        self.addParameter(self._defaultParameters,'names',['All'], "collection name; supported are 'Photons', 'Electrons','Muons', 'Taus', 'Jets', 'METs', 'All', 'PFAll', 'PFElectrons','PFTaus','PFMuons'", allowedValues=['Photons', 'Electrons','Muons', 'Taus', 'Jets', 'METs', 'All', 'PFAll', 'PFElectrons','PFTaus','PFMuons'])
        self.addParameter(self._defaultParameters,'postfix',"", "postfix of default sequence")
        self._parameters=copy.deepcopy(self._defaultParameters)
        self._comment = ""

    def getDefaultParameters(self):
        return self._defaultParameters

    def __call__(self,process,
                 names     = None,
                 postfix   = None) :
        if  names is None:
            names=self._defaultParameters['names'].value
        if postfix  is None:
            postfix=self._defaultParameters['postfix'].value
        self.setParameter('names',names)
        self.setParameter('postfix',postfix)
        self.apply(process) 
        
    def toolCode(self, process):        
        names=self._parameters['names'].value
        postfix=self._parameters['postfix'].value

        print "************** MC dependence removal ************"
        for obj in range(len(names)):    
            if( names[obj] == 'Photons'   or names[obj] == 'All' ):
                print "removing MC dependencies for photons"
                _removeMCMatchingForPATObject(process, 'patPhotons', postfix) 
            if( names[obj] == 'Electrons' or names[obj] == 'All' ):
                print "removing MC dependencies for electrons"
                _removeMCMatchingForPATObject(process, 'patElectrons', postfix) 
            if( names[obj] == 'Muons'     or names[obj] == 'All' ):
                print "removing MC dependencies for muons"
                _removeMCMatchingForPATObject(process, 'patMuons', postfix) 
            if( names[obj] == 'Taus'      or names[obj] == 'All' ):
                print "removing MC dependencies for taus"
                _removeMCMatchingForPATObject(process, 'patTaus', postfix)
                ## remove mc extra configs for taus
                tauProducer = getattr(process, 'patTaus'+postfix)
                tauProducer.addGenJetMatch      = False
                tauProducer.embedGenJetMatch    = False
                tauProducer.genJetMatch         = ''         
            if( names[obj] == 'Jets'      or names[obj] == 'All' ):
                print "removing MC dependencies for jets"
                ## remove mc extra configs for jets
                jetProducer = getattr(process, jetCollectionString()+postfix)
                jetProducer.addGenPartonMatch   = False
                jetProducer.embedGenPartonMatch = False
                jetProducer.genPartonMatch      = ''
                jetProducer.addGenJetMatch      = False
                jetProducer.genJetMatch         = ''
                jetProducer.getJetMCFlavour     = False
                jetProducer.JetPartonMapSource  = ''       
            if( names[obj] == 'METs'      or names[obj] == 'All' ):
                ## remove mc extra configs for jets
                metProducer = getattr(process, 'patMETs'+postfix)        
                metProducer.addGenMET           = False
                metProducer.genMETSource        = ''
            
removeMCMatching=RemoveMCMatching()

def _removeMCMatchingForPATObject(process, producerName, postfix=""):
    objectProducer = getattr(process, producerName+postfix)
    objectProducer.addGenMatch      = False
    objectProducer.embedGenMatch    = False
    objectProducer.genParticleMatch = ''
    
    
# The following is deprecated as we do things on demand anyhow now:
# - RemoveSpecificPATObjects
# - RemoveAllPATObjectsBut

# Do we need to reimplement this:
# (it should be a triviality now)
# - RemoveCleaning(ConfigToolBase)
# - AddCleaning(ConfigToolBase)

# What needs to be improved are the summary objects, which we need to activate via something like "addPATSummary"
