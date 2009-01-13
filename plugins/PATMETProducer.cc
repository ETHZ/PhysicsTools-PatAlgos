//
// $Id: PATMETProducer.cc,v 1.20 2009/01/13 19:24:34 xs32 Exp $
//

#include "PhysicsTools/PatAlgos/plugins/PATMETProducer.h"

//using namespace pat;


pat::PATMETProducer::PATMETProducer(const edm::ParameterSet & iConfig) {
  // initialize the configurables
  metSrc_         = iConfig.getParameter<edm::InputTag>("metSource");
  addGenMET_      = iConfig.getParameter<bool>         ("addGenMET");
  genMETSrc_      = iConfig.getParameter<edm::InputTag>("genMETSource");
  addResolutions_ = iConfig.getParameter<bool>         ("addResolutions");
  useNNReso_      = iConfig.getParameter<bool>         ("useNNResolutions");
  metResoFile_    = iConfig.getParameter<std::string>  ("metResoFile");


  // For the MET Significance calculation
  verbose_ = iConfig.getParameter<double>("verbose");
  
  jetLabel_ = iConfig.getUntrackedParameter<edm::InputTag>("jetTag");
  eleLabel_ = iConfig.getUntrackedParameter<edm::InputTag>("electronTag");
  muoLabel_ = iConfig.getUntrackedParameter<edm::InputTag>("muonTag");

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
  
  CaloTowerTag_  = iConfig.getParameter<edm::InputTag>("CaloTowerTag");
  noHF_ = iConfig.getParameter<bool>( "noHF"); 



  // construct resolution calculator
  if (addResolutions_) metResoCalc_ = new ObjectResolutionCalc(edm::FileInPath(metResoFile_).fullPath(), useNNReso_);
  
  // produces vector of mets
  produces<std::vector<MET> >();
}


pat::PATMETProducer::~PATMETProducer() {
  if (addResolutions_) delete metResoCalc_;
}


void pat::PATMETProducer::beginJob(const edm::EventSetup& iSetup) {
  setUncertaintyParameters();
}
void pat::PATMETProducer::beginRun(const edm::EventSetup& iSetup) {
}

void pat::PATMETProducer::endJob() {
}



void pat::PATMETProducer::produce(edm::Event & iEvent, const edm::EventSetup & iSetup) {
 
  // Get the vector of MET's from the event
  edm::Handle<edm::View<METType> > mets;
  iEvent.getByLabel(metSrc_, mets);

  // Get the vector of generated met from the event if needed
  edm::Handle<edm::View<reco::GenMET> > genMETs;
  if (addGenMET_) {
    iEvent.getByLabel(genMETSrc_, genMETs);
  }

  // loop over mets
  std::vector<MET> * patMETs = new std::vector<MET>(); 
  for (edm::View<METType>::const_iterator itMET = mets->begin(); itMET != mets->end(); itMET++) {
    // construct the MET from the ref -> save ref to original object
    unsigned int idx = itMET - mets->begin();
    edm::RefToBase<METType> metsRef = mets->refAt(idx);
    MET amet(metsRef);
    // add the generated MET
    if (addGenMET_) amet.setGenMET((*genMETs)[idx]);
    // matches to fired trigger primitives
    if ( addTrigMatch_ ) {
      for ( size_t i = 0; i < trigPrimSrc_.size(); ++i ) {
        edm::Handle<edm::Association<TriggerPrimitiveCollection> > trigMatch;
        iEvent.getByLabel(trigPrimSrc_[i], trigMatch);
        TriggerPrimitiveRef trigPrim = (*trigMatch)[metsRef];
        if ( trigPrim.isNonnull() && trigPrim.isAvailable() ) {
          amet.addTriggerMatch(*trigPrim);
        }
      }
    }
    // add MET resolution info if demanded
    if (addResolutions_) {
      (*metResoCalc_)(amet);
    }

    // add MET Significance
    double sgf = getSignificance(iEvent, iSetup);
    amet.setSignificance(sgf);

    // correct for muons if demanded ... never more: it's now done by JetMETCorrections
    // add the MET to the vector of METs
    patMETs->push_back(amet);
  }

  // sort MET in ET .. don't mess with this
  //  std::sort(patMETs->begin(), patMETs->end(), eTComparator_);

  // put genEvt object in Event
  std::auto_ptr<std::vector<MET> > myMETs(patMETs);
  iEvent.put(myMETs);

}


//------------------------------------------------------------
//  Produce the MET Significance
//------------------------------------------------------------

