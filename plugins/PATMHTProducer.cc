//
// $Id: PATMHTProducer.cc,v 1.23 2009/01/19 19:38:31 xs32 Exp $
//

#include "PhysicsTools/PatAlgos/plugins/PATMHTProducer.h"

pat::PATMHTProducer::PATMHTProducer(const edm::ParameterSet & iConfig){

  // Initialize the configurables
  verbose_ = iConfig.getParameter<double>("verbose");

  jetLabel_ = iConfig.getUntrackedParameter<edm::InputTag>("jetTag");
  eleLabel_ = iConfig.getUntrackedParameter<edm::InputTag>("electronTag");
  muoLabel_ = iConfig.getUntrackedParameter<edm::InputTag>("muonTag");
  tauLabel_ = iConfig.getUntrackedParameter<edm::InputTag>("tauTag");
  phoLabel_ = iConfig.getUntrackedParameter<edm::InputTag>("photonTag");
  
  uncertaintyScaleFactor_ = iConfig.getParameter<double>( "uncertaintyScaleFactor") ;
  controlledUncertainty_  = iConfig.getParameter<bool>( "controlledUncertainty") ;

  jetPtMin_     = iConfig.getParameter<double>("jetPtMin");
  jetEtaMax_    = iConfig.getParameter<double>("jetEtaMax");
  jetEMfracMax_ = iConfig.getParameter<double>("jetEMfracMax");
  elePtMin_     = iConfig.getParameter<double>("elePtMin");
  eleEtaMax_    = iConfig.getParameter<double>("eleEtaMax");
  muonPtMin_    = iConfig.getParameter<double>("muonPtMin");
  muonEtaMax_   = iConfig.getParameter<double>("muonEtaMax");

  jetEtUncertaintyParameter0_ =  iConfig.getParameter<double>( "jetEtUncertaintyParameter0") ; 
  jetEtUncertaintyParameter1_ =  iConfig.getParameter<double>( "jetEtUncertaintyParameter1") ; 
  jetEtUncertaintyParameter2_ =  iConfig.getParameter<double>( "jetEtUncertaintyParameter2") ; 
  jetPhiUncertaintyParameter0_=  iConfig.getParameter<double>( "jetPhiUncertaintyParameter0"); 
  jetPhiUncertaintyParameter1_=  iConfig.getParameter<double>( "jetPhiUncertaintyParameter1"); 
  jetPhiUncertaintyParameter2_=  iConfig.getParameter<double>( "jetPhiUncertaintyParameter2"); 
    
  eleEtUncertaintyParameter0_  =  iConfig.getParameter<double>( "eleEtUncertaintyParameter0") ; 
  elePhiUncertaintyParameter0_ =  iConfig.getParameter<double>( "elePhiUncertaintyParameter0") ; 

  muonEtUncertaintyParameter0_  =  iConfig.getParameter<double>( "muonEtUncertaintyParameter0") ; 
  muonPhiUncertaintyParameter0_ =  iConfig.getParameter<double>( "muonPhiUncertaintyParameter0") ; 

  produces<pat::MHTCollection>();

}


pat::PATMHTProducer::~PATMHTProducer() {
}

void pat::PATMHTProducer::beginJob(const edm::EventSetup& iSetup) {
  setUncertaintyParameters();
}
void pat::PATMHTProducer::beginRun(const edm::EventSetup& iSetup) {
}

void pat::PATMHTProducer::endJob() {
}


