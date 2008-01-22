//
// $Id: PATMETProducer.cc,v 1.2 2008/01/21 16:26:17 lowette Exp $
//

#include "PhysicsTools/PatAlgos/interface/PATMETProducer.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ParameterSet/interface/FileInPath.h"
#include "DataFormats/Common/interface/View.h"

#include "DataFormats/HepMCCandidate/interface/GenParticleCandidate.h"

#include "PhysicsTools/PatUtils/interface/ObjectResolutionCalc.h"

#include <memory>


using namespace pat;


PATMETProducer::PATMETProducer(const edm::ParameterSet & iConfig) {
  // initialize the configurables
  metSrc_         = iConfig.getParameter<edm::InputTag>("metSource");
  addGenMET_      = iConfig.getParameter<bool>         ("addGenMET");
  genPartSrc_     = iConfig.getParameter<edm::InputTag>("genParticleSource");
  addResolutions_ = iConfig.getParameter<bool>         ("addResolutions");
  useNNReso_      = iConfig.getParameter<bool>         ("useNNResolutions");
  metResoFile_    = iConfig.getParameter<std::string>  ("metResoFile");
  addMuonCorr_    = iConfig.getParameter<bool>         ("addMuonCorrections");
  muonSrc_        = iConfig.getParameter<edm::InputTag>("muonSource");   
  
  // construct resolution calculator
  if (addResolutions_) metResoCalc_ = new ObjectResolutionCalc(edm::FileInPath(metResoFile_).fullPath(), useNNReso_);
  
  // produces vector of mets
  produces<std::vector<MET> >();
}


PATMETProducer::~PATMETProducer() {
  if (addResolutions_) delete metResoCalc_;
}


void PATMETProducer::produce(edm::Event & iEvent, const edm::EventSetup & iSetup) {
 
  // Get the vector of MET's from the event
  edm::Handle<edm::View<METType> > mets;
  iEvent.getByLabel(metSrc_, mets);

  // Get the vector of generated particles from the event if needed
  edm::Handle<edm::View<reco::Candidate> > particles;
  if (addGenMET_) {
    iEvent.getByLabel(genPartSrc_, particles);
  }

  // read in the muons if demanded
  edm::Handle<edm::View<MuonType> > muons;
  if (addMuonCorr_) {
    iEvent.getByLabel(muonSrc_, muons);
  }
  
  // loop over mets
  std::vector<MET> * patMETs = new std::vector<MET>(); 
  for (edm::View<METType>::const_iterator itMET = mets->begin(); itMET != mets->end(); itMET++) {
    // construct the MET from the ref -> save ref to original object
    unsigned int idx = itMET - mets->begin();
    edm::Ref<std::vector<METType> > metsRef = mets->refAt(idx).castTo<edm::Ref<std::vector<METType> > >();
    MET amet(metsRef);
    // calculate the generated MET (just sum of neutrinos)
    if (addGenMET_) {
      reco::Particle theGenMET(0, reco::Particle::LorentzVector(0, 0, 0, 0), reco::Particle::Point(0,0,0));
//      for(reco::CandidateCollection::const_iterator itGenPart = particles->begin(); itGenPart != particles->end(); ++itGenPart) {
      for(edm::View<reco::Candidate>::const_iterator itGenPart = particles->begin(); itGenPart != particles->end(); ++itGenPart) {
        reco::Candidate * aTmpGenPart = const_cast<reco::Candidate *>(&*itGenPart);
        reco::GenParticleCandidate aGenPart = *(dynamic_cast<reco::GenParticleCandidate *>(aTmpGenPart));
        if ((aGenPart.status()==1) &&
            (abs(aGenPart.pdgId())==12 || abs(aGenPart.pdgId())==14 || abs(aGenPart.pdgId())==16)) {
          theGenMET.setP4(theGenMET.p4() + aGenPart.p4());
        }
      }
      amet.setGenMET(theGenMET);
    }
    // add MET resolution info if demanded
    if (addResolutions_) {
      (*metResoCalc_)(amet);
    }
    // correct for muons if demanded
    if (addMuonCorr_) {
      for (edm::View<MuonType>::const_iterator itMuon = muons->begin(); itMuon != muons->end(); itMuon++) {
        amet.setP4(reco::Particle::LorentzVector(
            amet.px()-itMuon->px(),
            amet.py()-itMuon->py(),
            0,
            sqrt(pow(amet.px()-itMuon->px(), 2)+pow(amet.py()-itMuon->py(), 2))
        ));
      }
    }
    // add the MET to the vector of METs
    patMETs->push_back(amet);
  }

  // sort MET in ET
  std::sort(patMETs->begin(), patMETs->end(), eTComparator_);

  // put genEvt object in Event
  std::auto_ptr<std::vector<MET> > myMETs(patMETs);
  iEvent.put(myMETs);

}
