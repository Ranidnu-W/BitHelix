import pytest
import tempfile
import os
from main import detect_file_type_from_binary


def test_detect_txt_file():
    """Test detection of text files."""
    text_data = b"This is a text file with some content.\nIt has multiple lines.\n"
    detected_type = detect_file_type_from_binary(text_data)
    assert detected_type == '.txt'


def test_detect_docx_file():
    """Test detection of DOCX files."""
    # DOCX files start with PK\x03\x04 and contain word/document.xml
    docx_header = b'PK\x03\x04\x14\x00\x00\x00\x08\x00'
    docx_content = docx_header + b'word/document.xml' + b'PK\x05\x06'
    detected_type = detect_file_type_from_binary(docx_content)
    assert detected_type == '.docx'


def test_detect_mp3_file():
    """Test detection of MP3 files."""
    # MP3 files can start with ID3 or sync bytes
    mp3_data = b'ID3\x03\x00\x00\x00\x00\x00\x00' + b'audio data'
    detected_type = detect_file_type_from_binary(mp3_data)
    assert detected_type == '.mp3'
    
    # Test with sync bytes
    mp3_sync = b'\xff\xfb\x90\x44\x00\x00\x00\x00\x00\x00\x00\x00'
    detected_type = detect_file_type_from_binary(mp3_sync)
    assert detected_type == '.mp3'


def test_detect_pdf_file():
    """Test detection of PDF files."""
    pdf_data = b'%PDF-1.4\n%\\x00\\x00\\x00\\x00\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj'
    detected_type = detect_file_type_from_binary(pdf_data)
    assert detected_type == '.pdf'


def test_detect_png_file():
    """Test detection of PNG files."""
    png_data = b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01'
    detected_type = detect_file_type_from_binary(png_data)
    assert detected_type == '.png'


def test_detect_jpeg_file():
    """Test detection of JPEG files."""
    jpeg_data = b'\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00'
    detected_type = detect_file_type_from_binary(jpeg_data)
    assert detected_type == '.jpg'


def test_detect_zip_file():
    """Test detection of ZIP files."""
    zip_data = b'PK\x03\x04\x14\x00\x00\x00\x08\x00\x00\x00\x00\x00'
    detected_type = detect_file_type_from_binary(zip_data)
    assert detected_type == '.zip'


def test_detect_gzip_file():
    """Test detection of GZIP files."""
    gzip_data = b'\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\x00'
    detected_type = detect_file_type_from_binary(gzip_data)
    assert detected_type == '.gz'


def test_detect_binary_file():
    """Test detection of unknown binary files."""
    binary_data = b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f'
    detected_type = detect_file_type_from_binary(binary_data)
    assert detected_type == '.bin'


def test_detect_empty_file():
    """Test detection of empty files."""
    empty_data = b''
    detected_type = detect_file_type_from_binary(empty_data)
    assert detected_type == '.bin'


def test_detect_mixed_binary_text():
    """Test detection of files with mixed binary and text content."""
    mixed_data = b'Some text content\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09'
    detected_type = detect_file_type_from_binary(mixed_data)
    # Should default to .bin for mixed content
    assert detected_type == '.bin'


def test_detect_text_with_special_chars():
    """Test detection of text files with special characters."""
    text_with_special = b'Text with special chars: \n\r\t\x00\x01\x02\x03'
    detected_type = detect_file_type_from_binary(text_with_special)
    # Should still be detected as text if mostly printable
    assert detected_type == '.txt'


def test_detect_xlsx_file():
    """Test detection of XLSX files."""
    xlsx_header = b'PK\x03\x04\x14\x00\x00\x00\x08\x00'
    xlsx_content = xlsx_header + b'xl/worksheets/sheet1.xml' + b'PK\x05\x06'
    detected_type = detect_file_type_from_binary(xlsx_content)
    assert detected_type == '.xlsx'


def test_detect_pptx_file():
    """Test detection of PPTX files."""
    pptx_header = b'PK\x03\x04\x14\x00\x00\x00\x08\x00'
    pptx_content = pptx_header + b'ppt/slides/slide1.xml' + b'PK\x05\x06'
    detected_type = detect_file_type_from_binary(pptx_content)
    assert detected_type == '.pptx'


def test_detect_wav_file():
    """Test detection of WAV files."""
    wav_data = b'RIFF\x24\x00\x00\x00WAVEfmt \x10\x00\x00\x00\x01\x00'
    detected_type = detect_file_type_from_binary(wav_data)
    assert detected_type == '.wav'


def test_detect_gif_file():
    """Test detection of GIF files."""
    gif_data = b'GIF87a\x10\x00\x10\x00\x91\x00\x00\xff\xff\xff\x00\x00\x00'
    detected_type = detect_file_type_from_binary(gif_data)
    assert detected_type == '.gif'
    
    gif89a_data = b'GIF89a\x10\x00\x10\x00\x91\x00\x00\xff\xff\xff\x00\x00\x00'
    detected_type = detect_file_type_from_binary(gif89a_data)
    assert detected_type == '.gif'


def test_detect_bmp_file():
    """Test detection of BMP files."""
    bmp_data = b'BM\x36\x04\x00\x00\x00\x00\x00\x00\x36\x00\x00\x00\x28\x00\x00\x00'
    detected_type = detect_file_type_from_binary(bmp_data)
    assert detected_type == '.bmp' 