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
    
    const response = await fetch(`${backendUrl}/api/decode`, {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      const errorData = await response.json()
      return NextResponse.json({ 
        error: errorData.detail || "Decoding failed" 
      }, { status: response.status })
    }

    const data = await response.json()
    
    return NextResponse.json({
      original_filename: data.original_filename,
      file_size: data.file_size,
      detected_file_type: data.detected_file_type,
      output_file: data.output_file
    })
  } catch (error) {
    console.error("Decoding error:", error)
    return NextResponse.json({ error: "Decoding failed" }, { status: 500 })
  }
} 