# RAG Prototypes

This folder contains various prototypes and experiments related to the Retrieval-Augmented Generation (RAG) component of the Digital Undergraduate Tutor project.

## Overview

These prototypes demonstrate the evolution of our RAG implementation, from initial experiments to more refined models. They showcase different approaches to document extraction, embedding, and retrieval mechanisms.

## Contents

1. `initial_ocr_attempts/`: Early experiments with various OCR libraries
2. `pix2text_implementation/`: Successful implementation using Pix2Text
3. `embedding_experiments/`: Tests with different embedding models
4. `vector_db_prototypes/`: Experiments with ChromaDB and other vector databases
5. `rag_pipeline_v1/`: First complete RAG pipeline prototype
6. `rag_pipeline_v2/`: Improved RAG pipeline with copyright compliance
7. `phi_3_5_integration/`: Integration of Phi-3.5 mini model

## Key Features

- Document extraction from scanned PDFs with complex equations
- Efficient chunking and embedding of extracted text
- Vector database implementation for fast retrieval
- Dynamic prompt templates for copyright compliance
- Integration with Phi-3.5 mini language model

## Usage

Each subfolder contains its own README with specific instructions on how to run and test the prototype. Generally, you'll need to:

1. Install the required dependencies (listed in each subfolder's README)
2. Prepare the input data as specified
3. Run the main script for each prototype

## Note on Resources

Due to the computational requirements of these prototypes, especially for OCR and embedding processes, we recommend running them on a machine with GPU access. Some prototypes may require access to the vector database stored on Google Drive.

## Contributing

Feel free to explore these prototypes and suggest improvements. If you have ideas for optimization or new approaches, please open an issue or submit a pull request.

## License

[Insert appropriate license information here]
