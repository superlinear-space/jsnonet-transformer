"""
Unit tests for the parser module.
"""

import pytest
import json
from src.parser import (
    parse_json_string,
    parse_json,
    validate_grafana_dashboard,
    extract_dashboard_data,
    JSONParseError,
)


class TestParseJsonString:
    """Tests for parse_json_string function."""
    
    def test_parse_valid_json_object(self):
        """Test parsing a valid JSON object."""
        json_str = '{"name": "test", "value": 123}'
        result = parse_json_string(json_str)
        assert result == {"name": "test", "value": 123}
    
    def test_parse_valid_json_array(self):
        """Test parsing a valid JSON array."""
        json_str = '[1, 2, 3, "test"]'
        result = parse_json_string(json_str)
        assert result == [1, 2, 3, "test"]
    
    def test_parse_nested_json(self):
        """Test parsing nested JSON."""
        json_str = '{"outer": {"inner": [1, 2, 3]}}'
        result = parse_json_string(json_str)
        assert result == {"outer": {"inner": [1, 2, 3]}}
    
    def test_parse_invalid_json_raises_error(self):
        """Test that invalid JSON raises JSONParseError."""
        with pytest.raises(JSONParseError):
            parse_json_string('{invalid json}')
    
    def test_parse_empty_string_raises_error(self):
        """Test that empty string raises JSONParseError."""
        with pytest.raises(JSONParseError):
            parse_json_string('')
    
    def test_parse_special_characters(self):
        """Test parsing JSON with special characters."""
        json_str = '{"text": "Hello\\nWorld\\tTab"}'
        result = parse_json_string(json_str)
        assert result == {"text": "Hello\nWorld\tTab"}


class TestParseJson:
    """Tests for parse_json function."""
    
    def test_parse_existing_file(self, tmp_path):
        """Test parsing an existing JSON file."""
        file_path = tmp_path / "test.json"
        file_path.write_text('{"key": "value"}')
        
        result = parse_json(str(file_path))
        assert result.data == {"key": "value"}
        assert result.source == str(file_path)
        assert result.errors == []
    
    def test_parse_nonexistent_file(self):
        """Test parsing a nonexistent file returns error."""
        result = parse_json("/nonexistent/path.json")
        assert result.data == {}
        assert "File not found" in result.errors[0]
    
    def test_parse_invalid_json_file(self, tmp_path):
        """Test parsing an invalid JSON file."""
        file_path = tmp_path / "invalid.json"
        file_path.write_text('{invalid}')
        
        result = parse_json(str(file_path))
        assert result.data == {}
        assert len(result.errors) > 0


class TestValidateGrafanaDashboard:
    """Tests for validate_grafana_dashboard function."""
    
    def test_valid_dashboard_with_dashboard_key(self):
        """Test validating a dashboard with 'dashboard' key."""
        data = {
            "dashboard": {
                "panels": [
                    {"id": 1, "type": "graph", "title": "Test Panel"}
                ]
            }
        }
        errors = validate_grafana_dashboard(data)
        assert errors == []
    
    def test_valid_dashboard_with_panels_key(self):
        """Test validating a dashboard with 'panels' key."""
        data = {
            "panels": [
                {"id": 1, "type": "graph", "title": "Test Panel"}
            ]
        }
        errors = validate_grafana_dashboard(data)
        assert errors == []
    
    def test_invalid_not_dict(self):
        """Test that non-dict data is invalid."""
        data = "not a dict"
        errors = validate_grafana_dashboard(data)
        assert len(errors) > 0
        assert "not a dictionary" in errors[0]
    
    def test_invalid_missing_panels(self):
        """Test that missing panels is invalid."""
        data = {"title": "Test"}
        errors = validate_grafana_dashboard(data)
        assert len(errors) > 0
        assert "Missing 'dashboard' or 'panels' field" in errors[0]
    
    def test_invalid_panels_not_array(self):
        """Test that non-array panels is invalid."""
        data = {"dashboard": {"panels": "not an array"}}
        errors = validate_grafana_dashboard(data)
        assert len(errors) > 0
        assert "'panels' field is not an array" in errors[0]


class TestExtractDashboardData:
    """Tests for extract_dashboard_data function."""
    
    def test_extract_with_dashboard_key(self):
        """Test extracting data with 'dashboard' key."""
        data = {
            "dashboard": {
                "title": "Test Dashboard",
                "panels": []
            }
        }
        result = extract_dashboard_data(data)
        assert result == {"title": "Test Dashboard", "panels": []}
    
    def test_extract_with_panels_key(self):
        """Test extracting data with 'panels' key."""
        data = {
            "panels": [
                {"id": 1, "type": "graph"}
            ]
        }
        result = extract_dashboard_data(data)
        assert result == {"panels": [{"id": 1, "type": "graph"}]}
    
    def test_extract_nested_structure(self):
        """Test extracting from nested structure."""
        data = {
            "grafana": {
                "dashboard": {
                    "title": "Nested Dashboard"
                }
            }
        }
        result = extract_dashboard_data(data)
        assert result == {"title": "Nested Dashboard"}
    
    def test_extract_returns_as_is(self):
        """Test that unknown structures are returned as-is."""
        data = {"title": "Unknown Structure"}
        result = extract_dashboard_data(data)
        assert result == {"title": "Unknown Structure"}