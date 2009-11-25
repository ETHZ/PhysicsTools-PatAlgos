from FWCore.GuiBrowsers.ConfigToolBase import *
#from PhysicsTools.PatAlgos.tools.ConfigToolBase import *
import FWCore.ParameterSet.Config as cms

from PhysicsTools.PatAlgos.patEventContent_cff import *

class SwitchOnTrigger(ConfigToolBase):    
    """ Enables trigger information in PAT
    """    
    _label='SwitchOnTrigger'    
    _defaultParameters={}
    def __init__(self):
        ConfigToolBase.__init__(self)
        self._parameters=copy.deepcopy(self._defaultParameters)
        self._comment = ""
    def getDefaultParameters(self):
        return self._defaultParameters

    def dumpPython(self):
        
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.trigTools import *\n"
        dumpPython=''
        if self._comment!="":
            dumpPython = '#'+self._comment
        dumpPython += "\nswitchOnTrigger(process) \n "
        return (dumpPythonImport,dumpPython)

    def __call__(self,process) :
        self.apply(process) 
        
    def apply(self, process):
        if hasattr(process, "addAction"):
            process.disableRecording()
    
        ## add trigger modules to path
        process.load("PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cff")
        process.patDefaultSequence += process.patTriggerSequence
        
        ## configure pat trigger
        process.patTrigger.onlyStandAlone = False
        
        ## add trigger specific event content to PAT event content
        process.out.outputCommands += patTriggerEventContent
        for matchLabel in process.patTriggerEvent.patTriggerMatches:
            process.out.outputCommands += [ 'keep patTriggerObjectsedmAssociation_patTriggerEvent_' + matchLabel + '_*' ]
        if hasattr(process, "addAction"):
            process.enableRecording()
            action=self.__copy__()
            process.addAction(action)

switchOnTrigger=SwitchOnTrigger()

class SwitchOnTriggerStandAlone(ConfigToolBase):
    """
    """
    _label='SwitchOnTriggerStandAlone'    
    _defaultParameters={}
    def __init__(self):
        ConfigToolBase.__init__(self)
        self._parameters=copy.deepcopy(self._defaultParameters)
        self._comment = ""
    def getDefaultParameters(self):
        return self._defaultParameters

    def dumpPython(self):
        
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.trigTools import *\n"
        dumpPython=''
        if self._comment!="":
            dumpPython = '#'+self._comment
        dumpPython += "\nswitchOnTriggerStandAlone(process) \n "
        return (dumpPythonImport,dumpPython)
     
    def __call__(self,process) :
        self.apply(process) 
        
    def apply(self, process):
        if hasattr(process, "addAction"):
            process.disableRecording()
        ## add trigger modules to path
        process.load("PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cff")
        process.patDefaultSequence += process.patTriggerSequence

        ## configure pat trigger
        process.patTrigger.onlyStandAlone = True
        process.patTriggerSequence.remove( process.patTriggerEvent )
        process.out.outputCommands += patTriggerStandAloneEventContent
        if hasattr(process, "addAction"):
            process.enableRecording()
            action=self.__copy__()
            process.addAction(action)
        
switchOnTriggerStandAlone=SwitchOnTriggerStandAlone()

class SwitchOnTriggerAll(ConfigToolBase):
    """
    """
    _label='SwitchOnTriggerAll'    
    _defaultParameters={}
    def __init__(self):
        ConfigToolBase.__init__(self)
        self._parameters=copy.deepcopy(self._defaultParameters)
        self._comment = ""
    def getDefaultParameters(self):
        return self._defaultParameters

    def dumpPython(self):
        
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.trigTools import *\n"
        dumpPython=''
        if self._comment!="":
            dumpPython = '#'+self._comment
        dumpPython +="\nswitchOnTriggerAll(process) \n "
        return (dumpPythonImport,dumpPython)
    
    def __call__(self,process) :
        self.apply(process) 
        
    def apply(self, process):
        if hasattr(process, "addAction"):
            process.disableRecording()
        switchOnTrigger( process )
        process.out.outputCommands += patTriggerStandAloneEventContent
        if hasattr(process, "addAction"):
            process.enableRecording()
            action=self.__copy__()
            process.addAction(action)

switchOnTriggerAll=SwitchOnTriggerAll()
        
class SwitchOnTriggerMatchEmbedding(ConfigToolBase):
    """
    """
    _label='SwitchOnTriggerMatchEmbedding'    
    _defaultParameters={}
    def __init__(self):
        ConfigToolBase.__init__(self)
        self._parameters=copy.deepcopy(self._defaultParameters)
        self._comment = ""
    def getDefaultParameters(self):
        return self._defaultParameters

    def dumpPython(self):
        
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.trigTools import *\n"
        dumpPython=''
        if self._comment!="":
            dumpPython = '#'+self._comment
        dumpPython += "\nswitchOnTriggerMatchEmbedding(process) \n "
        return (dumpPythonImport,dumpPython)
        
    def __call__(self,process) :
        self.apply(process) 
        
    def apply(self, process):
        if hasattr(process, "addAction"):
            process.disableRecording()
        process.patTriggerSequence += process.patTriggerMatchEmbedder
        process.out.outputCommands += patEventContentTriggerMatch
        if hasattr(process, "addAction"):
            process.enableRecording()
            action=self.__copy__()
            process.addAction(action)

switchOnTriggerMatchEmbedding=SwitchOnTriggerMatchEmbedding()