void 
pat::PATMHTProducer::produce(edm::Event & iEvent, const edm::EventSetup & iSetup) 
{
  // make sure the SigInputObj container is empty
  while(physobjvector_.size()>0){
    physobjvector_.erase(physobjvector_.begin(),physobjvector_.end());
  }

  double number_of_jets = getJets(iEvent, iSetup);

  double number_of_electrons = getElectrons(iEvent, iSetup);

  double number_of_muons = getMuons(iEvent, iSetup);

  if (verbose_ > 1.) {
    std::cout << ">>>---> Number of jets: "  <<  number_of_jets << std::endl;
    std::cout << ">>>---> Number of electrons: "  <<  number_of_jets << std::endl;
    std::cout << ">>>---> Number of muons: " <<  number_of_muons << std::endl;
  }

  double met_x=0;
  double met_y=0;
  double met_et=0;
  double met_phi=0;
  double met_set=0;
  
  // calculate the significance

  double significance = ASignificance(physobjvector_, met_et, met_phi, met_set);
  met_x=met_et*cos(met_phi);
  met_y=met_et*sin(met_phi);

  edm::LogInfo("PATMHTProducer")    << " met x,y: " << met_x << "," << met_y << " met_set: " << met_set << " met_et/sqrt(met_set): " << met_et/sqrt(met_set) << " met_phi: " << met_phi << " met_et: " << met_et << " met_et/sqrt(x,y): " << met_et/sqrt(met_x*met_x+met_y*met_y) << " met_sign: " << significance << std::endl;
  // and fill the output into the event..

  std::auto_ptr<pat::MHTCollection>  themetsigcoll (new pat::MHTCollection);
  pat::MHT themetsigobj(Particle::LorentzVector(met_x,met_y,0,met_et),met_set,significance);


  // Store the number of jets, electrons, muons
  themetsigobj.setNumberOfJets(number_of_jets);
  themetsigobj.setNumberOfElectrons(number_of_electrons);
  themetsigobj.setNumberOfMuons(number_of_muons);

  themetsigcoll->push_back(themetsigobj);

  iEvent.put( themetsigcoll);

}  

// --------------------------------------------------
//  Fill Input Vector with Jets
// --------------------------------------------------
double 
pat::PATMHTProducer::getJets(edm::Event& iEvent, const edm::EventSetup & iSetup){

  std::string objectname="jet";

  double number_of_jets_ = 0.0;

  edm::Handle<edm::View<pat::Jet> > jetHandle;
  iEvent.getByLabel(jetLabel_,jetHandle);
  edm::View<pat::Jet> jets = *jetHandle;

  for(edm::View<pat::Jet>::const_iterator jet_iter = jets.begin(); jet_iter!=jets.end(); ++jet_iter){
    
    if( (jet_iter->pt()  < jetPtMin_) ||
	(TMath::Abs(jet_iter->eta()) > jetEtaMax_) || 
        (jet_iter->emEnergyFraction() > jetEMfracMax_ ) )
      continue; 
    
    double jet_et = jet_iter->et();
    double jet_phi = jet_iter->phi();
    
    if (verbose_ > 1.) {
      std::cout << "jet pt : " << jet_iter->pt() << " eta : " << jet_iter->eta() 
		<< " EMF: "  << jet_iter->emEnergyFraction() <<  std::endl;
    }
    
    double sigma_et, sigma_phi ;

    if (controlledUncertainty_) {
      sigma_et  = jetUncertainty.etUncertainty->Eval(jet_et);
      sigma_phi = jetUncertainty.phiUncertainty->Eval(jet_et);
    } 
    else {
      sigma_et = jet_iter->resolutionEt();
      sigma_phi = jet_iter->resolutionPhi();
    }

    if (verbose_ > 1.) {
      std::cout << "jet sigma_et : " << sigma_et << ", jet sigma_phi : " << sigma_phi <<  std::endl;
    }

    if(sigma_et<=0 || sigma_phi<=0)
      edm::LogWarning("PATMHTProducer") << 
	" uncertainties for "  << objectname <<
	" are (et, phi): " << sigma_et << "," << sigma_phi << " (et,phi): " << jet_et << "," << jet_phi;

    //-- Store jet for Significance Calculation --//
    if (uncertaintyScaleFactor_ != 1.0){
      sigma_et  = sigma_et  * uncertaintyScaleFactor_;
      sigma_phi = sigma_phi * uncertaintyScaleFactor_;
    }

    metsig::SigInputObj tmp_jet(objectname,jet_et,jet_phi,sigma_et,sigma_phi);
    physobjvector_.push_back(tmp_jet);
    number_of_jets_ ++;
  }
  
  return number_of_jets_;

}


