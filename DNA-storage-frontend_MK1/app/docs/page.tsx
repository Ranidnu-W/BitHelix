"use client"

import { motion } from "framer-motion"
import { ArrowLeft, BookOpen, Dna, Database, Shield, Zap } from "lucide-react"
import Link from "next/link"
import DNATerminal from "@/components/dna-terminal"

export default function DocsPage() {
  return (
    <div className="min-h-screen bg-black text-white overflow-x-hidden">
      {/* Background Elements */}
      <div className="fixed inset-0 z-0">
        <div className="absolute inset-0 bg-gradient-to-br from-gray-900 via-black to-gray-900" />
        <div className="absolute top-0 right-0 w-1/2 h-full opacity-20">
          <div className="absolute top-20 right-20 w-96 h-96 bg-gradient-radial from-orange-400/30 via-orange-300/20 to-transparent rounded-full blur-3xl animate-pulse" />
        </div>
        <div className="absolute bottom-20 left-20 w-64 h-64 bg-gradient-radial from-green-400/20 via-green-300/10 to-transparent rounded-full blur-2xl animate-pulse" />
      </div>

      {/* Content */}
      <div className="relative z-10">
        {/* Navigation */}
        <motion.nav
          initial={{ y: -100, opacity: 0 }}
          animate={{ y: 0, opacity: 1 }}
          transition={{ duration: 0.8 }}
          className="fixed top-0 left-0 right-0 z-50 bg-gradient-to-b from-background/80 to-background/40 backdrop-blur-lg border-b border-cyan-500/20 shadow-lg"
        >
          <div className="max-w-7xl mx-auto px-4">
            <div className="flex items-center justify-between h-20">
              <Link href="/" className="flex items-center space-x-3 group">
                <motion.div
                  className="relative"
                  whileHover={{ scale: 1.1 }}
                  transition={{ type: "spring", stiffness: 300, damping: 20 }}
                >
                  <ArrowLeft className="h-6 w-6 text-cyan-400 transition-colors duration-300 group-hover:text-green-400" />
                </motion.div>
                <span className="text-xl font-bold bg-gradient-to-r from-cyan-400 to-green-400 bg-clip-text text-transparent">
                  Back to DNA Storage
                </span>
              </Link>
            </div>
          </div>
        </motion.nav>

        {/* Main Content */}
        <motion.main
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1, delay: 0.3 }}
          className="pt-32 px-4 sm:px-6 lg:px-8"
        >
          <div className="max-w-4xl mx-auto">
            {/* Header */}
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.5 }}
              className="mb-16"
            >
              <div className="flex items-center space-x-4 mb-6">
                <BookOpen className="h-8 w-8 text-cyan-400" />
                <h1 className="text-5xl font-bold text-white">
                  DNA DATA STORAGE
                </h1>
              </div>
              <p className="text-xl text-gray-300 max-w-3xl">
                Revolutionary technology that encodes digital information into synthetic DNA sequences,
                offering unprecedented density and longevity for data preservation.
              </p>
            </motion.div>

            {/* Features Grid */}
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.7 }}
              className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-16"
            >
              {/* Feature 1 */}
              <motion.div
                whileHover={{ scale: 1.05 }}
                transition={{ type: "spring", stiffness: 300, damping: 20 }}
                className="bg-gradient-to-br from-gray-800/50 to-gray-900/50 backdrop-blur-sm border border-gray-700/50 rounded-2xl p-6 hover:border-cyan-500/30 transition-all duration-300"
              >
                <Dna className="h-12 w-12 text-cyan-400 mb-4" />
                <h3 className="text-xl font-bold text-white mb-3">Molecular Encoding</h3>
                <p className="text-gray-300">
                  Converts binary data into DNA base pairs (A, C, G, T), achieving storage densities
                  millions of times greater than traditional media.
                </p>
              </motion.div>

              {/* Feature 2 */}
              <motion.div
                whileHover={{ scale: 1.05 }}
                transition={{ type: "spring", stiffness: 300, damping: 20 }}
                className="bg-gradient-to-br from-gray-800/50 to-gray-900/50 backdrop-blur-sm border border-gray-700/50 rounded-2xl p-6 hover:border-green-500/30 transition-all duration-300"
              >
                <Database className="h-12 w-12 text-green-400 mb-4" />
                <h3 className="text-xl font-bold text-white mb-3">Massive Capacity</h3>
                <p className="text-gray-300">
                  Store exabytes of data in a single gram of DNA, with the potential to preserve
                  humanity's entire digital heritage in a space smaller than a sugar cube.
                </p>
              </motion.div>

              {/* Feature 3 */}
              <motion.div
                whileHover={{ scale: 1.05 }}
                transition={{ type: "spring", stiffness: 300, damping: 20 }}
                className="bg-gradient-to-br from-gray-800/50 to-gray-900/50 backdrop-blur-sm border border-gray-700/50 rounded-2xl p-6 hover:border-orange-500/30 transition-all duration-300"
              >
                <Shield className="h-12 w-12 text-orange-400 mb-4" />
                <h3 className="text-xl font-bold text-white mb-3">Error Correction</h3>
                <p className="text-gray-300">
                  Advanced Reed-Solomon encoding ensures data integrity across thousands of years,
                  with built-in redundancy for reliable information recovery.
                </p>
              </motion.div>

              {/* Feature 4 */}
              <motion.div
                whileHover={{ scale: 1.05 }}
                transition={{ type: "spring", stiffness: 300, damping: 20 }}
                className="bg-gradient-to-br from-gray-800/50 to-gray-900/50 backdrop-blur-sm border border-gray-700/50 rounded-2xl p-6 hover:border-purple-500/30 transition-all duration-300"
              >
                <Zap className="h-12 w-12 text-purple-400 mb-4" />
                <h3 className="text-xl font-bold text-white mb-3">Biological Constraints</h3>
                <p className="text-gray-300">
                  Enforces GC content balance and avoids problematic sequences to ensure
                  DNA synthesis and sequencing compatibility.
                </p>
              </motion.div>
            </motion.div>

            {/* Analysis Panel - Positioned under Error Correction frame */}
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.8 }}
              className="absolute top-80 right-8 w-48"
            >
              <motion.div
                className="text-xs text-green-400 font-mono opacity-60 bg-black/20 backdrop-blur-sm rounded-lg p-4 border border-green-500/20"
                animate={{ opacity: [0.4, 0.9, 0.4] }}
                transition={{ duration: 4, repeat: Infinity, delay: 1 }}
              >
                <div className="mb-1">ANALYSIS</div>
                <div className="mb-1">GC: 50.2%</div>
                <div className="mb-1">Length: 1.2kb</div>
                <div className="mb-1">Quality: 99.8%</div>
                <div>Status: ✓</div>
              </motion.div>
            </motion.div>

            {/* DNA Terminal Animation */}
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.9 }}
              className="mb-16"
            >
              <h2 className="text-3xl font-bold text-white mb-6 text-center">Live DNA Sequence Analysis</h2>
              <div className="max-w-4xl mx-auto">
                <DNATerminal />
              </div>
            </motion.div>

            {/* Technical Details */}
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.9 }}
              className="bg-gradient-to-br from-gray-800/30 to-gray-900/30 backdrop-blur-sm border border-gray-700/50 rounded-2xl p-8"
            >
              <h2 className="text-3xl font-bold text-white mb-6">Technical Process</h2>
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div>
                  <h3 className="text-xl font-semibold text-cyan-400 mb-4">Encoding Pipeline</h3>
                  <ul className="space-y-3 text-gray-300">
                    <li className="flex items-start space-x-3">
                      <span className="text-cyan-400 font-bold">1.</span>
                      <span>Binary data conversion to base-4 (quaternary)</span>
                    </li>
                    <li className="flex items-start space-x-3">
                      <span className="text-cyan-400 font-bold">2.</span>
                      <span>Mapping to DNA bases (A=00, C=01, G=10, T=11)</span>
                    </li>
                    <li className="flex items-start space-x-3">
                      <span className="text-cyan-400 font-bold">3.</span>
                      <span>Reed-Solomon error correction encoding</span>
                    </li>
                    <li className="flex items-start space-x-3">
                      <span className="text-cyan-400 font-bold">4.</span>
                      <span>Biological constraint enforcement</span>
                    </li>
                  </ul>
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-green-400 mb-4">Supported Formats</h3>
                  <ul className="space-y-3 text-gray-300">
                    <li className="flex items-center space-x-3">
                      <span className="text-green-400">•</span>
                      <span>Text files (.txt, .docx)</span>
                    </li>
                    <li className="flex items-center space-x-3">
                      <span className="text-green-400">•</span>
                      <span>Audio files (.mp3, .wav)</span>
                    </li>
                    <li className="flex items-center space-x-3">
                      <span className="text-green-400">•</span>
                      <span>Images (.jpg, .png)</span>
                    </li>
                    <li className="flex items-center space-x-3">
                      <span className="text-green-400">•</span>
                      <span>Any binary file format</span>
                    </li>
                  </ul>
                </div>
              </div>
            </motion.div>

            {/* Call to Action */}
            <motion.div
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 1.1 }}
              className="mt-16 text-center"
            >
              <Link href="/">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="inline-flex items-center space-x-3 px-8 py-4 bg-gradient-to-r from-cyan-500 to-green-500 text-white font-bold rounded-full border-2 border-dashed border-white/20 hover:border-white/40 transition-all duration-300"
                >
                  <span>EXPLORE THE TECHNOLOGY</span>
                </motion.button>
              </Link>
            </motion.div>
          </div>
        </motion.main>
      </div>
    </div>
  )
} 