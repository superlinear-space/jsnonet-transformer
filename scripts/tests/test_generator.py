"""
Unit tests for the generator module.
"""

import pytest
from src.generator import JsonnetGenerator, GeneratorOptions
from src.analyzer import DashboardAnalysis, PanelInfo


class TestJsonnetGenerator:
    """Tests for JsonnetGenerator class."""
    
    def test_generate_basic_dashboard(self):
        """Test generating a basic dashboard."""
        analysis = DashboardAnalysis(
            title="Test Dashboard",
            uid="test-uid",
            tags=["test"],
            timezone="browser",
            panels=[
                PanelInfo(1, "graph", "CPU Usage", {"x": 0, "y": 0, "w": 12, "h": 8}, [], "prometheus", {}, {}, [])
            ],
            repeated_panels=[],
            repeated_values={},
            data_sources={"prometheus"},
            panel_types={"graph": 1},
            common_targets=[],
            dashboard_config={"schemaVersion": 38}
        )
        
        generator = JsonnetGenerator()
        result = generator.generate(analysis)
        
        assert "Test Dashboard" in result
        assert "test-uid" in result
        assert "CPU Usage" in result
        assert "graph" in result
    
    def test_generate_with_colors(self):
        """Test generating dashboard with color extraction."""
        analysis = DashboardAnalysis(
            title="Color Dashboard",
            uid=None,
            tags=[],
            timezone="browser",
            panels=[
                PanelInfo(1, "graph", "Panel 1", {"x": 0, "y": 0, "w": 12, "h": 8}, [], None, {}, {}, [], {"colors": ["#5794f2", "#b877d9"]})
            ],
            repeated_panels=[],
            repeated_values={},
            data_sources=set(),
            panel_types={"graph": 1},
            common_targets=[],
            dashboard_config={"schemaVersion": 38}
        )
        
        generator = JsonnetGenerator()
        result = generator.generate(analysis)
        
        assert "local colors" in result or "colors" in result
    
    def test_generate_with_templates(self):
        """Test generating dashboard with panel templates."""
        analysis = DashboardAnalysis(
            title="Template Dashboard",
            uid=None,
            tags=[],
            timezone="browser",
            panels=[
                PanelInfo(1, "graph", "Graph Panel", {"x": 0, "y": 0, "w": 12, "h": 8}, [], None, {}, {}, []),
                PanelInfo(2, "graph", "Another Graph", {"x": 0, "y": 8, "w": 12, "h": 8}, [], None, {}, {}, []),
            ],
            repeated_panels=[],
            repeated_values={},
            data_sources=set(),
            panel_types={"graph": 2},
            common_targets=[],
            dashboard_config={"schemaVersion": 38}
        )
        
        generator = JsonnetGenerator(GeneratorOptions(create_templates=True))
        result = generator.generate(analysis)
        
        assert "graphPanel" in result or "local graph" in result
    
    def test_generate_without_comments(self):
        """Test generating dashboard without comments."""
        analysis = DashboardAnalysis(
            title="No Comments",
            uid=None,
            tags=[],
            timezone="browser",
            panels=[],
            repeated_panels=[],
            repeated_values={},
            data_sources=set(),
            panel_types={},
            common_targets=[],
            dashboard_config={"schemaVersion": 38}
        )
        
        generator = JsonnetGenerator(GeneratorOptions(add_comments=False))
        result = generator.generate(analysis)
        
        assert "//" not in result
    
    def test_generate_with_different_indent(self):
        """Test generating dashboard with different indent size."""
        analysis = DashboardAnalysis(
            title="Indent Test",
            uid=None,
            tags=[],
            timezone="browser",
            panels=[],
            repeated_panels=[],
            repeated_values={},
            data_sources=set(),
            panel_types={},
            common_targets=[],
            dashboard_config={"schemaVersion": 38}
        )
        
        generator = JsonnetGenerator(GeneratorOptions(indent_size=2))
        result = generator.generate(analysis)
        
        # Check that 2 spaces are used for indentation
        lines = result.split('\n')
        for line in lines:
            if line.strip() and not line.strip().startswith('//'):
                # Count leading spaces should be multiple of 2
                leading_spaces = len(line) - len(line.lstrip())
                assert leading_spaces % 2 == 0


class TestFormatValue:
    """Tests for _format_value method."""
    
    def test_format_none(self):
        """Test formatting None value."""
        generator = JsonnetGenerator()
        result = generator._format_value(None)
        assert result == "null"
    
    def test_format_bool(self):
        """Test formatting boolean values."""
        generator = JsonnetGenerator()
        assert generator._format_value(True) == "true"
        assert generator._format_value(False) == "false"
    
    def test_format_string(self):
        """Test formatting string values."""
        generator = JsonnetGenerator()
        assert generator._format_value("hello") == '"hello"'
        assert generator._format_value("hello world") == '"hello world"'
    
    def test_format_string_with_quotes(self):
        """Test formatting string with quotes."""
        generator = JsonnetGenerator()
        result = generator._format_value('say "hello"')
        assert '\\"' in result
    
    def test_format_number(self):
        """Test formatting numbers."""
        generator = JsonnetGenerator()
        assert generator._format_value(42) == "42"
        assert generator._format_value(3.14) == "3.14"
    
    def test_format_list(self):
        """Test formatting lists."""
        generator = JsonnetGenerator()
        result = generator._format_value([1, 2, 3])
        assert result == "[1, 2, 3]"
    
    def test_format_dict(self):
        """Test formatting dictionaries."""
        generator = JsonnetGenerator()
        result = generator._format_value({"key": "value"})
        assert "key" in result
        assert "value" in result


class TestGetPanelDefaults:
    """Tests for _get_panel_defaults method."""
    
    def test_graph_defaults(self):
        """Test getting graph panel defaults."""
        generator = JsonnetGenerator()
        defaults = generator._get_panel_defaults("graph")
        
        assert defaults["lines"] == True
        assert defaults["fill"] == 1
        assert "legend" in defaults
        assert "tooltip" in defaults
    
    def test_timeseries_defaults(self):
        """Test getting timeseries panel defaults."""
        generator = JsonnetGenerator()
        defaults = generator._get_panel_defaults("timeseries")
        
        assert defaults["transparent"] == False
        assert defaults["fillOpacity"] == 80
    
    def test_stat_defaults(self):
        """Test getting stat panel defaults."""
        generator = JsonnetGenerator()
        defaults = generator._get_panel_defaults("stat")
        
        assert defaults["colorMode"] == "value"
        assert defaults["graphMode"] == "area"
    
    def test_unknown_panel_defaults(self):
        """Test getting defaults for unknown panel type."""
        generator = JsonnetGenerator()
        defaults = generator._get_panel_defaults("unknown")
        
        assert defaults["transparent"] == False
        assert "gridPos" in defaults


class TestGetTemplateName:
    """Tests for _get_template_name method."""
    
    def test_simple_panel_type(self):
        """Test getting template name for simple panel type."""
        generator = JsonnetGenerator()
        assert generator._get_template_name("graph") == "graphPanel"
    
    def test_hyphenated_panel_type(self):
        """Test getting template name for hyphenated panel type."""
        generator = JsonnetGenerator()
        assert generator._get_template_name("pie-chart") == "pie_chartPanel"
    
    def test_spaced_panel_type(self):
        """Test getting template name for spaced panel type."""
        generator = JsonnetGenerator()
        assert generator._get_template_name("grafana clock") == "grafana_clockPanel"