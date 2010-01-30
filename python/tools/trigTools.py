import FWCore.ParameterSet.Config as cms

from PhysicsTools.PatAlgos.patEventContent_cff import *
    
def switchOnTrigger( process, step = "clean" ):
    """ Enables trigger information in PAT  """
    ## add trigger modules to path
    process.load("PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cff")
    process.patDefaultSequence += process.patTriggerSequence

    ## configure pat trigger
    process.patTrigger.onlyStandAlone = False

    ## one might want to run the trigger not on clean, but on selected PAT objects
    inputs = ['Layer1Electrons','Layer1Jets','Layer1Taus','Layer1Muons','Layer1Photons']
    from PhysicsTools.PatAlgos.tools.helpers import massSearchReplaceAnyInputTag
    for input in inputs:
        massSearchReplaceAnyInputTag(process.patTriggerSequence, 'clean'+input, step+input)
        
    ## add trigger specific event content to PAT event content
    process.out.outputCommands += patTriggerEventContent
    for matchLabel in process.patTriggerEvent.patTriggerMatches:
        process.out.outputCommands += [ 'keep patTriggerObjectsedmAssociation_patTriggerEvent_' + matchLabel + '_*' ]

def switchOnTriggerStandAlone( process ):
    ## add trigger modules to path
    process.load("PhysicsTools.PatAlgos.triggerLayer1.triggerProducer_cff")
    process.patDefaultSequence += process.patTriggerSequence

    ## configure pat trigger
    process.patTrigger.onlyStandAlone = True
    process.patTriggerSequence.remove( process.patTriggerEvent )
    process.out.outputCommands += patTriggerStandAloneEventContent

def switchOnTriggerAll( process ):
    switchOnTrigger( process )
    process.out.outputCommands += patTriggerStandAloneEventContent

def switchOnTriggerMatchEmbedding( process ):
    process.patTriggerSequence += process.patTriggerMatchEmbedder
    process.out.outputCommands += patEventContentTriggerMatch
