#ifndef PhysicsTools_PatAlgos_PATCleanerBase_h
#define PhysicsTools_PatAlgos_PATCleanerBase_h
//
// $Id: PATCleanerBase.h,v 1.4 2008/07/22 12:47:02 gpetrucc Exp $
//

/**
  \class    PATCleanerBase PATCleanerBase.h "PhysicsTools/PatAlgos/interface/PATCleanerBase.h"
  \brief    Produces pat::GenericParticle's

   The PATCleanerBase produces analysis-level pat::GenericParticle's starting from
   a collection of objects of GenericParticleType.

  \author   Steven Lowette, Jeremy Andrea
  \version  $Id: PATCleanerBase.h,v 1.4 2008/07/22 12:47:02 gpetrucc Exp $
*/

#include "FWCore/Framework/interface/EDProducer.h"
#include "FWCore/Framework/interface/Event.h"
#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "FWCore/ParameterSet/interface/InputTag.h"

#include "PhysicsTools/Utilities/interface/StringCutObjectSelector.h"

#include "PhysicsTools/PatAlgos/interface/OverlapHelper.h"

#include <DataFormats/Common/interface/PtrVector.h>
#include <boost/iterator/indirect_iterator.hpp>

namespace pat {

  template<typename T>
  class PATCleanerBase : public edm::EDProducer {
    public:
      typedef StringCutObjectSelector<T> Selector;
      typedef typename std::vector<T>    OutputCollection;

      explicit PATCleanerBase(const edm::ParameterSet & iConfig);
      ~PATCleanerBase();

      virtual void produce(edm::Event & iEvent, const edm::EventSetup & iSetup);

      /// Perform the real cleaning
      ///   preselected = items passing the string-based preselection cut
      ///   overlaps    = result of simple overlap checking (see OverlapHelper docs)
      ///                 it may be a NULL pointer if overlap checking is not enabled
      ///   output      = put your selected items here
      ///   iEvent, iSetup = you might want these
      virtual void clean(const edm::PtrVector<T> & preselected,
                         const pat::helper::OverlapHelper::Result *overlaps,
                         OutputCollection & output,
                         edm::Event & iEvent, const edm::EventSetup & iSetup) = 0;

      virtual void endJob();

    protected:
      edm::InputTag src_;

      Selector                   preselection_;
      pat::helper::OverlapHelper overlapHelper_;

      uint64_t try_, presel_, sel_;

      /// Little class to work with a PtrVector as if it was a View or std::vector
      class PtrVectorFacade {
        public:
            PtrVectorFacade(const edm::PtrVector<T> &ptrs) : ptrs_(ptrs) {}

            size_t size() const { return ptrs_.size(); }
            const T & operator[](size_t i) const { return *ptrs_[i]; }

            typedef typename boost::indirect_iterator<typename edm::PtrVector<T>::const_iterator> const_iterator;
            const_iterator begin() const { return const_iterator(ptrs_.begin()); }
            const_iterator end()   const { return const_iterator(ptrs_.end()  ); }
        private:
            const edm::PtrVector<T> & ptrs_;
      };

  }; // class

} // namespace

template <typename T>
pat::PATCleanerBase<T>::PATCleanerBase(const edm::ParameterSet & iConfig) :
  src_(iConfig.getParameter<edm::InputTag>( "src" )),
  preselection_(iConfig.getParameter<std::string>("preselection")),
  try_(0), presel_(0), sel_(0)
{
  produces<OutputCollection>();
  if (iConfig.exists("removeOverlaps")) {
    edm::ParameterSet overlapConf = iConfig.getParameter<edm::ParameterSet>("removeOverlaps");
    overlapHelper_ = pat::helper::OverlapHelper(overlapConf);
  }
}


template <typename T>
pat::PATCleanerBase<T>::~PATCleanerBase() {
}


template <typename T>
void pat::PATCleanerBase<T>::produce(edm::Event & iEvent, const edm::EventSetup & iSetup) {     
    edm::Handle<edm::View<T> > src;
    iEvent.getByLabel(src_, src);
    try_ += src->size();

    edm::PtrVector<T> preselected;
    for (size_t i = 0, n = src->size(); i < n; ++i) {
        if (preselection_((*src)[i])) preselected.push_back(src->ptrAt(i));
    }
    presel_ += preselected.size();

    std::auto_ptr<pat::helper::OverlapHelper::Result> overlaps;
    if (overlapHelper_.enabled()) {
        overlaps = overlapHelper_.test( iEvent, PtrVectorFacade(preselected) );
    }

    std::auto_ptr<OutputCollection> output(new OutputCollection());
    output->reserve(preselected.size());

    clean(preselected, overlaps.get(), *output, iEvent, iSetup);
    sel_ += output->size();
    
    iEvent.put(output);
}


template <typename T>
void pat::PATCleanerBase<T>::endJob() { 
    edm::LogVerbatim("PATLayer0Summary|PATCleanerBase") << "PATCleanerBase end job. \n" <<
            "Input tag was " << src_.encode() <<
            "\t: try " << try_ <<
            ", preselected " << presel_ << " (" << (try_ > 0 ? presel_/double(try_) * 100.0 : 0) << "%)" <<
            ", pass " << sel_ << " (" << (try_ > 0 ? sel_/double(try_) * 100.0 : 0) << "%)" << "\n";

}

#endif

