import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

function ConsensusToggle({ checked, onChange }) {
  const [isAnimating, setIsAnimating] = useState(false);
  const [isHovered, setIsHovered] = useState(false);

  const handleToggle = () => {
    if (!checked) {
      setIsAnimating(true);
      setTimeout(() => setIsAnimating(false), 350);
    }
    onChange(!checked);
  };

  return (
    <motion.div
      className="relative inline-block"
      initial={false}
    >
      {/* Card container - smaller and more compact */}
      <motion.div
        className="relative px-3 py-1.5 rounded-lg cursor-pointer overflow-hidden select-none inline-flex"
        onClick={handleToggle}
        onMouseEnter={() => setIsHovered(true)}
        onMouseLeave={() => setIsHovered(false)}
        animate={{
          borderColor: checked
            ? isAnimating
              ? ["#2E2E2E", "rgba(168, 85, 247, 0.50)", "rgba(168, 85, 247, 0.40)"]
              : isHovered
                ? "rgba(168, 85, 247, 0.50)"
                : "rgba(168, 85, 247, 0.40)"
            : isHovered
              ? "#3E3E3E"
              : "#2E2E2E",
          backgroundColor: checked
            ? isAnimating
              ? ["#1F1F1F", "rgba(168, 85, 247, 0.12)", "rgba(168, 85, 247, 0.08)"]
              : isHovered
                ? "rgba(168, 85, 247, 0.10)"
                : "rgba(168, 85, 247, 0.08)"
            : isHovered
              ? "#232323"
              : "#1F1F1F",
        }}
        transition={{
          borderColor: { duration: 0.35 },
          backgroundColor: { duration: 0.4, ease: "easeOut" }
        }}
        style={{
          border: "1px solid",
          boxShadow: checked
            ? isHovered
              ? "0 0 24px rgba(168, 85, 247, 0.25), 0 0 48px rgba(168, 85, 247, 0.10), inset 0 0 32px rgba(168, 85, 247, 0.08)"
              : "0 0 20px rgba(168, 85, 247, 0.20), 0 0 40px rgba(168, 85, 247, 0.08), inset 0 0 24px rgba(168, 85, 247, 0.06)"
            : "none",
          transition: "box-shadow 0.4s ease-out"
        }}
      >
        {/* Gloss sweep animation */}
        <AnimatePresence>
          {isAnimating && checked && (
            <motion.div
              className="absolute inset-0 rounded-xl pointer-events-none"
              style={{
                background: "linear-gradient(to right, transparent, rgba(255, 255, 255, 0.1), transparent)",
                width: "100%",
                height: "100%"
              }}
              initial={{ x: "-120%" }}
              animate={{ x: "120%" }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.25, ease: "easeInOut", delay: 0.16 }}
            />
          )}
        </AnimatePresence>

        <div className="flex items-center gap-2">
          {/* Toggle switch - even smaller */}
          <div className="relative w-8 h-4 flex-shrink-0">
            <motion.div
              className="absolute inset-0 rounded-full"
              animate={{
                backgroundColor: checked ? "rgba(168, 85, 247, 0.30)" : "#2E2E2E",
                borderColor: checked ? "rgba(168, 85, 247, 0.5)" : "#2E2E2E"
              }}
              transition={{ duration: 0.25 }}
              style={{ border: "1px solid" }}
            />

            {/* Toggle knob - even smaller */}
            <motion.div
              className="absolute top-0.5 w-3 h-3 rounded-full"
              animate={{
                left: checked ? "calc(100% - 0.875rem)" : "0.125rem",
                scale: checked && isAnimating ? [1, 1.1, 1] : 1,
                backgroundColor: checked ? "#a855f7" : "#ffffff",
                boxShadow: checked
                  ? "0 1px 4px rgba(168, 85, 247, 0.5), 0 0 8px rgba(168, 85, 247, 0.3)"
                  : "0 1px 2px rgba(0, 0, 0, 0.15)"
              }}
              transition={{
                left: {
                  type: "spring",
                  stiffness: 700,
                  damping: 35
                },
                scale: {
                  duration: 0.2,
                  ease: "easeOut"
                },
                backgroundColor: {
                  duration: 0.2
                },
                boxShadow: {
                  duration: 0.25
                }
              }}
            />
          </div>

          {/* Label - compact */}
          <motion.span
            className="text-xs select-none"
            animate={{
              fontWeight: checked ? 500 : 400,
              color: checked ? "#E8E9EB" : "#9ca3af"
            }}
            transition={{ duration: 0.2 }}
          >
            Consensus Mode
          </motion.span>
        </div>
      </motion.div>
    </motion.div>
  );
}

export default ConsensusToggle;