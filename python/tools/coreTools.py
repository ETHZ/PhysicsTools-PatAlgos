from FWCore.GuiBrowsers.ConfigToolBase import *
#from PhysicsTools.PatAlgos.tools.ConfigToolBase import *
import FWCore.ParameterSet.Config as cms

from PhysicsTools.PatAlgos.tools.helpers import *



class RestrictInputToAOD (ConfigToolBase):

    """
    ------------------------------------------------------------------
    remove pat object production steps which rely on RECO event
    content:

    process : process
    name    : list of collection names; supported are 'Photons', 
              'Electrons', 'Muons', 'Taus', 'Jets', 'METs', 'All'
    ------------------------------------------------------------------    
    """
    _label='RestrictInputToAOD'
    
    _defaultParameters={}
    def __init__(self):
        ConfigToolBase.__init__(self)
        self.addParameter(self._defaultParameters,'names',['All'], "list of collection names; supported are 'Photons','Electrons', 'Muons', 'Taus', 'Jets', 'METs', 'All'",allowedValues=['Photons','Electrons', 'Muons', 'Taus', 'Jets', 'METs', 'All'])
        self._parameters=copy.deepcopy(self._defaultParameters)
        self._comment = ""
    def getDefaultParameters(self):
        return self._defaultParameters

    def dumpPython(self):
        
        dumpPythonImport= "\nfrom PhysicsTools.PatAlgos.tools.coreTools import *\n"
        dumpPython=''
        if self._comment!="":
            dumpPython = '#'+self._comment
        dumpPython = "\nrestrictInputToAOD(process, "
        dumpPython += str(self.getvalue('names'))+')'+'\n'
        return (dumpPythonImport,dumpPython)

    def __call__(self,process,names=None) :
        if  names is None:
            names=self._defaultParameters['names'].value
	self.setParameter('names',names)
        self.apply(process) 
        
    def apply(self, process):
                
        names=self._parameters['names'].value
        if hasattr(process, "addAction"):
            process.disableRecording()
        
        for obj in range(len(names)):
            print "---------------------------------------------------------------------"
            print "WARNING: the following additional information can only be used on "
            print "         RECO format:"
            if( names[obj] == 'Photons' or names[obj] == 'All' ):
                print "          * nothing needs to be done for Photons"
            if( names[obj] == 'Electrons' or names[obj] == 'All' ):
                print "          * nothing needs to be done for Electrons"            
            if( names[obj] == 'Muons' or names[obj] == 'All' ):
                print "          * nothing needs to be done for Muons"            
            if( names[obj] == 'Taus' or names[obj] == 'All' ):
                print "          * nothing needs to be done for Taus"            
            if( names[obj] == 'Jets' or names[obj] == 'All' ):
                print "          * nothing needs to be done for Jets"            
            if( names[obj] == 'METs' or names[obj] == 'All' ):
                print "          * nothing needs to be done for METs"            
            print "---------------------------------------------------------------------"
        if hasattr(process, "addAction"):
           process.enableRecording()
           action=self.__copy__()
           process.addAction(action)

restrictInputToAOD=RestrictInputToAOD() 

