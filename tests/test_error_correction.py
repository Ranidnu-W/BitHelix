from encoder.error_correction import add_reed_solomon

def test_add_reed_solomon():
    data = b'ACGT'
    encoded = add_reed_solomon(data, nsym=4)
    # The output should be longer than the input by nsym bytes
    assert len(encoded) == len(data) + 4
    # The original data should be at the start of the encoded output
    assert encoded.startswith(data) 