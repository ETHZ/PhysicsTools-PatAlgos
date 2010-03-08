/*   A macro for making a histogram of Jet Pt with cuts
This is a basic way to cut out jets of a certain Pt and Eta using an if statement
This example creates a histogram of Jet Pt, using Jets with Pt above 30 and ETA above -2.1 and below 2.1
*/

#include "DataFormats/FWLite/interface/Handle.h"
#include "DataFormats/FWLite/interface/Event.h"
#include "TFile.h"
#include "TH1.h"
#include "TH2.h"
#include "TCanvas.h"
#include "TLegend.h"


#if !defined(__CINT__) && !defined(__MAKECINT__)
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Photon.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Tau.h"
#endif

#include <iostream>
#include <cmath>      //necessary for absolute function fabs()

using namespace std;

void plotAllPATObjects()
{


  TFile  * file = new TFile("rereco_2360GeV_firstdata_pat.root");


  TFile * output = new TFile("plotAllPATObjects.root", "RECREATE");

  TH1D * hist_nJet             = new TH1D("hist_nJet", "Number of Jets", 10, 0, 10 );
  TH1D * hist_jetPt            = new TH1D("hist_jetPt", "Jet p_{T}", 20, 0, 100 );
  TH2D * hist_jetEtaVsPhi      = new TH2D("hist_jetEtaVsPhi", "Jet #phi versus #eta;#eta;#phi", 50, -5.0, 5.0, 50, -TMath::Pi(), TMath::Pi() );

  TH1D * hist_nElectron        = new TH1D("hist_nElectron", "Number of Electrons", 10, 0, 10 );
  TH1D * hist_electronPt       = new TH1D("hist_electronPt", "Electron p_{T}", 20, 0, 100 );
  TH2D * hist_electronEtaVsPhi = new TH2D("hist_electronEtaVsPhi", "Electron #phi versus #eta;#eta;#phi", 50, -5.0, 5.0, 50, -TMath::Pi(), TMath::Pi() );

  TH1D * hist_nMuon            = new TH1D("hist_nMuon", "Number of Muons", 10, 0, 10 );
  TH1D * hist_muonPt           = new TH1D("hist_muonPt", "Muon p_{T}", 20, 0, 100 );
  TH2D * hist_muonEtaVsPhi     = new TH2D("hist_muonEtaVsPhi", "Muon #phi versus #eta;#eta;#phi", 50, -5.0, 5.0, 50, -TMath::Pi(), TMath::Pi() );

  TH1D * hist_nTau             = new TH1D("hist_nTau", "Number of Taus", 10, 0, 10 );
  TH1D * hist_tauPt            = new TH1D("hist_tauPt", "Tau p_{T}", 20, 0, 100 );
  TH2D * hist_tauEtaVsPhi      = new TH2D("hist_tauEtaVsPhi", "Tau #phi versus #eta;#eta;#phi", 50, -5.0, 5.0, 50, -TMath::Pi(), TMath::Pi() );

  TH1D * hist_nPhoton          = new TH1D("hist_nPhoton", "Number of Photons", 10, 0, 10 );
  TH1D * hist_photonPt         = new TH1D("hist_photonPt", "Photon p_{T}", 20, 0, 100 );
  TH2D * hist_photonEtaVsPhi   = new TH2D("hist_photonEtaVsPhi", "Photon #phi versus #eta;#eta;#phi", 50, -5.0, 5.0, 50, -TMath::Pi(), TMath::Pi() );

  TH1D * hist_nMet             = new TH1D("hist_nMet", "Number of METS", 10, 0, 10 );
  TH1D * hist_metPt            = new TH1D("hist_metPt", "Met p_{T}", 20, 0, 100 );
  TH1D * hist_metPhi           = new TH1D("hist_metPhi", "Met #phi", 50, -TMath::Pi(), TMath::Pi() );

  fwlite::Event ev(file);

  //loop through each event
  for( ev.toBegin();
         ! ev.atEnd();
         ++ev) {

    edm::EventBase const & event = ev;

    edm::Handle<std::vector<pat::Jet> > h_jet;
    event.getByLabel(edm::InputTag("cleanLayer1Jets"), h_jet);

    edm::Handle<std::vector<pat::MET> > h_MET;
    event.getByLabel(edm::InputTag("layer1METs"), h_MET);

    edm::Handle<std::vector<pat::Electron> > h_electron;
    event.getByLabel(edm::InputTag("cleanLayer1Electrons"), h_electron);

    edm::Handle<std::vector<pat::Muon> > h_muon;
    event.getByLabel(edm::InputTag("cleanLayer1Muons"), h_muon);

    edm::Handle<std::vector<pat::Tau> > h_tau;
    event.getByLabel(edm::InputTag("cleanLayer1Taus"), h_tau);

    edm::Handle<std::vector<pat::Photon> > h_photon;
    event.getByLabel(edm::InputTag("cleanLayer1Photons"), h_photon);


    if ( h_jet.isValid() ) {
      hist_nJet->Fill( h_jet->size() );
      for ( std::vector<pat::Jet>::const_iterator jetBegin = h_jet->begin(),
	      jetEnd = h_jet->end(), ijet = jetBegin;
	    ijet != jetEnd; ++ijet ) {
	hist_jetPt->Fill( ijet->pt() );
	hist_jetEtaVsPhi->Fill( ijet->eta(), ijet->phi() );
      }
    }

    if ( h_MET.isValid() ) {
      hist_nMet->Fill( h_MET->size() );
      for ( std::vector<pat::MET>::const_iterator metBegin = h_MET->begin(),
	      metEnd = h_MET->end(), imet = metBegin;
	    imet != metEnd; ++imet ) {
	hist_metPt->Fill( imet->pt() );
	hist_metPhi->Fill( imet->phi() );
      }
    }

    if ( h_electron.isValid() ) {
      hist_nElectron->Fill( h_electron->size() );
      for ( std::vector<pat::Electron>::const_iterator electronBegin = h_electron->begin(),
	      electronEnd = h_electron->end(), ielectron = electronBegin;
	    ielectron != electronEnd; ++ielectron ) {
	hist_electronPt->Fill( ielectron->pt() );
	hist_electronEtaVsPhi->Fill( ielectron->eta(), ielectron->phi() );
      }
    }

    if ( h_muon.isValid() ) {
      hist_nMuon->Fill( h_muon->size() );
      for ( std::vector<pat::Muon>::const_iterator muonBegin = h_muon->begin(),
	      muonEnd = h_muon->end(), imuon = muonBegin;
	    imuon != muonEnd; ++imuon ) {
	hist_muonPt->Fill( imuon->pt() );
	hist_muonEtaVsPhi->Fill( imuon->eta(), imuon->phi() );
      }
    }

    if ( h_tau.isValid() ) {
      hist_nTau->Fill( h_tau->size() );
      for ( std::vector<pat::Tau>::const_iterator tauBegin = h_tau->begin(),
	      tauEnd = h_tau->end(), itau = tauBegin;
	    itau != tauEnd; ++itau ) {
	hist_tauPt->Fill( itau->pt() );
	hist_tauEtaVsPhi->Fill( itau->eta(), itau->phi() );
      }
    }

    if ( h_photon.isValid() ) {
      hist_nPhoton->Fill( h_photon->size() );
      for ( std::vector<pat::Photon>::const_iterator photonBegin = h_photon->begin(),
	      photonEnd = h_photon->end(), iphoton = photonBegin;
	    iphoton != photonEnd; ++iphoton ) {
	hist_photonPt->Fill( iphoton->pt() );
	hist_photonEtaVsPhi->Fill( iphoton->eta(), iphoton->phi() );
      }
    }
    
   }   //end event loop


  output->cd();

  hist_nJet             ->Write();
  hist_jetPt            ->Write();
  hist_jetEtaVsPhi      ->Write();

  hist_nElectron        ->Write();
  hist_electronPt       ->Write();
  hist_electronEtaVsPhi ->Write();

  hist_nMuon            ->Write();
  hist_muonPt           ->Write();
  hist_muonEtaVsPhi     ->Write();

  hist_nTau             ->Write();
  hist_tauPt            ->Write();
  hist_tauEtaVsPhi      ->Write();

  hist_nPhoton          ->Write();
  hist_photonPt         ->Write();
  hist_photonEtaVsPhi   ->Write();

  hist_nMet             ->Write();
  hist_metPt            ->Write();
  hist_metPhi           ->Write();




  delete hist_nJet             ;
  delete hist_jetPt            ;
  delete hist_jetEtaVsPhi      ;

  delete hist_nElectron        ;
  delete hist_electronPt       ;
  delete hist_electronEtaVsPhi ;

  delete hist_nMuon            ;
  delete hist_muonPt           ;
  delete hist_muonEtaVsPhi     ;

  delete hist_nTau             ;
  delete hist_tauPt            ;
  delete hist_tauEtaVsPhi      ;

  delete hist_nPhoton          ;
  delete hist_photonPt         ;
  delete hist_photonEtaVsPhi   ;

  delete hist_nMet             ;
  delete hist_metPt            ;
  delete hist_metPhi           ;
  

  output->Close();
  delete output;
  
}
