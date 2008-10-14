//
// $Id: PATTauCleaner.cc,v 1.6 2008/05/06 20:13:50 gpetrucc Exp $
//

/**
  \class    pat::PATTauCleaner PATTauCleaner.cc "PhysicsTools/PatAlgos/plugins/PATTauCleaner.cc"
  \brief    Produces a clean list of pat::Taus

   The PATTauCleaner produces a clean list of pat::Taus

  First, a string-based preselection is applied.
  Also, an additional overlap checking based on deltaR or the Candidate OverlapChecker can be applied.

  \author   The PAT team (twiki:SWGuidePAT; hn-cms-physTools@cern.ch)
  \version  $Id: PATTauCleaner.cc,v 1.7.2.1 2008/10/10 19:24:04 gpetrucc Exp $

*/

#include "PhysicsTools/PatAlgos/plugins/PATCleanerBase.h"
#include "DataFormats/PatCandidates/interface/Tau.h"


namespace pat {

  class PATTauCleaner : public pat::PATCleanerBase<pat::Tau> {

    public:

      explicit PATTauCleaner(const edm::ParameterSet & iConfig);
      ~PATTauCleaner() {}

      /// Perform the real cleaning
      ///   preselected = items passing the string-based preselection cut
      ///   overlaps    = result of simple overlap checking (see OverlapHelper docs)
      ///                 it may be a NULL pointer if overlap checking is not enabled
      ///   output      = put your selected items here
      ///   iEvent, iSetup = you might want these
      virtual void clean(const edm::PtrVector<pat::Tau> & preselected,
                         const pat::helper::OverlapHelper::Result *overlaps,
                         std::vector<pat::Tau>  & output,
                         edm::Event & iEvent, const edm::EventSetup & iSetup) ;
    private:
  };
}

pat::PATTauCleaner::PATTauCleaner(const edm::ParameterSet & iConfig) :
    pat::PATCleanerBase<pat::Tau>(iConfig)
{
}

void 
pat::PATTauCleaner::clean(const edm::PtrVector<pat::Tau> & preselected,
                         const pat::helper::OverlapHelper::Result *overlaps,
                         std::vector<pat::Tau>  & output,
                         edm::Event & iEvent, const edm::EventSetup & iSetup)
{
  for (size_t idx = 0, size = preselected.size(); idx < size; ++idx) {
    const edm::Ptr<pat::Tau> & tau = preselected[idx];;    

    if ((overlaps != 0) && ((*overlaps)[idx] != 0)) {
        continue; // FIXME should do something smarter?
    }

    output.push_back(*tau);
  }
}


#include "FWCore/Framework/interface/MakerMacros.h"
using namespace pat;
DEFINE_FWK_MODULE(PATTauCleaner);

