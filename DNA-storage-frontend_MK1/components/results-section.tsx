"use client"

import { useState } from "react"
import { motion } from "framer-motion"
import { Copy, Download, Check, Loader2, FileText, Info } from "lucide-react"

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

interface ResultsSectionProps {
  encodeResult: EncodeResult | null
  decodeResult: DecodeResult | null
  fileName: string
  isLoading: boolean
  mode: 'encode' | 'decode'
}

export default function ResultsSection({
  encodeResult,
  decodeResult,
  fileName,
  isLoading,
  mode
}: ResultsSectionProps) {
  const [copied, setCopied] = useState(false)

  const handleCopy = async () => {
    try {
      const textToCopy = mode === 'encode' && encodeResult
        ? encodeResult.dna_sequence
        : "No sequence to copy"
      await navigator.clipboard.writeText(textToCopy)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (error) {
      console.error("Failed to copy:", error)
    }
  }

  const handleDownload = () => {
    if (mode === 'encode' && encodeResult) {
      const blob = new Blob([encodeResult.dna_sequence], { type: "text/plain" })
      const url = URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      a.download = `${fileName.split(".")[0]}_dna_sequence.txt`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      URL.revokeObjectURL(url)
    } else if (mode === 'decode' && decodeResult) {
      // Download the decoded file from the backend
      const backendUrl = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000"

      // Extract just the filename from the full path
      const fileName = decodeResult.output_file.split(/[/\\]/).pop() || 'decoded_file'
      const filePath = encodeURIComponent(fileName)

      fetch(`${backendUrl}/api/download/${filePath}`)
        .then(response => {
          if (response.ok) {
            return response.blob()
          }
          throw new Error(`Download failed with status: ${response.status}`)
        })
        .then(blob => {
          const url = URL.createObjectURL(blob)
          const a = document.createElement("a")
          a.href = url
          a.download = decodeResult.original_filename || 'decoded_file'
          document.body.appendChild(a)
          a.click()
          document.body.removeChild(a)
          URL.revokeObjectURL(url)
        })
        .catch(error => {
          console.error('Download error:', error)
          alert('Failed to download file. Please try again.')
        })
    }
  }

  const formatSequence = (sequence: string) => {
    return sequence.match(/.{1,80}/g)?.join("\n") || sequence
  }

  const getModeInfo = () => {
    if (mode === 'encode') {
      return {
        title: "DNA Sequence Result",
        subtitle: "Your file has been encoded into DNA",
        headerText: `${fileName} → DNA Sequence`
      }
    } else {
      return {
        title: "Decoded File Result",
        subtitle: "Your DNA file has been decoded back to original data",
        headerText: `DNA File → ${decodeResult?.original_filename || 'Decoded File'}`
      }
    }
  }

  const modeInfo = getModeInfo()

  return (
    <section className="py-20 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
          className="text-center mb-12"
        >
          <h2 className="text-4xl font-bold mb-4 bg-gradient-to-r from-green-400 to-yellow-400 bg-clip-text text-transparent">
            {modeInfo.title}
          </h2>
          <p className="text-gray-400 text-lg">{modeInfo.subtitle}</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          whileInView={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="bg-gray-800/50 backdrop-blur-sm rounded-xl border border-gray-700 overflow-hidden"
        >
          {/* Header */}
          <div className="flex items-center justify-between p-4 border-b border-gray-700">
            <div className="flex items-center space-x-2">
              <div className="w-3 h-3 bg-red-500 rounded-full"></div>
              <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
              <div className="w-3 h-3 bg-green-500 rounded-full"></div>
              <span className="ml-4 text-gray-400 text-sm">{modeInfo.headerText}</span>
            </div>

            {(mode === 'encode' && encodeResult) || (mode === 'decode' && decodeResult) ? (
              <div className="flex items-center space-x-2">
                {mode === 'encode' && (
                  <button
                    onClick={handleCopy}
                    disabled={isLoading}
                    className="flex items-center space-x-1 px-3 py-1.5 bg-gray-700 hover:bg-gray-600 rounded-md text-sm transition-colors duration-200 disabled:opacity-50"
                  >
                    {copied ? (
                      <>
                        <Check className="h-4 w-4 text-green-400" />
                        <span className="text-green-400">Copied!</span>
                      </>
                    ) : (
                      <>
                        <Copy className="h-4 w-4" />
                        <span>Copy</span>
                      </>
                    )}
                  </button>
                )}

                <button
                  onClick={handleDownload}
                  disabled={isLoading}
                  className="flex items-center space-x-1 px-3 py-1.5 bg-cyan-600 hover:bg-cyan-500 rounded-md text-sm transition-colors duration-200 disabled:opacity-50"
                >
                  <Download className="h-4 w-4" />
                  <span>{mode === 'encode' ? 'Download DNA' : 'Download File'}</span>
                </button>
              </div>
            ) : null}
          </div>

          {/* Content */}
          <div className="p-6">
            {isLoading ? (
              <div className="flex items-center justify-center py-12">
                <Loader2 className="h-8 w-8 text-cyan-400 animate-spin mr-3" />
                <span className="text-gray-400">
                  {mode === 'encode' ? 'Generating DNA sequence...' : 'Decoding DNA sequence...'}
                </span>
              </div>
            ) : mode === 'encode' && encodeResult ? (
              <div className="space-y-6">
                {/* DNA Sequence */}
                <div className="relative">
                  <h3 className="text-lg font-semibold text-gray-300 mb-3">DNA Sequence</h3>
                  <pre className="text-sm text-green-400 font-mono leading-relaxed whitespace-pre-wrap max-h-96 overflow-y-auto scrollbar-thin scrollbar-thumb-gray-600 scrollbar-track-gray-800 bg-gray-900/50 p-4 rounded-lg">
                    {formatSequence(encodeResult.dna_sequence)}
                  </pre>
                  <div className="absolute bottom-0 left-0 right-0 h-8 bg-gradient-to-t from-gray-900/50 to-transparent pointer-events-none"></div>
                </div>

                {/* Analysis Results */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="bg-gray-700/30 p-4 rounded-lg">
                    <div className="flex items-center space-x-2 mb-2">
                      <Info className="h-4 w-4 text-blue-400" />
                      <span className="text-sm font-medium text-gray-300">GC Content</span>
                    </div>
                    <p className="text-2xl font-bold text-blue-400">{encodeResult.gc_content.toFixed(1)}%</p>
                  </div>

                  <div className="bg-gray-700/30 p-4 rounded-lg">
                    <div className="flex items-center space-x-2 mb-2">
                      <Info className="h-4 w-4 text-yellow-400" />
                      <span className="text-sm font-medium text-gray-300">Homopolymers</span>
                    </div>
                    <p className={`text-2xl font-bold ${encodeResult.has_homopolymers ? 'text-red-400' : 'text-green-400'}`}>
                      {encodeResult.has_homopolymers ? 'Present' : 'None'}
                    </p>
                  </div>

                  <div className="bg-gray-700/30 p-4 rounded-lg">
                    <div className="flex items-center space-x-2 mb-2">
                      <Info className="h-4 w-4 text-purple-400" />
                      <span className="text-sm font-medium text-gray-300">Unstable Motifs</span>
                    </div>
                    <p className={`text-2xl font-bold ${encodeResult.has_unstable_motifs ? 'text-red-400' : 'text-green-400'}`}>
                      {encodeResult.has_unstable_motifs ? 'Present' : 'None'}
                    </p>
                  </div>
                </div>
              </div>
            ) : mode === 'decode' && decodeResult ? (
              <div className="space-y-6">
                <div className="bg-green-900/20 border border-green-500/30 rounded-lg p-6">
                  <div className="flex items-center space-x-3 mb-4">
                    <Check className="h-6 w-6 text-green-400" />
                    <h3 className="text-lg font-semibold text-green-400">Decoding Successful!</h3>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <p className="text-sm text-gray-400 mb-1">Original Filename</p>
                      <p className="text-white font-medium">{decodeResult.original_filename}</p>
                    </div>

                    <div>
                      <p className="text-sm text-gray-400 mb-1">Detected File Type</p>
                      <p className="text-white font-medium">{decodeResult.detected_file_type}</p>
                    </div>

                    <div>
                      <p className="text-sm text-gray-400 mb-1">File Size</p>
                      <p className="text-white font-medium">{(decodeResult.file_size / 1024).toFixed(2)} KB</p>
                    </div>

                    <div>
                      <p className="text-sm text-gray-400 mb-1">Output File</p>
                      <p className="text-white font-medium">{decodeResult.output_file.split('/').pop()}</p>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="text-center py-12 text-gray-400">
                <FileText className="h-12 w-12 mx-auto mb-4 opacity-50" />
                <p>No results to display</p>
              </div>
            )}
          </div>

          {/* Stats */}
          {!isLoading && ((mode === 'encode' && encodeResult) || (mode === 'decode' && decodeResult)) && (
            <div className="px-6 py-4 bg-gray-800/30 border-t border-gray-700">
              <div className="flex items-center justify-between text-sm text-gray-400">
                {mode === 'encode' && encodeResult ? (
                  <>
                    <span>Length: {encodeResult.dna_sequence.length.toLocaleString()} base pairs</span>
                    <span>File: {encodeResult.original_filename}</span>
                    <span>Size: {(encodeResult.file_size / 1024).toFixed(2)} KB</span>
                  </>
                ) : mode === 'decode' && decodeResult ? (
                  <>
                    <span>Original: {decodeResult.original_filename}</span>
                    <span>Type: {decodeResult.detected_file_type}</span>
                    <span>Size: {(decodeResult.file_size / 1024).toFixed(2)} KB</span>
                  </>
                ) : null}
              </div>
            </div>
          )}
        </motion.div>
      </div>
    </section>
  )
}
