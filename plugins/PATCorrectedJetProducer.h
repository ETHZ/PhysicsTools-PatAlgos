#ifndef PhysicsTools_PatAlgos_PATCorrectedJetProducer_h
#define PhysicsTools_PatAlgos_PATCorrectedJetProducer_h

/**
  \class    pat::PATCorrectedJetProducer PATCorrectedJetProducer.h "PhysicsTools/PatAlgos/interface/PATCorrectedJetProducer.h"
  \brief    applies correction to PATLayer1 jets

  A new correction type is applied to a collection of pat::Jets and a new collection
  (sorted by corrected Et) is produced.

  \author   Wolfgang Adam
*/


#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/PatCandidates/interface/Jet.h"
#include "PhysicsTools/Utilities/interface/EtComparator.h"


namespace pat {
  
  class PATCorrectedJetProducer : public edm::EDProducer {
    
  public:
    
    explicit PATCorrectedJetProducer(const edm::ParameterSet & iConfig);
    ~PATCorrectedJetProducer();
    
    virtual void produce(edm::Event & iEvent, const edm::EventSetup & iSetup);
    
  private:
    // configurables
    edm::InputTag src_;                    ///< tag for input collection
    pat::Jet::CorrectionType correction_;  ///< jet correction type (see pat::Jet)

    // tools
    GreaterByEt<pat::Jet> eTComparator_;
  };

}

#endif
