from typing import List
from reedsolo import RSCodec


def dna_to_base4(dna_sequence: str) -> List[int]:
    """Convert a DNA sequence (A, C, G, T) to a list of base-4 digits (0-3).

    Args:
        dna_sequence (str): DNA sequence string.

    Returns:
        List[int]: List of base-4 digits.

    Raises:
        ValueError: If the DNA sequence contains invalid bases.
    """
    mapping = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
    try:
        return [mapping[base] for base in dna_sequence]
    except KeyError as e:
        raise ValueError(f"Invalid DNA base found: {e}")


def base4_to_binary(base4_digits: List[int]) -> bytes:
    """Convert a list of base-4 digits to binary data (bytes).

    Args:
        base4_digits (List[int]): List of base-4 digits (0-3).

    Returns:
        bytes: Decoded binary data.

    Raises:
        ValueError: If the base4_digits contain invalid digits.
    """
    # Validate input
    for digit in base4_digits:
        if not 0 <= digit <= 3:
            raise ValueError(f"Invalid base4 digit: {digit}. Must be 0-3.")
    
    # Convert base-4 digits to a bit string
    bit_str = ''.join(f'{d:02b}' for d in base4_digits)
    # Pad to a multiple of 8 bits
    if len(bit_str) % 8 != 0:
        bit_str = bit_str[:-(len(bit_str) % 8)]
    # Convert to bytes
    return bytes(int(bit_str[i:i+8], 2) for i in range(0, len(bit_str), 8))


def remove_reed_solomon(data: bytes, nsym: int = 10) -> bytes:
    """Remove Reed-Solomon error correction symbols from the input data.

    Args:
        data (bytes): Encoded data with ECC.
        nsym (int): Number of Reed-Solomon symbols used during encoding.

    Returns:
        bytes: Decoded data with ECC removed.
    """
    rsc = RSCodec(nsym)
    decoded, _, _ = rsc.decode(data)
    return decoded


def dna_and_metadata_to_base4(dna_sequence: str, metadata: list[int]) -> list[int]:
    """Reconstruct the original base-4 digits from the DNA sequence and metadata bitstream.

    Args:
        dna_sequence (str): DNA sequence string (A, C, G, T).
        metadata (list[int]): Metadata bitstream (offsets used for each digit).

    Returns:
        list[int]: Original base-4 digits.
    """
    BASES = ['A', 'C', 'G', 'T']
    base4_digits = []
    for i, (base, offset) in enumerate(zip(dna_sequence, metadata)):
        base_index = BASES.index(base)
        digit = (base_index - offset) % 4
        base4_digits.append(digit)
    return base4_digits


def decode_dna_sequence(dna_sequence: str, metadata: list[int], nsym: int = 10) -> bytes:
    """Decode a DNA sequence (with metadata) back to the original binary data, reversing the encoding pipeline.

    Args:
        dna_sequence (str): DNA sequence string (A, C, G, T).
        metadata (list[int]): Metadata bitstream (offsets used for each digit).
        nsym (int): Number of Reed-Solomon error correction symbols used during encoding.

    Returns:
        bytes: The original binary data (payload only, ECC removed).
    """
    base4_digits = dna_and_metadata_to_base4(dna_sequence, metadata)
    encoded_bytes = base4_to_binary(base4_digits)
    decoded_bytes = remove_reed_solomon(encoded_bytes, nsym=nsym)
    return decoded_bytes 