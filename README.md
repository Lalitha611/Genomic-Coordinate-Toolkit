# 🧬 Genomic Coordinate Liftover Utility

A robust Python utility to convert genomic coordinates between **GRCh37 (hg19)** and **GRCh38 (hg38)**.  

## 🌟 Key Features
- **Bidirectional Support:** Easily switch builds via command-line arguments.  
- **Column Preservation:** Handles BED3, BED6, and custom clinical formats without losing metadata (gene names, scores).  
- **Automated QC:** Segregates unmapped regions into a separate "leftover" file for manual review.  
- **Reproducible Environment:** Includes Conda `environment.yml` for consistent results.  

## 🚀 Quick Start

### 1️⃣ Create the environment
```bash
conda env create -f environment.yml
conda activate liftover-env
```

### 2️⃣ Run conversion

**Scenario A: hg19 → hg38**  
*Use case:* Convert ancient DNA variants (hg19) to compare with modern hg38 cohorts.  
```bash
python liftover_tool.py -d hg19tohg38 -i ancient_hg19.bed -o ancient_hg38.bed
```

**Scenario B: hg38 → hg19**  
*Use case:* Map modern clinical mutations (hg38) to older hg19 databases.  
```bash
python liftover_tool.py -d hg38tohg19 -i clinical_hg38.bed -o clinical_hg19.bed
```

## 🛠 Workflow & Usage

This toolkit is designed as a **two-step pipeline**:

### Step 1: Standardize Messy Input
Before liftover, use `prepare_bed.py` to convert human-readable text into a standardized **0-based BED file**.  
Supports formats like:  
- `chr6:160585140`  
- `6 160585140`  
- `chrX-155000-156000`  

```bash
python prepare_bed.py -i input.txt -o standardized.bed
```

### Step 2: Perform Bidirectional Liftover

- **Scenario A: hg19 → hg38**  
```bash
python liftover_tool.py -d hg19tohg38 -i ancient_hg19.bed -o ancient_hg38.bed
```

- **Scenario B: hg38 → hg19**  
```bash
python liftover_tool.py -d hg38tohg19 -i clinical_hg38.bed -o clinical_hg19.bed
```

## 📂 Example Transformation

**1️⃣ Messy Input (`input.txt`)**
```
chr6:160585140
6 160585140
chr17-41196312-41277500
```

**2️⃣ Standardized BED (`standardized.bed`)**  
*Automatically converts to 0-based start coordinates.*
```
chr6    160585139    160585140    chr6:160585140
chr6    160585139    160585140    6 160585140
chr17   41196311     41277500     chr17-41196312-41277500
```

**3️⃣ Final Lifted Output (`hg38_output.bed`)**  
*Coordinates converted to GRCh38 while preserving the original labels.*  
```
chr6    161112345    161112346    chr6:160585140
chr6    161112345    161112346    6 160585140
chr17   41234567     41315755     chr17-41196312-41277500
```
