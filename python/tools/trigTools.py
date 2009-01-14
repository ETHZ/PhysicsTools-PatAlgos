import FWCore.ParameterSet.Config as cms

def switchTriggerOff(process):
    """ Disables trigger matching in PAT  """
    process.patDefaultSequence.remove(process.patTrigMatch)
    process.allLayer1Electrons.addTrigMatch = False
    process.allLayer1Muons.addTrigMatch     = False
    process.allLayer1Jets.addTrigMatch      = False
    process.allLayer1Photons.addTrigMatch   = False
    process.allLayer1Taus.addTrigMatch      = False
    process.layer1METs.addTrigMatch         = False
