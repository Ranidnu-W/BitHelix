import pytest
from encoder.base_mapping import binary_to_base4, base4_to_dna

def test_binary_to_base4():
    # 0b11001010 = 202
    data = bytes([202])
    # 11001010 -> [3, 0, 2, 2]
    assert binary_to_base4(data) == [3, 0, 2, 2]

def test_base4_to_dna():
    base4 = [0, 1, 2, 3]
    dna_sequence, metadata = base4_to_dna(base4)
    assert dna_sequence == 'ACGT'
    assert len(metadata) == len(base4)  # Metadata should have same length as input

def test_base4_to_dna_with_constraints():
    """Test that the new base4_to_dna function returns both sequence and metadata."""
    base4 = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3]
    dna_sequence, metadata = base4_to_dna(base4)
    
    # Check that we get both DNA sequence and metadata
    assert len(dna_sequence) == len(base4)
    assert len(metadata) == len(base4)
    
    # Check that DNA sequence only contains valid bases
    valid_bases = {'A', 'C', 'G', 'T'}
    assert all(base in valid_bases for base in dna_sequence)
    
    # Check that metadata contains valid offsets
    assert all(0 <= offset <= 3 for offset in metadata) 