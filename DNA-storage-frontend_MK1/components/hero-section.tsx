"use client"

import { motion } from "framer-motion"
import { ArrowDown } from "lucide-react"

export default function HeroSection() {
  const scrollToUpload = () => {
    document.getElementById("upload-section")?.scrollIntoView({
      behavior: "smooth",
    })
  }

  return (
    <section className="min-h-screen flex items-center justify-center relative pt-16">
      <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1, delay: 0.2 }}
        >
          <h1 className="text-5xl md:text-7xl font-bold mb-6">
            <span className="bg-gradient-to-r from-cyan-400 via-green-400 to-yellow-400 bg-clip-text text-transparent">
              Encode Your Data
            </span>
            <br />
            <span className="bg-gradient-to-r from-yellow-400 via-green-400 to-cyan-400 bg-clip-text text-transparent">
              Into DNA
            </span>
          </h1>

          <motion.p
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.5 }}
            className="text-xl md:text-2xl text-gray-300 mb-8 leading-relaxed"
          >
            Upload any file and watch it transform into a DNA sequence.
            <br />
            The future of data storage is biological.
          </motion.p>

          <motion.div
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6, delay: 0.8 }}
            className="flex flex-col sm:flex-row gap-4 justify-center items-center"
          >
            <button
              onClick={scrollToUpload}
              className="group relative px-8 py-4 bg-gradient-to-r from-cyan-500 to-green-500 rounded-lg font-semibold text-white shadow-lg hover:shadow-cyan-500/25 transition-all duration-300 hover:scale-105"
            >
              <span className="relative z-10">Start Encoding</span>
              <div className="absolute inset-0 bg-gradient-to-r from-cyan-600 to-green-600 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
            </button>

            <div className="flex items-center space-x-2 text-gray-400">
              <span>Supports .txt, .docx, .mp3</span>
            </div>
          </motion.div>
        </motion.div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1, delay: 1.2 }}
          className="absolute bottom-8 left-1/2 transform -translate-x-1/2"
        >
          <button
            onClick={scrollToUpload}
            className="animate-bounce text-cyan-400 hover:text-cyan-300 transition-colors duration-200"
          >
            <ArrowDown className="h-8 w-8" />
          </button>
        </motion.div>
      </div>
    </section>
  )
}
