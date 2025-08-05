"use client"

import { useRef, useMemo } from "react"
import { Canvas, useFrame } from "@react-three/fiber"
import { Points, PointMaterial } from "@react-three/drei"
import * as THREE from "three"

function FloatingParticles() {
  const meshRef = useRef<THREE.Points>(null)

  const particles = useMemo(() => {
    const positions = new Float32Array(1000 * 3)
    const colors = new Float32Array(1000 * 3)
    const velocities = new Float32Array(1000 * 3)

    for (let i = 0; i < 1000; i++) {
      positions[i * 3] = (Math.random() - 0.5) * 50
      positions[i * 3 + 1] = (Math.random() - 0.5) * 50
      positions[i * 3 + 2] = (Math.random() - 0.5) * 20

      velocities[i * 3] = (Math.random() - 0.5) * 0.02
      velocities[i * 3 + 1] = (Math.random() - 0.5) * 0.02
      velocities[i * 3 + 2] = (Math.random() - 0.5) * 0.02

      // Random colors between cyan, green, and gold
      const colorChoice = Math.random()
      if (colorChoice < 0.33) {
        colors[i * 3] = 0.2
        colors[i * 3 + 1] = 0.8
        colors[i * 3 + 2] = 1
      } else if (colorChoice < 0.66) {
        colors[i * 3] = 0.2
        colors[i * 3 + 1] = 1
        colors[i * 3 + 2] = 0.3
      } else {
        colors[i * 3] = 1
        colors[i * 3 + 1] = 0.8
        colors[i * 3 + 2] = 0.2
      }
    }

    return { positions, colors, velocities }
  }, [])

  useFrame(() => {
    if (meshRef.current) {
      const positions = meshRef.current.geometry.attributes.position.array as Float32Array

      for (let i = 0; i < 1000; i++) {
        positions[i * 3] += particles.velocities[i * 3]
        positions[i * 3 + 1] += particles.velocities[i * 3 + 1]
        positions[i * 3 + 2] += particles.velocities[i * 3 + 2]

        // Wrap around boundaries
        if (Math.abs(positions[i * 3]) > 25) particles.velocities[i * 3] *= -1
        if (Math.abs(positions[i * 3 + 1]) > 25) particles.velocities[i * 3 + 1] *= -1
        if (Math.abs(positions[i * 3 + 2]) > 10) particles.velocities[i * 3 + 2] *= -1
      }

      meshRef.current.geometry.attributes.position.needsUpdate = true
    }
  })

  return (
    <Points ref={meshRef} positions={particles.positions} colors={particles.colors}>
      <PointMaterial
        size={0.02}
        vertexColors
        transparent
        opacity={0.4}
        sizeAttenuation
        blending={THREE.AdditiveBlending}
      />
    </Points>
  )
}

export default function ParticleSystem() {
  return (
    <div className="absolute inset-0 opacity-20">
      <Canvas camera={{ position: [0, 0, 10], fov: 60 }}>
        <FloatingParticles />
      </Canvas>
    </div>
  )
}
