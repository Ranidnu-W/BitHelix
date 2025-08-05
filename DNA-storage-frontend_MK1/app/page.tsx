"use client"

import { useState } from "react"
import { motion } from "framer-motion"
import Navbar from "@/components/navbar"
import HeroSection from "@/components/hero-section"
import UploadSection from "@/components/upload-section"
import ResultsSection from "@/components/results-section"
import Footer from "@/components/footer"
import DNABackground from "@/components/dna-background"
import ParticleSystem from "@/components/particle-system"
import FluidBackground from "@/components/fluid-background"
import DNAHelix from "@/components/dna-helix"

interface EncodeResult {
  dna_sequence: string
  original_filename: string
  file_size: number
  gc_content: number
  has_homopolymers: boolean
  has_unstable_motifs: boolean
  metadata: any
  output_file: string
}

interface DecodeResult {
  original_filename: string
  file_size: number
  detected_file_type: string
  output_file: string
}

export default function HomePage() {
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)
  const [encodeResult, setEncodeResult] = useState<EncodeResult | null>(null)
  const [decodeResult, setDecodeResult] = useState<DecodeResult | null>(null)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [mode, setMode] = useState<'encode' | 'decode'>('encode')

  const handleFileUpload = async (file: File) => {
    setUploadedFile(file)
    setIsLoading(true)
    setError(null)
    setEncodeResult(null)
    setDecodeResult(null)

    try {
      const formData = new FormData()
      formData.append("file", file)

      const endpoint = mode === 'encode' ? "/api/encode" : "/api/decode"
      const response = await fetch(endpoint, {
        method: "POST",
        body: formData,
      })

      if (response.ok) {
        const data = await response.json()
        if (mode === 'encode') {
          setEncodeResult(data)
        } else {
          setDecodeResult(data)
        }
      } else {
        const errorData = await response.json()
        setError(errorData.error || "Operation failed")
      }
    } catch (error) {
      console.error("Upload error:", error)
      setError("Network error. Please try again.")
    } finally {
      setIsLoading(false)
    }
  }

  const handleModeChange = (newMode: 'encode' | 'decode') => {
    setMode(newMode)
    setEncodeResult(null)
    setDecodeResult(null)
    setError(null)
    setUploadedFile(null)
  }

  return (
    <div className="min-h-screen bg-black text-white overflow-x-hidden">
      {/* Background Elements */}
      <div className="fixed inset-0 z-0">
        <DNABackground />
        <ParticleSystem />
        <FluidBackground />
        <DNAHelix />
      </div>

      {/* Content */}
      <div className="relative z-10">
        <Navbar />

        <motion.main initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 1 }}>
          <HeroSection />

          <div className="flex justify-center mb-8">
            <div className="flex bg-gray-800 rounded-lg p-1">
              <button
                onClick={() => handleModeChange('encode')}
                className={`px-6 py-2 rounded-md transition-all ${mode === 'encode'
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-300 hover:text-white'
                  }`}
              >
                Encode to DNA
              </button>
              <button
                onClick={() => handleModeChange('decode')}
                className={`px-6 py-2 rounded-md transition-all ${mode === 'decode'
                    ? 'bg-green-600 text-white'
                    : 'text-gray-300 hover:text-white'
                  }`}
              >
                Decode from DNA
              </button>
            </div>
          </div>

          <UploadSection
            onFileUpload={handleFileUpload}
            isLoading={isLoading}
            mode={mode}
          />

          {error && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="max-w-4xl mx-auto mt-8 p-4 bg-red-900/20 border border-red-500 rounded-lg"
            >
              <p className="text-red-400">Error: {error}</p>
            </motion.div>
          )}

          {(encodeResult || decodeResult || isLoading) && (
            <ResultsSection
              encodeResult={encodeResult}
              decodeResult={decodeResult}
              fileName={uploadedFile?.name || ""}
              isLoading={isLoading}
              mode={mode}
            />
          )}
        </motion.main>

        <Footer />
      </div>
    </div>
  )
}
