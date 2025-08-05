"use client"

import type React from "react"

import { useState, useCallback } from "react"
import { motion } from "framer-motion"
import { Upload, File, Loader2 } from "lucide-react"

interface UploadSectionProps {
  onFileUpload: (file: File) => void
  isLoading: boolean
  mode: 'encode' | 'decode'
}

export default function UploadSection({ onFileUpload, isLoading, mode }: UploadSectionProps) {
  const [isDragOver, setIsDragOver] = useState(false)

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragOver(true)
  }, [])

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragOver(false)
  }, [])

  const handleDrop = useCallback(
    (e: React.DragEvent) => {
      e.preventDefault()
      setIsDragOver(false)

      const files = Array.from(e.dataTransfer.files)
      if (files.length > 0) {
        const file = files[0]
        if (isValidFileType(file)) {
          onFileUpload(file)
        }
      }
    },
    [onFileUpload],
  )

  const handleFileSelect = useCallback(
    (e: React.ChangeEvent<HTMLInputElement>) => {
      const files = e.target.files
      if (files && files.length > 0) {
        const file = files[0]
        if (isValidFileType(file)) {
          onFileUpload(file)
        }
      }
    },
    [onFileUpload],
  )

  const isValidFileType = (file: File): boolean => {
    if (mode === 'encode') {
      // For encoding, accept various file types
      const validTypes = [".txt", ".docx", ".mp3", ".pdf", ".jpg", ".png", ".gif", ".zip"]
      const extension = "." + file.name.split(".").pop()?.toLowerCase()
      return validTypes.includes(extension)
    } else {
      // For decoding, only accept FASTA files
      const validTypes = [".fasta", ".fa", ".fas"]
      const extension = "." + file.name.split(".").pop()?.toLowerCase()
      return validTypes.includes(extension)
    }
  }

  const getModeInfo = () => {
    if (mode === 'encode') {
      return {
        title: "Upload Your File",
        subtitle: "Drag and drop your file or click to browse",
        loadingText: "Encoding your file...",
        loadingSubtext: "Converting data into DNA sequence",
        supportedFormats: "Supported formats: TXT, DOCX, MP3, PDF, Images, ZIP (Max 10MB)"
      }
    } else {
      return {
        title: "Upload DNA File",
        subtitle: "Drag and drop your FASTA file or click to browse",
        loadingText: "Decoding your file...",
        loadingSubtext: "Converting DNA sequence back to original data",
        supportedFormats: "Supported formats: FASTA files (.fasta, .fa, .fas)"
      }
    }
  }

  const modeInfo = getModeInfo()

  return (
    <section id="upload-section" className="py-20 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 50 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          viewport={{ once: true }}
          className="text-center mb-12"
        >
          <h2 className="text-4xl font-bold mb-4 bg-gradient-to-r from-cyan-400 to-green-400 bg-clip-text text-transparent">
            {modeInfo.title}
          </h2>
          <p className="text-gray-400 text-lg">{modeInfo.subtitle}</p>
        </motion.div>

        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          whileInView={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="relative"
        >
          <div
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            className={`
              relative border-2 border-dashed rounded-xl p-12 text-center transition-all duration-300
              ${isDragOver
                ? "border-cyan-400 bg-cyan-400/10 shadow-lg shadow-cyan-400/20"
                : "border-gray-600 hover:border-cyan-500 hover:bg-cyan-500/5"
              }
              ${isLoading ? "pointer-events-none opacity-50" : ""}
            `}
          >
            {/* Glowing border animation */}
            <div
              className={`
              absolute inset-0 rounded-xl transition-opacity duration-300
              ${isDragOver ? "opacity-100" : "opacity-0"}
            `}
            >
              <div className="absolute inset-0 rounded-xl bg-gradient-to-r from-cyan-400/20 to-green-400/20 animate-pulse" />
            </div>

            <div className="relative z-10">
              {isLoading ? (
                <div className="flex flex-col items-center">
                  <Loader2 className="h-16 w-16 text-cyan-400 animate-spin mb-4" />
                  <p className="text-xl font-semibold text-cyan-400 mb-2">{modeInfo.loadingText}</p>
                  <p className="text-gray-400">{modeInfo.loadingSubtext}</p>
                </div>
              ) : (
                <>
                  <Upload className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                  <p className="text-xl font-semibold text-gray-300 mb-2">Drop your file here</p>
                  <p className="text-gray-400 mb-6">or click to browse your files</p>

                  <input
                    type="file"
                    accept={mode === 'encode' ? ".txt,.docx,.mp3,.pdf,.jpg,.png,.gif,.zip" : ".fasta,.fa,.fas"}
                    onChange={handleFileSelect}
                    className="hidden"
                    id="file-upload"
                  />

                  <label
                    htmlFor="file-upload"
                    className="inline-flex items-center px-6 py-3 bg-gradient-to-r from-cyan-500 to-green-500 rounded-lg font-semibold text-white cursor-pointer hover:shadow-lg hover:shadow-cyan-500/25 transition-all duration-300 hover:scale-105"
                  >
                    <File className="h-5 w-5 mr-2" />
                    Choose File
                  </label>

                  <p className="text-sm text-gray-500 mt-4">{modeInfo.supportedFormats}</p>
                </>
              )}
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  )
}
