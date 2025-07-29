import pytest
import tempfile
import os
from decoder import (
    dna_to_base4, 
    base4_to_binary, 
    remove_reed_solomon, 
    decode_dna_sequence,
    dna_and_metadata_to_base4
)
from encoder.base_mapping import binary_to_base4, base4_to_dna
from encoder.error_correction import add_reed_solomon


def test_dna_to_base4():
    """Test DNA to base4 conversion."""
    dna_sequence = "ACGT"
    expected = [0, 1, 2, 3]
    assert dna_to_base4(dna_sequence) == expected


def test_base4_to_binary():
    """Test base4 to binary conversion."""
    base4_digits = [3, 0, 2, 2]  # 11001010
    expected = bytes([202])
    assert base4_to_binary(base4_digits) == expected


def test_remove_reed_solomon():
    """Test Reed-Solomon error correction removal."""
    original_data = b"Hello World"
    encoded_data = add_reed_solomon(original_data, nsym=4)
    decoded_data = remove_reed_solomon(encoded_data, nsym=4)
    assert decoded_data == original_data


def test_dna_and_metadata_to_base4():
    """Test reconstruction of base4 digits from DNA and metadata."""
    # Create test data
    original_base4 = [0, 1, 2, 3, 0, 1, 2, 3]
    dna_sequence, metadata = base4_to_dna(original_base4)
    
    # Reconstruct base4 digits
    reconstructed_base4 = dna_and_metadata_to_base4(dna_sequence, metadata)
    assert reconstructed_base4 == original_base4


def test_decode_dna_sequence():
    """Test full DNA sequence decoding."""
    original_data = b"Test data"
    encoded_data = add_reed_solomon(original_data, nsym=4)
    base4_digits = binary_to_base4(encoded_data)
    dna_sequence, metadata = base4_to_dna(base4_digits)
    
    # Decode back
    decoded_data = decode_dna_sequence(dna_sequence, metadata, nsym=4)
    assert decoded_data == original_data


def test_round_trip_integrity():
    """Test complete encode-decode round trip."""
    test_data = b"This is a test of the DNA encoding system"
    
    # Encode
    encoded_data = add_reed_solomon(test_data, nsym=4)
    base4_digits = binary_to_base4(encoded_data)
    dna_sequence, metadata = base4_to_dna(base4_digits)
    
    # Decode
    decoded_data = decode_dna_sequence(dna_sequence, metadata, nsym=4)
    
    # Verify integrity
    assert decoded_data == test_data


def test_metadata_constraint_aware_encoding():
    """Test that metadata encoding avoids homopolymers."""
    from dnaio.file_writer import encode_metadata_constraint_aware, decode_metadata_constraint_aware
    
    # Test metadata
    metadata = [0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3]
    
    # Encode
    metadata_dna = encode_metadata_constraint_aware(metadata)
    
    # Check for homopolymers (should not have more than 2 consecutive same bases)
    for i in range(len(metadata_dna) - 2):
        assert not (metadata_dna[i] == metadata_dna[i+1] == metadata_dna[i+2]), \
            f"Found homopolymer at position {i}: {metadata_dna[i:i+3]}"
    
    # Decode and verify
    decoded_metadata = decode_metadata_constraint_aware(metadata_dna)
    assert decoded_metadata == metadata


def test_error_handling_invalid_dna():
    """Test error handling for invalid DNA sequences."""
    with pytest.raises(ValueError):
        dna_to_base4("ACGTX")  # Invalid base X


def test_error_handling_invalid_base4():
    """Test error handling for invalid base4 digits."""
    with pytest.raises(ValueError):
        base4_to_binary([0, 1, 2, 5])  # Invalid digit 5


def test_empty_data():
    """Test handling of empty data."""
    empty_data = b""
    encoded_data = add_reed_solomon(empty_data, nsym=4)
    base4_digits = binary_to_base4(encoded_data)
    dna_sequence, metadata = base4_to_dna(base4_digits)
    
    decoded_data = decode_dna_sequence(dna_sequence, metadata, nsym=4)
    assert decoded_data == empty_data


def test_large_data():
    """Test handling of larger data."""
    large_data = b"X" * 1000  # 1KB of data
    
    encoded_data = add_reed_solomon(large_data, nsym=10)
    base4_digits = binary_to_base4(encoded_data)
    dna_sequence, metadata = base4_to_dna(base4_digits)
    
    decoded_data = decode_dna_sequence(dna_sequence, metadata, nsym=10)
    assert decoded_data == large_data


def test_different_nsym_values():
    """Test decoding with different Reed-Solomon symbol counts."""
    test_data = b"Test with different nsym values"
    
    for nsym in [4, 8, 10, 16]:
        encoded_data = add_reed_solomon(test_data, nsym=nsym)
        base4_digits = binary_to_base4(encoded_data)
        dna_sequence, metadata = base4_to_dna(base4_digits)
        
        decoded_data = decode_dna_sequence(dna_sequence, metadata, nsym=nsym)
        assert decoded_data == test_data 