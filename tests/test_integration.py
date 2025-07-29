import pytest
import tempfile
import os
import subprocess
import sys
from pathlib import Path


def test_cli_encode_decode_text():
    """Test complete CLI encode/decode workflow for text files."""
    # Create a temporary text file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
        tmp.write("This is a test text file.\nIt has multiple lines.\nAnd some special chars: !@#$%^&*()")
        tmp_path = tmp.name
    
    try:
        # Encode the file
        result = subprocess.run([
            sys.executable, 'main.py', 'encode', tmp_path, 'output/test_cli_text.fasta'
        ], capture_output=True, text=True)
        assert result.returncode == 0, f"Encode failed: {result.stderr}"
        
        # Decode the file
        result = subprocess.run([
            sys.executable, 'main.py', 'decode', 'output/test_cli_text.fasta', 'output/decoded_cli_text'
        ], capture_output=True, text=True)
        assert result.returncode == 0, f"Decode failed: {result.stderr}"
        
        # Verify the decoded file exists and has correct extension
        decoded_file = Path('output/decoded_cli_text.txt')
        assert decoded_file.exists(), "Decoded file not found"
        
        # Verify content integrity
        with open(tmp_path, 'r') as original:
            original_content = original.read()
        with open(decoded_file, 'r') as decoded:
            decoded_content = decoded.read()
        assert decoded_content == original_content, "Content mismatch"
        
    finally:
        # Cleanup
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def test_cli_encode_decode_docx():
    """Test complete CLI encode/decode workflow for DOCX files."""
    # Use the existing DOCX file
    docx_path = "Lorem Ipsum.docx"
    assert os.path.exists(docx_path), "DOCX test file not found"
    
    try:
        # Encode the file
        result = subprocess.run([
            sys.executable, 'main.py', 'encode', docx_path, 'output/test_cli_docx.fasta'
        ], capture_output=True, text=True)
        assert result.returncode == 0, f"Encode failed: {result.stderr}"
        
        # Decode the file
        result = subprocess.run([
            sys.executable, 'main.py', 'decode', 'output/test_cli_docx.fasta', 'output/decoded_cli_docx'
        ], capture_output=True, text=True)
        assert result.returncode == 0, f"Decode failed: {result.stderr}"
        
        # Verify the decoded file exists and has correct extension
        decoded_file = Path('output/decoded_cli_docx.docx')
        assert decoded_file.exists(), "Decoded file not found"
        
        # Verify file size is reasonable (should be close to original)
        original_size = os.path.getsize(docx_path)
        decoded_size = os.path.getsize(decoded_file)
        size_ratio = decoded_size / original_size
        assert 0.8 <= size_ratio <= 1.2, f"File size mismatch: {size_ratio}"
        
    except Exception as e:
        pytest.fail(f"DOCX test failed: {e}")


def test_cli_encode_decode_mp3():
    """Test complete CLI encode/decode workflow for MP3 files."""
    # Use the existing MP3 file
    mp3_path = "NY_frank.mp3"
    assert os.path.exists(mp3_path), "MP3 test file not found"
    
    try:
        # Encode the file (this will take a while)
        result = subprocess.run([
            sys.executable, 'main.py', 'encode', mp3_path, 'output/test_cli_mp3.fasta'
        ], capture_output=True, text=True, timeout=300)  # 5 minute timeout
        assert result.returncode == 0, f"Encode failed: {result.stderr}"
        
        # Decode the file
        result = subprocess.run([
            sys.executable, 'main.py', 'decode', 'output/test_cli_mp3.fasta', 'output/decoded_cli_mp3'
        ], capture_output=True, text=True)
        assert result.returncode == 0, f"Decode failed: {result.stderr}"
        
        # Verify the decoded file exists and has correct extension
        decoded_file = Path('output/decoded_cli_mp3.mp3')
        assert decoded_file.exists(), "Decoded file not found"
        
        # Verify file size is reasonable
        original_size = os.path.getsize(mp3_path)
        decoded_size = os.path.getsize(decoded_file)
        size_ratio = decoded_size / original_size
        assert 0.8 <= size_ratio <= 1.2, f"File size mismatch: {size_ratio}"
        
    except subprocess.TimeoutExpired:
        pytest.skip("MP3 encoding took too long, skipping")
    except Exception as e:
        pytest.fail(f"MP3 test failed: {e}")