// --------------------------------------------------
//  Fill Input Vector with Electrons
// --------------------------------------------------
double
pat::PATMHTProducer::getElectrons(edm::Event& iEvent, const edm::EventSetup & iSetup){

  std::string objectname="electron";

  double number_of_electrons_ = 0.0;

  edm::Handle<edm::View<pat::Electron> > electronHandle;
  iEvent.getByLabel(eleLabel_,electronHandle);
  edm::View<pat::Electron> electrons = *electronHandle;
  DetId nullDetId;

  // Fill Input Vector with Electrons 
  for(edm::View<pat::Electron>::const_iterator electron_iter = electrons.begin(); electron_iter!=electrons.end(); ++electron_iter){

    // Select electrons
    if (electron_iter->et() < elePtMin_ || 
	TMath::Abs(electron_iter->eta()) > eleEtaMax_  ) continue; 

    if (verbose_ > 1.) {
      std::cout << "electron pt = " << electron_iter->pt()  << " eta : " << electron_iter->eta() 
		<<  std::endl;
    }

    double electron_et  = electron_iter->et();
    double electron_phi = electron_iter->phi();

    double sigma_et, sigma_phi ;

    if (controlledUncertainty_) {
      sigma_et  = eleUncertainty.etUncertainty->Eval(electron_et);
      sigma_phi = eleUncertainty.phiUncertainty->Eval(electron_et);
    } 
    else {
      sigma_et = electron_iter->resolutionEt();
      sigma_phi = electron_iter->resolutionPhi();
    }

    if (verbose_ > 1.) {
      std::cout << "electron sigma_et : " << sigma_et << ", electron sigma_phi : " << sigma_phi
		<<  std::endl;}

    if(sigma_et< 0 || sigma_phi< 0)
      edm::LogWarning("PATMHTProducer") << " uncertainties for "  << objectname 
					<<" are (et, phi): " << sigma_et 
					<< "," << sigma_phi <<  " (et,phi): " 
					<< electron_et << "," << electron_phi;
    
    if (uncertaintyScaleFactor_ != 1.0){
      sigma_et  = sigma_et  * uncertaintyScaleFactor_;
      sigma_phi = sigma_phi * uncertaintyScaleFactor_;
    }

    metsig::SigInputObj tmp_electron(objectname,electron_et,electron_phi,sigma_et,sigma_phi);
    physobjvector_.push_back(tmp_electron);
    number_of_electrons_ ++; 
    
  }

  return number_of_electrons_; 
}



// --------------------------------------------------
//  Fill Input Vector with Muons
// --------------------------------------------------

double pat::PATMHTProducer::getMuons(edm::Event& iEvent, const edm::EventSetup & iSetup){

  std::string objectname="muon";
  edm::Handle<edm::View<pat::Muon> > muonHandle;
  iEvent.getByLabel(muoLabel_,muonHandle);
  edm::View<pat::Muon> muons = *muonHandle;

  double number_of_muons_ = 0.0;

  for(edm::View<pat::Muon>::const_iterator muon_iter = muons.begin(); muon_iter!=muons.end(); ++muon_iter){

    if (muon_iter->pt() < muonPtMin_ || TMath::Abs(muon_iter->eta()) > muonEtaMax_  ) continue; 

    if (verbose_ > 1.) {
      std::cout << "muon pt = " << muon_iter->pt() << " eta : " << muon_iter->eta() <<  std::endl;
    }

    double muon_pt  = muon_iter->pt();
    double muon_phi = muon_iter->phi();

    double sigma_et, sigma_phi ;

    if (controlledUncertainty_) {
       sigma_et  = muonUncertainty.etUncertainty->Eval(muon_pt);
       sigma_phi = muonUncertainty.phiUncertainty->Eval(muon_pt);
    } 
    else {
      sigma_et  = muon_iter->resolutionEt();
      sigma_phi = muon_iter->resolutionPhi();
    }

    if (verbose_ > 1.) {
      std::cout << "muon sigma_et : " << sigma_et
		<< ", muon sigma_phi : " << sigma_phi
		<<  std::endl;}

   if(sigma_et< 0 || sigma_phi< 0)
      edm::LogWarning("PATMHTProducer") << 
	" uncertainties for "  << objectname << " are (et, phi): " << sigma_et << "," <<
	sigma_phi << " (pt,phi): " << muon_pt << "," << muon_phi;

    if (uncertaintyScaleFactor_ != 1.0){
      sigma_et  = sigma_et  * uncertaintyScaleFactor_;
      sigma_phi = sigma_phi * uncertaintyScaleFactor_;
    }

    metsig::SigInputObj tmp_muon(objectname,muon_pt,muon_phi,sigma_et,sigma_phi);
    physobjvector_.push_back(tmp_muon);
    number_of_muons_ ++;
  }

  return number_of_muons_;
}


