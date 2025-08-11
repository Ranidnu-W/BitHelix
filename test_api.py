import requests
import os

def test_api_encoding_decoding():
    """Test the API server encoding and decoding with a DOCX file."""
    
    # Test file path
    test_file = "test_files/Lorem Ipsum.docx"
    
    print("Testing API encoding and decoding...")
    print(f"Input file: {test_file}")
    
    # Step 1: Encode the file
    print("\n1. Encoding file...")
    with open(test_file, 'rb') as f:
        files = {'file': (os.path.basename(test_file), f, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')}
        data = {'nsym': 10}
        
        response = requests.post('http://localhost:8000/api/encode', files=files, data=data)
        
        if response.status_code == 200:
            encode_result = response.json()
            print(f"✓ Encoding successful")
            print(f"  Output file: {encode_result['output_file']}")
            print(f"  Original filename: {encode_result['original_filename']}")
            print(f"  Metadata length: {len(encode_result['metadata'])}")
            
            # Step 2: Decode the file
            print("\n2. Decoding file...")
            fasta_file = encode_result['output_file']
            
            with open(fasta_file, 'rb') as f:
                files = {'file': (os.path.basename(fasta_file), f, 'text/plain')}
                data = {'nsym': 10}
                
                response = requests.post('http://localhost:8000/api/decode', files=files, data=data)
                
                if response.status_code == 200:
                    decode_result = response.json()
                    print(f"✓ Decoding successful")
                    print(f"  Output file: {decode_result['output_file']}")
                    print(f"  Original filename: {decode_result['original_filename']}")
                    print(f"  Detected file type: {decode_result['detected_file_type']}")
                    
                    # Step 3: Check the decoded file
                    print("\n3. Checking decoded file...")
                    decoded_file = decode_result['output_file']
                    
                    if os.path.exists(decoded_file):
                        with open(decoded_file, 'rb') as f:
                            header = f.read(10)
                            print(f"  File signature: {header.hex()}")
                            print(f"  Is DOCX/ZIP: {header.startswith(b'PK\\x03\\x04')}")
                            
                            # Check file size
                            f.seek(0, 2)  # Seek to end
                            size = f.tell()
                            print(f"  File size: {size} bytes")
                            
                            # Check if it's a valid DOCX by looking for word/document.xml
                            f.seek(0)
                            content = f.read()
                            has_word_doc = b'word/document.xml' in content
                            print(f"  Contains word/document.xml: {has_word_doc}")
                            
                            if header.startswith(b'PK\x03\x04') and has_word_doc:
                                print("✓ Decoded file appears to be a valid DOCX file!")
                            else:
                                print("✗ Decoded file does not appear to be a valid DOCX file!")
                    else:
                        print(f"✗ Decoded file not found: {decoded_file}")
                else:
                    print(f"✗ Decoding failed: {response.status_code}")
                    print(f"  Error: {response.text}")
        else:
            print(f"✗ Encoding failed: {response.status_code}")
            print(f"  Error: {response.text}")

if __name__ == "__main__":
    test_api_encoding_decoding()
