"""
FastAPI server for DNA encoding/decoding web interface.

This module provides REST API endpoints for encoding files to DNA sequences
and decoding DNA sequences back to original files. It includes error correction,
biological constraints enforcement, and file type detection.
"""

import shutil
import urllib.parse
from pathlib import Path
from typing import Optional
import uuid

from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

# Import DNA encoding/decoding modules
from dnaio.file_reader import convert_file_to_binary, read_fasta_with_metadata
from encoder.base_mapping import binary_to_base4, base4_to_dna
from encoder.error_correction import add_reed_solomon
from encoder.constraints import (
    enforce_constraints, 
    check_gc_content, 
    has_long_homopolymers, 
    contains_unstable_motifs
)
from dnaio.file_writer import write_fasta
from decoder import decode_dna_sequence

app = FastAPI(
    title="DNA Storage API",
    description="API for encoding and decoding files to/from DNA sequences",
    version="1.0.0"
)

# Configure CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create temporary directories for file processing
TEMP_DIR = Path("temp")
TEMP_DIR.mkdir(exist_ok=True)

class EncodeResponse(BaseModel):
    dna_sequence: str
    metadata: list[int]  # Changed from dict to list[int]
    original_filename: str
    file_size: int
    gc_content: float
    has_homopolymers: bool
    has_unstable_motifs: bool
    output_file: str

class DecodeResponse(BaseModel):
    original_filename: str
    file_size: int
    detected_file_type: str
    output_file: str

@app.get("/")
async def root():
    """Health check endpoint."""
    return {"message": "DNA Storage API is running"}

