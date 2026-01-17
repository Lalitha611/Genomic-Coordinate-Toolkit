#!/usr/bin/env python3
import re
import sys
import argparse

def parse_line(line):
    """
    Extracts Chrom, Start, End from messy strings.
    Handles: chr6:160, 6 160, chr6-160, chr6:160-170, etc.
    """
    line = line.strip()
    if not line: return None

    # Regex to find: (Chromosome) (Separator) (Start) (Optional Separator) (Optional End)
    # This covers chr6:160585140, chr6-160585140, 6 160585140, etc.
    match = re.search(r'(?:chr)?(\d+|X|Y|M|MT)[\s:\-._]+(\d+)(?:[\s:\-._]+(\d+))?', line, re.IGNORECASE)
    
    if match:
        chrom = f"chr{match.group(1).upper()}"
        pos1 = int(match.group(2))
        pos2 = int(match.group(3)) if match.group(3) else pos1
        
        # BED conversion logic:
        # Text coordinates are usually 1-based. BED is 0-based.
        # Single point P becomes: [P-1, P]
        # Interval S-E becomes: [S-1, E]
        start = pos1 - 1
        end = pos2
        
        return [chrom, start, end, line] # Keep original line as metadata
    return None

def main(input_file, output_file):
    print(f"🧹 Standardizing formats in {input_file}...")
    count = 0
    
    with open(input_file, 'r') as f_in, open(output_file, 'w') as f_out:
        for line in f_in:
            result = parse_line(line)
            if result:
                f_out.write(f"{result[0]}\t{result[1]}\t{result[2]}\t{result[3]}\n")
                count += 1
    
    print(f"✅ Created {output_file} with {count} BED regions.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert messy coordinates to BED format")
    parser.add_argument("-i", "--input", required=True, help="Input text file")
    parser.add_argument("-o", "--output", default="prepared.bed", help="Output BED file")
    args = parser.parse_args()
    main(args.input, args.output)
