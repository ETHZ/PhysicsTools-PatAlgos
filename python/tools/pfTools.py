from FWCore.GuiBrowsers.ConfigToolBase import *
#from PhysicsTools.PatAlgos.tools.ConfigToolBase import *
import FWCore.ParameterSet.Config as cms

from PhysicsTools.PatAlgos.tools.coreTools import *
from PhysicsTools.PatAlgos.tools.jetTools import *
from PhysicsTools.PatAlgos.tools.tauTools import *
from FWCore.ParameterSet.Modules  import EDProducer

def warningIsolation():
    print "WARNING: particle based isolation must be studied"

class AdaptPFMuons(ConfigToolBase):
    """
    """
    _label='AdaptPFMuons'
    _defaultParameters={}
    def __init__(self):
        ConfigToolBase.__init__(self)
        self.addParameter(self._defaultParameters,'module','No default value. Set your own', '',EDProducer)
        self._parameters=copy.deepcopy(self._defaultParameters)
        self._comment = ""
    def getDefaultParameters(self):
        return self._defaultParameters

    def dumpPython(self):
        
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.pfTools import *\n"
        dumpPython=''
        if self._comment!="":
            dumpPython = '#'+self._comment
        dumpPython += "\nadaptPFMuons(process, "
        dumpPython += str(self.getvalue('module'))+')'+'\n'
        return (dumpPythonImport,dumpPython)
    
    def __call__(self,process,module=None) :
        if  module is None:
            module=self._defaultParameters['module'].value 
        self.setParameter('module',module)
        self.apply(process) 
        
    def apply(self, process):
                
        module=self._parameters['module'].value
        if hasattr(process, "addAction"):
            process.disableRecording()

        print "Adapting PF Muons "
        print "***************** "
        warningIsolation()
        print 
        module.useParticleFlow = True
        module.userIsolation   = cms.PSet()
        module.isoDeposits = cms.PSet(
            pfChargedHadrons = cms.InputTag("isoDepMuonWithCharged"),
            pfNeutralHadrons = cms.InputTag("isoDepMuonWithNeutral"),
            pfPhotons = cms.InputTag("isoDepMuonWithPhotons")
            )
        module.isolationValues = cms.PSet(
            pfChargedHadrons = cms.InputTag("isoValMuonWithCharged"),
            pfNeutralHadrons = cms.InputTag("isoValMuonWithNeutral"),
            pfPhotons = cms.InputTag("isoValMuonWithPhotons")
            )
        # matching the pfMuons, not the standard muons.
        process.muonMatch.src = module.pfMuonSource
        
        print " muon source:", module.pfMuonSource
        print " isolation  :",
        print module.isolationValues
        print " isodeposits: "
        print module.isoDeposits
        print 
        if hasattr(process, "addAction"):
            process.enableRecording()
            action=self.__copy__()
            process.addAction(action)

adaptPFMuons=AdaptPFMuons()

