"""
Integration tests for the transformation pipeline.
"""

import pytest
import tempfile
import os
from src.main import transform, transform_string, TransformOptions, TransformResult


class TestTransform:
    """Integration tests for transform function."""
    
    def test_transform_simple_dashboard(self, tmp_path):
        """Test transforming a simple dashboard."""
        input_data = {
            "dashboard": {
                "title": "Simple Dashboard",
                "uid": "simple-dashboard",
                "tags": ["test"],
                "timezone": "browser",
                "schemaVersion": 38,
                "panels": [
                    {
                        "id": 1,
                        "type": "graph",
                        "title": "CPU Usage",
                        "gridPos": {"x": 0, "y": 0, "w": 12, "h": 8},
                        "targets": [{"expr": "cpu_usage", "refId": "A"}],
                        "datasource": "prometheus"
                    }
                ]
            }
        }
        
        # Write input file
        input_file = tmp_path / "input.json"
        input_file.write_text(str(input_data))
        
        # Transform
        result = transform(str(input_file))
        
        assert result.success
        assert result.jsonnet_code
        assert "Simple Dashboard" in result.jsonnet_code
        assert "CPU Usage" in result.jsonnet_code
        assert result.errors == []
    
    def test_transform_with_multiple_panels(self, tmp_path):
        """Test transforming dashboard with multiple panels."""
        input_data = {
            "dashboard": {
                "title": "Multi Panel Dashboard",
                "panels": [
                    {"id": 1, "type": "graph", "title": "Panel 1", "gridPos": {"x": 0, "y": 0, "w": 12, "h": 8}, "targets": []},
                    {"id": 2, "type": "stat", "title": "Panel 2", "gridPos": {"x": 12, "y": 0, "w": 12, "h": 8}, "targets": []},
                    {"id": 3, "type": "table", "title": "Panel 3", "gridPos": {"x": 0, "y": 8, "w": 24, "h": 8}, "targets": []},
                ]
            }
        }
        
        input_file = tmp_path / "multi.json"
        input_file.write_text(str(input_data))
        
        result = transform(str(input_file))
        
        assert result.success
        assert "Multi Panel Dashboard" in result.jsonnet_code
        assert "Panel 1" in result.jsonnet_code
        assert "Panel 2" in result.jsonnet_code
        assert "Panel 3" in result.jsonnet_code
    
    def test_transform_with_output_file(self, tmp_path):
        """Test transforming with output file."""
        input_data = {"dashboard": {"title": "Output Test", "panels": []}}
        
        input_file = tmp_path / "input.json"
        input_file.write_text(str(input_data))
        
        output_file = tmp_path / "output.jsonnet"
        
        options = TransformOptions(output_file=str(output_file))
        result = transform(str(input_file), options)
        
        assert result.success
        assert result.output_file == str(output_file)
        assert output_file.exists()
        
        content = output_file.read_text()
        assert "Output Test" in content
    
    def test_transform_nonexistent_file(self):
        """Test transforming nonexistent file."""
        result = transform("/nonexistent/file.json")
        
        assert not result.success
        assert len(result.errors) > 0
        assert "File not found" in result.errors[0]
    
    def test_transform_invalid_json(self, tmp_path):
        """Test transforming invalid JSON."""
        input_file = tmp_path / "invalid.json"
        input_file.write_text("{invalid json}")
        
        result = transform(str(input_file))
        
        assert not result.success
        assert len(result.errors) > 0


class TestTransformString:
    """Integration tests for transform_string function."""
    
    def test_transform_json_string(self):
        """Test transforming a JSON string."""
        json_string = '{"dashboard": {"title": "String Test", "panels": []}}'
        
        result = transform_string(json_string)
        
        assert result.success
        assert "String Test" in result.jsonnet_code
        assert result.errors == []
    
    def test_transform_complex_dashboard(self):
        """Test transforming a complex dashboard."""
        json_string = '''
        {
            "dashboard": {
                "title": "Complex Dashboard",
                "uid": "complex-uid",
                "tags": ["kubernetes", "monitoring"],
                "timezone": "browser",
                "schemaVersion": 38,
                "panels": [
                    {
                        "id": 1,
                        "type": "timeseries",
                        "title": "CPU Metrics",
                        "gridPos": {"x": 0, "y": 0, "w": 12, "h": 8},
                        "targets": [
                            {"expr": "rate(cpu_usage[5m])", "legendFormat": "CPU", "refId": "A"}
                        ],
                        "datasource": "prometheus"
                    },
                    {
                        "id": 2,
                        "type": "stat",
                        "title": "Memory Usage",
                        "gridPos": {"x": 12, "y": 0, "w": 12, "h": 8},
                        "targets": [
                            {"expr": "memory_usage", "refId": "A"}
                        ],
                        "datasource": "prometheus"
                    }
                ]
            }
        }
        '''
        
        result = transform_string(json_string)
        
        assert result.success
        assert "Complex Dashboard" in result.jsonnet_code
        assert "CPU Metrics" in result.jsonnet_code
        assert "Memory Usage" in result.jsonnet_code
        assert "timeseries" in result.jsonnet_code
        assert "stat" in result.jsonnet_code
    
    def test_transform_with_options(self):
        """Test transforming with custom options."""
        json_string = '{"dashboard": {"title": "Options Test", "panels": []}}'
        
        options = TransformOptions(
            add_comments=False,
            extract_repeated=False,
            create_templates=False,
        )
        
        result = transform_string(json_string, options)
        
        assert result.success
        # Should not have comments
        assert "//" not in result.jsonnet_code
    
    def test_transform_invalid_json_string(self):
        """Test transforming invalid JSON string."""
        result = transform_string("{invalid}")
        
        assert not result.success
        assert len(result.errors) > 0


class TestTransformOptions:
    """Tests for TransformOptions."""
    
    def test_default_options(self):
        """Test default transform options."""
        options = TransformOptions()
        
        assert options.validate == True
        assert options.extract_repeated == True
        assert options.create_templates == True
        assert options.add_comments == True
        assert options.indent_size == 4
    
    def test_custom_options(self):
        """Test custom transform options."""
        options = TransformOptions(
            validate=False,
            extract_repeated=False,
            create_templates=False,
            add_comments=False,
            indent_size=2,
            min_pattern_occurrences=3,
        )
        
        assert options.validate == False
        assert options.extract_repeated == False
        assert options.create_templates == False
        assert options.add_comments == False
        assert options.indent_size == 2
        assert options.min_pattern_occurrences == 3


class TestTransformResult:
    """Tests for TransformResult."""
    
    def test_successful_result(self):
        """Test creating a successful result."""
        result = TransformResult(
            success=True,
            jsonnet_code="{}",
            analysis=None,
            patterns=[],
            errors=[],
            warnings=[],
        )
        
        assert result.success
        assert result.jsonnet_code == "{}"
        assert result.errors == []
        assert result.warnings == []
    
    def test_error_result(self):
        """Test creating an error result."""
        result = TransformResult(
            success=False,
            jsonnet_code="",
            analysis=None,
            patterns=[],
            errors=["Error 1", "Error 2"],
            warnings=[],
        )
        
        assert not result.success
        assert result.jsonnet_code == ""
        assert len(result.errors) == 2