#ifndef PhysicsTools_PatAlgos_JPTJetCorrFactorsProducer_h
#define PhysicsTools_PatAlgos_JPTJetCorrFactorsProducer_h

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/InputTag.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include <string>

class ZSPJetCorrector;
class JetPlusTrackCorrector;

namespace pat {
  
  class JPTJetCorrFactorsProducer : public edm::EDProducer {
    
  public:

    ///
    explicit JPTJetCorrFactorsProducer( const edm::ParameterSet& );
    
    ///
    ~JPTJetCorrFactorsProducer();
    
    ///
    virtual void produce( edm::Event&, const edm::EventSetup& );
    
  private:
    
    ///
    edm::ParameterSet pset_;
    
    /// 
    ZSPJetCorrector* zspCorrector_;
    
    /// 
    JetPlusTrackCorrector* jptCorrector_;
    
    ///
    std::string label_;
    
  };
}

#endif // PhysicsTools_PatAlgos_JPTJetCorrFactorsProducer_h
