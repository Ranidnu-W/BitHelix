import pytest
from encoder.constraints import check_gc_content, has_long_homopolymers, contains_unstable_motifs, enforce_constraints
from encoder.base_mapping import base4_to_dna

def test_check_gc_content():
    assert check_gc_content('GCGC') == 100.0
    assert check_gc_content('ATAT') == 0.0
    assert check_gc_content('ATGC') == 50.0

def test_has_long_homopolymers():
    assert has_long_homopolymers('AAAAC', max_run=3) is True
    assert has_long_homopolymers('ACGTACGT', max_run=3) is False

def test_contains_unstable_motifs():
    assert contains_unstable_motifs('ATATATCG', ['ATATAT']) is True
    assert contains_unstable_motifs('GCGCGC', ['ATATAT']) is False

def test_base4_to_dna_constraints():
    """Test that base4_to_dna produces sequences and that constraint checking functions work."""
    from encoder.base_mapping import base4_to_dna
    
    # Test with a simple case
    base4 = [0, 0, 1, 0, 0, 0, 2, 2, 3, 3, 0, 0, 1, 0, 0, 0, 2, 2, 3, 3, 0, 0, 1, 0, 0, 0]
    dna, metadata = base4_to_dna(base4)
    
    # Check that we get both DNA sequence and metadata
    assert len(dna) == len(base4)
    assert len(metadata) == len(base4)
    
    # Check that constraint checking functions work (they may not always be satisfied)
    gc_content = check_gc_content(dna)
    has_homopolymers = has_long_homopolymers(dna, max_run=3)
    has_motifs = contains_unstable_motifs(dna, ["ATATAT", "CGCGCG"])
    
    # Verify the functions return the expected types
    assert isinstance(gc_content, float)
    assert isinstance(has_homopolymers, bool)
    assert isinstance(has_motifs, bool)
    
    # Check that DNA sequence only contains valid bases
    valid_bases = {'A', 'C', 'G', 'T'}
    assert all(base in valid_bases for base in dna) 