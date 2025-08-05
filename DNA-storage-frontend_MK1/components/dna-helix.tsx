"use client"

import React, { useState, useEffect } from "react"
import { motion } from "framer-motion"

export default function DNAHelix() {
    const [isClient, setIsClient] = useState(false)

    useEffect(() => {
        setIsClient(true)
    }, [])

    return (
        <div className="fixed top-0 right-0 w-1/3 h-full pointer-events-none z-0">
            {/* DNA Animation Container */}
            <div className="relative w-full h-full">

                {/* Floating Data Particles */}
                {isClient && [...Array(12)].map((_, i) => (
                    <motion.div
                        key={`particle-${i}`}
                        className="absolute w-1 h-1 bg-gradient-to-r from-cyan-400 to-green-400 rounded-full"
                        style={{
                            left: `${20 + (i % 4) * 15}%`,
                            top: `${10 + (i % 3) * 25}%`,
                        }}
                        animate={{
                            y: [0, -20, 0],
                            opacity: [0.3, 1, 0.3],
                            scale: [0.8, 1.2, 0.8],
                        }}
                        transition={{
                            duration: 3 + i * 0.2,
                            repeat: Infinity,
                            delay: i * 0.3,
                        }}
                    />
                ))}



                {/* Elegant DNA Helix */}
                {isClient && (
                    <motion.div
                        className="absolute top-40 right-8 w-32 h-72"
                        animate={{ rotateY: 360 }}
                        transition={{ duration: 30, repeat: Infinity, ease: "linear" }}
                        style={{ transformStyle: "preserve-3d" }}
                    >
                        {[...Array(12)].map((_, i) => (
                            <React.Fragment key={`helix-${i}`}>
                                {/* Left strand */}
                                <motion.div
                                    className="absolute w-2 h-2 bg-gradient-to-br from-cyan-400 to-blue-500 rounded-full"
                                    style={{
                                        left: `${50 + 8 * Math.cos(i * 0.5)}%`,
                                        top: `${i * 8}%`,
                                        transform: `translateZ(${8 * Math.sin(i * 0.5)}px)`,
                                        boxShadow: "0 0 12px rgba(34, 211, 238, 0.4)",
                                    }}
                                    animate={{
                                        opacity: [0.6, 1, 0.6],
                                        scale: [0.9, 1.1, 0.9],
                                    }}
                                    transition={{
                                        duration: 4,
                                        repeat: Infinity,
                                        delay: i * 0.2,
                                    }}
                                />

                                {/* Right strand */}
                                <motion.div
                                    className="absolute w-2 h-2 bg-gradient-to-br from-green-400 to-emerald-500 rounded-full"
                                    style={{
                                        left: `${50 + 8 * Math.cos(i * 0.5 + Math.PI)}%`,
                                        top: `${i * 8}%`,
                                        transform: `translateZ(${8 * Math.sin(i * 0.5 + Math.PI)}px)`,
                                        boxShadow: "0 0 12px rgba(34, 197, 94, 0.4)",
                                    }}
                                    animate={{
                                        opacity: [0.6, 1, 0.6],
                                        scale: [0.9, 1.1, 0.9],
                                    }}
                                    transition={{
                                        duration: 4,
                                        repeat: Infinity,
                                        delay: i * 0.2 + 2,
                                    }}
                                />

                                {/* Base pair connection */}
                                <motion.div
                                    className="absolute w-4 h-6"
                                    style={{
                                        left: "50%",
                                        top: `${i * 8}%`,
                                        transform: `translateX(-50%) translateZ(${8 * Math.sin(i * 0.5)}px)`,
                                    }}
                                    animate={{
                                        opacity: [0.3, 0.7, 0.3],
                                    }}
                                    transition={{
                                        duration: 6,
                                        repeat: Infinity,
                                        delay: i * 0.3,
                                    }}
                                >
                                    <div className="absolute left-0 w-0.5 h-full bg-gradient-to-b from-cyan-400 to-transparent" />
                                    <div className="absolute right-0 w-0.5 h-full bg-gradient-to-b from-green-400 to-transparent" />
                                    <div className="absolute top-1/2 left-0 w-full h-0.5 bg-gradient-to-r from-cyan-400 via-white to-green-400 opacity-50" />
                                </motion.div>
                            </React.Fragment>
                        ))}
                    </motion.div>
                )}




            </div>
        </div>
    )
} 