//
// $Id: PATMuonCleaner.cc,v 1.5 2008/06/20 13:15:32 gpetrucc Exp $
//

/**
  \class    pat::PATMuonCleaner PATMuonCleaner.cc "PhysicsTools/PatAlgos/plugins/PATMuonCleaner.cc"
  \brief    Produces a clean list of pat::Muons

  The PATMuonCleaner produces a list of clean pat::Muons

  First, a string-based preselection is applied.
  Also, an additional overlap checking based on deltaR or the Candidate OverlapChecker can be applied.

  The muon selection is based on reconstruction, custom selection or muon
  identification algorithms (to be implemented). It is steered by the configuration 
  parameters:

\code
 PSet selection = {
   string type = "none | globalMuons | muonPOG | custom"
   [ // If custom, give cut values
     double dPbyPmax = ...
     double chi2max  = ...
     int    nHitsMin = ...
   ]
 }
\endcode

  \author   The PAT team (twiki:SWGuidePAT, and hn-cms-physTools@cern.ch)
  \version  $Id: PATMuonCleaner.cc,v 1.9 2008/05/14 12:10:48 fronga Exp $
*/

#include "PhysicsTools/PatAlgos/plugins/PATCleanerBase.h"
#include "DataFormats/PatCandidates/interface/Muon.h"

#include "PhysicsTools/UtilAlgos/interface/ParameterAdapter.h"
#include "PhysicsTools/PatUtils/interface/MuonSelector.h"

namespace pat {

  class PATMuonCleaner : public pat::PATCleanerBase<pat::Muon> {

    public:
      explicit PATMuonCleaner(const edm::ParameterSet & iConfig);
      ~PATMuonCleaner() {}

      /// Perform the real cleaning
      ///   preselected = items passing the string-based preselection cut
      ///   overlaps    = result of simple overlap checking (see OverlapHelper docs)
      ///                 it may be a NULL pointer if overlap checking is not enabled
      ///   output      = put your selected items here
      ///   iEvent, iSetup = you might want these
      virtual void clean(const edm::PtrVector<pat::Muon> & preselected,
                         const pat::helper::OverlapHelper::Result *overlaps,
                         std::vector<pat::Muon>  & output,
                         edm::Event & iEvent, const edm::EventSetup & iSetup) ;

    private:
      edm::ParameterSet selectionCfg_; ///< Defines everything about the selection
      MuonSelector      selector_;     ///< Actually performs the selection

  };

}

namespace reco {
  namespace modules {
    /// Helper struct to convert from ParameterSet to MuonSelection
    template<> 
    struct ParameterAdapter<pat::MuonSelector> { 
      static pat::MuonSelector make(const edm::ParameterSet & cfg) {
        pat::MuonSelection config_;
        const std::string& selectionType = cfg.getParameter<std::string>("type");
        config_.selectionType = selectionType;
        if      ( selectionType == "custom" )
          {
            config_.dPbyPmax  = cfg.getParameter<double>("dPbyPmax");
            config_.chi2max  = cfg.getParameter<double>("chi2max");
            config_.nHitsMin = cfg.getParameter<int>("nHitsMin");
          }
        else if ( selectionType == "muonPOG" )
          {
            std::string flag = cfg.getParameter<std::string>("flag");
            if      ( flag == "TMLastStationLoose" ) {
              config_.flag = muonid::TMLastStationLoose;
            }
            else if ( flag == "TMLastStationTight" ) {
              config_.flag = muonid::TMLastStationTight;
            }
            else if ( flag == "TM2DCompatibilityLoose" ) {
              config_.flag = muonid::TM2DCompatibilityLoose;
            }
            else if ( flag == "TM2DCompatibilityTight" ) {
              config_.flag = muonid::TM2DCompatibilityTight;
            }
            else {
              throw edm::Exception(edm::errors::UnimplementedFeature) 
                << "muonPOG flag is not valid or not implemented yet";
            }
            config_.minCaloCompatibility    = cfg.getParameter<double>("minCaloCompatibility");
            config_.minSegmentCompatibility = cfg.getParameter<double>("minSegmentCompatibility");
          }
        return pat::MuonSelector( config_ );
      }
    };
  }
}


pat::PATMuonCleaner::PATMuonCleaner(const edm::ParameterSet & iConfig) :
  pat::PATCleanerBase<pat::Muon>(iConfig),
  selectionCfg_(iConfig.getParameter<edm::ParameterSet>("selection")),
  selector_(reco::modules::make<MuonSelector>(selectionCfg_))
{
}

void 
pat::PATMuonCleaner::clean(const edm::PtrVector<pat::Muon> & preselected,
                         const pat::helper::OverlapHelper::Result *overlaps,
                         std::vector<pat::Muon>  & output,
                         edm::Event & iEvent, const edm::EventSetup & iSetup)
{
  for (size_t idx = 0, size = preselected.size(); idx < size; ++idx) {
    const edm::Ptr<pat::Muon> & muon = preselected[idx];;    

    if ((overlaps != 0) && ((*overlaps)[idx] != 0)) {
        continue; // FIXME should do something smarter?
    }

    // FIXME can't do this because MuonSelector expects for a View
    /* 
    if ( selector_.filter(muon) != pat::GOOD ) {
        helper_.addMark(selIdx, pat::Flags::Selection::Bit0); // opaque, at the moment
    }
    */
    
    output.push_back(*muon);
  }
}

#include "FWCore/Framework/interface/MakerMacros.h"
using pat::PATMuonCleaner;
DEFINE_FWK_MODULE(PATMuonCleaner);