@app.post("/api/encode", response_model=EncodeResponse)
async def encode_file(
    file: UploadFile = File(...),
    nsym: int = Form(10),
    motifs: Optional[str] = Form("ATATAT,CGCGCG")
):
    """
    Encode a file to DNA sequence.
    
    Args:
        file: The file to encode
        nsym: Number of Reed-Solomon error correction symbols
        motifs: Comma-separated list of unstable motifs to check for
    
    Returns:
        DNA sequence and metadata
    """
    try:
        # Create unique temporary file
        temp_id = str(uuid.uuid4())
        temp_input = TEMP_DIR / f"input_{temp_id}_{file.filename}"
        temp_output = TEMP_DIR / f"output_{temp_id}.fasta"
        
        # Save uploaded file
        with open(temp_input, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Parse motifs
        motif_list = [m.strip() for m in motifs.split(",")]
        
        # 1. Read file and convert to binary
        binary_data = convert_file_to_binary(str(temp_input))
        
        # 2. Add Reed-Solomon error correction
        corrected_data = add_reed_solomon(binary_data, nsym=nsym)
        
        # 3. Convert to base-4
        base4_digits = binary_to_base4(corrected_data)
        
        # 4. Map to DNA (constraint-aware, returns both sequence and metadata)
        dna_sequence, metadata = base4_to_dna(base4_digits)
        
        # 5. Check constraints
        gc_content = check_gc_content(dna_sequence)
        has_homopolymers = has_long_homopolymers(dna_sequence)
        has_motifs = contains_unstable_motifs(dna_sequence, motif_list)
        
        # 6. Write output
        write_fasta(str(temp_output), dna_sequence, metadata=metadata, original_filename=file.filename)
        
        # Clean up input file
        temp_input.unlink()
        
        return EncodeResponse(
            dna_sequence=dna_sequence,
            metadata=metadata,
            original_filename=file.filename,
            file_size=len(binary_data),
            gc_content=gc_content,
            has_homopolymers=has_homopolymers,
            has_unstable_motifs=has_motifs,
            output_file=str(temp_output)
        )
        
    except Exception as e:
        # Clean up on error
        if 'temp_input' in locals() and temp_input.exists():
            temp_input.unlink()
        raise HTTPException(status_code=500, detail=f"Encoding failed: {str(e)}")

@app.post("/api/decode", response_model=DecodeResponse)
async def decode_file(
    file: UploadFile = File(...),
    nsym: int = Form(10)
):
    """
    Decode a DNA file back to the original data.
    
    Args:
        file: The FASTA file containing DNA sequence
        nsym: Number of Reed-Solomon error correction symbols
    
    Returns:
        Decoded file information
    """
    try:
        # Create unique temporary files
        temp_id = str(uuid.uuid4())
        temp_input = TEMP_DIR / f"input_{temp_id}_{file.filename}"
        temp_output = TEMP_DIR / f"decoded_{temp_id}"
        
        # Save uploaded file
        with open(temp_input, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Read DNA sequence, metadata, and original filename
        dna_sequence, metadata, original_filename = read_fasta_with_metadata(str(temp_input))
        
        # Decode the data
        decoded_data = decode_dna_sequence(dna_sequence, metadata, nsym=nsym)
        
        # Use original filename if available, otherwise detect file type
        if original_filename:
            # Extract extension from original filename
            import os
            _, detected_extension = os.path.splitext(original_filename)
            if not detected_extension:
                # Fallback to detection if no extension in original filename
                detected_extension = detect_file_type_from_binary(decoded_data)
        else:
            # Fallback to detection if no original filename stored
            detected_extension = detect_file_type_from_binary(decoded_data)
        
        # Add extension to output file
        temp_output = temp_output.with_suffix(detected_extension)
        
        # Write the decoded data
        with open(temp_output, "wb") as f:
            f.write(decoded_data)
        
        # Clean up input file
        temp_input.unlink()
        
        return DecodeResponse(
            original_filename=original_filename or file.filename,  # Use original filename if available
            file_size=len(decoded_data),
            detected_file_type=detected_extension,
            output_file=str(temp_output)
        )
        
    except Exception as e:
        # Clean up on error
        if 'temp_input' in locals() and temp_input.exists():
            temp_input.unlink()
        raise HTTPException(status_code=500, detail=f"Decoding failed: {str(e)}")

@app.get("/api/download/{file_path:path}")
async def download_file(file_path: str):
    """Download a processed file by its path."""
    # Decode the file path
    decoded_path = urllib.parse.unquote(file_path)
    
    # Construct the full path in the temp directory
    full_path = TEMP_DIR / decoded_path
    
    # If the file doesn't exist, try to find it by searching in the temp directory
    if not full_path.exists():
        # Look for files that contain the filename
        for temp_file in TEMP_DIR.iterdir():
            if temp_file.is_file() and decoded_path in temp_file.name:
                full_path = temp_file
                break
        else:
            raise HTTPException(status_code=404, detail=f"File not found: {decoded_path}")
    
    # Try to get the original filename from the FASTA file
    original_filename = None
    try:
        if full_path.suffix == '.fasta':
            dna_sequence, metadata, original_filename = read_fasta_with_metadata(str(full_path))
    except:
        pass
    
    # Use original filename if available, otherwise use the file's name
    download_filename = original_filename if original_filename else full_path.name
    
    return FileResponse(
        path=str(full_path),
        filename=download_filename,
        media_type='application/octet-stream'
    )

def detect_file_type_from_binary(binary_data: bytes) -> str:
    """Detect the original file type from binary data using file signatures."""
    # Check for common file signatures
    if binary_data.startswith(b'\xff\xd8\xff'):  # JPEG
        return '.jpg'
    elif binary_data.startswith(b'\x89PNG\r\n\x1a\n'):  # PNG
        return '.png'
    elif binary_data.startswith(b'GIF87a') or binary_data.startswith(b'GIF89a'):  # GIF
        return '.gif'
    elif binary_data.startswith(b'BM'):  # BMP
        return '.bmp'
    elif binary_data.startswith(b'ID3') or binary_data.startswith(b'\xff\xfb') or binary_data.startswith(b'\xff\xf3'):  # MP3
        return '.mp3'
    elif binary_data.startswith(b'RIFF') and binary_data[8:12] == b'WAVE':  # WAV
        return '.wav'
    elif binary_data.startswith(b'PK\x03\x04'):  # ZIP/DOCX/XLSX/PPTX
        # Check if it's a DOCX file by looking for specific files in the ZIP
        if b'word/document.xml' in binary_data:
            return '.docx'
        elif b'xl/worksheets/' in binary_data:
            return '.xlsx'
        elif b'ppt/slides/' in binary_data:
            return '.pptx'
        else:
            return '.zip'
    elif binary_data.startswith(b'%PDF'):  # PDF
        return '.pdf'
    elif binary_data.startswith(b'\x1f\x8b'):  # GZIP
        return '.gz'
    elif binary_data.startswith(b'PK\x05\x06'):  # ZIP (end of central directory)
        return '.zip'
    else:
        # Default to .txt for text files or unknown types
        # Check if it looks like text (mostly printable ASCII)
        try:
            text_sample = binary_data[:1000].decode('utf-8', errors='ignore')
            # Count printable characters vs non-printable
            printable_count = sum(1 for c in text_sample if 32 <= ord(c) <= 126 or c in '\n\r\t')
            total_count = len(text_sample)
            if total_count > 0 and printable_count / total_count > 0.8:  # 80% printable characters
                return '.txt'
        except:
            pass
        return '.bin'  # Generic binary file

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 