class RemoveMCMatching(ConfigToolBase):

    """
    ------------------------------------------------------------------
    remove monte carlo matching from a given collection or all PAT
    candidate collections:

    process : process
    name    : collection name; supported are 'Photons', 'Electrons',
              'Muons', 'Taus', 'Jets', 'METs', 'All'
    ------------------------------------------------------------------    
    """
    _label='RemoveMCMatching'   
    _defaultParameters={}
    def __init__(self):
        ConfigToolBase.__init__(self)
        self.addParameter(self._defaultParameters,'name','No default value. Set your own', "collection name; supported are 'Photons', 'Electrons','Muons', 'Taus', 'Jets', 'METs', 'All'",str, allowedValues=['Photons', 'Electrons','Muons', 'Taus', 'Jets', 'METs', 'All'])                                 
        self._parameters=copy.deepcopy(self._defaultParameters)
        self._comment = ""
    def getDefaultParameters(self):
        return self._defaultParameters

    def dumpPython(self):        
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.coreTools import *\n"
        dumpPython=''
        if self._comment!="":
            dumpPython = '#'+self._comment
        dumpPython = "\nremoveMCMatching(process, "
        dumpPython += '"'+str(self.getvalue('name'))+'"'+')'+'\n'
        return (dumpPythonImport,dumpPython)
    def __call__(self,process,
                 name = None) :
        if  name is None:
            name=self._defaultParameters['name'].value 
	self.setParameter('name',name)
        self.apply(process) 
        
    def apply(self, process):
                
        name=self._parameters['name'].value
        if hasattr(process, "addAction"):
            process.disableRecording()
        
        if( name == 'Photons'   or name == 'All' ):
            _removeMCMatchingForPATObject(process, 'photonMatch', 'allLayer1Photons') 
        if( name == 'Electrons' or name == 'All' ):
            _removeMCMatchingForPATObject(process, 'electronMatch', 'allLayer1Electrons') 
        if( name == 'Muons'     or name == 'All' ):
            _removeMCMatchingForPATObject(process, 'muonMatch', 'allLayer1Muons') 
        if( name == 'Taus'      or name == 'All' ):
            _removeMCMatchingForPATObject(process, 'tauMatch', 'allLayer1Taus')
            ## remove mc extra modules for taus
            process.patDefaultSequence.remove(process.tauGenJets)
            process.patDefaultSequence.remove(process.tauGenJetMatch)
            ## remove mc extra configs for taus
            tauProducer = getattr(process, 'allLayer1Taus')
            tauProducer.addGenJetMatch      = False
            tauProducer.embedGenJetMatch    = False
            tauProducer.genJetMatch         = ''         
        if( name == 'Jets'      or name == 'All' ):
            ## remove mc extra modules for jets
            process.patDefaultSequence.remove(process.jetPartonMatch)
            process.patDefaultSequence.remove(process.jetGenJetMatch)
            process.patDefaultSequence.remove(process.jetFlavourId)
            ## remove mc extra configs for jets
            jetProducer = getattr(process, 'allLayer1Jets')
            jetProducer.addGenPartonMatch   = False
            jetProducer.embedGenPartonMatch = False
            jetProducer.genPartonMatch      = ''
            jetProducer.addGenJetMatch      = False
            jetProducer.genJetMatch         = ''
            jetProducer.getJetMCFlavour     = False
            jetProducer.JetPartonMapSource  = ''       
        if( name == 'METs'      or name == 'All' ):
            ## remove mc extra configs for jets
            metProducer = getattr(process, 'layer1METs')        
            metProducer.addGenMET           = False
            metProducer.genMETSource        = ''       
        if hasattr(process, "addAction"):
            process.enableRecording()
            action=self.__copy__()
            process.addAction(action)

removeMCMatching = RemoveMCMatching()   

def _removeMCMatchingForPATObject(process, matcherName, producerName):
    ## remove mcMatcher from the default sequence
    objectMatcher = getattr(process, matcherName)
    process.patDefaultSequence.remove(objectMatcher)
    ## straighten photonProducer
    objectProducer = getattr(process, producerName)
    objectProducer.addGenMatch      = False
    objectProducer.embedGenMatch    = False
    objectProducer.genParticleMatch = ''    

