//
// $Id: PATMHTProducer.cc,v 1.3 2008/09/08 20:40:03 xs32 Exp xs32 $
//

#include "PhysicsTools/PatAlgos/plugins/PATMHTProducer.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ParameterSet/interface/FileInPath.h"
#include "DataFormats/Common/interface/View.h"

#include "DataFormats/Math/interface/LorentzVector.h"
#include "DataFormats/PatCandidates/interface/MHT.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "RecoMET/METAlgorithms/interface/SigInputObj.h"
#include "RecoMET/METAlgorithms/interface/SignAlgoResolutions.h"
#include "RecoMET/METAlgorithms/interface/significanceAlgo.h"
#include "DataFormats/Candidate/interface/Candidate.h"

 
#include <memory>


//using namespace pat;


pat::PATMHTProducer::PATMHTProducer(const edm::ParameterSet & iConfig){

  // Initialize the configurables
  mhtLabel_ = iConfig.getUntrackedParameter<edm::InputTag>("missingHTTag");
  jetLabel_ = iConfig.getUntrackedParameter<edm::InputTag>("jetTag");
  eleLabel_ = iConfig.getUntrackedParameter<edm::InputTag>("electronTag");
  muoLabel_ = iConfig.getUntrackedParameter<edm::InputTag>("muonTag");
  tauLabel_ = iConfig.getUntrackedParameter<edm::InputTag>("tauTag");
  phoLabel_ = iConfig.getUntrackedParameter<edm::InputTag>("photonTag");
  
  // Produce MHT and the corresponding Significance
  produces<double>(mhtLabel_.label());
  produces<pat::MHT>(mhtLabel_.label());

}


pat::PATMHTProducer::~PATMHTProducer() {
}

void pat::PATMHTProducer::beginJob(const edm::EventSetup& iSetup) {
}
void pat::PATMHTProducer::beginRun(const edm::EventSetup& iSetup) {
}

void pat::PATMHTProducer::endJob() {
}


void pat::PATMHTProducer::produce(edm::Event & iEvent, const edm::EventSetup & iSetup) {
  // Get the jet object

  edm::Handle<edm::View<pat::Jet> > jetHandle;
  iEvent.getByLabel(jetLabel_,jetHandle);
  edm::View<pat::Jet> jets = *jetHandle;

  // Fill Input Vector with Jets 
  std::string objectname="";
  for(edm::View<pat::Jet>::const_iterator jet_iter = jets.begin(); jet_iter!=jets.end(); ++jet_iter){
    double jet_px = jet_iter->px();
    double jet_py = jet_iter->py();
    double sigma_et = jet_iter->resolutionEt();
    double sigma_phi = jet_iter->resolutionPhi();
    objectname="jet";
    // try to read out the jet resolution from the root file at PatUtils
    //-- Store jet for Significance Calculation --//
    metsig::SigInputObj tmp_jet(objectname,jet_px,jet_py,sigma_et,sigma_phi);
    physobjvector_.push_back(tmp_jet);
     
  }
  
  double met_x=0;
  double met_y=0;
  double met_set=0;
  
  // calculate the significance

  double significance = ASignificance(physobjvector_, met_x, met_y, met_set);

  // and fill the output into the event..
  std::auto_ptr<pat::MHT> themetsigobj (new pat::MHT(math::XYZTLorentzVector(met_x,met_y,0,sqrt(met_x*met_x+met_y*met_y)),met_set,significance));
  iEvent.put( themetsigobj, mhtLabel_.label());
  //double significance = 0.0;

  std::auto_ptr<double> themetsig(new double(significance));
  iEvent.put( themetsig, mhtLabel_.label() );

}  


using namespace pat; 
DEFINE_FWK_MODULE(PATMHTProducer);