class AdaptPFElectrons(ConfigToolBase):
    """
    """
    _label='AdaptPFElectrons'
    _defaultParameters={}
    def __init__(self):
        ConfigToolBase.__init__(self)
        self.addParameter(self._defaultParameters,'module','No default value. Set your own', '',EDProducer)
        self._parameters=copy.deepcopy(self._defaultParameters)
        self._comment = ""
    def getDefaultParameters(self):
        return self._defaultParameters

    def dumpPython(self):
        
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.pfTools import *\n"
        dumpPython=''
        if self._comment!="":
            dumpPython = '#'+self._comment
        dumpPython += "\nadaptPFElectrons(process, "
        dumpPython += str(self.getvalue('module'))+')'+'\n'
        return (dumpPythonImport,dumpPython)
           
    def __call__(self,process,module=None) :
        if  module is None:
            module=self._defaultParameters['module'].value 
        self.setParameter('module',module)
        self.apply(process) 
        
    def apply(self, process):
                
        module=self._parameters['module'].value
        if hasattr(process, "addAction"):
            process.disableRecording()
        # module.useParticleFlow = True

        print "Adapting PF Electrons "
        print "********************* "
        warningIsolation()
        print 
        module.useParticleFlow = True
        module.userIsolation   = cms.PSet()
        module.isoDeposits = cms.PSet(
            pfChargedHadrons = cms.InputTag("isoDepElectronWithCharged"),
            pfNeutralHadrons = cms.InputTag("isoDepElectronWithNeutral"),
            pfPhotons = cms.InputTag("isoDepElectronWithPhotons")
            )
        module.isolationValues = cms.PSet(
            pfChargedHadrons = cms.InputTag("isoValElectronWithCharged"),
            pfNeutralHadrons = cms.InputTag("isoValElectronWithNeutral"),
            pfPhotons = cms.InputTag("isoValElectronWithPhotons")
            )

        # COLIN: since we take the egamma momentum for pat Electrons, we must
        # match the egamma electron to the gen electrons, and not the PFElectron.  
        # -> do not uncomment the line below.
        # process.electronMatch.src = module.pfElectronSource
        # COLIN: how do we depend on this matching choice? 
        
        print " PF electron source:", module.pfElectronSource
        print " isolation  :"
        print module.isolationValues
        print " isodeposits: "
        print module.isoDeposits
        print 
        
        print "removing traditional isolation"
        process.patDefaultSequence.remove(getattr(process, 'patElectronIsolation'))


        ##     print "Temporarily switching off isolation & isoDeposits for PF Electrons"
        ##     module.isolation   = cms.PSet()
        ##     module.isoDeposits = cms.PSet()
        ##     print "Temporarily switching off electron ID for PF Electrons"
        ##     module.isolation   = cms.PSet()
        ##     module.addElectronID = False
        ##     if module.embedTrack.value(): 
        ##         module.embedTrack = False
        ##         print "Temporarily switching off electron track embedding"
        ##     if module.embedGsfTrack.value(): 
        ##         module.embedGsfTrack = False
        ##         print "Temporarily switching off electron gsf track embedding"
        ##     if module.embedSuperCluster.value(): 
        ##         module.embedSuperCluster = False
        ##         print "Temporarily switching off electron supercluster embedding"
        if hasattr(process, "addAction"):
            process.enableRecording()
            action=self.__copy__()
            process.addAction(action)
        
adaptPFElectrons=AdaptPFElectrons()

class AdaptPFPhotons(ConfigToolBase):
    """
    """
    _label='AdaptPFPhotons'
    _defaultParameters={}
    def __init__(self):
        ConfigToolBase.__init__(self)
        self.addParameter(self._defaultParameters,'module','No default value. Set your own', '',EDProducer)
        self._parameters=copy.deepcopy(self._defaultParameters)
        self._comment = ""
    def getDefaultParameters(self):
        return self._defaultParameters

    def dumpPython(self):
        
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.pfTools import *\n"
        dumpPython=''
        if self._comment!="":
            dumpPython = '#'+self._comment 
        dumpPython += "\nadaptPFPhotons(process, "
        dumpPython += str(self.getvalue('module'))+')'+'\n'
        return (dumpPythonImport,dumpPython)
           
    def __call__(self,process,module=None) :
        if  module is None:
            module=self._defaultParameters['module'].value 
        self.setParameter('module',module)
        self.apply(process) 
        
    def apply(self, process):
                
        module=self._parameters['module'].value
        process.disableRecording()
        process.enableRecording()
        action=self.__copy__()
        process.addAction(action)
        raise RuntimeError, "Photons are not supported yet"

adaptPFPhotons=AdaptPFPhotons()

class AdaptPFJets(ConfigToolBase):
    """
    """
    _label='AdaptPFJets'
    _defaultParameters={}
    def __init__(self):
        ConfigToolBase.__init__(self)
        self.addParameter(self._defaultParameters,'module','No default value. Set your own', '',EDProducer)
        self._parameters=copy.deepcopy(self._defaultParameters)
        self._comment = ""
    def getDefaultParameters(self):
        return self._defaultParameters

    def dumpPython(self):
       
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.pfTools import *\n"
        dumpPython=''
        if self._comment!="":
            dumpPython = '#'+self._comment
        dumpPython += "\nadaptPFJets(process, "
        dumpPython += str(self.getvalue('module'))+')'+'\n'
        return (dumpPythonImport,dumpPython)
           
    def __call__(self,process,module=None) :
        if  module is None:
            module=self._defaultParameters['module'].value 
        self.setParameter('module',module)
        self.apply(process) 
        
    def apply(self, process):
                
        module=self._parameters['module'].value
        if hasattr(process, "addAction"):
            process.disableRecording()
        module.embedCaloTowers   = False
        if hasattr(process, "addAction"):
            process.enableRecording()
            action=self.__copy__()
            process.addAction(action)
        