// --------------------------------------------------
//  Fill Input Vector with Taus and Photons ...
// --------------------------------------------------

  /* We'll deal with photons and taus later for sure

  edm::Handle<edm::View<pat::Photon> > photonHandle;
  iEvent.getByLabel(phoLabel_,photonHandle);
  edm::View<pat::Photon> photons = *photonHandle;

  // Fill Input Vector with Photons 
  for(edm::View<pat::Photon>::const_iterator photon_iter = photons.begin(); photon_iter!=photons.end(); ++photon_iter){
    double photon_et = photon_iter->et();
    double photon_phi = photon_iter->phi();
    double sigma_et = photon_iter->resolutionEt();
    double sigma_phi = photon_iter->resolutionPhi();
    objectname="photon";
    if(sigma_et<=0 || sigma_phi<=0)
      edm::LogWarning("PATMHTProducer") << " uncertainties for "  << objectname << " are (et, phi): " << sigma_et << "," << sigma_phi << " (et,phi): " << photon_et << "," << photon_phi;
    // try to read out the photon resolution from the root file at PatUtils
    //-- Store photon for Significance Calculation --//
    metsig::SigInputObj tmp_photon(objectname,photon_et,photon_phi,sigma_et,sigma_phi);
    physobjvector_.push_back(tmp_photon);
     
  }


  edm::Handle<edm::View<pat::Tau> > tauHandle;
  iEvent.getByLabel(tauLabel_,tauHandle);
  edm::View<pat::Tau> taus = *tauHandle;

  std::cout << "------ Filling taus ... ---------" <<  std::endl;
  // Fill Input Vector with Taus 
  for(edm::View<pat::Tau>::const_iterator tau_iter = taus.begin(); tau_iter!=taus.end(); ++tau_iter){
    double tau_pt = tau_iter->pt();
    double tau_phi = tau_iter->phi();
    double sigma_et = tau_iter->resolutionEt();
    double sigma_phi = tau_iter->resolutionPhi();
    std::cout << "sigma_et = " << sigma_et << " , sigma_phi = " << sigma_phi << std::endl;

    objectname="tau";
    if(sigma_et<=0 || sigma_phi<=0)
      edm::LogWarning("PATMHTProducer") << " uncertainties for "  << objectname << " are (et, phi): " << sigma_et << "," << sigma_phi << " (pt,phi): " << tau_pt << "," << tau_phi;
    // try to read out the tau resolution from the root file at PatUtils
    //-- Store tau for Significance Calculation --//
    metsig::SigInputObj tmp_tau(objectname,tau_pt,tau_phi,sigma_et,sigma_phi);
    physobjvector_.push_back(tmp_tau);
     
  }
  */