double pat::PATMETProducer::getSignificance(edm::Event& iEvent, const edm::EventSetup & iSetup){

  // make sure the SigInputObj container is empty
  while(physobjvector_.size()>0){
    physobjvector_.erase(physobjvector_.begin(),physobjvector_.end());

  }

  getJets(iEvent, iSetup);

  getElectrons(iEvent, iSetup);

  getMuons(iEvent, iSetup);

  getTowers(iEvent, iSetup);

  // calculate the significance

  double met_et=0;
  double met_phi=0;
  double met_set=0;
  
  double significance = metsig::ASignificance(physobjvector_, met_et, met_phi, met_set);
 
  return significance;
}


//=== Uncertainty Functions ===============================================
void pat::PATMETProducer::setUncertaintyParameters(){

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




// --------------------------------------------------
//  Fill Input Vector with Jets
// --------------------------------------------------
void pat::PATMETProducer::getJets(edm::Event& iEvent, const edm::EventSetup & iSetup){

  objectname="jet";

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

    //-- Store tower DetId's to be removed from Calo Tower sum later --//
    std::vector<CaloTowerRef> v_towers = jet_iter->getCaloConstituents();
    for (unsigned int ii=0; ii < v_towers.size(); ii++) {
      s_clusteredTowers.insert( (*v_towers.at(ii)).id() );
    }

  }
}




// --------------------------------------------------
//  Fill Input Vector with Electrons
// --------------------------------------------------
void pat::PATMETProducer::getElectrons(edm::Event& iEvent, const edm::EventSetup & iSetup){

  objectname="electron";

  edm::ESHandle<CaloTowerConstituentsMap> cttopo;
  iSetup.get<IdealGeometryRecord>().get(cttopo);
  const CaloTowerConstituentsMap* caloTowerMap = cttopo.product();
  

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
     
    //-- Store tower DetId's to be removed from Calo Tower sum later --//
    const SuperCluster& eleSC = *( electron_iter->superCluster() );

    std::vector<DetId> v_eleDetIds = eleSC.getHitsByDetId();

    //-- Convert cells to calo towers and add to set --//
    for( std::vector<DetId>::iterator cellId = v_eleDetIds.begin();
         cellId != v_eleDetIds.end();
         cellId++) {

      CaloTowerDetId towerId = caloTowerMap->towerOf(*cellId);
      if (towerId != nullDetId) {
	std::pair<std::_Rb_tree_const_iterator<CaloTowerDetId>,bool> p1 = s_clusteredTowers.insert(towerId);
      }
      else
	std::cerr<<"No matching tower found for electron cell!\n";
    }

  }

}


// --------------------------------------------------
//  Fill Input Vector with Muons
// --------------------------------------------------
void pat::PATMETProducer::getMuons(edm::Event& iEvent, const edm::EventSetup & iSetup){

  objectname="muon";
  edm::Handle<edm::View<pat::Muon> > muonHandle;
  iEvent.getByLabel(muoLabel_,muonHandle);
  edm::View<pat::Muon> muons = *muonHandle;

  //double numberOfMuons = muons.size();

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
     
  }
}