adaptPFJets=AdaptPFJets()
        
class AdaptPFTaus(ConfigToolBase):
    """
    """
    _label='AdaptPFTaus'
    _defaultParameters={}
    def __init__(self):
        ConfigToolBase.__init__(self)
        self.addParameter(self._defaultParameters,'tauType',"shrinkingConePFTau", '')
        self._parameters=copy.deepcopy(self._defaultParameters)
        self._comment = ""
    def getDefaultParameters(self):
        return self._defaultParameters

    def dumpPython(self):
       
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.pfTools import *\n"
        dumpPython=''
        if self._comment!="":
            dumpPython = '#'+self._comment
        dumpPython += "\nadaptPFTaus(process, "
        dumpPython += '"'+str(self.getvalue('tauType'))+'"'+')'+'\n'
        return (dumpPythonImport,dumpPython)
           
    def __call__(self,process,tauType=None) :
        if  tauType is None:
            tauType=self._defaultParameters['tauType'].value 
        self.setParameter('tauType',tauType)
        self.apply(process) 
        
    def apply(self, process):
                
        tauType=self._parameters['tauType'].value
        if hasattr(process, "addAction"):
            process.disableRecording()
        
        # MICHAL: tauType can be changed only to fixed cone one, otherwise request is igonred
        oldTaus = process.allLayer1Taus.tauSource
        process.allLayer1Taus.tauSource = cms.InputTag("allLayer0Taus")

        if tauType == 'fixedConePFTau': 
            print "PF2PAT: tauType changed from default \'shrinkingConePFTau\' to \'fixedConePFTau\'"
            process.allLayer0TausDiscriminationByLeadTrackPt.PFTauProducer = cms.InputTag(tauType+"Producer") 
            process.allLayer0TausDiscriminationByIsolation.PFTauProducer = cms.InputTag(tauType+"Producer")
            process.allLayer0Taus.src = cms.InputTag(tauType+"Producer")
            process.pfTauSequence.replace(process.shrinkingConePFTauProducer,
                                          process.fixedConePFTauProducer)
            
        
        if (tauType != 'shrinkingConePFTau' and tauType != 'fixedConePFTau'):
            print "PF2PAT: TauType \'"+tauType+"\' is not supported. Default \'shrinkingConePFTau\' is used instead."
            tauType = 'shrinkingConePFTau'
        
        redoPFTauDiscriminators(process, cms.InputTag(tauType+'Producer'),
                                process.allLayer1Taus.tauSource,
                                tauType)
        switchToAnyPFTau(process, oldTaus, process.allLayer1Taus.tauSource, tauType)
        if hasattr(process, "addAction"):
            process.enableRecording()
            action=self.__copy__()
            process.addAction(action)

adaptPFTaus=AdaptPFTaus()

