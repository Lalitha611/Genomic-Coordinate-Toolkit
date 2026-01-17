#!/usr/bin/env python3
import argparse
import pandas as pd
from pyliftover import LiftOver
import sys
import os

def run_liftover(direction, input_file, output_file, unmapped_file):
    # Dictionary defining the builds for bidirectional support
    build_map = {
        "hg19tohg38": ('hg19', 'hg38'),
        "hg38tohg19": ('hg38', 'hg19')
    }
    
    source_build, target_build = build_map[direction]
    
    # Initialize LiftOver (automatically downloads chain files if missing)
    lo = LiftOver(source_build, target_build)
    
    # Load input data
    try:
        # Read file, handling potential headers or comments
        df = pd.read_csv(input_file, sep=r'\s+', header=None, comment='#')
    except Exception as e:
        print(f"❌ Error: Could not read input file. {e}")
        return

    converted = []
    unmapped = []

    print(f"🔄 Direction: {source_build} ➜ {target_build}")

    for _, row in df.iterrows():
        # BED format: Chrom, Start, End + anything else
        chrom = str(row[0])
        start = int(row[1])
        end = int(row[2])
        metadata = row[3:].tolist() # Preserve extra info (Gene names, IDs)

        # Standards Check: Liftover requires 'chr' prefix
        search_chrom = chrom if chrom.startswith('chr') else f'chr{chrom}'

        # Convert Start and End
        res_start = lo.convert_coordinate(search_chrom, start)
        res_end = lo.convert_coordinate(search_chrom, end)

        if res_start and res_end:
            # Successfully mapped to target build
            new_chrom = res_start[0][0]
            new_start = res_start[0][1]
            new_end = res_end[0][1]
            converted.append([new_chrom, new_start, new_end] + metadata)
        else:
            # Could not map (deleted or significantly changed region)
            unmapped.append(row.tolist())

    # Save outputs
    pd.DataFrame(converted).to_csv(output_file, sep='\t', index=False, header=False)
    
    if unmapped:
        pd.DataFrame(unmapped).to_csv(unmapped_file, sep='\t', index=False, header=False)
        print(f"⚠️  Mapping incomplete: {len(unmapped)} regions saved to {unmapped_file}")

    print(f"✅ Conversion complete: {len(converted)} regions saved to {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Bidirectional Genomic Liftover (hg19 <-> hg38)")
    parser.add_argument("-d", "--direction", choices=["hg19tohg38", "hg38tohg19"], required=True, 
                        help="Direction of conversion (e.g., hg19tohg38 or hg38tohg19)")
    parser.add_argument("-i", "--input", required=True, help="Input file (BED or TXT)")
    parser.add_argument("-o", "--output", required=True, help="Output file name")
    parser.add_argument("-u", "--unmapped", default="failed_mapping.txt", help="Log for unmapped regions")
    
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)
        
    args = parser.parse_args()
    run_liftover(args.direction, args.input, args.output, args.unmapped)
