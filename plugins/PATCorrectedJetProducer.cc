#include "PhysicsTools/PatAlgos/plugins/PATCorrectedJetProducer.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "DataFormats/Common/interface/View.h"
#include <memory>

using namespace pat;

PATCorrectedJetProducer::PATCorrectedJetProducer (const edm::ParameterSet & iConfig) :
  src_(iConfig.getParameter<edm::InputTag>("src")),
  correction_(pat::Jet::correctionType(iConfig.getParameter<std::string>("correction"))) 
{
  // produces vector of jets
  produces< std::vector<pat::Jet> >();
}

PATCorrectedJetProducer::~PATCorrectedJetProducer() {}

void PATCorrectedJetProducer::produce (edm::Event & iEvent, const edm::EventSetup & iSetup) {
  // Get the vector of Jets from the event
  edm::Handle< edm::View<pat::Jet> > jetHandle;
  iEvent.getByLabel(src_,jetHandle);
  // Prepare product
  std::auto_ptr< std::vector<pat::Jet> > product(new std::vector<pat::Jet>());
  //
  // produce jets with new correction
  //
  for ( size_t i=0; i<jetHandle->size(); ++i ) {
    const pat::Jet& jet = (*jetHandle)[i];
    switch ( correction_ ) {
    case Jet::NoCorrection:
      product->push_back(jet.noCorrJet());
      break;
    case Jet::udsCorrection:
      product->push_back(jet.udsCorrJet());
      break;
    case Jet::cCorrection:
      product->push_back(jet.cCorrJet());
      break;
    case Jet::bCorrection:
      product->push_back(jet.bCorrJet());
      break;
    case Jet::gCorrection:
      product->push_back(jet.gluCorrJet());
      break;
    default:
      product->push_back(jet.defaultCorrJet());
      break;
    }
//     edm::LogVerbatim("PATCOrrectedJetProducer") << " jet ets before / after correction "
// 						<< jet.et() << " " << product->back().et();
  }

  // sort jets in ET
  std::sort(product->begin(),product->end(),eTComparator_);

  // put genEvt object in Event
  iEvent.put(product);

}

#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE(PATCorrectedJetProducer);
