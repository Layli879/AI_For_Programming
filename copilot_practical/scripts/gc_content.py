"""Calculate GC content for each record in a FASTA file."""

import argparse
import sys


def read_fasta(path):
    """Yield (header, sequence) pairs from a FASTA file."""
    header = None
    sequence = []

    with open(path, encoding="utf-8") as fasta:
        for line in fasta:
            line = line.strip()
            if line.startswith(">"):
                if header is not None:
                    yield header, "".join(sequence)
                header = line[1:]
                sequence = []
            elif header is not None:
                sequence.append(line)

    if header is not None:
        yield header, "".join(sequence)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("fasta", help="path to a FASTA file")
    parser.add_argument(
        "--min-gc",
        type=float,
        help="only print records with GC content above this percentage",
    )
    args = parser.parse_args()

    for header, sequence in read_fasta(args.fasta):
        if not sequence:
            print(f"Warning: skipping empty sequence for {header!r}", file=sys.stderr)
            continue
        sequence = sequence.upper()
        gc_percent = (sequence.count("G") + sequence.count("C")) / len(sequence) * 100
        if args.min_gc is None or gc_percent > args.min_gc:
            print(f"{header}\t{gc_percent:.2f}%")


if __name__ == "__main__":
    main()
