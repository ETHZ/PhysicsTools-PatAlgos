//
// $Id: PATPhotonCleaner.h,v 1.6 2008/06/05 17:54:06 gpetrucc Exp $
//

/**
  \class    pat::PATPhotonCleaner PATPhotonCleaner.cc "PhysicsTools/PatAlgos/plugins/PATPhotonCleaner.cc"
  \brief    Produces a clean list of pat::Photons

  The PATPhotonCleaner produces a list of clean pat::Photons

  First, a string-based preselection is applied.

  Then, an additional overlap checking based on deltaR or the Candidate OverlapChecker can be applied.

  Then, a specific removal of electrons by superCluster or by superCluster seed can be applied

  \author   The PAT team (twiki:SWGuidePAT, and hn-cms-physTools@cern.ch)
  \version  $Id: PATPhotonCleaner.cc,v 1.9 2008/05/14 12:10:48 fronga Exp $
*/

#include "PhysicsTools/PatAlgos/plugins/PATCleanerBase.h"
#include "DataFormats/PatCandidates/interface/Photon.h"

#include "PhysicsTools/PatUtils/interface/DuplicatedPhotonRemover.h"

namespace pat {

  class PATPhotonCleaner : public pat::PATCleanerBase<pat::Photon> {
    public:
      enum RemovalAlgo { None, BySeed, BySuperCluster };
    
      explicit PATPhotonCleaner(const edm::ParameterSet & iConfig);
      ~PATPhotonCleaner() {}

      /// Perform the real cleaning
      ///   preselected = items passing the string-based preselection cut
      ///   overlaps    = result of simple overlap checking (see OverlapHelper docs)
      ///                 it may be a NULL pointer if overlap checking is not enabled
      ///   output      = put your selected items here
      ///   iEvent, iSetup = you might want these
      virtual void clean(const edm::PtrVector<pat::Photon> & preselected,
                         const pat::helper::OverlapHelper::Result *overlaps,
                         std::vector<pat::Photon>  & output,
                         edm::Event & iEvent, const edm::EventSetup & iSetup) ;

    private:
      // configurables
      RemovalAlgo                 electronRemovalAlgo_;
      std::vector<edm::InputTag>  electronsToCheck_;
        
      // duplicate removal algo
      pat::DuplicatedPhotonRemover remover_;

      static RemovalAlgo fromString(const edm::ParameterSet & iConfig, const std::string &name);

      typedef pat::PATCleanerBase<pat::Photon>::PtrVectorFacade PreselectedCollection;
      void removeElectrons(const PreselectedCollection &photons, const edm::Event &iEvent, std::vector<uint32_t> &result) ;
  };

}

pat::PATPhotonCleaner::RemovalAlgo
pat::PATPhotonCleaner::fromString(const edm::ParameterSet & iConfig, 
        const std::string &parName) 
{
    std::string name = iConfig.getParameter<std::string>(parName);
    if (name == "none"  )         return None;
    if (name == "bySeed")         return BySeed;
    if (name == "bySuperCluster") return BySuperCluster;
    throw cms::Exception("Configuraton Error") << 
        "PATPhotonCleaner: " <<
        "Invalid choice '" << name <<"' for parameter " << name << ", valid options are " <<
        " 'none', 'bySeed', 'bySuperCluster'";
}


pat::PATPhotonCleaner::PATPhotonCleaner(const edm::ParameterSet & iConfig) :
  pat::PATCleanerBase<pat::Photon>(iConfig),
  electronRemovalAlgo_( fromString(iConfig, "removeElectrons"))
{
    if (electronRemovalAlgo_ != None) {
        if (iConfig.existsAs<edm::InputTag>("electrons")) {
            electronsToCheck_.push_back(iConfig.getParameter<edm::InputTag>("electrons"));
        } else if (iConfig.existsAs<edm::InputTag>("electrons"))  {
            electronsToCheck_ = iConfig.getParameter<std::vector<edm::InputTag> >("electrons");
        } else {
            throw cms::Exception("Configuraton Error") <<
                "PATPhotonCleaner: if using any electron removal, you have to specify" <<
                " the collection(s) of electrons, either as InputTag or VInputTag";
        }
    }
}

void pat::PATPhotonCleaner::clean(const edm::PtrVector<pat::Photon> & preselected,
                         const pat::helper::OverlapHelper::Result *overlaps,
                         std::vector<pat::Photon>  & output,
                         edm::Event & iEvent, const edm::EventSetup & iSetup) 
{
  std::vector<uint32_t> markElectrons(preselected.size(), 0);
  removeElectrons(PreselectedCollection(preselected), iEvent, markElectrons);

  for (size_t idx = 0, size = preselected.size(); idx < size; ++idx) {
    const edm::Ptr<pat::Photon> & photon = preselected[idx];;    

    if ((overlaps != 0) && ((*overlaps)[idx] != 0)) {
        continue; // FIXME should do something smarter?
    }

    if (markElectrons[idx] != 0) {
        continue; // FIXME should do something smarter?
    }

    output.push_back(*photon);
  }

}

void pat::PATPhotonCleaner::removeElectrons(const PreselectedCollection &photons, 
                                            const edm::Event &iEvent, 
                                            std::vector<uint32_t> &result) {
    uint32_t bit = 1; 
    typedef std::vector<edm::InputTag> VInputTag;
    for (VInputTag::const_iterator itt = electronsToCheck_.begin(), edt = electronsToCheck_.end();
                itt != edt; ++itt, bit <<= 1) {

        edm::Handle<edm::View<reco::RecoCandidate> > handle;
        iEvent.getByLabel(*itt, handle);

        std::auto_ptr< pat::OverlapList > electrons;
        if (electronRemovalAlgo_ == BySeed) {
            electrons = remover_.electronsBySeed(photons, *handle);
        } else if (electronRemovalAlgo_ == BySuperCluster) {
            electrons = remover_.electronsBySuperCluster(photons, *handle);
        }
        if (!electrons.get()) return;
        for (pat::OverlapList::const_iterator it = electrons->begin(),
                ed = electrons->end();
                it != ed;
                ++it) {
            size_t idx = it->first;
            result[idx] += bit;
        }
    }
}


#include "FWCore/Framework/interface/MakerMacros.h"
using namespace pat;
DEFINE_FWK_MODULE(PATPhotonCleaner);
