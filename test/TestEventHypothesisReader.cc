#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/EDAnalyzer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Run.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/InputTag.h"

#include "DataFormats/PatCandidates/interface/StringMap.h"
#include "DataFormats/PatCandidates/interface/EventHypothesis.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/Math/interface/deltaR.h"

class TestEventHypothesisReader : public edm::EDAnalyzer {
    public:
        TestEventHypothesisReader(const edm::ParameterSet &iConfig) ;
        virtual void analyze( const edm::Event &iEvent, const edm::EventSetup &iSetup) ;
        virtual void beginRun(const edm::Run   &iRun,   const edm::EventSetup &iSetup) ;     
    private:
        edm::InputTag events_;
        edm::Handle<StringMap> namesH_;
};



TestEventHypothesisReader::TestEventHypothesisReader(const edm::ParameterSet &iConfig) :
    events_(iConfig.getParameter<edm::InputTag>("events"))
{
}

void 
TestEventHypothesisReader::beginRun(const edm::Run &iRun, const edm::EventSetup &iSetup) {
    iRun.getByLabel(events_, namesH_);
}

void
TestEventHypothesisReader::analyze(const edm::Event &iEvent, const edm::EventSetup &iSetup) {
    using namespace edm; using namespace std;
    using reco::Candidate; 
    using reco::CandidateBaseRef;

    const StringMap &names_ = *namesH_;

    Handle<vector<pat::EventHypothesis> > hyps;
    iEvent.getByLabel(events_, hyps);

    Handle<ValueMap<double> >  deltaRsH;
    iEvent.getByLabel(InputTag(events_.label(), "deltaR"), deltaRsH);
    const ValueMap<double> & deltaRs = *deltaRsH;
    
    for (size_t i = 0, n = hyps->size(); i < n; ++i) {
        const pat::EventHypothesis &h = (*hyps)[i];

        std::cout << "Hypothesis " << (i+1) << ": " << std::endl;
        CandidateBaseRef  mu = h[names_["muon"]];
        std::cout << "   muon : pt = " << mu->pt() << ", eta = " << mu->eta() << ", phi = " << mu->phi() << std::endl;
        CandidateBaseRef jet = h[names_["nearest jet"]];
        std::cout << "   n jet: pt = " << jet->pt() << ", eta = " << jet->eta() << ", phi = " << jet->phi() << std::endl;
    
        int32_t role = names_["other jet"];
        for (pat::EventHypothesis::const_iterator it = h.begin(), ed = h.end(); it != ed; ++it) {
            if (it->second != role) continue;
            CandidateBaseRef j2 = it->first;
            std::cout << "   0 jet: pt = " << j2->pt() << ", eta = " << j2->eta() << ", phi = " << j2->phi() << std::endl;
        }

        Ref< vector<pat::EventHypothesis> > key(hyps,i);
        std::cout << "   deltaR: " << deltaRs[key] << "\n" << std::endl;
        
    }

    std::cout << "Found " << hyps->size() << " possible options" << "\n\n" << std::endl;

}

DEFINE_FWK_MODULE(TestEventHypothesisReader);
