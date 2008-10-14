//
// $Id: IsolatedTauSelector.h,v 1.3 2008/03/12 16:13:27 gpetrucc Exp $
//

/**
  \class    pat::IsolatedTauSelector IsolatedTauSelector.h "PhysicsTools/PatAlgos/interface/IsolatedTauSelector.h"
  \brief    Produces pat::Tau's

   The IsolatedTauSelector produces analysis-level pat::Tau's starting from
   a collection of objects of TauType.

  \author   Steven Lowette, Christophe Delaere
  \version  $Id: IsolatedTauSelector.h,v 1.3 2008/03/12 16:13:27 gpetrucc Exp $
*/


#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/InputTag.h"

#include "PhysicsTools/PatAlgos/plugins/CleanerHelper.h"
#include "PhysicsTools/PatAlgos/interface/OverlapHelper.h"

#include "DataFormats/TauReco/interface/BaseTau.h"
#include "DataFormats/TauReco/interface/PFTau.h"
#include "DataFormats/TauReco/interface/PFTauDiscriminatorByIsolation.h"
#include "DataFormats/TauReco/interface/CaloTau.h"
#include "DataFormats/TauReco/interface/CaloTauDiscriminatorByIsolation.h"

#include "PhysicsTools/Utilities/interface/PtComparator.h"

#include <string>


namespace pat {


  template<typename TauIn, typename TauTag>
  class IsolatedTauSelector : public edm::EDProducer {

    public:
      typedef edm::RefVector<std::vector<TauIn> > OutputRefVector;

      explicit IsolatedTauSelector(const edm::ParameterSet & iConfig);
      ~IsolatedTauSelector();

      virtual void produce(edm::Event & iEvent, const edm::EventSetup & iSetup);
      virtual void endJob();

    private:
      // configurables
      edm::InputTag tauSrc_;
      edm::InputTag tauDiscSrc_;
      // counters
      uint64_t try_, pass_;
  };

  typedef IsolatedTauSelector<reco::PFTau,reco::PFTauDiscriminatorByIsolation>       IsolatedPFTauSelector;
  typedef IsolatedTauSelector<reco::CaloTau,reco::CaloTauDiscriminatorByIsolation>   IsolatedCaloTauSelector;

}


template<typename TauIn, typename TauTag>
pat::IsolatedTauSelector<TauIn,TauTag>::IsolatedTauSelector(const edm::ParameterSet & iConfig) :
  tauSrc_(iConfig.getParameter<edm::InputTag>( "tauSource" )),
  tauDiscSrc_(iConfig.getParameter<edm::InputTag>( "tauDiscriminatorSource")),
  try_(0), pass_(0)
{
  produces<OutputRefVector>();
}


template<typename TauIn, typename TauTag>
pat::IsolatedTauSelector<TauIn,TauTag>::~IsolatedTauSelector() {
}


template<typename TauIn, typename TauTag>
void pat::IsolatedTauSelector<TauIn,TauTag>::produce(edm::Event & iEvent, const edm::EventSetup & iSetup) {     
  // prepare output
  std::auto_ptr<OutputRefVector> out(new OutputRefVector());

  edm::Handle<TauTag> TauIsolator;
  iEvent.getByLabel(tauDiscSrc_, TauIsolator);

  try_ += TauIsolator->size();

  for (typename TauTag::const_iterator it = TauIsolator->begin(); it != TauIsolator->end(); ++it) {
    if (it->second) out->push_back(it->first);
  }

  pass_ += out->size();

  iEvent.put(out);
}

template<typename TauIn, typename TauTag>
void pat::IsolatedTauSelector<TauIn,TauTag>::endJob() { 
    edm::LogVerbatim("PATLayer0Summary|IsolatedTauSelector") << "IsolatedTauSelector end job. \n" <<
            "Input tag " << tauSrc_.encode() << ", discriminator " << tauDiscSrc_.encode() << 
            "\t: try " << try_ << 
            ", pass " << pass_ << " (" << (try_ > 0 ? pass_/double(try_) * 100.0 : 0) << "%)" << 
            ", fail " << (try_-pass_) << " (" << (try_ > 0 ? (try_-pass_)/double(try_) * 100.0 : 0) << "%)" << "\n";
}

#include "FWCore/Framework/interface/MakerMacros.h"
using namespace pat;
DEFINE_FWK_MODULE(IsolatedPFTauSelector);
DEFINE_FWK_MODULE(IsolatedCaloTauSelector);
