//
// $Id: PATElectronCleaner.cc,v 1.7 2008/06/20 13:15:31 gpetrucc Exp $
//

/**
  \class    pat::PATElectronCleaner PATElectronCleaner.cc "PhysicsTools/PatAlgos/plugins/PATElectronCleaner.cc"
  \brief    Produces a clean list of pat::Electrons

   The PATElectronCleaner produces a clean list of pat::Electrons

  First, a string-based preselection is applied.
  Also, an additional overlap checking based on deltaR or the Candidate OverlapChecker can be applied.

   The selection is based on the electron ID or on user-defined cuts.
   It is steered by the configuration parameters:

\code
 PSet selection = {
   string type = "none | cut | likelihood | neuralnet | custom"
   [ // If cut-based, give electron ID source
     InputTag eIdSource = <source>
   ]
   [ // If likelihood/neuralnet, give ID source and cut value
     InputTag eIdSource = <source>
     double value = xxx
   ]
   [ // If custom, give cluster shape sources and cut values
     InputTag clusterShapeBarrel = <source 1>
     InputTag clusterShapeEndcap = <source 2>
     double <cut> = <value>
     ...
   ]
 }
\endcode

  The actual selection is performed by the ElectronSelector.

  \author   The PAT team (twiki:SWGuidePAT; hn-cms-physTools@cern.ch)
  \version  $Id: PATElectronCleaner.h,v 1.7 2008/06/20 13:15:32 gpetrucc Exp $
*/

#include "PhysicsTools/PatAlgos/plugins/PATCleanerBase.h"
#include "DataFormats/PatCandidates/interface/Electron.h"

#include "DataFormats/EgammaReco/interface/ClusterShapeFwd.h"
#include "DataFormats/EgammaReco/interface/BasicClusterShapeAssociation.h"
#include "DataFormats/EgammaReco/interface/BasicCluster.h"

#include "PhysicsTools/UtilAlgos/interface/ParameterAdapter.h"
#include "PhysicsTools/PatUtils/interface/ElectronSelector.h"

namespace pat {

  class PATElectronCleaner : public pat::PATCleanerBase<pat::Electron> {

    public:
      explicit PATElectronCleaner(const edm::ParameterSet & iConfig);
      ~PATElectronCleaner() {}

      /// Perform the real cleaning
      ///   preselected = items passing the string-based preselection cut
      ///   overlaps    = result of simple overlap checking (see OverlapHelper docs)
      ///                 it may be a NULL pointer if overlap checking is not enabled
      ///   output      = put your selected items here
      ///   iEvent, iSetup = you might want these
      virtual void clean(const edm::PtrVector<pat::Electron> & preselected,
                         const pat::helper::OverlapHelper::Result *overlaps,
                         std::vector<pat::Electron>  & output,
                         edm::Event & iEvent, const edm::EventSetup & iSetup) ;
    private:
     edm::ParameterSet selectionCfg_;  ///< Defines all about the selection
      std::string       selectionType_; ///< Selection type (none, custom, cut,...)
      bool              doSelection_;   ///< False if type = "none", true otherwise
      ElectronSelector  selector_;      ///< Actually performs the selection

  };
}

