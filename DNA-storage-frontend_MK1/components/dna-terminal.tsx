"use client"

import React, { useState, useEffect } from "react"
import { motion } from "framer-motion"

const DNA_SEQUENCES = [
    "ATCGATCGATCGATCGATCGATCGATCGATCG",
    "GCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTA",
    "TAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC",
    "CGATCGATCGATCGATCGATCGATCGATCGA",
    "ATCGATCGATCGATCGATCGATCGATCGATCG",
    "GCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTA",
    "TAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC",
    "CGATCGATCGATCGATCGATCGATCGATCGA"
]

const DNA_TERMINAL_LINES = [
    "> Initializing DNA sequence analysis...",
    "> Loading genetic algorithms...",
    "> Scanning base pairs...",
    "> ATCGATCGATCGATCGATCGATCGATCGATCG",
    "> GCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTA",
    "> TAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC",
    "> CGATCGATCGATCGATCGATCGATCGATCGA",
    "> Processing sequence data...",
    "> ATCGATCGATCGATCGATCGATCGATCGATCG",
    "> GCTAGCTAGCTAGCTAGCTAGCTAGCTAGCTA",
    "> TAGCTAGCTAGCTAGCTAGCTAGCTAGCTAGC",
    "> CGATCGATCGATCGATCGATCGATCGATCGA",
    "> Sequence analysis complete.",
    "> Ready for DNA storage encoding..."
]

