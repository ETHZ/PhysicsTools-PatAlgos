#from PhysicsTools.PatAlgos.tools.ConfigToolBase import *
from FWCore.GuiBrowsers.ConfigToolBase import *

class AddTcMET(ConfigToolBase):
    """
    ------------------------------------------------------------------
    add track corrected MET collection to patEventContent:

    process : process
    ------------------------------------------------------------------
    """
    _label='AddTcMET'
    
    _defaultParameters={}

    def __init__(self):
        ConfigToolBase.__init__(self)
        self.addParameter(self._defaultParameters,'postfixLabel','TC', '')
        self._parameters=copy.deepcopy(self._defaultParameters)
        self._comment = ''
    def getDefaultParameters(self):
        return self._defaultParameters
    def dumpPython(self):
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.metTools import *\n"
        dumpPython=''
        if self._comment!="":
            dumpPython = '#'+self._comment
        dumpPython += "\naddTcMET(process, "
        dumpPython += '"'+str(self.getvalue('postfixLabel'))+'"'+')'+'\n'
        return (dumpPythonImport,dumpPython)

    def __call__(self,process,postfixLabel=None) :
        if  postfixLabel is None:
            postfixLabel=self._defaultParameters['postfixLabel'].value 
        self.setParameter('postfixLabel',postfixLabel)
        self.apply(process) 
        
    def apply(self, process):
                
        postfixLabel=self._parameters['postfixLabel'].value
        if hasattr(process, "addAction"):
            process.disableRecording()

        ## add module as process to the default sequence
        def addAlso (label,value):
            existing = getattr(process, label)
            setattr( process, label+postfixLabel, value)
            process.patDefaultSequence.replace( existing, existing*value )        

        ## clone and add a module as process to the
        ## default sequence
        def addClone(label,**replaceStatements):
            new = getattr(process, label).clone(**replaceStatements)
            addAlso(label, new)

        ## addClone('corMetType1Icone5Muons', uncorMETInputTag = cms.InputTag("tcMet"))
        addClone('layer1METs', metSource = cms.InputTag("tcMet"))

        ## add new met collections output to the pat summary
        process.allLayer1Summary.candidates += [ cms.InputTag('layer1METs'+postfixLabel) ]

        if hasattr(process, "addAction"):
            process.enableRecording()
            action=self.__copy__()
            process.addAction(action)

addTcMET=AddTcMET()

class AddPfMET(ConfigToolBase):
    """
    ------------------------------------------------------------------
    add pflow MET collection to patEventContent:

    process : process
    ------------------------------------------------------------------
    """
    _label='AddPfMET'
    
    _defaultParameters={}
    def __init__(self):
        ConfigToolBase.__init__(self)
        self.addParameter(self._defaultParameters,'postfixLabel','PF', '')
        self._parameters=copy.deepcopy(self._defaultParameters)
        self._comment = ''
    def getDefaultParameters(self):
        return self._defaultParameters

    def dumpPython(self):
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.metTools import *\n"
        dumpPython=''
        if self._comment!="":
            dumpPython = '#'+self._comment
        dumpPython += "\naddPfMET(process, "
        dumpPython +='"'+ str(self.getvalue('postfixLabel'))+'"'+')'+'\n'
        return (dumpPythonImport,dumpPython)
    
    def __call__(self,process,postfixLabel=None):
        if  postfixLabel is None:
            postfixLabel=self._defaultParameters['postfixLabel'].value 
        self.setParameter('postfixLabel',postfixLabel)
        self.apply(process) 

    def apply(self, process): 
        postfixLabel=self._parameters['postfixLabel'].value
        if hasattr(process, "addAction"):
            process.disableRecording()
        
        ## add module as process to the default sequence
        def addAlso (label,value):
            existing = getattr(process, label)
            setattr( process, label+postfixLabel, value)
            process.patDefaultSequence.replace( existing, existing*value )        
            
        ## clone and add a module as process to the
        ## default sequence
        def addClone(label,**replaceStatements):
            new = getattr(process, label).clone(**replaceStatements)
            addAlso(label, new)

        ## addClone('corMetType1Icone5Muons', uncorMETInputTag = cms.InputTag("tcMet"))
        addClone('layer1METs', metSource = cms.InputTag("pfMet"), addMuonCorrections = False)

        ## add new met collections output to the pat summary
        process.allLayer1Summary.candidates += [ cms.InputTag('layer1METs'+postfixLabel) ]

        if hasattr(process, "addAction"):
            process.enableRecording()
            action=self.__copy__()
            process.addAction(action)

addPfMET=AddPfMET()
