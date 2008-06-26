import FWCore.ParameterSet.Config as cms

allLayer0METs = cms.EDFilter("PATCaloMETCleaner",
    metSource = cms.InputTag("corMetType1Icone5Muons"),
    saveAll = cms.string(''), ## set this to a non empty label to save a list of all items both passing and failing

    bitsToIgnore = cms.vstring(), ## You can specify some bit names, e.g. "Overflow/User1", "Core/Duplicate", "Isolation/All".

    wantSummary = cms.untracked.bool(True), ## print summary information for each status flag

    markItems = cms.bool(True), ## write the status flags in the output items

    saveRejected = cms.string('') ## set this to a non empty label to save the list of items which fail

)


