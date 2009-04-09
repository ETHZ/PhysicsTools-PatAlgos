#include "PhysicsTools/PatAlgos/plugins/JPTJetCorrFactorsProducer.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/Common/interface/View.h"
#include "DataFormats/JetReco/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/JetCorrFactors.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ParameterSet/interface/InputTag.h"
#include "JetMETCorrections/Algorithms/interface/JetPlusTrackCorrector.h"
#include "JetMETCorrections/Algorithms/interface/ZSPJetCorrector.h"
#include <vector>

using namespace pat;

// -----------------------------------------------------------------------------
//
JPTJetCorrFactorsProducer::JPTJetCorrFactorsProducer( const edm::ParameterSet& pset ) 
  : pset_( pset ),
    zspCorrector_( new ZSPJetCorrector(pset) ),
    jptCorrector_( new JetPlusTrackCorrector(pset) ),
    label_( pset_.getParameter<std::string>("@module_label") )
{
  produces< edm::ValueMap<pat::JetCorrFactors> >();
}

// -----------------------------------------------------------------------------
//
JPTJetCorrFactorsProducer::~JPTJetCorrFactorsProducer() {
  if ( zspCorrector_ ) { delete zspCorrector_; }
  if ( jptCorrector_ ) { delete jptCorrector_; }
}

// -----------------------------------------------------------------------------
//
void JPTJetCorrFactorsProducer::produce( edm::Event& event, const edm::EventSetup& setup ) { 

  // Check on pointers
  if ( !zspCorrector_ || !jptCorrector_ ) { return; }
  
  // Retrieve jet collection from the event
  edm::Handle< edm::View<reco::Jet> > jets;
  event.getByLabel( pset_.getParameter<edm::InputTag>("JetsInputTag"), jets );
  
  // Correction factors
  std::vector<JetCorrFactors> corrections;
  corrections.reserve( jets->size() );
  
  // Iterate through jets
  edm::View<reco::Jet>::const_iterator ijet = jets->begin();
  edm::View<reco::Jet>::const_iterator jjet = jets->end();
  for ( ; ijet != jjet; ++ijet ) { 
    
    // Defaults for different corrections
    float l1=-1, l3=-1;
    
    // Copy of jet
    reco::Jet refJet(*ijet);
    
    // ZSP correction
    l1 = zspCorrector_->correction( refJet );
    
    // Apply correction to (copy of) jet before JPT correction
    refJet.setP4( l1 * refJet.p4() );
    
    // JPT correction
    l3 = jptCorrector_->correction( refJet, event, setup );  
    
    // Create JetCorrFactors object
    float corr = 1.;
    JetCorrFactors::FlavourCorrections corrs(1.,1.,1.,1.);
    JetCorrFactors correction( label_, l1, corr, l3, corr, corrs, corrs, corrs );
    
    // Store corrections
    corrections.push_back(correction);
    
  } // Jet loop
  
  // Build map b/w jets and corrections
  std::auto_ptr< edm::ValueMap<pat::JetCorrFactors> > correctionsMap( new edm::ValueMap<pat::JetCorrFactors>() );
  edm::ValueMap<pat::JetCorrFactors>::Filler filler( *correctionsMap );
  filler.insert( jets, corrections.begin(), corrections.end() );
  filler.fill();
  
  // Put map in event
  event.put( correctionsMap );
  
}

#include "FWCore/Framework/interface/MakerMacros.h"
DEFINE_FWK_MODULE(JPTJetCorrFactorsProducer);
