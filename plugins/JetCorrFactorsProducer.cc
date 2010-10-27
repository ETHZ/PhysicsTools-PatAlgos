#include <memory>
#include <vector>
#include <string>
#include <iostream>

#include "FWCore/Framework/interface/ESHandle.h"
#include "FWCore/Framework/interface/EventSetup.h"
#include "DataFormats/JetReco/interface/CaloJet.h"
#include "FWCore/MessageLogger/interface/MessageLogger.h"
#include "PhysicsTools/PatAlgos/plugins/JetCorrFactorsProducer.h"
#include "JetMETCorrections/Objects/interface/JetCorrectionsRecord.h"

#include "FWCore/ParameterSet/interface/ParameterDescription.h"
#include "FWCore/ParameterSet/interface/ParameterSetDescription.h"
#include "FWCore/ParameterSet/interface/ConfigurationDescriptions.h"


using namespace pat;

JetCorrFactorsProducer::JetCorrFactorsProducer(const edm::ParameterSet& cfg):
  emf_(cfg.getParameter<bool>( "emf" )), 
  era_(cfg.getParameter<std::string>( "era" )),
  src_(cfg.getParameter<edm::InputTag>( "src" )),
  type_ (cfg.getParameter<std::string>("flavorType")),
  label_(cfg.getParameter<std::string>( "@module_label" ))
{
  std::vector<std::string> levels = cfg.getParameter<std::vector<std::string> >("levels"); 
  // fill the std::map for levels_, which might be flavor dependent or not; 
  // flavor dependency is determined from the fact whether the std::string 
  // L5Flavor or L7Parton can be found in levels; if flavor dependent four
  // vectors of strings will be filled into the map corresponding to GLUON, 
  // UDS, CHARM and BOTTOM (according to JetCorrFactors::Flavor), 'L5Flavor'
  // and 'L7Parton' will be expanded accordingly; if not levels_ is filled 
  // with only one vector of strings according to NONE. This vector will be 
  // equivalent to the original vector of strings.
  flavorDependent_= (std::find(levels.begin(), levels.end(), "L5FLavor")!=levels.end() || std::find(levels.begin(), levels.end(), "L7Parton")!=levels.end());
  if(flavorDependent_){
    levels_[JetCorrFactors::GLUON ] = expand(levels, JetCorrFactors::GLUON );
    levels_[JetCorrFactors::UDS   ] = expand(levels, JetCorrFactors::UDS   );
    levels_[JetCorrFactors::CHARM ] = expand(levels, JetCorrFactors::CHARM );
    levels_[JetCorrFactors::BOTTOM] = expand(levels, JetCorrFactors::BOTTOM);
  }
  else{
    levels_[JetCorrFactors::NONE  ] = levels;
  }
  produces<JetCorrFactorsMap>();
}

std::vector<std::string>
JetCorrFactorsProducer::expand(const std::vector<std::string>& levels, const JetCorrFactors::Flavor& flavor)
{
  std::vector<std::string> expand;
  for(std::vector<std::string>::const_iterator level=levels.begin(); level!=levels.end(); ++level){
    if((*level)=="L5Flavor" || (*level)=="L7Parton"){
      if(flavor==JetCorrFactors::GLUON ){
	if(*level=="L7Parton" && type_=="T"){
	  edm::LogWarning message( "L7Parton::GLUON not available" );
	  message << "Jet energy corrections requested for level: L7Parton and type: 'T'. \n"
		  << "For this combination there is no GLUON correction available. The    \n"
		  << "correction for this flavor type will be filled set to -1.";
	  expand.clear(); break;
	}
	else{
	  expand.push_back(std::string(*level).append("_").append("g").append(type_));	
	}
      }
      if(flavor==JetCorrFactors::UDS   ) expand.push_back(std::string(*level).append("_").append("q").append(type_));	
      if(flavor==JetCorrFactors::CHARM ) expand.push_back(std::string(*level).append("_").append("c").append(type_));	
      if(flavor==JetCorrFactors::BOTTOM) expand.push_back(std::string(*level).append("_").append("b").append(type_));
    }
    expand.push_back(*level); 
  }
  return expand;
}

std::vector<JetCorrectorParameters>
JetCorrFactorsProducer::params(const JetCorrectorParametersCollection& parameters, const JetCorrFactors::Flavor& flavor) const 
{
  std::vector<JetCorrectorParameters> params;
  for(std::vector<std::string>::const_iterator level=levels_.find(flavor)->second.begin(); level!=levels_.find(flavor)->second.end(); ++level){ 
    params.push_back(parameters[*level]); 
  } 
  return params;
}

float
JetCorrFactorsProducer::evaluate(edm::View<reco::Jet>::const_iterator& jet, boost::shared_ptr<FactorizedJetCorrector>& corrector, int level)
{
  corrector->setJetEta(jet->eta()); corrector->setJetPt(jet->pt()); corrector->setJetE(jet->energy()); 
  if( emf_ && dynamic_cast<const reco::CaloJet*>(&*jet)){ 
    corrector->setJetEMF(dynamic_cast<const reco::CaloJet*>(&*jet)->emEnergyFraction()); 
  }
  return corrector->getSubCorrections()[level];
}

