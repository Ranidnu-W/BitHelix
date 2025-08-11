import requests
import os

# Test encoding
print("Testing API encoding...")
with open("test_files/Lorem Ipsum.docx", "rb") as f:
    files = {"file": ("Lorem Ipsum.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")}
    data = {"nsym": 10}
    
    response = requests.post("http://localhost:8000/api/encode", files=files, data=data)
    
    if response.status_code == 200:
        result = response.json()
        print(f"✓ Encoding successful")
        print(f"Output file: {result['output_file']}")
        print(f"Original filename: {result['original_filename']}")
        
        # Test decoding
        print("\nTesting API decoding...")
        with open(result['output_file'], "rb") as f:
            files = {"file": ("encoded.fasta", f, "text/plain")}
            data = {"nsym": 10}
            
            response = requests.post("http://localhost:8000/api/decode", files=files, data=data)
            
            if response.status_code == 200:
                decode_result = response.json()
                print(f"✓ Decoding successful")
                print(f"Output file: {decode_result['output_file']}")
                print(f"Original filename: {decode_result['original_filename']}")
                print(f"Detected file type: {decode_result['detected_file_type']}")
                
                # Check the decoded file
                if os.path.exists(decode_result['output_file']):
                    with open(decode_result['output_file'], "rb") as f:
                        header = f.read(10)
                        print(f"File signature: {header.hex()}")
                        is_docx = header.startswith(b'PK\x03\x04')
                        print(f"Is DOCX/ZIP: {is_docx}")
                        
                        # Check for word/document.xml
                        f.seek(0)
                        content = f.read()
                        has_word_doc = b'word/document.xml' in content
                        print(f"Contains word/document.xml: {has_word_doc}")
                        
                        if is_docx and has_word_doc:
                            print("✓ Decoded file is a valid DOCX!")
                        else:
                            print("✗ Decoded file is NOT a valid DOCX!")
                else:
                    print(f"✗ Decoded file not found: {decode_result['output_file']}")
            else:
                print(f"✗ Decoding failed: {response.status_code}")
                print(f"Error: {response.text}")
    else:
        print(f"✗ Encoding failed: {response.status_code}")
        print(f"Error: {response.text}")