namespace reco {
  namespace modules {
    /// Helper struct to convert from ParameterSet to ElectronSelection
    template<> 
    struct ParameterAdapter<pat::ElectronSelector> { 
      static pat::ElectronSelector make(const edm::ParameterSet & cfg) {
        pat::ElectronSelection config_;
        const std::string& selectionType = cfg.getParameter<std::string>("type");
        config_.selectionType = selectionType;
        if ( selectionType == "likelihood" || selectionType == "neuralnet" )
	  config_.value = cfg.getParameter<double>("value");
        else if ( selectionType == "custom" ) {
	  config_.HoverEBarmax        = cfg.getParameter<double>("HoverEBarmax");
	  config_.SigmaEtaEtaBarmax   = cfg.getParameter<double>("SigmaEtaEtaBarmax");
	  config_.SigmaPhiPhiBarmax   = cfg.getParameter<double>("SigmaPhiPhiBarmax");
	  config_.DeltaEtaInBarmax    = cfg.getParameter<double>("DeltaEtaInBarmax");
	  config_.DeltaPhiInBarmax    = cfg.getParameter<double>("DeltaPhiInBarmax");
	  config_.DeltaPhiOutBarmax   = cfg.getParameter<double>("DeltaPhiOutBarmax");
	  config_.EoverPInBarmin      = cfg.getParameter<double>("EoverPInBarmin");
	  config_.EoverPOutBarmin     = cfg.getParameter<double>("EoverPOutBarmin");
	  config_.InvEMinusInvPBarmax = cfg.getParameter<double>("InvEMinusInvPBarmax");
	  config_.E9overE25Barmin     = cfg.getParameter<double>("E9overE25Barmin");
	  config_.HoverEEndmax        = cfg.getParameter<double>("HoverEEndmax");
	  config_.SigmaEtaEtaEndmax   = cfg.getParameter<double>("SigmaEtaEtaEndmax");
	  config_.SigmaPhiPhiEndmax   = cfg.getParameter<double>("SigmaPhiPhiEndmax");
	  config_.DeltaEtaInEndmax    = cfg.getParameter<double>("DeltaEtaInEndmax");
	  config_.DeltaPhiInEndmax    = cfg.getParameter<double>("DeltaPhiInEndmax");
	  config_.DeltaPhiOutEndmax   = cfg.getParameter<double>("DeltaPhiOutEndmax");
	  config_.EoverPInEndmin      = cfg.getParameter<double>("EoverPInEndmin");
	  config_.EoverPOutEndmin     = cfg.getParameter<double>("EoverPOutEndmin");
	  config_.InvEMinusInvPEndmax = cfg.getParameter<double>("InvEMinusInvPEndmax");
	  config_.E9overE25Endmin     = cfg.getParameter<double>("E9overE25Endmin");
	  config_.doBremEoverPcomp    = cfg.getParameter<bool>  ("doBremEoverPcomp");
	}
        return pat::ElectronSelector( config_ );
      }
    };
  }
}

pat::PATElectronCleaner::PATElectronCleaner(const edm::ParameterSet & iConfig) :
    pat::PATCleanerBase<pat::Electron>(iConfig),
    selectionCfg_(iConfig.getParameter<edm::ParameterSet>("selection")),
    selectionType_(selectionCfg_.getParameter<std::string>("type")),
    selector_(reco::modules::make<ElectronSelector>(selectionCfg_)) 
{
}

void 
pat::PATElectronCleaner::clean(const edm::PtrVector<pat::Electron> & preselected,
                         const pat::helper::OverlapHelper::Result *overlaps,
                         std::vector<pat::Electron>  & output,
                         edm::Event & iEvent, const edm::EventSetup & iSetup)
{
  // Get additional info from the event, if needed
  //const reco::ClusterShape* clusterShape = 0;
  edm::Handle<reco::ElectronIDAssociationCollection> electronIDs;
  if ( selectionType_ != "none" && selectionType_ != "custom" ) {
    iEvent.getByLabel( selectionCfg_.getParameter<edm::InputTag>("eIdSource"), 
                       electronIDs );
  } 

  for (size_t idx = 0, size = preselected.size(); idx < size; ++idx) {
    const edm::Ptr<pat::Electron> & electron = preselected[idx];;    

    if ((overlaps != 0) && ((*overlaps)[idx] != 0)) {
        continue; // FIXME should do something smarter?
    }

    // FIXME can't do this because ElectronSelector expects for a View
    /* 
    if ( selector_.filter(idx,helper_.source(),(*electronIDs),clusterShape) != pat::GOOD) {
        helper_.addMark(selIdx, pat::Flags::Selection::Bit0); // opaque, at the moment
    }
    */

    output.push_back(*electron);
  }
}


#include "FWCore/Framework/interface/MakerMacros.h"
using pat::PATElectronCleaner;
DEFINE_FWK_MODULE(PATElectronCleaner);
