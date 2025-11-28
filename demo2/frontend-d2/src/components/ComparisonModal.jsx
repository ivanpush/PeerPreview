import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';

function ComparisonModal({ isOpen, onClose }) {
  if (!isOpen) return null;

  const comparisonData = [
    {
      feature: 'Focus',
      firstPass: 'Major issues only',
      fullReview: 'All sections',
      deepAnalysis: 'Every claim + method'
    },
    {
      feature: 'Depth',
      firstPass: 'Preliminary assessment',
      fullReview: 'Detailed critique',
      deepAnalysis: 'Adversarial reasoning'
    },
    {
      feature: 'Methods Review',
      firstPass: 'High-level scan',
      fullReview: 'Methodological evaluation',
      deepAnalysis: 'Expert-level scrutiny'
    },
    {
      feature: 'Ideal For',
      firstPass: 'Quick feedback',
      fullReview: 'Pre-submission refinement',
      deepAnalysis: 'High-stakes or publication prep'
    },
    {
      feature: 'Models Called',
      firstPass: '1 general model',
      fullReview: '1 high-end model',
      deepAnalysis: (<span>1 top model / 3 top models (<strong className="font-bold">Consensus mode*</strong>)</span>)
    }
  ];

  return (
    <AnimatePresence>
      {isOpen && (
        <>
          {/* Backdrop */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black bg-opacity-60 z-50"
            onClick={onClose}
          />

          {/* Modal */}
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            transition={{ duration: 0.2 }}
            className="fixed inset-0 flex items-center justify-center z-50 p-4"
            onClick={onClose}
          >
            <div
              className="relative bg-[#1A1C1F] border border-[#2E2E2E] rounded-xl max-w-4xl w-full max-h-[90vh] overflow-auto"
              onClick={(e) => e.stopPropagation()}
            >
              {/* Close button positioned in top-right corner */}
              <button
                onClick={onClose}
                className="absolute top-4 right-4 text-[#6A6D73] hover:text-[#A1A5AC] transition-colors z-10"
                aria-label="Close"
              >
                <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                  <path d="M15 5L5 15M5 5L15 15" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" />
                </svg>
              </button>

              {/* Table */}
              <div className="p-6">
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b border-[#3A3A3A]">
                        <th className="text-left py-4 px-5 text-[11px] font-bold text-[#A1A5AC] uppercase tracking-wider w-1/4">

                        </th>
                        <th className="text-left py-4 px-5 text-[11px] font-bold text-[#10b981] uppercase tracking-wider w-1/4">
                          FIRST PASS
                        </th>
                        <th className="text-left py-4 px-5 text-[11px] font-bold text-[#3C82F6] uppercase tracking-wider w-1/4">
                          FULL REVIEW
                        </th>
                        <th className="text-left py-4 px-5 text-[11px] font-bold text-[#a855f7] uppercase tracking-wider w-1/4">
                          DEEP ANALYSIS
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      {comparisonData.map((row, index) => (
                        <tr
                          key={row.feature}
                          className={`border-b border-[#2E2E2E] ${index === comparisonData.length - 1 ? 'border-none' : ''}`}
                        >
                          <td className="py-4 px-5 text-[13px] font-medium text-[#A1A5AC] align-top">
                            {row.feature}
                          </td>
                          <td className="py-4 px-5 text-[13px] text-[#8B8F96] align-top">
                            <div className="leading-relaxed">
                              {row.firstPass}
                            </div>
                          </td>
                          <td className="py-4 px-5 text-[13px] text-[#8B8F96] align-top">
                            <div className="leading-relaxed">
                              {row.fullReview}
                            </div>
                          </td>
                          <td className="py-4 px-5 text-[13px] text-[#8B8F96] align-top">
                            <div className="leading-relaxed">
                              {row.deepAnalysis}
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

              {/* Footer */}
              <div className="px-6 pb-6 pt-2">
                <div className="text-xs text-[#6A6D73] leading-relaxed px-5">
                  <strong className="text-[#a855f7] font-bold">*</strong>Consensus mode calls 3 top models independently and iteratively to cross-check findings and reconcile disagreements
                </div>
              </div>
            </div>
          </motion.div>
        </>
      )}
    </AnimatePresence>
  );
}

export default ComparisonModal;