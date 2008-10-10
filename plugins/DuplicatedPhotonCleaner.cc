//
// $Id: DuplicatedPhotonCleaner.h,v 1.7 2008/06/20 13:15:32 gpetrucc Exp $
//

/**
  \class    pat::DuplicatedPhotonCleaner DuplicatedPhotonCleaner.h "PhysicsTools/PatAlgos/interface/DuplicatedPhotonCleaner.h"
  \brief    Remove duplicates from the list of photons

   The DuplicatedPhotonCleaner removes duplicates from the input collection.
   Two photons are considered duplicate if they share the same superCluster or superCluster seed.
   Among the two, the one with highest Et is kept.
   This is performed by the DuplicatedPhotonRemover in PhysicsTools/PatUtils

   The output is an edm::PtrVector<reco:::Photon>, 
   which can be read through edm::View<reco::Photon>

  \author   Giovanni Petrucciani
  \version  $Id: DuplicatedPhotonCleaner.h,v 1.7 2008/06/20 13:15:32 gpetrucc Exp $
*/


#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/InputTag.h"

#include "DataFormats/Common/interface/PtrVector.h"

#include "DataFormats/EgammaCandidates/interface/PhotonFwd.h"
#include "DataFormats/EgammaCandidates/interface/Photon.h"

#include "PhysicsTools/PatUtils/interface/DuplicatedPhotonRemover.h"

namespace pat {

  class DuplicatedPhotonCleaner : public edm::EDProducer {
    public:
      enum RemovalAlgo { BySeed, BySuperCluster };

      explicit DuplicatedPhotonCleaner(const edm::ParameterSet & iConfig);
      ~DuplicatedPhotonCleaner();  

      virtual void produce(edm::Event & iEvent, const edm::EventSetup & iSetup);
      virtual void endJob();

    private:
      edm::InputTag photonSrc_;
      pat::DuplicatedPhotonRemover duplicateRemover_; 
      RemovalAlgo                  removalAlgo_;
      static RemovalAlgo fromString(const edm::ParameterSet & iConfig, const std::string &name);

      uint64_t try_, pass_;
  }; 

}// namespace

pat::DuplicatedPhotonCleaner::DuplicatedPhotonCleaner(const edm::ParameterSet & iConfig) :
    photonSrc_(iConfig.getParameter<edm::InputTag>("photonSource")),
    removalAlgo_(fromString(iConfig, "removalAlgo")),
    try_(0), pass_(0)
{
    produces<edm::PtrVector<reco::Photon> >();
}

pat::DuplicatedPhotonCleaner::~DuplicatedPhotonCleaner() {
}

pat::DuplicatedPhotonCleaner::RemovalAlgo
pat::DuplicatedPhotonCleaner::fromString(const edm::ParameterSet & iConfig,
        const std::string &parName)
{
    std::string name = iConfig.getParameter<std::string>(parName);
    if (name == "bySeed")         return BySeed;
    if (name == "bySuperCluster") return BySuperCluster;
    throw cms::Exception("Configuraton Error") <<
        "DuplicatedPhotonCleaner: " <<
        "Invalid choice '" << name <<"' for parameter " << name << ", valid options are " <<
        " 'bySeed', 'bySuperCluster'";
}


void 
pat::DuplicatedPhotonCleaner::produce(edm::Event & iEvent, const edm::EventSetup & iSetup) {
  using namespace edm;

  Handle<View<reco::Photon> > photons;
  iEvent.getByLabel(photonSrc_, photons);
  try_ += photons->size();

  std::auto_ptr<PtrVector<reco::Photon> > result(new PtrVector<reco::Photon>());

  std::auto_ptr< std::vector<size_t> > duplicates;
  switch (removalAlgo_) {
    case BySeed: 
        duplicates = duplicateRemover_.duplicatesBySeed(*photons);
        break;
    case BySuperCluster:
        duplicates = duplicateRemover_.duplicatesBySuperCluster(*photons);
  }

  std::vector<size_t>::const_iterator itdup = duplicates->begin(), enddup = duplicates->end();
  for (size_t i = 0, n = photons->size(); i < n; ++i) {
        while ((itdup != enddup) && (*itdup < i)) { ++itdup; }
        if ((itdup != enddup) && (*itdup == i)) continue;
        result->push_back(photons->ptrAt(i));
  }

  pass_ += result->size();

  iEvent.put(result);
}


void 
pat::DuplicatedPhotonCleaner::endJob() { 
    edm::LogVerbatim("PATLayer0Summary|DuplicatedPhotonCleaner") << "DuplicatedPhotonCleaner end job. \n" <<
            "Input tag " << photonSrc_.encode() <<
            "\t: try " << try_ << 
            ", pass " << pass_ << " (" << (pass_/double(try_) * 100.0) << "%)" << 
            ", fail " << (try_-pass_) << " (" << ((try_-pass_)/double(try_) * 100.0) << "%)" << "\n";
}

#include "FWCore/Framework/interface/MakerMacros.h"
using pat::DuplicatedPhotonCleaner;
DEFINE_FWK_MODULE(DuplicatedPhotonCleaner);
