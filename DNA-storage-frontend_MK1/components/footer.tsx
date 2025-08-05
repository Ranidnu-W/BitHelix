"use client"

import { motion } from "framer-motion"


export default function Footer() {
  return (
    <motion.footer
      initial={{ opacity: 0, y: 50 }}
      whileInView={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8 }}
      viewport={{ once: true }}
      className="py-12 px-4 sm:px-6 lg:px-8 border-t border-gray-800"
    >
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-center">
          <div>
            <p className="text-gray-400 text-sm">© 2025 DNA Storage Project. Built with cutting-edge biotechnology.</p>
          </div>
        </div>
      </div>
    </motion.footer>
  )
}
