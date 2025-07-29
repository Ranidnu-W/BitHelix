"""Main runner script for DNA encoding experiment."""

import argparse
import os
from dnaio.file_reader import convert_file_to_binary, read_fasta_with_metadata
from encoder.base_mapping import binary_to_base4, base4_to_dna
from encoder.error_correction import add_reed_solomon
from encoder.constraints import enforce_constraints, check_gc_content, has_long_homopolymers, contains_unstable_motifs
from dnaio.file_writer import write_txt, write_fasta
from decoder import decode_dna_sequence


def ensure_output_dir(filepath: str) -> str:
    """Ensure the output directory exists and prepend 'output/' if no directory is given."""
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # If the filepath is just a filename (no directory), prepend 'output/'
    if not os.path.dirname(filepath):
        return os.path.join(output_dir, filepath)
    return filepath


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


def encode_file(input_file: str, output_file: str, nsym: int = 10, motifs: list = None):
    """Encode a file to DNA sequence with metadata."""
    if motifs is None:
        motifs = ["ATATAT", "CGCGCG"]
    
    # 1. Read file and convert to binary
    binary_data = convert_file_to_binary(input_file)

    # 2. Add Reed-Solomon error correction
    corrected_data = add_reed_solomon(binary_data, nsym=nsym)

    # 3. Convert to base-4
    base4_digits = binary_to_base4(corrected_data)

    # 4. Map to DNA (now returns both sequence and metadata)
    dna_sequence, metadata = base4_to_dna(base4_digits)

    # 5. Enforce constraints
    dna_sequence = enforce_constraints(dna_sequence)

    # 6. Report constraints
    gc_content = check_gc_content(dna_sequence)
    has_homopolymers = has_long_homopolymers(dna_sequence)
    has_motifs = contains_unstable_motifs(dna_sequence, motifs)
    print(f'GC content: {gc_content:.2f}%')
    print(f'Long homopolymers: {has_homopolymers}')
    print(f'Unstable motifs present: {has_motifs}')

    # 7. Write output
    output_file = ensure_output_dir(output_file)
    if output_file.endswith('.fasta'):
        write_fasta(output_file, dna_sequence, metadata=metadata)
    elif output_file.endswith('.txt'):
        write_txt(output_file, dna_sequence)
    else:
        raise ValueError('Output file must be .txt or .fasta')


def decode_file(input_file: str, output_file: str, nsym: int = 10):
    """Decode a DNA file back to the original data with automatic file type detection."""
    # Read DNA sequence and metadata
    dna_sequence, metadata = read_fasta_with_metadata(input_file)
    
    # Decode the data
    decoded_data = decode_dna_sequence(dna_sequence, metadata, nsym=nsym)
    
    # Detect the original file type
    detected_extension = detect_file_type_from_binary(decoded_data)
    
    # If no extension provided or different extension, use the detected one
    if not os.path.splitext(output_file)[1] or os.path.splitext(output_file)[1] != detected_extension:
        base_name = os.path.splitext(output_file)[0]
        output_file = base_name + detected_extension
    
    # Ensure output directory exists
    output_file = ensure_output_dir(output_file)
    
    # Write the decoded data
    with open(output_file, 'wb') as f:
        f.write(decoded_data)
    
    print(f"Decoded data written to {output_file} (detected type: {detected_extension})")


def main():
    """Entry point for the DNA encoding/decoding CLI."""
    parser = argparse.ArgumentParser(description="DNA Data Storage Encoder/Decoder")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Encode command
    encode_parser = subparsers.add_parser('encode', help='Encode a file to DNA')
    encode_parser.add_argument('input_file', type=str, help='Path to input file (.txt, .docx, .mp3)')
    encode_parser.add_argument('output_file', type=str, help='Path to output file (.txt or .fasta)')
    encode_parser.add_argument('--nsym', type=int, default=10, help='Number of Reed-Solomon error correction symbols (default: 10)')
    encode_parser.add_argument('--motifs', nargs='*', default=["ATATAT", "CGCGCG"], help='List of unstable motifs to check for')
    
    # Decode command
    decode_parser = subparsers.add_parser('decode', help='Decode a DNA file back to original data')
    decode_parser.add_argument('input_file', type=str, help='Path to input FASTA file')
    decode_parser.add_argument('output_file', type=str, help='Path to output file')
    decode_parser.add_argument('--nsym', type=int, default=10, help='Number of Reed-Solomon error correction symbols (default: 10)')
    
    args = parser.parse_args()
    
    if args.command == 'encode':
        encode_file(args.input_file, args.output_file, args.nsym, args.motifs)
    elif args.command == 'decode':
        decode_file(args.input_file, args.output_file, args.nsym)
    else:
        parser.print_help()


if __name__ == "__main__":
    main() 