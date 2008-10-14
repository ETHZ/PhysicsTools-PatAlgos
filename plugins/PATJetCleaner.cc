//
// $Id: PATJetCleaner.cc,v 1.6 2008/05/06 20:13:50 gpetrucc Exp $
//

/**
  \class    pat::PATJetCleaner PATJetCleaner.cc "PhysicsTools/PatAlgos/plugins/PATJetCleaner.cc"
  \brief    Produces a clean list of pat::Jets

   The PATJetCleaner produces a clean list of pat::Jets

  First, a string-based preselection is applied.
  Also, an additional overlap checking based on deltaR or the Candidate OverlapChecker can be applied.

  The actual selection is performed by the JetSelector.

  \author   The PAT team (twiki:SWGuidePAT; hn-cms-physTools@cern.ch)
  \version  $Id: PATJetCleaner.cc,v 1.7.2.1 2008/10/10 19:24:04 gpetrucc Exp $

*/

#include "PhysicsTools/PatAlgos/plugins/PATCleanerBase.h"
#include "DataFormats/PatCandidates/interface/Jet.h"

// Can't use this at all
/*
#include "PhysicsTools/PatUtils/interface/JetSelector.h"
#include "PhysicsTools/PatUtils/interface/JetSelector.icc"
#include "PhysicsTools/PatUtils/interface/JetSelection.h"
*/

namespace pat {

  class PATJetCleaner : public pat::PATCleanerBase<pat::Jet> {

    public:

      explicit PATJetCleaner(const edm::ParameterSet & iConfig);
      ~PATJetCleaner() {}

      /// Perform the real cleaning
      ///   preselected = items passing the string-based preselection cut
      ///   overlaps    = result of simple overlap checking (see OverlapHelper docs)
      ///                 it may be a NULL pointer if overlap checking is not enabled
      ///   output      = put your selected items here
      ///   iEvent, iSetup = you might want these
      virtual void clean(const edm::PtrVector<pat::Jet> & preselected,
                         const pat::helper::OverlapHelper::Result *overlaps,
                         std::vector<pat::Jet>  & output,
                         edm::Event & iEvent, const edm::EventSetup & iSetup) ;
    private:
      /*
      ///Jet Selection  similar to Electrons
      edm::ParameterSet selectionCfg_;  ///< Defines all about the selection
      typedef JetSelector<pat::Jet> JetSelectorType;
      std::auto_ptr<JetSelectorType> selector_;   ///< Actually performs the selection
      
      /// Helper method to fill configuration selection struct
      // Because I wasn't able to use the ParameterAdapter here (templates...)
      const JetSelection fillSelection_( const edm::ParameterSet & iConfig);
      */
  };
}

pat::PATJetCleaner::PATJetCleaner(const edm::ParameterSet & iConfig) :
    pat::PATCleanerBase<pat::Jet>(iConfig)
{
}

void 
pat::PATJetCleaner::clean(const edm::PtrVector<pat::Jet> & preselected,
                         const pat::helper::OverlapHelper::Result *overlaps,
                         std::vector<pat::Jet>  & output,
                         edm::Event & iEvent, const edm::EventSetup & iSetup)
{
  for (size_t idx = 0, size = preselected.size(); idx < size; ++idx) {
    const edm::Ptr<pat::Jet> & jet = preselected[idx];;    

    if ((overlaps != 0) && ((*overlaps)[idx] != 0)) {
        continue; // FIXME should do something smarter?
    }

    // FIXME can't do this because JetSelector doesn't work on pat::Jet
    /* 
    if ( selector_.filter(idx,helper_.source(),(*electronIDs),clusterShape) != pat::GOOD) {
        helper_.addMark(selIdx, pat::Flags::Selection::Bit0); // opaque, at the moment
    }
    */

    output.push_back(*jet);
  }
}


#if 0
const pat::JetSelection
pat::PATJetCleaner::fillSelection_( const edm::ParameterSet & cfg)
{
  // Fill selector struct here: I'm not able to do it in the ParameterAdapter
  JetSelection config_;

  config_.selectionType = cfg.getParameter<std::string>("type");;
  if ( config_.selectionType == "IDmap" ) {
    config_.value = cfg.template getParameter<double>("value");
  } else if ( config_.selectionType == "custom" ) {
    config_.EMFmin                 = cfg.getParameter<double>("EMFmin");
    config_.EMFmax                 = cfg.getParameter<double>("EMFmax");
    config_.Etamax                 = cfg.getParameter<double>("Etamax");
    config_.Ptmin                  = cfg.getParameter<double>("Ptmin");
    config_.EMvsHadFmin            = cfg.getParameter<double>("EMvsHadFmin");
    config_.EMvsHadFmax            = cfg.getParameter<double>("EMvsHadFmax");
    config_.HadFmin                = cfg.getParameter<double>("HadFmin");
    config_.HadFmax                = cfg.getParameter<double>("HadFmax");
    config_.N90min                 = cfg.getParameter<double>("N90min");
    config_.N90max                 = cfg.getParameter<double>("N90max");
    config_.NCaloTowersmin         = cfg.getParameter<double>("NCaloTowersmin");
    config_.NCaloTowersmax         = cfg.getParameter<double>("NCaloTowersmax");
    config_.HighestTowerOverJetmin = cfg.getParameter<double>("HighestTowerOverJetmin");
    config_.HighestTowerOverJetmax = cfg.getParameter<double>("HighestTowerOverJetmax");
    config_.RWidthmin              = cfg.getParameter<double>("RWidthmin");
    config_.RWidthmax              = cfg.getParameter<double>("RWidthmax");
    config_.PtJetOverArea_min      = cfg.getParameter<double>("PtJetOverAreamin");
    config_.PtJetOverArea_max      = cfg.getParameter<double>("PtJetOverAreamax");
    config_.PtTowerOverArea_min    = cfg.getParameter<double>("PtTowerOverAreamin");
    config_.PtTowerOverArea_max    = cfg.getParameter<double>("PtTowerOverAreamax");
  }
  return config_;
}
#endif

#include "FWCore/Framework/interface/MakerMacros.h"
using namespace pat;
DEFINE_FWK_MODULE(PATJetCleaner);

