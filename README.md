# 🧬 DNA Storage Application

A full-stack web application for encoding and decoding files to/from DNA sequences. This project combines a Python backend with DNA encoding/decoding algorithms and a modern React/Next.js frontend.

## 🌟 Features

### Backend (Python)
- **File Encoding**: Convert any file type to DNA sequences
- **File Decoding**: Reconstruct original files from DNA sequences
- **Error Correction**: Reed-Solomon error correction for data integrity
- **Constraint Checking**: GC content, homopolymer, and unstable motif analysis
- **File Type Detection**: Automatic detection of original file types
- **REST API**: FastAPI-based web API for frontend integration

### Frontend (React/Next.js)
- **Modern UI**: Beautiful, responsive interface with animations
- **File Upload**: Drag-and-drop file upload with progress indicators
- **Real-time Processing**: Live encoding/decoding with detailed results
- **Dual Mode**: Switch between encoding and decoding operations
- **Results Display**: Detailed analysis with DNA sequence visualization
- **Download Support**: Export DNA sequences and decoded files

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn

### Installation

1. **Clone and navigate to the project:**
   ```bash
   git clone <repository-url>
   cd DNA_Python_Cursor
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install frontend dependencies:**
   ```bash
   cd DNA-storage-frontend_MK1
   npm install
   cd ..
   ```

### Running the Application

#### Option 1: Automated Startup
```bash
python start_app.py
```

#### Option 2: Manual Startup

1. **Start the backend:**
   ```bash
   python api_server.py
   ```
   Backend will be available at: http://localhost:8000

2. **Start the frontend (in a new terminal):**
   ```bash
   cd DNA-storage-frontend_MK1
   npm run dev
   ```
   Frontend will be available at: http://localhost:3000

## 📁 Project Structure

```
DNA_Python_Cursor/
├── api_server.py              # FastAPI backend server
├── main.py                    # Original CLI interface
├── start_app.py              # Automated startup script
├── requirements.txt           # Python dependencies
├── README.md                 # This file
├── encoder/                  # DNA encoding modules
│   ├── base_mapping.py
│   ├── constraints.py
│   └── error_correction.py
├── decoder/                  # DNA decoding modules
├── dnaio/                    # File I/O modules
├── tests/                    # Test suite
├── test_files/               # Sample files for testing
├── output/                   # Generated files
├── temp/                     # Temporary files
└── DNA-storage-frontend_MK1/ # Frontend application
    ├── app/                  # Next.js app directory
    ├── components/           # React components
    ├── package.json          # Frontend dependencies
    └── ...
```

## 🔧 API Endpoints

### Encode File
- **POST** `/api/encode`
- **Parameters:**
  - `file`: File to encode
  - `nsym`: Error correction symbols (default: 10)
  - `motifs`: Unstable motifs to check (default: "ATATAT,CGCGCG")

### Decode File
- **POST** `/api/decode`
- **Parameters:**
  - `file`: FASTA file containing DNA sequence
  - `nsym`: Error correction symbols (default: 10)

### Download File
- **GET** `/api/download/{file_id}`

## 🧪 Usage Examples

### Using the Web Interface

1. **Encode a file:**
   - Open http://localhost:3000
   - Click "Encode to DNA"
   - Upload any supported file
   - View the generated DNA sequence and analysis

2. **Decode a file:**
   - Click "Decode from DNA"
   - Upload a FASTA file containing DNA sequence
   - Download the reconstructed original file

### Using the CLI (Original Interface)

```bash
# Encode a file
python main.py encode input.txt output.fasta

# Decode a file
python main.py decode input.fasta output.txt
```

## 🔬 Supported File Types

### Encoding (Input)
- Text files (.txt)
- Word documents (.docx)
- Audio files (.mp3)
- Images (.jpg, .png, .gif)
- PDFs (.pdf)
- Archives (.zip)
- And more...

### Decoding (Input)
- FASTA files (.fasta, .fa, .fas)

## 📊 Analysis Features

### DNA Sequence Analysis
- **GC Content**: Percentage of G+C bases
- **Homopolymer Detection**: Long runs of identical bases
- **Unstable Motif Detection**: Problematic sequence patterns
- **Sequence Length**: Total base pairs
- **File Size**: Original and encoded sizes

### Error Correction
- Reed-Solomon error correction
- Configurable correction symbols
- Data integrity validation

## 🛠️ Development

### Backend Development
```bash
# Run tests
pytest

# Format code
black .

# Lint code
flake8
```

### Frontend Development
```bash
cd DNA-storage-frontend_MK1

# Run in development mode
npm run dev

# Build for production
npm run build

# Lint code
npm run lint
```

## 🔍 API Documentation

When the backend is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🙏 Acknowledgments

- DNA encoding/decoding algorithms
- FastAPI for the backend API
- Next.js and React for the frontend
- Tailwind CSS for styling
- Framer Motion for animations 