class AddPFCandidates(ConfigToolBase):
    """
    """
    _label='AddPFCandidates'
    _defaultParameters={}
    def __init__(self):
        ConfigToolBase.__init__(self)
        self.addParameter(self._defaultParameters,'src','No default value. Set your own', '', cms.InputTag)
        self.addParameter(self._defaultParameters,'patLabel','PFParticles', '')
        self.addParameter(self._defaultParameters,'cut',"", '')
                
        self._parameters=copy.deepcopy(self._defaultParameters)
        self._comment = ""
    def getDefaultParameters(self):
        return self._defaultParameters
    def dumpPython(self):
        
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.pfTools import *\n"
        dumpPython=''
        if self._comment!="":
            dumpPython = '#'+self._comment
        dumpPython += "\naddPFCandidates(process, "
        dumpPython += str(self.getvalue('src'))+ ", "
        dumpPython += '"'+str(self.getvalue('patLabel'))+'"'+', '
        dumpPython += '"'+str(self.getvalue('cut'))+'"'+')'+'\n'
        return (dumpPythonImport,dumpPython)
               
    def __call__(self,process,src=None,patLabel=None,cut=None) :
        if  src is None:
            src=self._defaultParameters['src'].value
        if  patLabel is None:
            patLabel=self._defaultParameters['patLabel'].value
        if cut  is None:
            cut=self._defaultParameters['cut'].value 
        self.setParameter('src',src)
        self.setParameter('patLabel',patLabel)
        self.setParameter('cut',cut)
        self.apply(process) 
        
    def apply(self, process):
                
        src=self._parameters['src'].value
        patLabel =self._parameters['patLabel'].value
        cut=self._parameters['cut'].value
        if hasattr(process, "addAction"):
            process.disableRecording()
        from PhysicsTools.PatAlgos.producersLayer1.pfParticleProducer_cfi import allLayer1PFParticles
        # make modules
        producer = allLayer1PFParticles.clone(pfCandidateSource = src)
        filter   = cms.EDFilter("PATPFParticleSelector", 
                                src = cms.InputTag('allLayer1' + patLabel), 
                                cut = cms.string(cut))
        counter  = cms.EDFilter("PATCandViewCountFilter",
                                minNumber = cms.uint32(0),
                                maxNumber = cms.uint32(999999),
                                src       = cms.InputTag('selectedLayer1' + patLabel))
        # add modules to process
        setattr(process, 'allLayer1'      + patLabel, producer)
        setattr(process, 'selectedLayer1' + patLabel, filter)
        setattr(process, 'countLayer1'    + patLabel, counter)
        # insert into sequence
        process.allLayer1Objects.replace(process.allLayer1Summary, producer +  process.allLayer1Summary)
        process.selectedLayer1Objects.replace(process.selectedLayer1Summary, filter +  process.selectedLayer1Summary)
        process.countLayer1Objects    += counter
        # summary tables
        process.allLayer1Summary.candidates.append(cms.InputTag('allLayer1' + patLabel))
        process.selectedLayer1Summary.candidates.append(cms.InputTag('selectedLayer1' + patLabel))
        if hasattr(process, "addAction"):
            process.enableRecording()
            action=self.__copy__()
            process.addAction(action)

addPFCandidates= AddPFCandidates()

class SwitchToPFMET(ConfigToolBase):
    """
    """
    _label='SwitchToPFMET'
    _defaultParameters={}
    def __init__(self):
        ConfigToolBase.__init__(self)
        self.addParameter(self._defaultParameters,'input',cms.InputTag('pfMET'), '')
        self._parameters=copy.deepcopy(self._defaultParameters)
        self._comment = ""
    def getDefaultParameters(self):
        return self._defaultParameters

    def dumpPython(self):
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.pfTools import *\n"
        dumpPython=''
        if self._comment!="":
            dumpPython = '#'+self._comment
        dumpPython += "\nswitchToPFMET(process, "
        dumpPython += str(self.getvalue('input'))+')'+'\n'
        return (dumpPythonImport,dumpPython)
               
    def __call__(self,process,input=None) :
        if input  is None:
            input=self._defaultParameters['input'].value
        self.setParameter('input',input)
        self.apply(process)
    def apply(self, process):         
        input=self._parameters['input'].value
        if hasattr(process, "addAction"):
            process.disableRecording() 
        print 'MET: using ', input
        oldMETSource = process.layer1METs.metSource
        process.layer1METs.metSource = input
        process.layer1METs.addMuonCorrections = False
        process.patDefaultSequence.remove(getattr(process, 'makeLayer1METs'))
        if hasattr(process, "addAction"):
            process.enableRecording()
            action=self.__copy__()
            process.addAction(action)

switchToPFMET=SwitchToPFMET()