//=== Fill Input Vector with Calo Towers ==================================
void pat::PATMETProducer::getTowers(edm::Event& iEvent, const edm::EventSetup & iSetup){

  edm::Handle<edm::View<reco::Candidate> > towers;
  iEvent.getByLabel(CaloTowerTag_, towers);
  edm::Ref<CaloTowerCollection> towerRef = towers->begin()->get<CaloTowerRef>();
  const CaloTowerCollection *towerCollection = towerRef.product();

  double globalEtThreshold = 0.0; // cut value

  //--- Loop over all calotowers, treating ECAL and HCAL differently ---//
  for( CaloTowerCollection::const_iterator calotower = towerCollection->begin();
       calotower != towerCollection->end(); 
       calotower++ ) 
    {
      if(calotower->et()<globalEtThreshold)
	continue;

      if (verbose_ > 1.) {
	std::cout << ">>>---> calotower et : " << calotower->et() <<  std::endl;
      }

      double sign_tower_et = calotower->et();
      double sigma_et;
      double sigma_phi;
      
      bool wasused = false;
      bool hadIsDone = false;
      bool emIsDone = false;
      int cell = calotower->constituentsSize();


      while ( --cell >= 0 && (!hadIsDone || !emIsDone) )
	{
	  DetId id = calotower->constituent( cell );

	  if (verbose_ > 1.) {
	    std::cout << ">>>---> DetId.det: " << id.det() <<  std::endl;
	  }
	  
	  //-- HCAL -----------------------------------------------------
	  if( !hadIsDone && id.det() == DetId::Hcal )
	    {
	      objectname="hadcalotower";
	      HcalSubdetector subdet = HcalDetId(id).subdet();
	      if(subdet == HcalBarrel){
		sign_tower_et = calotower->hadEt();
		sigma_et = hcalHBUncertainty.etUncertainty->Eval(sign_tower_et);
		sigma_phi= hcalHBUncertainty.phiUncertainty->Eval(sign_tower_et);
	      }

	      else if(subdet==HcalOuter){
		sign_tower_et = calotower->outerEt();
	        sigma_et = hcalHOUncertainty.etUncertainty->Eval(sign_tower_et);
                sigma_phi= hcalHOUncertainty.phiUncertainty->Eval(sign_tower_et);
	      }
	      else if(subdet==HcalEndcap){
		sign_tower_et = calotower->hadEt();
		sigma_et = hcalHEUncertainty.etUncertainty->Eval(sign_tower_et);
                sigma_phi= hcalHEUncertainty.phiUncertainty->Eval(sign_tower_et);
	      }
	      else if(subdet == HcalForward){
		sign_tower_et = calotower->et();
		sigma_et = hcalHFUncertainty.etUncertainty->Eval(sign_tower_et);
                sigma_phi= hcalHFUncertainty.phiUncertainty->Eval(sign_tower_et);
	      }
	      else{
		std::cerr << " HCAL tower cell not assigned to an HCAL subdetector!!!" << std::endl;
                sign_tower_et = calotower->et();
                sigma_et = hcalHEUncertainty.etUncertainty->Eval(sign_tower_et);
                sigma_phi= hcalHEUncertainty.phiUncertainty->Eval(sign_tower_et);
	      }

	      double sign_tower_phi = calotower->phi();
	      
	      //-- Store HCAL object for Significance Calculation --//
	      metsig::SigInputObj temp(objectname, sign_tower_et, sign_tower_phi, sigma_et,sigma_phi);
              std::set<CaloTowerDetId>::iterator towerId = s_clusteredTowers.find(calotower->id());

	      if (verbose_ > 1.) {
		std::cout << ">>>---> HCAL towerID: " << *towerId <<  std::endl;
	      }

	      if(!noHF_ || subdet !=HcalForward) {
		if( towerId == s_clusteredTowers.end() ) { // => tower not in set
		  physobjvector_.push_back(temp);

		  if (verbose_ > 1.) {
		    std::cout << ">>>---> adding phy vector from HCAL... "  <<  std::endl;
		  }
		}
	      }

	      wasused = true;
	      hadIsDone = true;
	    }

	  //-- ECAL -----------------------------------------------------
	  else if( !emIsDone && id.det() == DetId::Ecal )
	    {
	      EcalSubdetector subdet = EcalSubdetector( id.subdetId() );

	      if (verbose_ > 1.) {
		std::cout << ">>>---> ECAL: id.det= " << id.det()
			  << " subdetId = " << id.subdetId() <<  std::endl;
	      }

	      objectname="emcalotower";

	      if(subdet == EcalBarrel){
		sign_tower_et = calotower->emEt();
                sigma_et = ecalEBUncertainty.etUncertainty->Eval(sign_tower_et);
                sigma_phi = ecalEBUncertainty.phiUncertainty->Eval(sign_tower_et);
	      }
	      else if(subdet == EcalEndcap ){
		sign_tower_et = calotower->emEt();
                sigma_et = ecalEEUncertainty.etUncertainty->Eval(sign_tower_et);
                sigma_phi = ecalEEUncertainty.phiUncertainty->Eval(sign_tower_et);
	      }

	      double sign_tower_phi = calotower->phi();

	      //-- Store ECAL object for Significance Calculation --//
	      metsig::SigInputObj temp(objectname, sign_tower_et, sign_tower_phi, sigma_et,sigma_phi);
	      std::set<CaloTowerDetId>::iterator towerId = s_clusteredTowers.find(calotower->id());
	      
	      if( towerId == s_clusteredTowers.end() ) {  // => tower not in set
		physobjvector_.push_back(temp);
	      }

	      wasused = true;
	      emIsDone = true;
	    }

	} // End while loop

      if( wasused==false )
	std::cerr << "found non-assigned cell, " << std::endl;
      
    }// End Loop over all calotowers 

}  // End getTowers()


using namespace pat;
DEFINE_FWK_MODULE(PATMETProducer);