void 
JetCorrFactorsProducer::produce(edm::Event& event, const edm::EventSetup& setup) 
{
  // get jet collection from the event
  edm::Handle<edm::View<reco::Jet> > jets;
  event.getByLabel(src_, jets);

  // retreive parameters from the DB this still need a proper configurable 
  // payloadName like: JetCorrectorParametersCollection_Spring10_AK5Calo.
  edm::ESHandle<JetCorrectorParametersCollection> parameters;
  setup.get<JetCorrectionsRecord>().get(std::string("JetCorrectorParametersCollection_Spring10_AK5Calo"), parameters); 

  // initialize jet correctors
  std::map<JetCorrFactors::Flavor, boost::shared_ptr<FactorizedJetCorrector> > corrector;
  if(flavorDependent_){
    // there is at least one flavor dependent jet energy correction level
    // in levels_; When derived from the ttbar samples there is no GLUON 
    // corrections for L7Parton ('L7Parton_gT' does not exist); at the 
    // moment params is empty in this case. If the FactorizedJetCorrector
    // can not catch this this has to be done here.
    corrector[JetCorrFactors::GLUON ] = boost::shared_ptr<FactorizedJetCorrector>( new FactorizedJetCorrector(params(*parameters, JetCorrFactors::GLUON )) );
    corrector[JetCorrFactors::UDS   ] = boost::shared_ptr<FactorizedJetCorrector>( new FactorizedJetCorrector(params(*parameters, JetCorrFactors::UDS   )) );
    corrector[JetCorrFactors::CHARM ] = boost::shared_ptr<FactorizedJetCorrector>( new FactorizedJetCorrector(params(*parameters, JetCorrFactors::CHARM )) );
    corrector[JetCorrFactors::BOTTOM] = boost::shared_ptr<FactorizedJetCorrector>( new FactorizedJetCorrector(params(*parameters, JetCorrFactors::BOTTOM)) );
  }
  else{
    corrector[JetCorrFactors::NONE  ] = boost::shared_ptr<FactorizedJetCorrector>( new FactorizedJetCorrector(params(*parameters, JetCorrFactors::NONE  )) );
  }

  std::vector<JetCorrFactors> jetCorrs;
  for(edm::View<reco::Jet>::const_iterator jet = jets->begin(); jet!=jets->end(); ++jet){
    std::vector<JetCorrFactors::CorrectionFactor> jec;
    // loop over all correction levels and create a JetCorrFactors instance for each jet. 
    // This consists of a std::vector<std::pair<std::string>, std::vector<float> > where
    // the std::vector<float> corresponds to the potentially flavor dependent correction 
    // factors (with length 4 if flavor dependent and 1 else), std::string corresponds to
    // the label of the correction level (defined by JetMET). Per construction the jet 
    // energy correction will be flavor independent up to the first flavor dependent 
    // correction and flavor dependent afterwards.
    for(std::map<JetCorrFactors::Flavor, std::vector<std::string> >::const_iterator levels=levels_.begin(); levels!=levels_.end(); ++levels){
      bool flavorDependent=false;
      // loop the correction levels
      for(unsigned int idx=0; idx<levels->second.size(); ++idx){
	// correction factors
	std::vector<float> factors;
	if(levels->second[idx].find("L5FLavor")!=std::string::npos || levels->second[idx].find("L7Parton")!=std::string::npos){
	  flavorDependent=true;
	}
	if(flavorDependent){
	  factors.push_back(evaluate(jet, corrector.find(levels->first)->second, idx));
	}
	else{
	  // either these jec factors are not flavor dependent at all; in this case use
	  // the corrector for NONE, or these jec factors are flavor dependent, but the 
	  // current correction level is not. In this case use just one of the flavor 
	  // dependent correctors, as they will all give the same results. Don't use the 
	  // corrector for GLUON though as it might be blank due the to non existing 
	  // correction type L7Parton_gT 
	  if( corrector.find(JetCorrFactors::NONE)!=corrector.end() ){
	    factors.push_back(evaluate(jet, corrector.find(JetCorrFactors::NONE)->second, idx));
	  }
	  else{
	    factors.push_back(evaluate(jet, corrector.find(JetCorrFactors::UDS )->second, idx));
	  }
	}
	// push back the set of JetCorrFactors: the first entry corresponds to the label 
	// of the  correction level, the second parameter to the jec factors
	jec.push_back(std::make_pair<std::string, std::vector<float> >(levels->second[idx], factors));
      }
      if(!flavorDependent){break;}
    }
    // create the actual object with scale factors we want the valuemap to refer to
    JetCorrFactors corrFactors(label_, jec);
    jetCorrs.push_back(corrFactors);
  }

  // build the value map
  std::auto_ptr<JetCorrFactorsMap> jetCorrsMap(new JetCorrFactorsMap());
  JetCorrFactorsMap::Filler filler(*jetCorrsMap);
  // jets and jetCorrs have their indices aligned by construction
  filler.insert(jets, jetCorrs.begin(), jetCorrs.end());
  filler.fill(); // do the actual filling

  // put our produced stuff in the event
  event.put(jetCorrsMap);
}

// ParameterSet description for module
void
JetCorrFactorsProducer::fillDescriptions(edm::ConfigurationDescriptions & descriptions)
{
//   edm::ParameterSetDescription iDesc;
//   iDesc.add<bool>("useEMF", false);
//   iDesc.add<std::string>("sampleType", "dijet");
//   iDesc.add<std::string>("corrSample", "Spring10");
//   iDesc.add<edm::InputTag>("jetSource", edm::InputTag("ak5CaloJets")); 

//   edm::ParameterSetDescription corrLevels;
//   corrLevels.add<std::string>("label" , "none");
//   corrLevels.add<std::string>("level" , "none");
//   corrLevels.add<std::string>("sample", "dijet");
//   iDesc.add("corrLevels", corrLevels);

//   descriptions.add("JetCorrFactorsProducer", iDesc);
}

#include "FWCore/Framework/interface/MakerMacros.h"

DEFINE_FWK_MODULE(JetCorrFactorsProducer);
