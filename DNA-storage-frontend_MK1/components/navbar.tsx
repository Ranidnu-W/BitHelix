"use client"

import React from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Dna, FileText, Github } from "lucide-react"

const itemFlipVariants = {
  initial: { rotateX: 0, opacity: 1 },
  hover: { rotateX: -90, opacity: 0 },
}

const itemBackVariants = {
  initial: { rotateX: 90, opacity: 0 },
  hover: { rotateX: 0, opacity: 1 },
}

const itemGlowVariants = {
  initial: { opacity: 0, scale: 0.8 },
  hover: {
    opacity: 1,
    scale: 2,
    transition: {
      opacity: { duration: 0.5, ease: "easeInOut" as const },
      scale: { duration: 0.5, type: "spring" as const, stiffness: 300, damping: 25 },
    },
  },
}

const containerGlowVariants = {
  initial: { opacity: 0 },
  hover: {
    opacity: 1,
    transition: {
      duration: 0.5,
      ease: "easeInOut" as const,
    },
  },
}

const springTransition = {
  type: "spring" as const,
  stiffness: 100,
  damping: 20,
  duration: 0.5,
}

export default function Navbar() {
  return (
    <nav className="absolute top-0 left-0 right-0 z-50 p-4">
      <div className="max-w-7xl mx-auto">
        <motion.div
          className="p-3 rounded-2xl bg-gradient-to-b from-background/80 to-background/40 backdrop-blur-lg border border-cyan-500/20 shadow-lg relative overflow-hidden"
          initial="initial"
          whileHover="hover"
        >
          {/* Container-level glow effect */}
          <motion.div
            className="absolute -inset-2 bg-gradient-radial from-transparent via-cyan-400/30 via-30% via-green-400/30 via-60% via-blue-400/30 via-90% to-transparent rounded-3xl z-0 pointer-events-none"
            variants={containerGlowVariants}
          />

          <div className="flex items-center justify-between relative z-10">
            <div className="flex items-center space-x-3">
              <motion.div
                className="relative"
                whileHover={{ scale: 1.1 }}
                transition={{ type: "spring", stiffness: 300, damping: 20 }}
              >
                <Dna className="h-10 w-10 text-cyan-400 transition-colors duration-300 hover:text-green-400" />
                <div className="absolute inset-0 h-10 w-10 text-cyan-400 animate-pulse opacity-50 transition-colors duration-300 hover:text-green-400" />
              </motion.div>
              <motion.div
                className="relative"
                whileHover="hover"
                initial="initial"
              >
                {/* Individual item glow effect */}
                <motion.div
                  className="absolute inset-0 z-0 pointer-events-none"
                  variants={itemGlowVariants}
                  style={{
                    background: "radial-gradient(circle, rgba(239,68,68,0.25) 0%, rgba(220,38,38,0.12) 50%, rgba(185,28,28,0) 100%)",
                    opacity: 0,
                    borderRadius: "16px",
                  }}
                />

                <motion.span
                  className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-green-400 bg-clip-text text-transparent cursor-pointer relative z-10 px-2 py-1 rounded-lg"
                  whileHover={{ scale: 1.05 }}
                  transition={{ type: "spring", stiffness: 300, damping: 20 }}
                >
                  DNA Storage
                </motion.span>
              </motion.div>
            </div>

            <div className="flex items-center space-x-6">
              <motion.div
                className="relative"
                style={{ perspective: "600px" }}
                whileHover="hover"
                initial="initial"
              >
                {/* Individual item glow effect */}
                <motion.div
                  className="absolute inset-0 z-0 pointer-events-none"
                  variants={itemGlowVariants}
                  style={{
                    background: "radial-gradient(circle, rgba(59,130,246,0.15) 0%, rgba(37,99,235,0.06) 50%, rgba(29,78,216,0) 100%)",
                    opacity: 0,
                    borderRadius: "16px",
                  }}
                />

                {/* Front face of the flip animation */}
                <motion.a
                  href="/docs"
                  className="flex items-center gap-2 px-4 py-2 relative z-10 bg-transparent text-gray-300 hover:text-blue-400 transition-colors rounded-xl"
                  variants={itemFlipVariants}
                  transition={springTransition}
                  style={{
                    transformStyle: "preserve-3d",
                    transformOrigin: "center bottom",
                  }}
                >
                  <FileText className="h-5 w-5 transition-colors duration-300" />
                  <span>Docs</span>
                </motion.a>

                {/* Back face of the flip animation */}
                <motion.a
                  href="/docs"
                  className="flex items-center gap-2 px-4 py-2 absolute inset-0 z-10 bg-transparent text-gray-300 hover:text-blue-400 transition-colors rounded-xl"
                  variants={itemBackVariants}
                  transition={springTransition}
                  style={{
                    transformStyle: "preserve-3d",
                    transformOrigin: "center top",
                    rotateX: 90,
                  }}
                >
                  <FileText className="h-5 w-5 transition-colors duration-300" />
                  <span>Docs</span>
                </motion.a>
              </motion.div>

              <motion.div
                className="relative"
                style={{ perspective: "600px" }}
                whileHover="hover"
                initial="initial"
              >
                {/* Individual item glow effect */}
                <motion.div
                  className="absolute inset-0 z-0 pointer-events-none"
                  variants={itemGlowVariants}
                  style={{
                    background: "radial-gradient(circle, rgba(34,197,94,0.15) 0%, rgba(22,163,74,0.06) 50%, rgba(21,128,61,0) 100%)",
                    opacity: 0,
                    borderRadius: "16px",
                  }}
                />

                {/* Front face of the flip animation */}
                <motion.a
                  href="https://github.com/Ranidnu-W/BitHelix"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-2 px-4 py-2 relative z-10 bg-transparent text-gray-300 hover:text-green-400 transition-colors rounded-xl"
                  variants={itemFlipVariants}
                  transition={springTransition}
                  style={{
                    transformStyle: "preserve-3d",
                    transformOrigin: "center bottom",
                  }}
                >
                  <Github className="h-5 w-5 transition-colors duration-300" />
                  <span>GitHub</span>
                </motion.a>

                {/* Back face of the flip animation */}
                <motion.a
                  href="https://github.com/Ranidnu-W/BitHelix"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center gap-2 px-4 py-2 absolute inset-0 z-10 bg-transparent text-gray-300 hover:text-green-400 transition-colors rounded-xl"
                  variants={itemBackVariants}
                  transition={springTransition}
                  style={{
                    transformStyle: "preserve-3d",
                    transformOrigin: "center top",
                    rotateX: 90,
                  }}
                >
                  <Github className="h-5 w-5 transition-colors duration-300" />
                  <span>GitHub</span>
                </motion.a>
              </motion.div>
            </div>
          </div>
        </motion.div>
      </div>
    </nav>
  )
}
