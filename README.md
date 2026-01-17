# Genomic Coordinate Liftover Utility

A robust Python utility to convert genomic coordinates between **GRCh37 (hg19)** and **GRCh38 (hg38)**. 

### 🌟 Key Features
- **Bidirectional Support:** Easily switch builds via command-line arguments.
- **Column Preservation:** Handles BED3, BED6, and custom clinical formats without losing metadata (gene names, scores).
- **Automated QC:** Segregates unmapped regions into a separate "leftover" file for manual review.
- **Reproducible Environment:** Includes Conda `environment.yml`.

### 🚀 Quick Start
1. **Create the environment:**
   ```bash
   conda env create -f environment.yml
   conda activate liftover-env
