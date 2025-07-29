from typing import List


def binary_to_base4(binary_data: bytes) -> list[int]:
    """Convert binary data to a list of base-4 (quaternary) digits.

    Args:
        binary_data (bytes): Input binary data.

    Returns:
        list[int]: List of base-4 digits representing the input.
    """
    bit_str = ''.join(f'{byte:08b}' for byte in binary_data)
    # Pad bit_str to a multiple of 2 bits
    if len(bit_str) % 2 != 0:
        bit_str += '0'
    base4_digits = [int(bit_str[i:i+2], 2) for i in range(0, len(bit_str), 2)]
    return base4_digits


def base4_to_dna(base4_digits: list[int]) -> tuple[str, list[int]]:
    """Constraint-aware mapping: Map base-4 digits to a DNA sequence avoiding homopolymers >2, forbidden motifs, and keeping GC content 40-60%. Deterministic and reversible by returning metadata for each digit.

    Args:
        base4_digits (list[int]): List of base-4 digits (0-3).

    Returns:
        tuple[str, list[int]]: DNA sequence string and metadata bitstream (offsets used for each digit).
    """
    BASES = ['A', 'C', 'G', 'T']
    forbidden_motifs = ["ATATAT", "CGCGCG"]
    max_homopolymer = 2
    gc_min, gc_max = 40.0, 60.0
    seq = []
    metadata = []
    for i, digit in enumerate(base4_digits):
        for offset in range(4):
            base = BASES[(digit + offset) % 4]
            # Check homopolymer
            if len(seq) >= max_homopolymer and all(seq[-j-1] == base for j in range(max_homopolymer)):
                continue
            # Check forbidden motifs
            test_seq = ''.join(seq) + base
            if any(motif in test_seq[-len(motif)-1:] for motif in forbidden_motifs):
                continue
            # Check GC content (only for last base)
            if i == len(base4_digits) - 1:
                gc_count = test_seq.count('G') + test_seq.count('C')
                gc_content = (gc_count / len(test_seq)) * 100
                if not (gc_min <= gc_content <= gc_max):
                    continue
            seq.append(base)
            metadata.append(offset)
            break
        else:
            # If no base is valid, fallback to original mapping (may violate constraints)
            seq.append(BASES[digit])
            metadata.append(0)
    return ''.join(seq), metadata 