class RemoveAllPATObjectsBut(ConfigToolBase):

    """
    ------------------------------------------------------------------
    remove all PAT objects from the default sequence but a specific
    one:

    process         : process
    name            : list of collection names; supported are
                      'Photons', 'Electrons', 'Muons', 'Taus',
                      'Jets', 'METs'
    outputInProcess : indicate whether there is an output module
                      specified for the process (default is True)            
    ------------------------------------------------------------------    
    """
    _label='RemoveAllPATObjectsBut'   
    _defaultParameters={}
    def __init__(self):
        ConfigToolBase.__init__(self)
        self.addParameter(self._defaultParameters,'names','No default value. Set your own', "collection name; supported are 'Photons', 'Electrons','Muons', 'Taus', 'Jets', 'METs', 'All'",list, allowedValues=['Photons', 'Electrons','Muons', 'Taus', 'Jets', 'METs', 'All'])
        self.addParameter(self._defaultParameters,'outputInProcess',True, "indicate whether there is an output module specified for the process (default is True)")                                 
        self._parameters=copy.deepcopy(self._defaultParameters)
        self._comment = ""
    def getDefaultParameters(self):
        return self._defaultParameters
    	
    def dumpPython(self):
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.coreTools import *\n"
        dumpPython=''
        if self._comment!="":
            dumpPython = '#'+self._comment
        dumpPython = "\nremoveAllPATObjectsBut(process, "
        dumpPython += str(self.getvalue('names'))+','
        dumpPython += str(self.getvalue('outputInProcess'))+')'+'\n'
        return (dumpPythonImport,dumpPython)
    def __call__(self,process,
                 names = None,
                 outputInProcess = None) :
        if  names is None:
            names=self._defaultParameters['names'].value
        if outputInProcess is None:
            outputInProcess=self._defaultParameters['outputInProcess'].value 
	self.setParameter('names',names)
        self.setParameter('outputInProcess',outputInProcess)
        self.apply(process) 
        
    def apply(self, process):
                
        names=self._parameters['names'].value
        outputInProcess=self._parameters['outputInProcess'].value
        if hasattr(process, "addAction"):
            process.disableRecording()
        
        removeTheseObjectCollections = ['Photons', 'Electrons', 'Muons', 'Taus', 'Jets', 'METs']
        for obj in range(len(names)):
            removeTheseObjectCollections.remove(names[obj])
        removeSpecificPATObjects(process, removeTheseObjectCollections, outputInProcess)
        if hasattr(process, "addAction"):
            process.enableRecording()
            action=self.__copy__()
            process.addAction(action)

removeAllPATObjectsBut=RemoveAllPATObjectsBut()

