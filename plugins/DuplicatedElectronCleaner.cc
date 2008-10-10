//
// $Id: DuplicatedElectronCleaner.cc,v 1.1.2.1 2008/10/10 13:10:32 gpetrucc Exp $
//

/**
  \class    pat::DuplicatedElectronCleaner DuplicatedElectronCleaner.h "PhysicsTools/PatAlgos/interface/DuplicatedElectronCleaner.h"
  \brief    Remove duplicates from the list of electrons

   The DuplicatedElectronCleaner removes duplicates from the input collection.
   Two electrons are considered duplicate if they share the same gsfTrack or the same superCluster.
   Among the two, the one with |E/P| nearest to 1 is kept.
   This is performed by the DuplicatedElectronRemover in PhysicsTools/PatUtils

   The output is an edm::PtrVector<reco:::GsfElectron>, 
   which can be read through edm::View<reco::GsfElectron>

  \author   Giovanni Petrucciani
  \version  $Id: DuplicatedElectronCleaner.cc,v 1.1.2.1 2008/10/10 13:10:32 gpetrucc Exp $
*/


#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/InputTag.h"

#include "DataFormats/Common/interface/PtrVector.h"

#include "DataFormats/EgammaCandidates/interface/GsfElectronFwd.h"
#include "DataFormats/EgammaCandidates/interface/GsfElectron.h"

#include "PhysicsTools/PatUtils/interface/DuplicatedElectronRemover.h"

namespace pat {

  class DuplicatedElectronCleaner : public edm::EDProducer {
    public:
      explicit DuplicatedElectronCleaner(const edm::ParameterSet & iConfig);
      ~DuplicatedElectronCleaner();  

      virtual void produce(edm::Event & iEvent, const edm::EventSetup & iSetup);
      virtual void endJob();

    private:
      edm::InputTag electronSrc_;
      pat::DuplicatedElectronRemover duplicateRemover_; 
      uint64_t try_, pass_;
  };

} // namespace

pat::DuplicatedElectronCleaner::DuplicatedElectronCleaner(const edm::ParameterSet & iConfig) :
    electronSrc_(iConfig.getParameter<edm::InputTag>("electronSource")),
    try_(0), pass_(0)
{
    produces<edm::PtrVector<reco::GsfElectron> >();
}

pat::DuplicatedElectronCleaner::~DuplicatedElectronCleaner() {
}

void 
pat::DuplicatedElectronCleaner::produce(edm::Event & iEvent, const edm::EventSetup & iSetup) {
  using namespace edm;

  Handle<View<reco::GsfElectron> > electrons;
  iEvent.getByLabel(electronSrc_, electrons);
  try_ += electrons->size();

  std::auto_ptr<PtrVector<reco::GsfElectron> > result(new PtrVector<reco::GsfElectron>());

  std::auto_ptr< std::vector<size_t> > duplicates = duplicateRemover_.duplicatesToRemove(*electrons);

  std::vector<size_t>::const_iterator itdup = duplicates->begin(), enddup = duplicates->end();
  for (size_t i = 0, n = electrons->size(); i < n; ++i) {
        while ((itdup != enddup) && (*itdup < i)) { ++itdup; }
        if ((itdup != enddup) && (*itdup == i)) continue;
        result->push_back(electrons->ptrAt(i));
  }

  pass_ += result->size();

  iEvent.put(result);
}


void 
pat::DuplicatedElectronCleaner::endJob() { 
    edm::LogVerbatim("PATLayer0Summary|DuplicatedElectronCleaner") << "DuplicatedElectronCleaner end job. \n" <<
            "Input tag " << electronSrc_.encode() <<
            "\t: try " << try_ << 
            ", pass " << pass_ << " (" << (try_ > 0 ? pass_/double(try_) * 100.0 : 0) << "%)" << 
            ", fail " << (try_-pass_) << " (" << (try_ > 0 ? (try_-pass_)/double(try_) * 100.0 : 0) << "%)" << "\n";
}

#include "FWCore/Framework/interface/MakerMacros.h"
using pat::DuplicatedElectronCleaner;
DEFINE_FWK_MODULE(DuplicatedElectronCleaner);
