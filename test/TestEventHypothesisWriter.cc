#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/Run.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/InputTag.h"

#include "DataFormats/PatCandidates/interface/StringMap.h"
#include "DataFormats/PatCandidates/interface/EventHypothesis.h"
#include "DataFormats/Common/interface/ValueMap.h"
#include "DataFormats/Math/interface/deltaR.h"

class TestEventHypothesisWriter : public edm::EDProducer {
    public:
        TestEventHypothesisWriter(const edm::ParameterSet &iConfig) ;
        virtual void produce( edm::Event &iEvent, const edm::EventSetup &iSetup) ;
        virtual void beginRun(edm::Run   &iRun,   const edm::EventSetup &iSetup) ;     
    private:
        edm::InputTag jets_, muons_;
        StringMap names_;
};



TestEventHypothesisWriter::TestEventHypothesisWriter(const edm::ParameterSet &iConfig) :
    jets_(iConfig.getParameter<edm::InputTag>("jets")),
    muons_(iConfig.getParameter<edm::InputTag>("muons"))
{
    produces<StringMap, edm::InRun>();
    produces<std::vector<pat::EventHypothesis> >();
    produces<edm::ValueMap<double> >("deltaR");
}

void 
TestEventHypothesisWriter::beginRun(edm::Run &iRun, const edm::EventSetup &iSetup) {
    names_.clear();
    names_.add("muon", 1);
    names_.add("nearest jet",  2);
    names_.add("other jet",    3);
    iRun.put(std::auto_ptr<StringMap>(new StringMap(names_))); // put a copy in the run
}

void
TestEventHypothesisWriter::produce(edm::Event &iEvent, const edm::EventSetup &iSetup) {
    using namespace edm;
    using namespace std;
    using reco::Candidate; 
    using reco::CandidateBaseRef;

    auto_ptr<vector<pat::EventHypothesis> > hyps(new vector<pat::EventHypothesis>());;
    vector<double>  deltaRs;
    
    Handle<View<Candidate> > hMu; 
    iEvent.getByLabel(muons_, hMu);

    Handle<View<Candidate> > hJet; 
    iEvent.getByLabel(jets_, hJet);
    
    // fake analysis
    for (size_t imu = 0, nmu = hMu->size(); imu < nmu; ++imu) {
        pat::EventHypothesis h;
        CandidateBaseRef mu = hMu->refAt(imu);
        h.add(mu, names_["muon"]);
        
        int bestj = -1; double drmin = 99.0;
        for (size_t ij = 0, nj = hJet->size(); ij < nj; ++ij) {
            CandidateBaseRef jet = hJet->refAt(ij);
            if (jet->et() < 20) break;
            double dr = deltaR(*jet, *mu);
            if (dr < drmin) {
                bestj = ij; drmin = dr;
            }
        }
        if (bestj == -1) continue;

        h.add(hJet->refAt(bestj), names_["nearest jet"]);

        for (size_t ij = 0, nj = hJet->size(); ij < nj; ++ij) {
            if (ij == size_t(bestj)) continue;
            CandidateBaseRef jet = hJet->refAt(ij);
            if (jet->et() < 20) break;
            h.add(jet, names_["other jet"]);
        }
        
        // save hypothesis
        deltaRs.push_back(drmin);
        hyps->push_back(h);
    }

    std::cout << "Found " << deltaRs.size() << " possible options" << std::endl;

    // work done, save results
    OrphanHandle<vector<pat::EventHypothesis> > handle = iEvent.put(hyps);
    auto_ptr<ValueMap<double> > deltaRMap(new ValueMap<double>());
    //if (deltaRs.size() > 0) {
        ValueMap<double>::Filler filler(*deltaRMap);
        filler.insert(handle, deltaRs.begin(), deltaRs.end());
        filler.fill();
    //}
    iEvent.put(deltaRMap, "deltaR");
}

DEFINE_FWK_MODULE(TestEventHypothesisWriter);
