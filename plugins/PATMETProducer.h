//
// $Id: PATMETProducer.h,v 1.17 2009/01/13 19:24:34 xs32 Exp $
//

#ifndef PhysicsTools_PatAlgos_PATMETProducer_h
#define PhysicsTools_PatAlgos_PATMETProducer_h

/**
  \class    pat::PATMETProducer PATMETProducer.h "PhysicsTools/PatAlgos/interface/PATMETProducer.h"
  \brief    Produces the pat::MET

   The PATMETProducer produces the analysis-level pat::MET starting from
   a collection of objects of METType.

  \author   Steven Lowette
  \version  $Id: PATMETProducer.h,v 1.17 2009/01/13 19:24:34 xs32 Exp $
*/


#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/MakerMacros.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "PhysicsTools/Utilities/interface/EtComparator.h"

#include "DataFormats/PatCandidates/interface/MET.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "FWCore/ParameterSet/interface/FileInPath.h"
#include "DataFormats/Common/interface/View.h"

#include "PhysicsTools/PatUtils/interface/ObjectResolutionCalc.h"

#include <memory>


//--- Files required for including Calo Towers to calculate MET Significance ------------------//
#include "DataFormats/CaloTowers/interface/CaloTowerDetId.h"
#include "DataFormats/RecoCandidate/interface/RecoCandidate.h"
#include "DataFormats/EcalDetId/interface/EcalSubdetector.h"
#include "DataFormats/HcalDetId/interface/HcalDetId.h"
#include "TF1.h"
#include "RecoMET/METAlgorithms/interface/SigInputObj.h"
#include "RecoMET/METAlgorithms/interface/SignAlgoResolutions.h"
#include "RecoMET/METAlgorithms/interface/significanceAlgo.h"

//--- For jets ------------------------------//
#include "JetMETCorrections/Objects/interface/JetCorrector.h"

//--- For electrons ------------------------------//
#include "FWCore/Framework/interface/ESHandle.h"
#include "Geometry/CaloTopology/interface/CaloTowerConstituentsMap.h"
#include "Geometry/Records/interface/IdealGeometryRecord.h"


namespace pat {


  class ObjectResolutionCalc;

  
  class PATMETProducer : public edm::EDProducer {
    
  public:
    
    explicit PATMETProducer(const edm::ParameterSet & iConfig);
    ~PATMETProducer();
    
    virtual void produce(edm::Event & iEvent, const edm::EventSetup & iSetup);
    
  private:

      virtual void beginJob(const edm::EventSetup&) ;
      virtual void beginRun(const edm::EventSetup&) ;
      virtual void endJob() ;
    
    // configurables
    edm::InputTag metSrc_;
    bool          addGenMET_;
    edm::InputTag genMETSrc_;
    bool          addTrigMatch_;
    std::vector<edm::InputTag> trigPrimSrc_;
    bool          addResolutions_;
    bool          useNNReso_;
    std::string   metResoFile_;
    bool          addMuonCorr_;
    edm::InputTag muonSrc_;
    
   
    // tools
    ObjectResolutionCalc * metResoCalc_;
    GreaterByEt<MET> eTComparator_;
    
    // --------------------------------------------------
    // Calculate MET Significance
    // --------------------------------------------------
    std::vector<metsig::SigInputObj> physobjvector_;
    double getSignificance(edm::Event&, const edm::EventSetup&);
    void getJets(edm::Event&, const edm::EventSetup&);
    void getElectrons(edm::Event&, const edm::EventSetup&);
    void getMuons(edm::Event&, const edm::EventSetup&);
    void getTowers(edm::Event&, const edm::EventSetup&);
 

    double verbose_;
    double uncertaintyScaleFactor_; // scale factor for the uncertainty parameters.
    bool    controlledUncertainty_; // use controlled uncertainty parameters.

    edm::InputTag jetLabel_;
    double jetPtMin_;
    double jetEtaMax_;
    double jetEMfracMax_;

    edm::InputTag eleLabel_;
    double elePtMin_;
    double eleEtaMax_;

    edm::InputTag muoLabel_;
    double muonPtMin_;
    double muonEtaMax_;
    
    edm::InputTag CaloTowerTag_;
    std::set<CaloTowerDetId> s_clusteredTowers; 
    bool noHF_;

    std::string objectname;


    class uncertaintyFunctions{
    public:
      TF1 *etUncertainty;
      TF1 *phiUncertainty;
    };

    void setUncertaintyParameters();// fills the following uncertaintyFunctions objects:
    uncertaintyFunctions ecalEBUncertainty;
    uncertaintyFunctions ecalEEUncertainty;
    uncertaintyFunctions hcalHBUncertainty;
    uncertaintyFunctions hcalHEUncertainty;
    uncertaintyFunctions hcalHOUncertainty;
    uncertaintyFunctions hcalHFUncertainty;
    
    uncertaintyFunctions jetUncertainty;
    uncertaintyFunctions jetCorrUncertainty;
    uncertaintyFunctions eleUncertainty;
    uncertaintyFunctions muonUncertainty;
    uncertaintyFunctions muonCorrUncertainty;
    
    double jetEtUncertaintyParameter0_ ; 
    double jetEtUncertaintyParameter1_ ; 
    double jetEtUncertaintyParameter2_ ; 
    
    double jetPhiUncertaintyParameter0_ ; 
    double jetPhiUncertaintyParameter1_ ; 
    double jetPhiUncertaintyParameter2_ ; 
    
    double eleEtUncertaintyParameter0_ ; 
    double elePhiUncertaintyParameter0_ ; 

    double muonEtUncertaintyParameter0_ ; 
    double muonPhiUncertaintyParameter0_ ; 
    
  };

}

#endif
