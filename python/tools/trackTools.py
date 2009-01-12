import FWCore.ParameterSet.Config as cms

def makeAODTrackCandidates(process, label='TrackCands',                ## output collection will be <'patAOD'+label>
                                tracks=cms.InputTag('generalTracks'),  ## input tracks
                                particleType="pi+",                    ## particle type (for mass)
                                candSelection='pt > 10'):              ## preselection cut on candidates
    process.load("SimGeneral.HepPDTESSource.pythiapdt_cfi");
    setattr(process, 'patAOD' + label + 'Unfiltered', 
                     cms.EDProducer("ConcreteChargedCandidateProducer",
                        src  = tracks,
                        particleType = cms.string(particleType) ) )
    setattr(process, 'patAOD' + label,
                     cms.EDFilter("CandViewSelector",
                        src = cms.InputTag('patAOD' + label + 'Unfiltered'),
                        cut = cms.string(candSelection) ) )
    process.patAODReco.replace( process.patCoreAODReco, 
            process.patCoreAODReco +
            getattr(process, 'patAOD' + label + 'Unfiltered') * getattr(process, 'patAOD' + label)
    )

def makePATTrackCandidates(process, label='TrackCands',                     # output will be 'allLayer'+(0/1)+label , 'selectedLayer1' + label
                                    input=cms.InputTag('patAODTrackCands'), # Name of input collection
                                    selection='pt > 10',                    # Selection on PAT Layer 1 objects;
                                                                            #   The output will be 'selectedLayer1' + label
                                    isolation=['tracker','caloTowers'],     # Isolations to use (currently only 'tracker' and 'caloTowers' are valid options)
                                    mcAs=cms.InputTag("muons"),             # Replicate MC match as the one used by PAT on this AOD collection (None = no mc match)
                                    triggerAs=[]                            # Replicate trigger match as all the ones used by PAT on these AOD collections (None = no trig.)
    from PhysicsTools.PatAlgos.producersLayer1.genericParticleProducer_cfi import allLayer1GenericParticles
    setattr(process, 'allLayer1' + label, allLayer1GenericParticles.clone(src = input))
    l1cands = getattr(process, 'allLayer1' + label)
    process.allLayer1Objects.replace(process.allLayer1Summary, l1cands + process.allLayer1Summary)
    process.aodObjects.candidates += [ input ]
    process.allLayer1Objects.candidates += [ cms.InputTag("allLayer1"+label) ]
    process.selectedLayer1Objects.candidates += [ cms.InputTag("selectedLayer1"+label) ]
    setattr(process, 'selectedLayer1' + label, 
        cms.EDFilter("PATGenericParticleSelector",
            src = cms.InputTag("allLayer1"+label),
            cut = cms.string(selection) ) )
    process.selectedLayer1Objects.replace(process.selectedLayer1Summary, 
        getattr(process, 'selectedLayer1' + label) + process.selectedLayer1Summary)
    
    # Isolation: start with empty config
    if isolation == None or isolation == []:
        l1cands.isolation = cms.PSet()
        l1cands.isoDeposits = cms.PSet()
    else:
        isoLabels = []; isoModules = []
        isoDets = { 'tracker':False, 'ecal':False, 'hcal':False }
        for source in isolation:
            if source == 'tracker':
                isoDets['tracker'] = True
                from RecoMuon.MuonIsolationProducers.trackExtractorBlocks_cff import MIsoTrackExtractorCtfBlock
                setattr(process, 'patAOD'+label+'IsoDepositTracks',
                                 cms.EDProducer("CandIsoDepositProducer",
                                        src                  = input,
                                        trackType            = cms.string('best'),
                                        MultipleDepositsFlag = cms.bool(False),
                                        ExtractorPSet        = cms.PSet( MIsoTrackExtractorCtfBlock )
                                    ) )
                isoLabels.append(cms.InputTag('patAOD'+label+'IsoDepositTracks'))
                isoModules.append(getattr(process, 'patAOD'+label+'IsoDepositTracks'))
                l1cands.isolation.tracker.src = cms.InputTag('layer0'+label+'Isolations', 'patAOD'+label+'IsoDepositTracks') 
                l1cands.isoDeposits.tracker   = cms.InputTag('layer0'+label+'Isolations', 'patAOD'+label+'IsoDepositTracks') 
            elif source == 'caloTowers':
                isoDets['ecal'] = True
                isoDets['hcal'] = True
                from RecoMuon.MuonIsolationProducers.caloExtractorByAssociatorBlocks_cff import MIsoCaloExtractorByAssociatorTowersBlock
                setattr(process, 'patAOD'+label+'IsoDepositCaloTowers',
                                 cms.EDProducer("CandIsoDepositProducer",
                                        src                  = input,
                                        trackType            = cms.string('best'),
                                        MultipleDepositsFlag = cms.bool(True),
                                        ExtractorPSet        = cms.PSet( MIsoCaloExtractorByAssociatorTowersBlock )
                                    ) )
                isoLabels += [ cms.InputTag('patAOD'+label+'IsoDepositCaloTowers',x) for x in ('ecal', 'hcal') ]
                isoModules.append(getattr(process, 'patAOD'+label+'IsoDepositCaloTowers') )
                l1cands.isolation.ecal.src   = cms.InputTag('layer0'+label+'Isolations', 'patAOD'+label+'IsoDepositCaloTowers' + 'ecal')
                l1cands.isolation.hcal.src   = cms.InputTag('layer0'+label+'Isolations', 'patAOD'+label+'IsoDepositCaloTowers' + 'hcal')
                l1cands.isoDeposits.ecal = cms.InputTag('layer0'+label+'Isolations', 'patAOD'+label+'IsoDepositCaloTowers' + 'ecal')
                l1cands.isoDeposits.hcal = cms.InputTag('layer0'+label+'Isolations', 'patAOD'+label+'IsoDepositCaloTowers' + 'hcal')
            else:
                raise ValueError, "Unknown isolation '%s'"%(source,)
        # turn off unused dets
        for det in [ x for (x,y) in isoDets.items() if y == False]: # loop on unread detector labels
            setattr(l1cands.isolation,   source, cms.PSet())
            setattr(l1cands.isoDeposits, source, cms.InputTag(''))
        # now make up sequences, converter, re-keyer
        seq = isoModules[0];
        for m in isoModules[1:]: seq += m
        if l0cands != None:
            setattr(process, 'pat'+label+'Isolations', 
                             cms.EDFilter("MultipleIsoDepositsToValueMaps",
                                collection   = input,
                                associations = cms.VInputTag(*isoLabels) ) )
            seq += getattr(process, 'pat'+label+'Isolations')
            setattr(process, 'layer0'+label+'Isolations',
                             cms.EDFilter("CandManyValueMapsSkimmerIsoDeposits",
                                 collection   = input,
                                 backrefs     = input,
                                 commonLabel  = cms.InputTag('patAOD'+label+'Isolations'),
                                 associations = cms.VInputTag(*isoLabels) ) )
            setattr(process, 'patAOD'+label+'Isolation', cms.Sequence( seq ) )
            # put AOD iso
            process.patLayer0.replace(process.patBeforeLevel0Reco, process.patBeforeLevel0Reco + getattr(process, 'patAOD'+label+'Isolation'))
            # put Keyeyer
            process.patLayer0.replace(process.patHighLevelReco,    process.patHighLevelReco    + getattr(process, 'layer0'+label+'Isolations'))  
        else:
            setattr(process, 'layer0'+label+'Isolations', 
                             cms.EDFilter("MultipleIsoDepositsToValueMaps",
                                collection   = input,
                                associations = cms.VInputTag(*isoLabels) ) )
            # do directly in post-layer0
            setattr(process, 'layer0'+label+'Isolation', cms.Sequence( seq ) )
            process.patLayer0.replace(process.patHighLevelReco,    process.patHighLevelReco    + getattr(process, 'layer0'+label+'Isolation'))  
    
    # MC and trigger
    from PhysicsTools.PatAlgos.tools.jetTools import MassSearchParamVisitor;
    if mcAs != None:
        searchMC = MassSearchParamVisitor('src', cms.InputTag(mcAs));
        process.patMCTruth.visit(searchMC)
        modulesMC = searchMC.modules()
        if len(modulesMC) != 1: raise RuntimeError, "Can't find MC-Truth match for '%s', or it's not unique."%(mcAs,)
        setattr(process, 'pat'+label+'MCMatch', modulesMC[0].clone(src = input))
        process.patMCTruth.replace( modulesMC[0], modulesMC[0] + getattr(process, 'pat'+label+'MCMatch'))
        l1cands.addGenMatch = True
        l1cands.genParticleMatch = cms.InputTag('pat'+label+'MCMatch')
    if triggerAs != None and triggerAs != []:
        modulesTR = []; labelsTR = []
        for t in triggerAs:
            searchTR = MassSearchParamVisitor('src', cms.InputTag(t));
            process.patTrigMatch.visit(searchTR)
            modulesTR += searchTR.modules()
        if len(modulesTR) == 0: raise RuntimeError, "Can't find any trigger match among %s" % (triggerAs)
        def ucfirst(x): return x[0].upper() + x[1:]
        for m in modulesTR:
            lbl = 'pat'+label+'TrigMatchAs' + ucfirst(m.label())
            setattr(process, lbl, m.clone(src = input))
            process.patTrigMatch.replace( m, m + getattr(process, lbl))
            labelsTR.append (cms.InputTag(lbl))
        l1cands.addTrigMatch = cms.bool(True)
        l1cands.trigPrimMatch = cms.VInputTag(*labelsTR)

def makeTrackCandidates(process, 
        label='TrackCands',                   # output collection will be 'allLayer'+(0/1)+label , 'selectedLayer1' + label
        tracks=cms.InputTag('generalTracks'), # input track collection
        particleType="pi+",                   # particle type (for assigning a mass)
        preselection='pt > 10',               # preselection cut on candidates
        selection='pt > 10',                  # Selection on PAT Layer 1 objects; The output will be 'selectedLayer1' + label
        isolation=['tracker','caloTowers'],   # Isolations to use (currently only 'tracker' and 'caloTowers' are valid options)
        mcAs='allLayer0Muons',                # Replicate MC match as the one used for this PAT collection (None = no mc match)
        triggerAs=['allLayer0Muons'],         # Replicate trigger match as all the ones used by these PAT collections (None = no trig.)
        layers=[0,1]):
    makeAODTrackCandidates(process, tracks=tracks, particleType=particleType, candSelection=preselection, label=label) 
    makePATTrackCandidates(process, label=label, input='patAOD' + label, 
                           isolation=isolation, mcAs=mcAs, triggerAs=triggerAs, layers=layers, selection=selection)
