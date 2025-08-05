"use client"

import { useRef, useMemo } from "react"
import { Canvas, useFrame } from "@react-three/fiber"
import { Points, PointMaterial } from "@react-three/drei"
import * as THREE from "three"

function DNAHelix() {
  const meshRef = useRef<THREE.Points>(null)

  const particles = useMemo(() => {
    const positions = new Float32Array(2000 * 3)
    const colors = new Float32Array(2000 * 3)

    for (let i = 0; i < 2000; i++) {
      const t = (i / 2000) * Math.PI * 20
      const radius = 2

      // Create double helix structure
      const strand = i % 2
      const x = Math.cos(t + strand * Math.PI) * radius
      const y = (i / 2000) * 20 - 10
      const z = Math.sin(t + strand * Math.PI) * radius

      positions[i * 3] = x
      positions[i * 3 + 1] = y
      positions[i * 3 + 2] = z

      // Color gradient from cyan to green to gold
      const colorT = i / 2000
      if (colorT < 0.5) {
        colors[i * 3] = 0.2 + colorT * 0.6 // R
        colors[i * 3 + 1] = 0.8 + colorT * 0.2 // G
        colors[i * 3 + 2] = 1 - colorT * 0.5 // B
      } else {
        const t2 = (colorT - 0.5) * 2
        colors[i * 3] = 0.8 + t2 * 0.2 // R
        colors[i * 3 + 1] = 1 // G
        colors[i * 3 + 2] = 0.5 - t2 * 0.5 // B
      }
    }

    return { positions, colors }
  }, [])

  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.y = state.clock.elapsedTime * 0.1
      meshRef.current.position.y = Math.sin(state.clock.elapsedTime * 0.2) * 0.5
    }
  })

  return (
    <Points ref={meshRef} positions={particles.positions} colors={particles.colors}>
      <PointMaterial
        size={0.05}
        vertexColors
        transparent
        opacity={0.6}
        sizeAttenuation
        blending={THREE.AdditiveBlending}
      />
    </Points>
  )
}

function DNAConnections() {
  const meshRef = useRef<THREE.Group>(null)

  const connections = useMemo(() => {
    const lines = []
    for (let i = 0; i < 100; i++) {
      const t = (i / 100) * Math.PI * 20
      const radius = 2

      const x1 = Math.cos(t) * radius
      const y = (i / 100) * 20 - 10
      const z1 = Math.sin(t) * radius

      const x2 = Math.cos(t + Math.PI) * radius
      const z2 = Math.sin(t + Math.PI) * radius

      lines.push([new THREE.Vector3(x1, y, z1), new THREE.Vector3(x2, y, z2)])
    }
    return lines
  }, [])

  useFrame((state) => {
    if (meshRef.current) {
      meshRef.current.rotation.y = state.clock.elapsedTime * 0.1
    }
  })

  return (
    <group ref={meshRef}>
      {connections.map((line, index) => (
        <line key={index}>
          <bufferGeometry>
            <bufferAttribute
              attach="attributes-position"
              count={2}
              array={new Float32Array([line[0].x, line[0].y, line[0].z, line[1].x, line[1].y, line[1].z])}
              itemSize={3}
            />
          </bufferGeometry>
          <lineBasicMaterial color="#00ff88" transparent opacity={0.3} />
        </line>
      ))}
    </group>
  )
}

export default function DNABackground() {
  return (
    <div className="absolute inset-0 opacity-30">
      <Canvas camera={{ position: [0, 0, 10], fov: 60 }}>
        <ambientLight intensity={0.5} />
        <DNAHelix />
        <DNAConnections />
      </Canvas>
    </div>
  )
}
