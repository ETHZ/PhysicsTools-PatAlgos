#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/InputTag.h"

#include "DataFormats/BTauReco/interface/JetTag.h"
#include "DataFormats/Common/interface/ValueMap.h"

#include "PhysicsTools/PatUtils/interface/RefHelper.h"

class RefTestAnalyzer : public edm::EDAnalyzer {
    public:
        RefTestAnalyzer(const edm::ParameterSet &iConfig) ;
        virtual void analyze(const edm::Event &iEvent, const edm::EventSetup &iSetup) ;
    private:
        edm::InputTag jets0_, jets1_, jtag_, btag_, newbtag_, backmap_;
};



RefTestAnalyzer::RefTestAnalyzer(const edm::ParameterSet &iConfig) :
    jets0_(iConfig.getParameter<edm::InputTag>("jets0")),
    jets1_(iConfig.getParameter<edm::InputTag>("jets1")),
    jtag_(iConfig.getParameter<edm::InputTag>("jtag")),
    btag_(iConfig.getParameter<edm::InputTag>("btag")),
    newbtag_(iConfig.getParameter<edm::InputTag>("newbtag")),
    backmap_(iConfig.getParameter<edm::InputTag>("backmap")) 
{

}
void
RefTestAnalyzer::analyze(const edm::Event &iEvent, const edm::EventSetup &iSetup) {
    using namespace edm;
    using namespace std;
    using namespace reco;
    
    Handle<View<Jet> > jets0; iEvent.getByLabel(jets0_, jets0);
    Handle<View<Jet> > jets1; iEvent.getByLabel(jets1_, jets1);
    Handle<ValueMap<float> > btag;  iEvent.getByLabel(btag_, btag);
    Handle<ValueMap<float> > newbtag;  iEvent.getByLabel(newbtag_, newbtag);
    Handle<ValueMap<CandidateBaseRef> > backmap;  iEvent.getByLabel(backmap_, backmap);
    //    Handle<vector<JetTag> > jtag; iEvent.getByLabel(jtag_, jtag);
    
    ::pat::helper::RefHelper<Candidate> refhelper(*backmap);

    size_t max = 0;
    /*
    for (vector<JetTag>::const_iterator it = jtag->begin(), ed = jtag->end(); it != ed; ++it) {
        std::cout << "Jet (pt " << it->jet()->pt() <<", eta " << it->jet()->eta() <<", phi " << it->jet()->phi() << 
            ")\t disc = " << it->discriminator() << "\t from VMAP disc = " << (*btag)[it->jet()] << std::endl;
        if (max++ > 8) break;
    }
    */
    max = 0;
    for (size_t i = 0, n = jets1->size(); i < n; ++i) {
        RefToBase<Jet> jet = jets1->refAt(i);
        std::cout << "Jet (pt " << jet->pt() <<", eta " << jet->eta() <<", phi " << jet->phi() << std::endl;
        std::cout << "\t Lookup:   "  << refhelper.ancestorLookup(jet, *btag) << std::endl;
        std::cout << "\t New BTag: "  << (*newbtag)[jet] << std::endl;
        if (max++ > 8) break;
    }
}

DEFINE_FWK_MODULE(RefTestAnalyzer);
