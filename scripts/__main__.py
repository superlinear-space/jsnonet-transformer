#!/usr/bin/env python3
"""
Main entry point for the Grafana Dashboard JSON to Jsonnet Transformer.

This module can be run as a module: python3 -m scripts
Or directly: python3 scripts/__main__.py
"""

import sys
import argparse
from pathlib import Path

from .main import transform, transform_string, TransformOptions


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Transform Grafana dashboard JSON to Jsonnet"
    )
    
    parser.add_argument(
        "--input", "-i",
        help="Path to input JSON file"
    )
    parser.add_argument(
        "--output", "-o",
        help="Path to output Jsonnet file"
    )
    parser.add_argument(
        "--string", "-s",
        help="JSON string to transform (alternative to --input)"
    )
    parser.add_argument(
        "--no-comments",
        action="store_true",
        help="Don't add comments to output"
    )
    parser.add_argument(
        "--no-extract-repeated",
        action="store_true",
        help="Don't extract repeated values"
    )
    parser.add_argument(
        "--no-templates",
        action="store_true",
        help="Don't create panel templates"
    )
    parser.add_argument(
        "--indent-size",
        type=int,
        default=4,
        help="Spaces per indent level (default: 4)"
    )
    parser.add_argument(
        "--max-line-length",
        type=int,
        default=120,
        help="Maximum line length (default: 120)"
    )
    
    return parser.parse_args()


def main():
    """Main entry point."""
    args = parse_args()
    
    # Validate input
    if not args.input and not args.string:
        print("Error: Must specify --input or --string", file=sys.stderr)
        sys.exit(1)
    
    # Build options
    options = TransformOptions(
        extract_repeated=not args.no_extract_repeated,
        create_templates=not args.no_templates,
        add_comments=not args.no_comments,
        indent_size=args.indent_size,
        max_line_length=args.max_line_length,
        output_file=args.output,
        overwrite=True,
    )
    
    # Transform
    if args.string:
        result = transform_string(args.string, options)
    else:
        result = transform(args.input, options)
    
    # Handle errors
    if result.errors:
        print("Errors:", file=sys.stderr)
        for error in result.errors:
            print(f"  - {error}", file=sys.stderr)
    
    if result.warnings:
        print("Warnings:")
        for warning in result.warnings:
            print(f"  - {warning}")
    
    if not result.success:
        print("Transformation failed.", file=sys.stderr)
        sys.exit(1)
    
    # Output
    if args.output:
        print(f"Output written to: {args.output}")
    else:
        print(result.jsonnet_code)
    
    print(f"Patterns detected: {len(result.patterns)}")


if __name__ == "__main__":
    main()