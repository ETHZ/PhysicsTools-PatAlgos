import FWCore.ParameterSet.Config as cms

# Be sure to change the "V5" to whatever is in your sqlite file.
# Also change the name of the sqlite file itself if different than what is
# here currently
PoolDBESSource = cms.ESSource("PoolDBESSource",
      DBParameters = cms.PSet(
        messageLevel = cms.untracked.int32(0)
        ),
      timetype = cms.string('runnumber'),
      toGet = cms.VPSet(
      cms.PSet(
            record = cms.string('JetCorrectionsRecord'),
            tag    = cms.string('JetCorrectorParametersCollection_Spring10_V6_AK5Calo'),
            label  = cms.untracked.string('AK5CaloLocal')
            ),
      cms.PSet(
            record = cms.string('JetCorrectionsRecord'),
            tag    = cms.string('JetCorrectorParametersCollection_Spring10_V6_AK7Calo'),
            label  = cms.untracked.string('AK7CaloLocal')
            ),
      cms.PSet(
            record = cms.string('JetCorrectionsRecord'),
            tag    = cms.string('JetCorrectorParametersCollection_Spring10_V6_KT4Calo'),
            label  = cms.untracked.string('KT4CaloLocal')
            ),
      cms.PSet(
            record = cms.string('JetCorrectionsRecord'),
            tag    = cms.string('JetCorrectorParametersCollection_Spring10_V6_KT6Calo'),
            label  = cms.untracked.string('KT6CaloLocal')
            ),
      cms.PSet(
            record = cms.string('JetCorrectionsRecord'),
            tag    = cms.string('JetCorrectorParametersCollection_Spring10_V6_AK5PF'),
            label  = cms.untracked.string('AK5PFLocal')
            ),
      cms.PSet(
            record = cms.string('JetCorrectionsRecord'),
            tag    = cms.string('JetCorrectorParametersCollection_Summer10_V6_AK5JPT'),
            label  = cms.untracked.string('AK5JPTLocal')
            ),
      cms.PSet(
            record = cms.string('JetCorrectionsRecord'),
            tag    = cms.string('JetCorrectorParametersCollection_Spring10_V6_IC5Calo'),
            label  = cms.untracked.string('IC5CaloLocal')
            ),
       ),
      connect = cms.string('sqlite:JEC_Spring10.db')
)
