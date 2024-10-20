# OCR Experiments

This folder contains various experiments and implementations related to Optical Character Recognition (OCR) for the Digital Undergraduate Tutor project.

## Overview

These experiments showcase our journey in finding the most effective OCR solution for extracting complex chemical engineering content from scanned PDFs. The focus was on accurately capturing text, equations, and tables while maintaining formatting.

## Contents

1. `pytesseract_attempts/`: Initial experiments with Pytesseract
2. `pymupdf_experiments/`: Trials using PyMuPDF for PDF processing
3. `llama_index_ocr/`: Implementation and results using Llama Index OCR
4. `pix2text_implementation/`: Our most successful implementation using Pix2Text
5. `comparison_results/`: Comparative analysis of different OCR methods

## Key Features

- Handling of complex chemical equations and symbols
- Table recognition and extraction
- Markdown formatting preservation
- Metadata extraction (e.g., page numbers)
- Performance benchmarks for different OCR methods

## Llama Index OCR

The `llama_index_ocr/` folder contains our experiments with Llama Index's OCR capabilities. While this method showed promise in handling structured documents, it faced challenges with our specific use case.

### Key Findings:
- Strengths in processing well-structured documents
- Challenges in accurately capturing complex equations
- Integration complexities with our existing pipeline

## Pix2Text Implementation

The `pix2text_implementation/` folder showcases our most successful OCR approach using Pix2Text.

### Key Achievements:
- High accuracy in extracting text, equations, and tables
- Effective handling of LaTeX-style mathematical notations
- Efficient processing of large documents
- Seamless integration with our document object creation pipeline

## Usage

Each subfolder contains its own README with specific instructions on how to run and test the OCR implementations. Generally, you'll need to:

1. Install the required dependencies (listed in each subfolder's README)
2. Prepare sample PDF documents for testing
3. Run the main script for each OCR method
4. Compare the outputs using the scripts in the `comparison_results/` folder

## Note on Resources

OCR processes, especially for large documents with complex content, can be computationally intensive. We recommend running these experiments on a machine with sufficient RAM and, ideally, GPU acceleration for optimal performance.

## Contributing

We welcome contributions to improve our OCR implementations. If you have suggestions for optimization or new approaches, please open an issue or submit a pull request.

## License

[Insert appropriate license information here]
