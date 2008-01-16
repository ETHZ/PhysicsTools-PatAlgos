//
// $Id: PATMuonCleaner.cc,v 1.2 2008/01/15 22:05:03 gpetrucc Exp $
//

#include "PhysicsTools/PatAlgos/interface/PATMuonCleaner.h"

#include "FWCore/MessageLogger/interface/MessageLogger.h"

#include "DataFormats/Candidate/interface/CandAssociation.h"
#include "DataFormats/MuonReco/interface/Muon.h"
#include "DataFormats/MuonReco/interface/MuonFwd.h"

#include "TMath.h"

#include <vector>
#include <memory>

using pat::PATMuonCleaner;

PATMuonCleaner::PATMuonCleaner(const edm::ParameterSet & iConfig) :
  muonSrc_(iConfig.getParameter<edm::InputTag>( "muonSource" )),
  helper_(muonSrc_) 
{
  // produces vector of muons
  produces<std::vector<reco::Muon> >();

  // producers also backmatch to the muons
  produces<reco::CandRefValueMap>();
}


PATMuonCleaner::~PATMuonCleaner() {
}


void PATMuonCleaner::produce(edm::Event & iEvent, const edm::EventSetup & iSetup) {
  // start a new event
  helper_.newEvent(iEvent);
  
  for (size_t idx = 0, size = helper_.srcSize(); idx < size; ++idx) {
    // read the source muon
    const reco::Muon &srcMuon = helper_.srcAt(idx);    

    // clone the muon so we can modify it
    reco::Muon ourMuon = srcMuon; 

    // perform the selection
    if (false) continue; // now there is no real selection for muons

    // write the muon
    helper_.addItem(idx, ourMuon); 
  }

  // tell him that we're done.
  helper_.done(); // he does event.put by itself

}

