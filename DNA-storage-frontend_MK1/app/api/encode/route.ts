import { type NextRequest, NextResponse } from "next/server"

export async function POST(request: NextRequest) {
  try {
    const formData = await request.formData()
    const file = formData.get("file") as File

    if (!file) {
      return NextResponse.json({ error: "No file provided" }, { status: 400 })
    }

    // Connect to the FastAPI backend
    const backendUrl = process.env.BACKEND_URL || "http://localhost:8000"
    
    const response = await fetch(`${backendUrl}/api/encode`, {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      const errorData = await response.json()
      return NextResponse.json({ 
        error: errorData.detail || "Encoding failed" 
      }, { status: response.status })
    }

    const data = await response.json()
    
    return NextResponse.json({
      dna_sequence: data.dna_sequence,
      original_filename: data.original_filename,
      file_size: data.file_size,
      gc_content: data.gc_content,
      has_homopolymers: data.has_homopolymers,
      has_unstable_motifs: data.has_unstable_motifs,
      metadata: data.metadata,
      output_file: data.output_file
    })
  } catch (error) {
    console.error("Encoding error:", error)
    return NextResponse.json({ error: "Encoding failed" }, { status: 500 })
  }
}
