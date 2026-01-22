"""
JSON Parser Module

Provides functionality for parsing and validating JSON files.
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional
from dataclasses import dataclass


@dataclass
class ParseResult:
    """Result of parsing a JSON file."""
    data: Dict[str, Any]
    source: str
    errors: list[str]


class JSONParseError(Exception):
    """Exception raised when JSON parsing fails."""
    pass


def parse_json_string(json_string: str) -> Dict[str, Any]:
    """
    Parse a JSON string into a Python dictionary.
    
    Args:
        json_string: The JSON string to parse.
        
    Returns:
        A dictionary representing the parsed JSON.
        
    Raises:
        JSONParseError: If the JSON is invalid.
    """
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        raise JSONParseError(f"Invalid JSON: {e}")


def parse_json(file_path: str) -> ParseResult:
    """
    Parse a JSON file into a Python dictionary.
    
    Args:
        file_path: Path to the JSON file.
        
    Returns:
        A ParseResult containing the parsed data, source path, and any errors.
    """
    path = Path(file_path)
    errors = []
    
    if not path.exists():
        errors.append(f"File not found: {file_path}")
        return ParseResult(data={}, source=str(path), errors=errors)
    
    if not path.suffix.lower() == '.json':
        errors.append(f"Warning: File extension is not .json: {file_path}")
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            data = parse_json_string(content)
            return ParseResult(data=data, source=str(path), errors=errors)
    except JSONParseError as e:
        errors.append(str(e))
        return ParseResult(data={}, source=str(path), errors=errors)
    except IOError as e:
        errors.append(f"IO error reading file: {e}")
        return ParseResult(data={}, source=str(path), errors=errors)


def validate_grafana_dashboard(data: Dict[str, Any]) -> list[str]:
    """
    Validate that the parsed JSON is a valid Grafana dashboard.
    
    Args:
        data: The parsed JSON data.
        
    Returns:
        A list of validation errors (empty if valid).
    """
    errors = []
    
    if not isinstance(data, dict):
        errors.append("Data is not a dictionary")
        return errors
    
    # Check for required fields
    if 'dashboard' not in data and 'panels' not in data:
        errors.append("Missing 'dashboard' or 'panels' field")
    
    # Check dashboard structure
    if 'dashboard' in data:
        dashboard = data['dashboard']
        if not isinstance(dashboard, dict):
            errors.append("'dashboard' field is not an object")
        else:
            if 'panels' in dashboard:
                panels = dashboard['panels']
                if not isinstance(panels, list):
                    errors.append("'panels' field is not an array")
    
    return errors


def extract_dashboard_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract the dashboard data from various possible structures.
    
    Args:
        data: The parsed JSON data.
        
    Returns:
        The dashboard data dictionary.
    """
    # Handle direct dashboard structure
    if 'dashboard' in data:
        return data['dashboard']
    
    # Handle direct panels structure
    if 'panels' in data:
        return data
    
    # Handle nested structure
    for key in ['grafana', 'spec', 'resource']:
        if key in data and isinstance(data[key], dict):
            if 'dashboard' in data[key]:
                return data[key]['dashboard']
            if 'panels' in data[key]:
                return data[key]
    
    # Return as-is if it looks like a dashboard
    return data