export default function DNATerminal() {
    const [displayedLines, setDisplayedLines] = useState<string[]>([])
    const [currentLineIndex, setCurrentLineIndex] = useState(0)
    const [currentCharIndex, setCurrentCharIndex] = useState(0)
    const [isTyping, setIsTyping] = useState(false)
    const [isClient, setIsClient] = useState(false)

    useEffect(() => {
        setIsClient(true)
    }, [])

    useEffect(() => {
        if (currentLineIndex >= DNA_TERMINAL_LINES.length) {
            // Reset animation when it completes
            setTimeout(() => {
                setDisplayedLines([])
                setCurrentLineIndex(0)
                setCurrentCharIndex(0)
                setIsTyping(true)
            }, 1000) // Wait 1 second before restarting
            return
        }

        const currentLine = DNA_TERMINAL_LINES[currentLineIndex]

        if (currentCharIndex < currentLine.length) {
            const timer = setTimeout(() => {
                setCurrentCharIndex(prev => prev + 1)
            }, 50) // Typing speed

            return () => clearTimeout(timer)
        } else {
            // Line complete, move to next line
            setTimeout(() => {
                setDisplayedLines(prev => [...prev, currentLine])
                setCurrentLineIndex(prev => prev + 1)
                setCurrentCharIndex(0)
            }, 200) // Pause between lines
        }
    }, [currentLineIndex, currentCharIndex])

    useEffect(() => {
        if (currentLineIndex < DNA_TERMINAL_LINES.length) {
            setIsTyping(true)
        } else {
            setIsTyping(false)
        }
    }, [currentLineIndex])

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 1.2 }}
            className="bg-black/80 backdrop-blur-sm border border-green-500/30 rounded-lg p-6 font-mono text-sm overflow-hidden relative"
        >
            {/* 3D Double Helix Animation */}
            {isClient && (
                <div className="absolute top-4 right-4 w-32 h-56 pointer-events-none">
                    <motion.div
                        className="relative w-full h-full"
                        animate={{ rotateY: 360 }}
                        transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
                        style={{ transformStyle: "preserve-3d" }}
                    >
                        {/* First helix strand - Red */}
                        {[...Array(16)].map((_, i) => (
                            <motion.div
                                key={`strand1-${i}`}
                                className="absolute w-1.5 h-1.5 bg-gradient-to-br from-red-400 to-red-300 rounded-full shadow-lg"
                                style={{
                                    left: `${50 + 12 * Math.cos(i * 0.4)}%`,
                                    top: `${i * 6}%`,
                                    transform: `translateZ(${12 * Math.sin(i * 0.4)}px)`,
                                    boxShadow: "0 0 4px rgba(248, 113, 113, 0.3)",
                                }}
                                animate={{
                                    opacity: [0.4, 1, 0.4],
                                    scale: [0.8, 1.1, 0.8],
                                }}
                                transition={{
                                    duration: 3,
                                    repeat: Infinity,
                                    delay: i * 0.15,
                                }}
                            />
                        ))}

                        {/* Second helix strand - Blue */}
                        {[...Array(16)].map((_, i) => (
                            <motion.div
                                key={`strand2-${i}`}
                                className="absolute w-1.5 h-1.5 bg-gradient-to-br from-blue-500 to-blue-400 rounded-full shadow-lg"
                                style={{
                                    left: `${50 + 12 * Math.cos(i * 0.4 + Math.PI)}%`,
                                    top: `${i * 6}%`,
                                    transform: `translateZ(${12 * Math.sin(i * 0.4 + Math.PI)}px)`,
                                    boxShadow: "0 0 4px rgba(59, 130, 246, 0.3)",
                                }}
                                animate={{
                                    opacity: [0.4, 1, 0.4],
                                    scale: [0.8, 1.1, 0.8],
                                }}
                                transition={{
                                    duration: 3,
                                    repeat: Infinity,
                                    delay: i * 0.15 + 1.5,
                                }}
                            />
                        ))}

                        {/* Base pair connections - Red/Blue rungs */}
                        {[...Array(16)].map((_, i) => (
                            <motion.div
                                key={`base-${i}`}
                                className="absolute w-1 h-6"
                                style={{
                                    left: "50%",
                                    top: `${i * 6}%`,
                                    transform: `translateX(-50%) translateZ(${12 * Math.sin(i * 0.4)}px)`,
                                }}
                                animate={{
                                    opacity: [0.3, 0.8, 0.3],
                                }}
                                transition={{
                                    duration: 4,
                                    repeat: Infinity,
                                    delay: i * 0.2,
                                }}
                            >
                                {/* Left half - Red */}
                                <div className="absolute left-0 w-0.5 h-full bg-gradient-to-b from-red-400 to-red-300 rounded-l-sm shadow-sm" />
                                {/* Right half - Blue */}
                                <div className="absolute right-0 w-0.5 h-full bg-gradient-to-b from-blue-500 to-blue-400 rounded-r-sm shadow-sm" />
                            </motion.div>
                        ))}

                        {/* Additional metallic highlights */}
                        {[...Array(8)].map((_, i) => (
                            <motion.div
                                key={`highlight-${i}`}
                                className="absolute w-1 h-1 bg-white rounded-full opacity-60"
                                style={{
                                    left: `${50 + 12 * Math.cos(i * 0.8)}%`,
                                    top: `${i * 12}%`,
                                    transform: `translateZ(${12 * Math.sin(i * 0.8)}px)`,
                                }}
                                animate={{
                                    opacity: [0.2, 0.8, 0.2],
                                }}
                                transition={{
                                    duration: 2,
                                    repeat: Infinity,
                                    delay: i * 0.3,
                                }}
                            />
                        ))}
                    </motion.div>
                </div>
            )}

            <div className="flex items-center space-x-2 mb-4">
                <div className="flex space-x-1">
                    <div className="w-3 h-3 bg-red-500 rounded-full"></div>
                    <div className="w-3 h-3 bg-yellow-500 rounded-full"></div>
                    <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                </div>
                <span className="text-gray-400 text-xs">DNA Terminal v1.0</span>
            </div>

            <div className="space-y-1 h-64 overflow-y-auto scrollbar-hide pr-36">
                {displayedLines.map((line, index) => (
                    <div key={index} className="text-green-400">
                        {line}
                    </div>
                ))}

                {isTyping && (
                    <div className="text-green-400">
                        {DNA_TERMINAL_LINES[currentLineIndex]?.slice(0, currentCharIndex)}
                        <motion.span
                            animate={{ opacity: [1, 0, 1] }}
                            transition={{ duration: 0.8, repeat: Infinity }}
                            className="inline-block w-2 h-4 bg-green-400 ml-1"
                        />
                    </div>
                )}
            </div>
        </motion.div>
    )
} 