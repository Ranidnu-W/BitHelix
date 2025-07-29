import os
from typing import Optional


def read_txt_file(filepath: str) -> bytes:
    """Read a text file and return its contents as bytes.

    Args:
        filepath (str): Path to the .txt file.

    Returns:
        bytes: File contents as bytes.
    """
    with open(filepath, 'rb') as f:
        return f.read()


def read_docx_file(filepath: str) -> bytes:
    """Read a .docx file and return its contents as bytes.

    Args:
        filepath (str): Path to the .docx file.

    Returns:
        bytes: File contents as bytes (preserves original DOCX structure).
    """
    # Read the DOCX file as binary to preserve its structure for file type detection
    with open(filepath, 'rb') as f:
        return f.read()


def read_mp3_file(filepath: str) -> bytes:
    """Read an .mp3 file and return its contents as bytes.

    Args:
        filepath (str): Path to the .mp3 file.

    Returns:
        bytes: File contents as bytes.
    """
    with open(filepath, 'rb') as f:
        return f.read()


def read_fasta_with_metadata(filepath: str) -> tuple[str, list[int]]:
    """Read a FASTA file containing both a main DNA sequence and metadata DNA sequence.
    
    Args:
        filepath (str): Path to the FASTA file.
        
    Returns:
        tuple[str, list[int]]: Main DNA sequence and metadata list.
    """
    from Bio import SeqIO
    from dnaio.file_writer import decode_metadata_constraint_aware
    
    records = list(SeqIO.parse(filepath, "fasta"))
    
    if len(records) < 1:
        raise ValueError("FASTA file must contain at least one DNA sequence")
    
    # First record is the main DNA sequence
    main_dna = str(records[0].seq)
    
    # Second record (if present) is the metadata
    metadata = []
    if len(records) >= 2:
        metadata_dna = str(records[1].seq)
        # Decode metadata using constraint-aware decoding
        metadata = decode_metadata_constraint_aware(metadata_dna)
    
    return main_dna, metadata


def convert_file_to_binary(filepath: str) -> bytes:
    """Detect file type and convert the file to a binary bitstream.

    Args:
        filepath (str): Path to the input file.

    Returns:
        bytes: File contents as a binary bitstream.
    """
    ext = os.path.splitext(filepath)[1].lower()
    if ext == '.txt':
        return read_txt_file(filepath)
    elif ext == '.docx':
        return read_docx_file(filepath)
    elif ext == '.mp3':
        return read_mp3_file(filepath)
    else:
        raise ValueError(f"Unsupported file type: {ext}") 