class SwitchToPFJets(ConfigToolBase):
    """
    """
    _label='SwitchToPFJets'
    _defaultParameters={}
    def __init__(self):
        ConfigToolBase.__init__(self)
        self.addParameter(self._defaultParameters,'input',cms.InputTag('pfNoTau'), '')
        self._parameters=copy.deepcopy(self._defaultParameters)
        self._comment = ""
    def getDefaultParameters(self):
        return self._defaultParameters

    def dumpPython(self): 
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.pfTools import *\n"
        dumpPython=''
        if self._comment!="":
            dumpPython = '#'+self._comment
        dumpPython += "\nswitchToPFJets(process, "
        dumpPython += str(self.getvalue('input'))+')'+'\n'
        return (dumpPythonImport,dumpPython)
    def __call__(self,process,input=None) :
        if input  is None:
            input=self._defaultParameters['input'].value
        self.setParameter('input',input)
        self.apply(process)
    def apply(self, process):         
        input=self._parameters['input'].value
        if hasattr(process, "addAction"):
            process.disableRecording() 
        print 'Jets: using ', input
        switchJetCollection(process,
                            input,
                            doJTA=True,
                            doBTagging=True,
                            jetCorrLabel=('IC5','PF'), 
                            doType1MET=False)  
        adaptPFJets(process, process.allLayer1Jets)
        if hasattr(process, "addAction"):
            process.enableRecording()
            action=self.__copy__()
            process.addAction(action)

switchToPFJets=SwitchToPFJets()


class UsePF2PAT(ConfigToolBase):

    # PLEASE DO NOT CLOBBER THIS FUNCTION WITH CODE SPECIFIC TO A GIVEN PHYSICS OBJECT.
    # CREATE ADDITIONAL FUNCTIONS IF NEEDED. 
    """Switch PAT to use PF2PAT instead of AOD sources. if 'runPF2PAT' is true, we'll also add PF2PAT in front of the PAT sequence
    """
    
    _label='UsePF2PAT'
    _defaultParameters={}
    def __init__(self):
        ConfigToolBase.__init__(self)
        self.addParameter(self._defaultParameters,'runPF2PAT',True, '')
        self._parameters=copy.deepcopy(self._defaultParameters)
        self._comment = ""
    def getDefaultParameters(self):
        return self._defaultParameters

    def dumpPython(self):
        
        dumpPythonImport = "\nfrom PhysicsTools.PatAlgos.tools.pfTools import *\n"
        dumpPython=''
        if self._comment!="":
            dumpPython = '#'+self._comment
        dumpPython += "\nusePF2PAT(process, "
        dumpPython += str(self.getvalue('runPF2PAT'))+')'+'\n'
        return (dumpPythonImport,dumpPython)
  
    def __call__(self,process,runPF2PAT=None) :
        if runPF2PAT  is None:
            runPF2PAT=self._defaultParameters['runPF2PAT'].value
        self.setParameter('runPF2PAT',runPF2PAT)
        self.apply(process)
    def apply(self, process):         
        runPF2PAT=self._parameters['runPF2PAT'].value
        if hasattr(process, "addAction"):
            process.disableRecording() 
        # -------- CORE ---------------
        if runPF2PAT:
            process.load("PhysicsTools.PFCandProducer.PF2PAT_cff")
            
            #        process.dump = cms.EDAnalyzer("EventContentAnalyzer")
            process.patDefaultSequence.replace(process.allLayer1Objects,
                                               process.PF2PAT +
                                               process.allLayer1Objects
                                               )
            
        removeCleaning(process)
    
        # -------- OBJECTS ------------
        # Muons
        adaptPFMuons(process,process.allLayer1Muons)
        
        
        # Electrons
        adaptPFElectrons(process,process.allLayer1Electrons)
        
        # Photons
        print "Temporarily switching off photons completely"
        removeSpecificPATObjects(process,['Photons'])
        process.patDefaultSequence.remove(process.patPhotonIsolation)
        
        # Jets
        switchToPFJets( process, cms.InputTag('pfNoTau') )
        
        # Taus
        adaptPFTaus( process ) #default (i.e. shrinkingConePFTau)
        #adaptPFTaus( process, tauType='fixedConePFTau' )
        
        # MET
        switchToPFMET(process, cms.InputTag('pfMET'))
        
        # Unmasked PFCandidates
        addPFCandidates(process,cms.InputTag('pfNoJet'),patLabel='PFParticles',cut="")

        if hasattr(process, "addAction"):
            process.enableRecording()
            action=self.__copy__()
            process.addAction(action)

usePF2PAT=UsePF2PAT()