//=== Uncertainty Functions ===============================================
void pat::PATMHTProducer::setUncertaintyParameters(){

  // set the various functions here:

  //-- For Et functions, [0]= par_n, [1]=par_s, [2]= par_c ---//
  //-- Ecal Uncertainty Functions ------------------------------------//
  //-- From: FastSimulation/Calorimetry/data/HcalResponse.cfi --//
  //-- Ecal Barrel --//
  ecalEBUncertainty.etUncertainty = new TF1("ecalEBEtFunc","x*sqrt(([0]*[0]/(x*x))+([1]*[1]/x)+([2]*[2]))",3);
  ecalEBUncertainty.etUncertainty->SetParameter(0,0.2);
  ecalEBUncertainty.etUncertainty->SetParameter(1,0.03);
  ecalEBUncertainty.etUncertainty->SetParameter(2,0.005);

  ecalEBUncertainty.phiUncertainty = new TF1("ecalEBphiFunc","[0]*x",1);
  ecalEBUncertainty.phiUncertainty->SetParameter(0,0.0174);

  //-- Ecal Endcap --//
  ecalEEUncertainty.etUncertainty = new TF1("ecalEEEtFunc","x*sqrt(([0]*[0]/(x*x))+([1]*[1]/x)+([2]*[2]))",3);
  ecalEEUncertainty.etUncertainty->SetParameter(0,0.2);
  ecalEEUncertainty.etUncertainty->SetParameter(1,0.03);
  ecalEEUncertainty.etUncertainty->SetParameter(2,0.005);

  ecalEEUncertainty.phiUncertainty = new TF1("ecalEEphiFunc","[0]*x",1);
  ecalEEUncertainty.phiUncertainty->SetParameter(0,0.087);

  //-- Hcal Uncertainty Functions --------------------------------------//
  //-- From: FastSimulation/Calorimetry/data/HcalResponse.cfi --//
  //-- Hcal Barrel --//
  hcalHBUncertainty.etUncertainty = new TF1("hcalHBEtFunc","x*sqrt(([0]*[0]/(x*x))+([1]*[1]/x)+([2]*[2]))",3);
  hcalHBUncertainty.etUncertainty->SetParameter(0,0.);
  hcalHBUncertainty.etUncertainty->SetParameter(1,1.22);
  hcalHBUncertainty.etUncertainty->SetParameter(2,0.05);

  hcalHBUncertainty.phiUncertainty = new TF1("ecalHBphiFunc","[0]*x",1);
  hcalHBUncertainty.phiUncertainty->SetParameter(0,0.087);

  //-- Hcal Endcap --//
  hcalHEUncertainty.etUncertainty = new TF1("hcalHEEtFunc","x*sqrt(([0]*[0]/(x*x))+([1]*[1]/x)+([2]*[2]))",3);
  hcalHEUncertainty.etUncertainty->SetParameter(0,0.);
  hcalHEUncertainty.etUncertainty->SetParameter(1,1.3);
  hcalHEUncertainty.etUncertainty->SetParameter(2,0.05);

  hcalHEUncertainty.phiUncertainty = new TF1("ecalHEphiFunc","[0]*x",1);
  hcalHEUncertainty.phiUncertainty->SetParameter(0,0.087);

  //-- Hcal Outer --//
  hcalHOUncertainty.etUncertainty = new TF1("hcalHOEtFunc","x*sqrt(([0]*[0]/(x*x))+([1]*[1]/x)+([2]*[2]))",3);
  hcalHOUncertainty.etUncertainty->SetParameter(0,0.);
  hcalHOUncertainty.etUncertainty->SetParameter(1,1.82);
  hcalHOUncertainty.etUncertainty->SetParameter(2,0.09);

  hcalHOUncertainty.phiUncertainty = new TF1("ecalHOphiFunc","[0]*x",1);
  hcalHOUncertainty.phiUncertainty->SetParameter(0,0.087);

  //-- Hcal Forward --//
  hcalHFUncertainty.etUncertainty = new TF1("hcalHFEtFunc","x*sqrt(([0]*[0]/(x*x))+([1]*[1]/x)+([2]*[2]))",3);
  hcalHFUncertainty.etUncertainty->SetParameter(0,0.);
  hcalHFUncertainty.etUncertainty->SetParameter(1,1.82);
  hcalHFUncertainty.etUncertainty->SetParameter(2,0.09);

  hcalHFUncertainty.phiUncertainty = new TF1("ecalHFphiFunc","[0]*x",1);
  hcalHFUncertainty.phiUncertainty->SetParameter(0,0.174);

  //--- Jet Uncertainty Functions --------------------------------------//
  jetUncertainty.etUncertainty = new TF1("jetEtFunc","x*sqrt(([0]*[0]/(x*x))+([1]*[1]/x)+([2]*[2]))",3);
  //-- values from PTDR 1, ch 11.4 --//
  jetUncertainty.etUncertainty->SetParameter(0, jetEtUncertaintyParameter0_);
  jetUncertainty.etUncertainty->SetParameter(1, jetEtUncertaintyParameter1_);
  jetUncertainty.etUncertainty->SetParameter(2, jetEtUncertaintyParameter2_);


  //-- phi value from our own fits --//
  //jetUncertainty.phiUncertainty = new TF1("jetPhiFunc","[0]*x",1);
  //jetUncertainty.phiUncertainty->SetParameter(0, jetPhiUncertaintyParameter0_);

  //-- phi Functions and values from 
  // http://indico.cern.ch/getFile.py/access?contribId=9&sessionId=0&resId=0&materialId=slides&confId=46394
  jetUncertainty.phiUncertainty = new TF1("jetPhiFunc","x*sqrt(([0]*[0]/(x*x))+([1]*[1]/x)+([2]*[2]))",3);
  jetUncertainty.phiUncertainty->SetParameter(0, jetPhiUncertaintyParameter0_);
  jetUncertainty.phiUncertainty->SetParameter(1, jetPhiUncertaintyParameter1_);
  jetUncertainty.phiUncertainty->SetParameter(2, jetPhiUncertaintyParameter2_);
  


  //-- Jet corrections are assumed not to have an error --//
  /*jetCorrUncertainty.etUncertainty = new TF1("jetCorrEtFunc","[0]*x",1);
  jetCorrUncertainty.etUncertainty->SetParameter(0,0.0);
  jetCorrUncertainty.phiUncertainty = new TF1("jetCorrPhiFunc","[0]*x",1);
  jetCorrUncertainty.phiUncertainty->SetParameter(0,0.0*(3.14159/180.));*/


  //--- Electron Uncertainty Functions ---------------------------------//
  // completely ambiguious values for electron-like jets...
  // the egamma group keeps track of these here:
  // https://twiki.cern.ch/twiki/bin/view/CMS/EgammaCMSSWVal
  // electron resolution in energy is around 3.4%, measured for 10 < pT < 50 at realistic events with pile-up.
  
  eleUncertainty.etUncertainty = new TF1("eleEtFunc","[0] * x",1);
  //  eleUncertainty.etUncertainty->SetParameter(0,0.034); 
  eleUncertainty.etUncertainty->SetParameter(0, eleEtUncertaintyParameter0_); 


  eleUncertainty.phiUncertainty = new TF1("elePhiFunc","[0] * x",1);
  //  eleUncertainty.phiUncertainty->SetParameter(0,1*(3.14159/180.));
  eleUncertainty.phiUncertainty->SetParameter(0, elePhiUncertaintyParameter0_);

  //--- Muon Uncertainty Functions ------------------------------------//
  // and ambiguious values for the muons...
  
  muonUncertainty.etUncertainty = new TF1("muonEtFunc","[0] * x",1);
  //  muonUncertainty.etUncertainty->SetParameter(0,0.01);
  muonUncertainty.etUncertainty->SetParameter(0, muonEtUncertaintyParameter0_);
  muonUncertainty.phiUncertainty = new TF1("muonPhiFunc","[0] * x",1);
  //  muonUncertainty.phiUncertainty->SetParameter(0,1*(3.14159/180.));
  muonUncertainty.phiUncertainty->SetParameter(0, muonPhiUncertaintyParameter0_);

  //-- Muon calo deposites are assumed not to have an error --//
  /*muonCorrUncertainty.etUncertainty = new TF1("muonCorrEtFunc","[0] * x",1);
  muonCorrUncertainty.etUncertainty->SetParameter(0,0.0);
  muonCorrUncertainty.phiUncertainty = new TF1("muonCorrPhiFunc","[0] * x",1);
  muonCorrUncertainty.phiUncertainty->SetParameter(0,0.0*(3.14159/180.)); */
 
}




using namespace pat; 
DEFINE_FWK_MODULE(PATMHTProducer);

