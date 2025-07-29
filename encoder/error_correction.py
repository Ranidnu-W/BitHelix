from reedsolo import RSCodec

def add_reed_solomon(data: bytes, nsym: int = 10) -> bytes:
    """Add Reed-Solomon error correction symbols to the input data."""
    rsc = RSCodec(nsym)
    return rsc.encode(data) 