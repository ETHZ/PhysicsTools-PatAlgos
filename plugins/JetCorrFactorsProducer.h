#ifndef PhysicsTools_PatAlgos_JetCorrFactorsProducer_h
#define PhysicsTools_PatAlgos_JetCorrFactorsProducer_h

/**
  \class    pat::JetCorrFactorsProducer JetCorrFactorsProducer.h "PhysicsTools/PatAlgos/interface/JetCorrFactorsProducer.h"
  \brief    Produces JetCorrFactors and a ValueMap to the originating
            reco jets

   The JetCorrFactorsProducer produces a set of correction factors, defined in the class pat::JetCorrFactors. The vector 
   of these factors is linked to the originating reco jets through an edm::ValueMap. The initializing parameters of the 
   module can be found in the recoLayer1/jetCorrFactors_cf.py of the PatAlgos package. In the standard PAT workflow the 
   module has to be run before the creation of the pat::Jet. The edm::ValueMap will then be embedded into the pat::Jet. 
   Jets corrected up to a given correction level can then be accessed via the pat::Jet member function correctedJet. For 
   more details have a look into the class description of the pat::Jet.

   ATTENTION: available options for flavor corrections are 
    * L5Flavor:gJ       L7Parton:gJ        gluon   from dijets
    * L5Flavor:qJ/qT    L7Parton:qJ/qT     quark   from dijets/top
    * L5Flavor:cJ/cT    L7Parton:cJ/cT     charm   from dijets/top
    * L5Flavor:bJ/bT    L7Parton:bJ/bT     beauty  from dijets/top
    *                   L7Parton:jJ/tT     mixture from dijets/top

   where mixture refers to the flavor mixture as determined from the MC sample the flavor dependen corrections have been
   derived from. 'J' and 'T' stand for a typical dijet (ttbar) sample. 

   NOTE:

    * the mixed mode (mc input mixture from dijets/ttbar) only exists for parton level corrections.

    * jJ and tT are not covered in this implementation of the JetCorrFactorsProducer

    * there are no gluon corrections available from the top sample neighter on the L7Parton level.
*/

#include <map>
#include <string>

#include "DataFormats/Common/interface/View.h"
#include "DataFormats/JetReco/interface/Jet.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Utilities/interface/InputTag.h"
#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"

#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/PatCandidates/interface/JetCorrFactors.h"
#include "CondFormats/JetMETObjects/interface/FactorizedJetCorrector.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"


namespace pat {

  class JetCorrFactorsProducer : public edm::EDProducer {
  public:
    /// value map for JetCorrFactors (to be written into the event)
    typedef edm::ValueMap<pat::JetCorrFactors> JetCorrFactorsMap;

  public:
    // default constructor
    explicit JetCorrFactorsProducer(const edm::ParameterSet& cfg);
    // default destructor
    ~JetCorrFactorsProducer() {};
    // everything that needs to be done per event
    virtual void produce(edm::Event& event, const edm::EventSetup& setup);
    // description of configuration file parameters
    static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);
    
  private:
    // return the jec parameters as input to the FactorizedJetCorrector for different flavors
    std::vector<JetCorrectorParameters> params(const JetCorrectorParametersCollection& parameters, const JetCorrFactors::Flavor& flavor) const;
    // return an expanded version of correction levels for different flavors; the result should
    // be of type ['L2Relative', 'L3Absolute', 'L5FLavor_gJ', 'L7Parton_gJ']; L7Parton_gT will 
    // result in an empty string as this correction level is not available
    std::vector<std::string> expand(const std::vector<std::string>& levels, const JetCorrFactors::Flavor& flavor);
    // evaluate jet correction factor up to a given level
    float evaluate(edm::View<reco::Jet>::const_iterator& jet, FactorizedJetCorrector* corrector, int level);
    
  private:
    // use electromagnetic fraction for jet energy corrections or not (will only have an effect for jets CaloJets)
    bool emf_;
    // era of JEC factors (e.g. Spring10, Summer09, ... this might become obsolete after the DB transition)
    std::string era_;
    // input jet collection
    edm::InputTag src_;
    // type of flavor dependent JEC factors (only 'J' and 'T' are allowed)
    std::string type_;
    // label of jec factors
    std::string label_;
    // contains flavor dependent corrections
    bool flavorDependent_;
    // jec levels
    std::map<JetCorrFactors::Flavor, std::vector<std::string> > levels_;

  };
}

#endif
