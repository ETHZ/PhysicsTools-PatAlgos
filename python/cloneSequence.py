
import FWCore.ParameterSet.Config as cms
from PhysicsTools.PatAlgos.tools.helpers import massSearchReplaceAnyInputTag

class ListAllModulesVisitor(object):
   """Visitor that travels within a cms.Sequence, and returns a list of modules that have it"""
   def __init__(self):
       self._modules = []
   def enter(self,visitee):
       if isinstance(visitee,cms._Module): 
         self._modules.append(visitee)
   def leave(self,visitee):
       pass
   def modules(self):
       return self._modules


def cloneProcessingSnippet(process, sequence, postfix):
   """
   copy a sequence plus the modules therein 
   the modules are renamed by getting a postfix
   input tags are automatically adjusted
   """

   # retrieve modules from old sequence 
   visitor = ListAllModulesVisitor()
   sequence.visit(visitor)
   modules = visitor.modules()

   # clone modules and put them into a new sequence
   labels = []
   tmpSequence = None
   for module in modules:
       label = module.label() 
       if label not in labels:
          labels.append(label) 
          newModule = module.clone()  
          setattr(process, label+postfix,newModule)
          if tmpSequence:    
             tmpSequence += newModule      
          else:
             tmpSequence = newModule  

   # create a new sequence
   newSequence = cms.Sequence(tmpSequence)
   newSequenceLabel = sequence.label()+postfix
   if hasattr(process, newSequenceLabel):
       raise AtributeError("Cloning the sequence "+sequence.label()+" would overwrite existing object." )
   else:
       setattr(process, newSequenceLabel, newSequence)

   # adjust all input tags
   for label in labels:
       massSearchReplaceAnyInputTag(newSequence, label, label+postfix)

   # return the new Sequence
   return newSequence



if __name__=="__main__":
   import unittest
   class TestModuleCommand(unittest.TestCase):
       def setUp(self):
           """Nothing to do """
           pass
       def testCloning(self):
           p = cms.Process("test")
           p.a = cms.EDProducer("a", src=cms.InputTag("gen"))
           p.b = cms.EDProducer("b", src=cms.InputTag("a"))
           p.c = cms.EDProducer("c", src=cms.InputTag("b"))
           p.s = cms.Sequence(p.a*p.b*p.c *p.a)
           cloneProcessingSnippet(p, p.s, "New")
           self.assertEqual(p.dumpPython(),'import FWCore.ParameterSet.Config as cms\n\nprocess = cms.Process("test")\n\nprocess.a = cms.EDProducer("a",\n    src = cms.InputTag("gen")\n)\n\n\nprocess.c = cms.EDProducer("c",\n src = cms.InputTag("b")\n)\n\n\nprocess.cNew = cms.EDProducer("c",\n    src = cms.InputTag("bNew")\n)\n\n\nprocess.bNew = cms.EDProducer("b",\n    src = cms.InputTag("aNew")\n)\n\n\nprocess.aNew = cms.EDProducer("a",\n    src = cms.InputTag("gen")\n)\n\n\nprocess.b = cms.EDProducer("b",\n    src = cms.InputTag("a")\n)\n\n\nprocess.s = cms.Sequence(process.a*process.b*process.c*process.a)\n\n\nprocess.sNew = cms.Sequence(process.aNew+process.bNew+process.cNew)\n\n\n')

   unittest.main()

