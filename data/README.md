# Dataset Documentation & Source Guide

This folder contains the source document collection for the **RAG-Powered Document Assistant** (Domain: *University Computer Science Educational Documents*).

## Directory Structure

- `data/raw/`: Place original raw PDF documents here.
- `data/processed/`: Extracted text chunks, metadata json files, and preprocessed document representations.

## Included Course Documents

The dataset consists of comprehensive core Computer Science educational reference PDFs:

1. **`CS101_Operating_Systems_Guide.pdf`**:
   - Covers: Operating system kernels, process execution, thread synchronization, deadlocks, virtual memory management, page tables, and file systems.
2. **`CS102_Database_Management_Systems.pdf`**:
   - Covers: Relational model, SQL query execution, normalization (1NF, 2NF, 3NF, BCNF), ACID transaction properties, indexing structures (B-Trees, Hash indexes), and concurrency control.
3. **`CS103_Computer_Networks_Handout.pdf`**:
   - Covers: OSI 7-layer model, TCP/IP protocol suite, TCP 3-way handshake, IP routing algorithms, DNS resolution, HTTP/HTTPS protocols, and socket programming.
4. **`CS104_Software_Engineering_Principles.pdf`**:
   - Covers: Software development lifecycles (Agile, Waterfall), architectural styles (Microservices, Layered, Event-Driven), RESTful API design rules, CI/CD pipelines, and design patterns.

## Instructions for Adding New Documents

To add new PDF documents to the dataset:
1. Copy your `.pdf` files into `data/raw/`.
2. Run the RAG pipeline notebook (`notebooks/rag_pipeline.ipynb`) from top to bottom.
3. The notebook will automatically clean, chunk, embed, and update the ChromaDB vector store located at `backend/data/vector_store/`.