class RemoveSpecificPATObjects(ConfigToolBase):

    """
    ------------------------------------------------------------------
    remove a specific PAT object from the default sequence:

    process         : process
    names           : listr of collection names; supported are
                      'Photons', 'Electrons', 'Muons', 'Taus', 'Jets',
                      'METs'
    outputInProcess : indicate whether there is an output module
                      specified for the process (default is True)
    ------------------------------------------------------------------    
    """
    _label='RemoveSpecificPATObjects'   
    _defaultParameters={}
    def __init__(self):
        ConfigToolBase.__init__(self)
        self.addParameter(self._defaultParameters,'names','No default value. Set your own', "collection name; supported are 'Photons', 'Electrons','Muons', 'Taus', 'Jets', 'METs', 'All'",list,['Photons', 'Electrons', 'Muons', 'Taus', 'Jets','METs'] )
        self.addParameter(self._defaultParameters,'outputInProcess',True, "indicate whether there is an output module specified for the process (default is True)")                                 
        self._parameters=copy.deepcopy(self._defaultParameters)
        self._comment = ""
    def getDefaultParameters(self):
        return self._defaultParameters
    
    def dumpPython(self):
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.coreTools import *\n"
        dumpPython=''
        if self._comment!="":
            dumpPython = '#'+self._comment 
        dumpPython = "\nremoveSpecificPATObjects(process, "
        dumpPython += str(self.getvalue('names'))+', '
        dumpPython += str(self.getvalue('outputInProcess'))+')'+'\n'
        return (dumpPythonImport,dumpPython)

    def __call__(self,process,
                 names = None,
                 outputInProcess = None) :
        if  names is None:
            names=self._defaultParameters['names'].value
        if outputInProcess is None:
            outputInProcess=self._defaultParameters['outputInProcess'].value 
	self.setParameter('names',names)
        self.setParameter('outputInProcess',outputInProcess)
        self.apply(process) 
        
    def apply(self, process):
                
        names=self._parameters['names'].value
        outputInProcess=self._parameters['outputInProcess'].value
        if hasattr(process, "addAction"):
            process.disableRecording()
        
        ## remove pre object production steps from the default sequence
        for obj in range(len(names)):
            if( names[obj] == 'Photons' ):
                process.patDefaultSequence.remove(getattr(process, 'patPhotonIsolation'))
                process.patDefaultSequence.remove(getattr(process, 'photonMatch'))            
            if( names[obj] == 'Electrons' ):
                process.patDefaultSequence.remove(getattr(process, 'patElectronId'))
                process.patDefaultSequence.remove(getattr(process, 'patElectronIsolation'))
                process.patDefaultSequence.remove(getattr(process, 'electronMatch'))        
            if( names[obj] == 'Muons' ):
                process.patDefaultSequence.remove(getattr(process, 'muonMatch'))
            if( names[obj] == 'Taus' ):
                process.patDefaultSequence.remove(getattr(process, 'patPFCandidateIsoDepositSelection'))
                process.patDefaultSequence.remove(getattr(process, 'patPFTauIsolation'))
                process.patDefaultSequence.remove(getattr(process, 'tauMatch'))
                process.patDefaultSequence.remove(getattr(process, 'tauGenJets'))
                process.patDefaultSequence.remove(getattr(process, 'tauGenJetMatch'))
            if( names[obj] == 'Jets' ):
                process.patDefaultSequence.remove(getattr(process, 'patJetCharge'))
                process.patDefaultSequence.remove(getattr(process, 'patJetCorrections'))
                process.patDefaultSequence.remove(getattr(process, 'jetPartonMatch'))
                process.patDefaultSequence.remove(getattr(process, 'jetGenJetMatch'))
                process.patDefaultSequence.remove(getattr(process, 'jetFlavourId'))                
            if( names[obj] == 'METs' ):
                process.patDefaultSequence.remove(getattr(process, 'patMETCorrections'))                
            ## remove cleaning for the moment; in principle only the removed object
            ## could be taken out of the checkOverlaps PSet
            removeCleaning(process, outputInProcess)
        
            ## remove object production steps from the default sequence    
            if( names[obj] == 'METs' ):
                process.allLayer1Objects.remove( getattr(process, 'layer1'+names[obj]) )
            else:
                process.allLayer1Objects.remove( getattr(process, 'allLayer1'+names[obj]) )
                process.selectedLayer1Objects.remove( getattr(process, 'selectedLayer1'+names[obj]) )
                process.countLayer1Objects.remove( getattr(process, 'countLayer1'+names[obj]) )
            ## in the case of leptons, the lepton counter must be modified as well
            if( names[obj] == 'Electrons' ):
                print 'removed from lepton counter: electrons'
                process.countLayer1Leptons.countElectrons = False
            elif( names[obj] == 'Muons' ):
                print 'removed from lepton counter: muons'
                process.countLayer1Leptons.countMuons = False
            elif( names[obj] == 'Taus' ):
                print 'removed from lepton counter: taus'
                process.countLayer1Leptons.countTaus = False
            ## remove from summary
            if( names[obj] == 'METs' ):
                process.allLayer1Summary.candidates.remove( cms.InputTag('layer1'+names[obj]) )
            else:
                process.allLayer1Summary.candidates.remove( cms.InputTag('allLayer1'+names[obj]) )
                process.selectedLayer1Summary.candidates.remove( cms.InputTag('selectedLayer1'+names[obj]) )
                process.cleanLayer1Summary.candidates.remove( cms.InputTag('cleanLayer1'+names[obj]) )
        if hasattr(process, "addAction"):
            process.enableRecording()
            action=self.__copy__()
            process.addAction(action)
        
removeSpecificPATObjects=RemoveSpecificPATObjects()


