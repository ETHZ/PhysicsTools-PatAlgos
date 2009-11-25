#import FWCore.ParameterSet.Config as cms
from FWCore.GuiBrowsers.ConfigToolBase import *
from PhysicsTools.PatAlgos.tools.jetTools import *

class Run33xOn31xMC(ConfigToolBase):
    
    """
    ------------------------------------------------------------------
    switch appropriate jet collections to run 33x on 31x MC

    process : process
    jetSrc  : jet source to use
    jetID   : jet ID to make
    ------------------------------------------------------------------    
    """
    _label='Run33xOn31xMC'
    _defaultParameters={}

    def __init__(self):
        ConfigToolBase.__init__(self)
        self.addParameter(self._defaultParameters,'jetSrc',cms.InputTag("antikt5CaloJets"), 'jet source to use')
        self.addParameter(self._defaultParameters,'jetIdTag','antikt5', 'jet ID to make ')
        self._parameters=copy.deepcopy(self._defaultParameters)
        self._comment = ""
    def getDefaultParameters(self):
        return self._defaultParameters
   
    def dumpPython(self):
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.cmsswVersionTools import *\n"
        dumpPython=''
        if self._comment!="":
            dumpPython = '#'+self._comment
        dumpPython += "\nrun33xOn31xMC(process, "
        dumpPython += str(self.getvalue('jetSrc'))+', '
        dumpPython +='"'+ str(self.getvalue('jetIdTag'))+'"'+')'+'\n'
        return (dumpPythonImport,dumpPython)

    def __call__(self,process,jetSrc=None,jetIdTag=None ) :
        if  jetSrc is None:
            jetSrc = self._defaultParameters['jetSrc'].value
        if  jetIdTag is None:
            jetIdTag = self._defaultParameters['jetIdTag'].value 
        self.setParameter('jetSrc',jetSrc)
        self.setParameter('jetIdTag',jetIdTag)
        self.apply(process) 
        
    def apply(self, process):
                
        jetSrc=self._parameters['jetSrc'].value
        jetIdTag=self._parameters['jetIdTag'].value
        if hasattr(process, "addAction"):
            process.disableRecording()

            print "*********************************************************************"
            print "NOTE TO USER: when running on 31X samples with this CMSSW version    "
            print "              of PAT the collection label for anti-kt has to be      "
            print "              switched from \'ak*\' to \'antikt*\'. This is going    "
            print "              to be done now. Also note that the *JetId collections  "
            print "              are not stored on these input files in contrary to     "
            print "              input files in 33X. Please use the _addJetId_ tool     "
            print "              as described on SWGuidePATTools, when adding new jet   "
            print "              collections! Such a line could look like this:         "
            print ""
            print "  addJetID( process, \"sisCone5CaloJets\", \"sc5\")"
            print "  from PhysicsTools.PatAlgos.tools.jetTools import *"
            print "  addJetCollection(process,cms.InputTag('sisCone5CaloJets'),"
            print "  ..."
            print "  )"
            print "*********************************************************************"
            addJetID( process, jetSrc, jetIdTag )
            # in PAT (iterativeCone5) to ak5 (anti-kt cone = 0.5)
            switchJetCollection(process, 
                                cms.InputTag('antikt5CaloJets'),   
                                doJTA            = True,            
                                doBTagging       = True,            
                                jetCorrLabel     = ('AK5','Calo'),  
                                doType1MET       = True,
                                genJetCollection = cms.InputTag("antikt5GenJets"),
                                doJetID          = True,
                                jetIdLabel       = "antikt5"
                                )
            
            if hasattr(process, "addAction"):
                process.enableRecording()
                action=self.__copy__()
                process.addAction(action)

run33xOn31xMC=Run33xOn31xMC()

class RestrictInputToAOD31X(ConfigToolBase):
    """
    ------------------------------------------------------------------
    restrict input for pat tuple production to AOD 31x. Here the jet
    ID needs to be switched to false for the jets, as the information
    to produce it is not available on the 31X ADO samples.

    process : process
    ------------------------------------------------------------------    
    """
    _label='RestrictInputToAOD31X'
    _defaultParameters={}
    
    def __init__(self):
        ConfigToolBase.__init__(self)
        self._parameters=copy.deepcopy(self._defaultParameters)
        self._comment = ""
    def getDefaultParameters(self):
        return self._defaultParameters
    
    def dumpPython(self):
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.cmsswVersionTools import *\n"
        dumpPython=''
        if self._comment!="":
            dumpPython = '#'+self._comment
        dumpPython += "\nrestrictInputToAOD31X(process)\n "
        return (dumpPythonImport,dumpPython)

    def __call__(self,process ) :
        self.apply(process) 
        
    def apply(self, process):
        if hasattr(process, "addAction"):
            process.disableRecording()
            
        process.patDefaultSequence.remove(getattr(process, 'antikt5JetID'))
        jetProducer = getattr(process, 'allLayer1Jets')
        jetProducer.addJetID = False
        
        if hasattr(process, "addAction"):
            process.enableRecording()
            action=self.__copy__()
            process.addAction(action)

restrictInputToAOD31X=RestrictInputToAOD31X()