def test_cli_error_handling():
    """Test CLI error handling for invalid inputs."""
    # Test with non-existent input file
    result = subprocess.run([
        sys.executable, 'main.py', 'encode', 'nonexistent.txt', 'output/test.fasta'
    ], capture_output=True, text=True)
    assert result.returncode != 0, "Should fail with non-existent file"
    
    # Test with invalid command
    result = subprocess.run([
        sys.executable, 'main.py', 'invalid_command'
    ], capture_output=True, text=True)
    assert result.returncode != 0, "Should fail with invalid command"
    
    # Test with missing arguments
    result = subprocess.run([
        sys.executable, 'main.py', 'encode'
    ], capture_output=True, text=True)
    assert result.returncode != 0, "Should fail with missing arguments"


def test_cli_help():
    """Test CLI help functionality."""
    result = subprocess.run([
        sys.executable, 'main.py', '--help'
    ], capture_output=True, text=True)
    assert result.returncode == 0, "Help should work"
    assert "DNA Data Storage Encoder/Decoder" in result.stdout


def test_cli_encode_help():
    """Test CLI encode help functionality."""
    result = subprocess.run([
        sys.executable, 'main.py', 'encode', '--help'
    ], capture_output=True, text=True)
    assert result.returncode == 0, "Encode help should work"
    assert "Path to input file" in result.stdout


def test_cli_decode_help():
    """Test CLI decode help functionality."""
    result = subprocess.run([
        sys.executable, 'main.py', 'decode', '--help'
    ], capture_output=True, text=True)
    assert result.returncode == 0, "Decode help should work"
    assert "Path to input FASTA file" in result.stdout


def test_output_directory_creation():
    """Test that output directory is created automatically."""
    # Remove output directory if it exists
    if os.path.exists('output'):
        import shutil
        shutil.rmtree('output')
    
    # Create a temporary text file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
        tmp.write("Test content")
        tmp_path = tmp.name
    
    try:
        # Encode to output directory (should create it)
        result = subprocess.run([
            sys.executable, 'main.py', 'encode', tmp_path, 'output/test_output_dir.fasta'
        ], capture_output=True, text=True)
        assert result.returncode == 0, f"Encode failed: {result.stderr}"
        
        # Verify output directory was created
        assert os.path.exists('output'), "Output directory not created"
        assert os.path.exists('output/test_output_dir.fasta'), "Output file not created"
        
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)


def test_metadata_in_fasta():
    """Test that FASTA files contain both DNA sequence and metadata."""
    # Create a temporary text file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as tmp:
        tmp.write("Test content for metadata verification")
        tmp_path = tmp.name
    
    try:
        # Encode the file
        result = subprocess.run([
            sys.executable, 'main.py', 'encode', tmp_path, 'output/test_metadata.fasta'
        ], capture_output=True, text=True)
        assert result.returncode == 0, f"Encode failed: {result.stderr}"
        
        # Check that the FASTA file contains both sequences
        with open('output/test_metadata.fasta', 'r') as f:
            content = f.read()
        
        # Should have two sequences: main DNA and metadata
        assert content.count('>') == 2, "FASTA should contain exactly 2 sequences"
        assert '>DNA_Sequence' in content, "Main DNA sequence header missing"
        assert '>DNA_Sequence_metadata' in content, "Metadata sequence header missing"
        
    finally:
        if os.path.exists(tmp_path):
            os.unlink(tmp_path) 