class RemoveCleaning(ConfigToolBase):
    """
    ------------------------------------------------------------------
    remove PAT cleaning from the default sequence:

    process         : process
    outputInOricess : indicate whether there is an output module
                      specified for the process (default is True)
    ------------------------------------------------------------------    
    """
    _label='RemoveCleaning'   
    _defaultParameters={}
    def __init__(self):
        ConfigToolBase.__init__(self)
        self.addParameter(self._defaultParameters,'outputInProcess',True, "indicate whether there is an output module specified for the process (default is True)")                                 
        self._parameters=copy.deepcopy(self._defaultParameters)
        self._comment = ""
    def getDefaultParameters(self):
        return self._defaultParameters
    def dumpPython(self):
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.coreTools import *\n"
        dumpPython=''
        if self._comment!="":
            dumpPython = '#'+self._comment
        dumpPython = "\nremoveCleaning(process, "
        dumpPython += str(self.getvalue('outputInProcess'))+')'+'\n'
        return (dumpPythonImport,dumpPython)
    def __call__(self,process,
                 outputInProcess = None) :
        if outputInProcess is None:
            outputInProcess=self._defaultParameters['outputInProcess'].value 
        self.setParameter('outputInProcess',outputInProcess)
        self.apply(process) 
        
    def apply(self, process):
                
        outputInProcess=self._parameters['outputInProcess'].value
        if hasattr(process, "addAction"):
            process.disableRecording()
        
        ## adapt single object counters
        for m in listModules(process.countLayer1Objects):
            if hasattr(m, 'src'): m.src = m.src.value().replace('cleanLayer1','selectedLayer1')
        ## adapt lepton counter
        countLept = process.countLayer1Leptons
        countLept.electronSource = countLept.electronSource.value().replace('cleanLayer1','selectedLayer1')
        countLept.muonSource = countLept.muonSource.value().replace('cleanLayer1','selectedLayer1')
        countLept.tauSource = countLept.tauSource.value().replace('cleanLayer1','selectedLayer1')
        process.patDefaultSequence.remove(process.cleanLayer1Objects)
        if ( outputInProcess ):
            ## add selected layer1 objects to the pat output
            from PhysicsTools.PatAlgos.patEventContent_cff import patEventContentNoLayer1Cleaning
            process.out.outputCommands = patEventContentNoLayer1Cleaning
        if hasattr(process, "addAction"):
            process.enableRecording()
            action=self.__copy__()
            process.addAction(action)

removeCleaning=RemoveCleaning()

class AddCleaning(ConfigToolBase):

    """
    ------------------------------------------------------------------
    add PAT cleaning from the default sequence:

    process : process
    ------------------------------------------------------------------    
    """
    _label='AddCleaning'   
    _defaultParameters={}
    def __init__(self):
        ConfigToolBase.__init__(self)
        self._parameters=copy.deepcopy(self._defaultParameters)
        self._comment = ""
        
    def getDefaultParameters(self):
        return self._defaultParameters
       
    def dumpPython(self):
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.coreTools import *\n"
        dumpPython=''
        if self._comment!="":
            dumpPython = '#'+self._comment 
        dumpPython = "\naddCleaning(process)\n" 
        return (dumpPythonImport,dumpPython)

    def __call__(self,process) :
        self.apply(process) 
        
    def apply(self, process):
        if hasattr(process, "addAction"):
            process.disableRecording()
        ## adapt single object counters
        process.patDefaultSequence.replace(process.countLayer1Objects, process.cleanLayer1Objects * process.countLayer1Objects)
        for m in listModules(process.countLayer1Objects):
            if hasattr(m, 'src'): m.src = m.src.value().replace('selectedLayer1','cleanLayer1')
        ## adapt lepton counter
        countLept = process.countLayer1Leptons
        countLept.electronSource = countLept.electronSource.value().replace('selectedLayer1','cleanLayer1')
        countLept.muonSource = countLept.muonSource.value().replace('selectedLayer1','cleanLayer1')
        countLept.tauSource = countLept.tauSource.value().replace('selectedLayer1','cleanLayer1')
        ## add clean layer1 objects to the pat output
        from PhysicsTools.PatAlgos.patEventContent_cff import patEventContent
        process.out.outputCommands = patEventContent               
        if hasattr(process, "addAction"):
            process.enableRecording()
            action=self.__copy__()
            process.addAction(action)

addCleaning=AddCleaning()
