"""
Grafana Dashboard JSON to Jsonnet Transformer

A skill that transforms Grafana dashboard JSON files into well-structured Jsonnet programs.
"""

__version__ = "1.0.0"
__author__ = "Kilo Code"

from .main import transform, transform_string, TransformOptions
from .parser import parse_json, parse_json_string
from .analyzer import analyze_dashboard
from .generator import JsonnetGenerator
from .patterns import PatternDetector

__all__ = [
    "transform",
    "transform_string",
    "TransformOptions",
    "parse_json",
    "parse_json_string",
    "analyze_dashboard",
    "JsonnetGenerator",
    "PatternDetector",
]