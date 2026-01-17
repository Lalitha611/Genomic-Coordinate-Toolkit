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
   
2. **Run conversion:**
   - **Scenario A:**  hg19 → hg38\
      Use case: Convert ancient DNA variants (hg19) to compare with modern hg38 cohorts. \
   ```python liftover_tool.py -d hg19tohg38 -i ancient_hg19.bed -o ancient_hg38.bed```

   - **Scenario B:** hg38 → hg19 \
      Use case: Map modern clinical mutations (hg38) to older hg19 databases.\
   ```python liftover_tool.py -d hg38tohg19 -i clinical_hg38.bed -o clinical_hg19.bed```
