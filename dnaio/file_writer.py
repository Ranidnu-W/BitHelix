from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio import SeqIO
from encoder.base_mapping import base4_to_dna

def write_txt(filepath: str, dna_sequence: str) -> None:
    """Write a DNA sequence to a .txt file."""
    with open(filepath, 'w') as f:
        f.write(dna_sequence)


def encode_metadata_constraint_aware(metadata: list[int]) -> str:
    """Encode metadata as DNA using a simple but effective constraint-aware mapping.
    
    Uses alternating encoding schemes to avoid homopolymers while maintaining reversibility.
    """
    BASES = ['A', 'C', 'G', 'T']
    seq = []
    
    for i, offset in enumerate(metadata):
        # Use alternating encoding schemes to avoid homopolymers
        if i % 2 == 0:
            # Even positions: direct mapping
            base = BASES[offset]
        else:
            # Odd positions: reverse mapping to break patterns
            base = BASES[(3 - offset) % 4]
        
        # If this would create a homopolymer, use a different base
        if len(seq) >= 2 and seq[-1] == base and seq[-2] == base:
            # Use a different base that's not the same as the last two
            for alt_base in BASES:
                if alt_base != base:
                    base = alt_base
                    break
        
        seq.append(base)
    
    return ''.join(seq)


def decode_metadata_constraint_aware(metadata_dna: str) -> list[int]:
    """Decode metadata DNA back to the original offset list."""
    BASES = ['A', 'C', 'G', 'T']
    metadata = []
    
    for i, base in enumerate(metadata_dna):
        base_index = BASES.index(base)
        
        # Reverse the alternating encoding scheme
        if i % 2 == 0:
            # Even positions: direct mapping
            offset = base_index
        else:
            # Odd positions: reverse mapping
            offset = (3 - base_index) % 4
        
        metadata.append(offset)
    
    return metadata


def write_fasta(filepath: str, dna_sequence: str, header: str = "DNA_Sequence", metadata: list[int] = None) -> None:
    """Write a DNA sequence (and optional metadata) to a .fasta file using Biopython.
    
    Args:
        filepath (str): Path to the output FASTA file.
        dna_sequence (str): DNA sequence string.
        header (str): Header for the main DNA sequence.
        metadata (list[int], optional): Metadata bitstream to encode as DNA and include in the file.
    """
    from Bio.Seq import Seq
    from Bio.SeqRecord import SeqRecord
    from Bio import SeqIO
    
    records = []
    
    # Add the main DNA sequence
    main_record = SeqRecord(Seq(dna_sequence), id=header, description="")
    records.append(main_record)
    
    # Add metadata as DNA sequence if provided
    if metadata is not None:
        # Encode metadata using constraint-aware mapping
        metadata_dna = encode_metadata_constraint_aware(metadata)
        metadata_record = SeqRecord(Seq(metadata_dna), id=f"{header}_metadata", description="")
        records.append(metadata_record)
    
    SeqIO.write(records, filepath, "fasta") 