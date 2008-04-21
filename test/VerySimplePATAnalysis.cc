// -*- C++ -*-
//
// Package:    PatAlgos
// Class:      VerySimplePATAnalysis
// 
/**\class VerySimplePATAnalysis VerySimplePATAnalysis.cc PhysicsTools/PatAlgos/test/VerySimplePATAnalysis.cc

 Description: <A very (very) simple CMSSW analyzer for PAT objects>

 Implementation:
 
 this analyzer shows how to loop over PAT output. 
*/
//
// Original Author:  Freya Blekman
//         Created:  Mon Apr 21 10:03:50 CEST 2008
// $Id$
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ServiceRegistry/interface/Service.h"
#include "PhysicsTools/UtilAlgos/interface/TFileService.h"
#include "FWCore/ParameterSet/interface/InputTag.h"


#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/PatCandidates/interface/MET.h"

#include "TH1D.h"
#include <map>
#include <vector>
#include <string>
//
// class decleration
//

class VerySimplePATAnalysis : public edm::EDAnalyzer {
   public:
      explicit VerySimplePATAnalysis(const edm::ParameterSet&);
      ~VerySimplePATAnalysis();


   private:
      virtual void beginJob(const edm::EventSetup&) ;
      virtual void analyze(const edm::Event&, const edm::EventSetup&);
      virtual void endJob() ;

      // ----------member data ---------------------------

  
  std::map<std::string,TH1D*> histocontainer_; // simple map to contain all histograms. Histograms are booked in the beginJob() method
  
  edm::InputTag eleLabel_;
  edm::InputTag muoLabel_;
  edm::InputTag jetLabel_;
  edm::InputTag tauLabel_;
  edm::InputTag metLabel_;
  edm::InputTag phoLabel_;
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
VerySimplePATAnalysis::VerySimplePATAnalysis(const edm::ParameterSet& iConfig):
  histocontainer_(),
  eleLabel_(iConfig.getUntrackedParameter<edm::InputTag>("electronTag")),
  muoLabel_(iConfig.getUntrackedParameter<edm::InputTag>("muonTag")),
  jetLabel_(iConfig.getUntrackedParameter<edm::InputTag>("jetTag")),
  tauLabel_(iConfig.getUntrackedParameter<edm::InputTag>("tauTag")),
  metLabel_(iConfig.getUntrackedParameter<edm::InputTag>("metTag")),
  phoLabel_(iConfig.getUntrackedParameter<edm::InputTag>("photonTag"))

{
   //now do what ever initialization is needed

}


VerySimplePATAnalysis::~VerySimplePATAnalysis()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)

}


//
// member functions
//

// ------------ method called to for each event  ------------
void
VerySimplePATAnalysis::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;


   //{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
   // first: get all objects from the event.
   //{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}

   edm::Handle<std::vector<pat::Muon> > muonHandle;
   iEvent.getByLabel(muoLabel_,muonHandle);
   std::vector<pat::Muon> muons = *muonHandle;
   
   edm::Handle<std::vector<pat::Jet> > jetHandle;
   iEvent.getByLabel(jetLabel_,jetHandle);
   std::vector<pat::Jet> jets = *jetHandle;

   edm::Handle<std::vector<pat::Electron> > electronHandle;
   iEvent.getByLabel(eleLabel_,electronHandle);
   std::vector<pat::Electron> electrons = *electronHandle;

   edm::Handle<std::vector<pat::MET> > metHandle;
   iEvent.getByLabel(metLabel_,metHandle);
   std::vector<pat::MET> mets = *metHandle;

   edm::Handle<std::vector<pat::Photon> > phoHandle;
   iEvent.getByLabel(phoLabel_,phoHandle);
   std::vector<pat::Photon> photons = *phoHandle;

   edm::Handle<std::vector<pat::Tau> > tauHandle;
   iEvent.getByLabel(tauLabel_,tauHandle);
   std::vector<pat::Tau> taus = *tauHandle;

   //{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
   // example of a loop over objects... this works identical for all vectors defined above
   //   once you have a jet object you can use all methods defined in the header file 
   // (DataFormats/PatCandidates/interface/Jet.h and equivalent for other objects)
   //{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
   size_t njetscounter=0;
   for(std::vector<pat::Jet>::const_iterator jet_iter = jets.begin(); jet_iter!=jets.end(); ++jet_iter){
     if(jet_iter->pt()>50)
       njetscounter++;
     
   }

   //{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
   //histocontainer_ is of type std::map<std::vector, TH1D*>. This means you can use it with this syntax:
   // histocontainer_["histname"]->Fill(x); 
   // histocontainer_["histname"]->Draw(); 
   // etc, etc. Essentially you use the histname string to look up a pointer to a TH1D* 
   // which you can do everything to you would normally do in ROOT.
   //{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
   
   histocontainer_["njets"]->Fill(njetscounter);
   //{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
   // for the other objects just quickly book the multiplicity. Again, just use the same infrastructure as for jets if you want to loop over them.
   //{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
   histocontainer_["nelectrons"]->Fill(electrons.size());
   histocontainer_["nphotons"]->Fill(photons.size());
   histocontainer_["nmuons"]->Fill(muons.size());
   histocontainer_["ntaus"]->Fill(taus.size());
}
// ------------ method called once each job just before starting event loop  ------------
void 
VerySimplePATAnalysis::beginJob(const edm::EventSetup&)
{
  //{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
  // define some histograms using the framework tfileservice. Define the output file name in your .cfg.
  //{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
  edm::Service<TFileService> fs;
  
  //{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
  //histocontainer_ is of type std::map<std::vector, TH1D*>. This means you can use it with this syntax:
  // histocontainer_["histname"]->Fill(x); 
  // histocontainer_["histname"]->Draw(); 
  // etc, etc. Essentially you use the histname string to look up a pointer to a TH1D* 
  // which you can do everything to you would normally do in ROOT.
  //{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}

  
  //{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}
  // here we book new histograms:
  //{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}{}

  histocontainer_["njets"]=fs->make<TH1D>("njets","jet multiplicity for jets with p_{T} > 50 GeV/c",10,0,10);
  histocontainer_["nelectrons"]=fs->make<TH1D>("nelectrons","electron multiplicity",10,0,10);
  histocontainer_["ntaus"]=fs->make<TH1D>("ntaus","tau multiplicity",10,0,10);
  histocontainer_["nphotons"]=fs->make<TH1D>("nphotons","photon multiplicity",10,0,10);
  histocontainer_["nmuons"]=fs->make<TH1D>("nmuons","muon multiplicity",10,0,10);

}

// ------------ method called once each job just after ending the event loop  ------------
void 
VerySimplePATAnalysis::endJob() {
}

//define this as a plug-in
DEFINE_FWK_MODULE(VerySimplePATAnalysis);
