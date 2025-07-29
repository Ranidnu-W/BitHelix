# DNA Python Cursor

A research-oriented Python project to simulate storing digital data in synthetic DNA sequences.

## Main Goals
- Accept various digital file types as input (.txt, .docx, .mp3)
- Convert input files to binary bitstreams
- Encode binary into base-4 (quaternary)
- Map base-4 digits to DNA bases (A, C, G, T)
- Apply Reed-Solomon error correction for redundancy
- Enforce biological constraints (GC content, homopolymers, motifs)
- Export DNA sequences as `.txt` or `.fasta` files

## Folder Structure
```
project_root/
├── encoder/
│   ├── base_mapping.py
│   ├── constraints.py
│   └── error_correction.py
├── decoder/
├── io/
│   ├── file_reader.py
│   └── file_writer.py
├── main.py
├── requirements.txt
├── README.md
└── tests/
    └── test_base_mapping.py
```

## Requirements
See `requirements.txt` for dependencies. 