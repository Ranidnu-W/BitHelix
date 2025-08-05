# Test Files for DNA Storage Application

This directory contains sample files for testing the DNA encoding and decoding functionality.

## Available Test Files

### Text Files (.txt)

1. **sample_1.txt** - Basic test file
   - Simple text content
   - Multiple lines
   - Special characters and numbers
   - Good for basic functionality testing

2. **sample_2.txt** - Scientific content
   - Information about DNA storage technology
   - Lists and structured content
   - Technical terminology
   - Tests encoding of educational content

3. **sample_3.txt** - Programming code
   - Python code example
   - Comments and documentation
   - Function definitions
   - Tests encoding of code content

4. **sample_4.txt** - Mathematical content
   - Mathematical constants
   - Formulas and equations
   - Scientific notation
   - Tests encoding of mathematical data

5. **sample_5.txt** - Poetry
   - Creative writing
   - Rhyming structure
   - Literary content
   - Tests encoding of artistic content

### Document Files (.docx)

1. **Lorem Ipsum.docx** - Standard Lorem Ipsum document
   - Microsoft Word format
   - Longer content
   - Rich text formatting
   - Tests encoding of complex document formats

## Usage

To test the DNA encoding/decoding:

1. **Web Interface:**
   - Upload any of these files to the web interface
   - Encode to DNA and download the FASTA file
   - Upload the FASTA file back to decode

2. **Command Line:**
   ```bash
   # Encode a file
   python main.py encode test_files/sample_1.txt output.fasta
   
   # Decode a file
   python main.py decode output.fasta decoded_file.txt
   ```

## File Characteristics

- **Small size:** All files are under 1KB for quick testing
- **Varied content:** Different types of text to test encoding robustness
- **Special characters:** Include symbols, numbers, and formatting
- **Multiple languages:** Some files include non-ASCII characters

## Expected Results

When encoding these files, you should see:
- Different DNA sequences for each file
- Varying GC content percentages
- Different constraint analysis results
- Successful decoding back to original content

These files provide a comprehensive test suite for the DNA storage application. 