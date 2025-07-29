import os
import tempfile
from dnaio.file_writer import write_txt, write_fasta, encode_metadata_constraint_aware, decode_metadata_constraint_aware
from dnaio.file_reader import read_txt_file, read_fasta_with_metadata
from Bio import SeqIO

def test_write_and_read_txt():
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt') as tmp:
        write_txt(tmp.name, 'ACGT')
        tmp.close()
        data = read_txt_file(tmp.name)
        assert data.decode('utf-8') == 'ACGT'
    if os.path.exists(tmp.name) and os.path.dirname(tmp.name) == tempfile.gettempdir():
        os.remove(tmp.name)

def test_write_and_read_fasta():
    with tempfile.NamedTemporaryFile(delete=False, suffix='.fasta') as tmp:
        write_fasta(tmp.name, 'ACGT', header='test')
        tmp.close()
        record = next(SeqIO.parse(tmp.name, 'fasta'))
        assert str(record.seq) == 'ACGT'
        assert record.id == 'test'
    if os.path.exists(tmp.name) and os.path.dirname(tmp.name) == tempfile.gettempdir():
        os.remove(tmp.name)

def test_write_and_read_fasta_with_metadata():
    """Test FASTA writing and reading with metadata."""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.fasta') as tmp:
        metadata = [0, 1, 2, 3, 0, 1, 2, 3]
        write_fasta(tmp.name, 'ACGTACGT', header='test', metadata=metadata)
        tmp.close()
        
        # Read back the DNA sequence and metadata
        dna_sequence, decoded_metadata = read_fasta_with_metadata(tmp.name)
        
        assert dna_sequence == 'ACGTACGT'
        assert decoded_metadata == metadata
        
    if os.path.exists(tmp.name) and os.path.dirname(tmp.name) == tempfile.gettempdir():
        os.remove(tmp.name)

def test_metadata_constraint_aware_encoding():
    """Test metadata encoding and decoding."""
    metadata = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3]
    
    # Encode metadata
    metadata_dna = encode_metadata_constraint_aware(metadata)
    
    # Check that encoded DNA avoids homopolymers
    for i in range(len(metadata_dna) - 2):
        assert not (metadata_dna[i] == metadata_dna[i+1] == metadata_dna[i+2]), \
            f"Found homopolymer at position {i}: {metadata_dna[i:i+3]}"
    
    # Decode metadata
    decoded_metadata = decode_metadata_constraint_aware(metadata_dna)
    
    # Verify round-trip integrity
    assert decoded_metadata == metadata

def test_fasta_without_metadata():
    """Test FASTA reading when no metadata is present."""
    with tempfile.NamedTemporaryFile(delete=False, suffix='.fasta') as tmp:
        write_fasta(tmp.name, 'ACGT', header='test')  # No metadata
        tmp.close()
        
        # Read back
        dna_sequence, metadata = read_fasta_with_metadata(tmp.name)
        
        assert dna_sequence == 'ACGT'
        assert metadata == []  # Should be empty list when no metadata
        
    if os.path.exists(tmp.name) and os.path.dirname(tmp.name) == tempfile.gettempdir():
        os.remove(tmp.name) 