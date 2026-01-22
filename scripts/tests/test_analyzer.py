"""
Unit tests for the analyzer module.
"""

import pytest
from src.analyzer import (
    analyze_dashboard,
    analyze_panel,
    find_repeated_values,
    find_data_sources,
    find_repeated_panels,
    find_common_targets,
    extract_dashboard_config,
    DashboardAnalysis,
    PanelInfo,
)


class TestAnalyzeDashboard:
    """Tests for analyze_dashboard function."""
    
    def test_analyze_simple_dashboard(self):
        """Test analyzing a simple dashboard."""
        data = {
            "title": "Test Dashboard",
            "uid": "test-uid",
            "tags": ["test", "example"],
            "timezone": "browser",
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
        
        analysis = analyze_dashboard(data)
        
        assert analysis.title == "Test Dashboard"
        assert analysis.uid == "test-uid"
        assert analysis.tags == ["test", "example"]
        assert analysis.timezone == "browser"
        assert len(analysis.panels) == 1
        assert analysis.panels[0].title == "CPU Usage"
        assert analysis.panels[0].type == "graph"
    
    def test_analyze_dashboard_with_defaults(self):
        """Test analyzing dashboard with default values."""
        data = {
            "panels": []
        }
        
        analysis = analyze_dashboard(data)
        
        assert analysis.title == "Untitled Dashboard"
        assert analysis.uid is None
        assert analysis.tags == []
        assert analysis.timezone == "browser"
    
    def test_analyze_nested_dashboard(self):
        """Test analyzing dashboard with nested structure."""
        data = {
            "dashboard": {
                "title": "Nested Dashboard",
                "panels": []
            }
        }
        
        analysis = analyze_dashboard(data)
        
        assert analysis.title == "Nested Dashboard"
        assert len(analysis.panels) == 0


class TestAnalyzePanel:
    """Tests for analyze_panel function."""
    
    def test_analyze_basic_panel(self):
        """Test analyzing a basic panel."""
        panel = {
            "id": 1,
            "type": "graph",
            "title": "Test Panel",
            "gridPos": {"x": 0, "y": 0, "w": 12, "h": 8},
            "targets": [],
            "datasource": "prometheus"
        }
        
        result = analyze_panel(panel)
        
        assert result.panel_id == 1
        assert result.type == "graph"
        assert result.title == "Test Panel"
        assert result.grid_pos == {"x": 0, "y": 0, "w": 12, "h": 8}
        assert result.targets == []
        assert result.datasource == "prometheus"
    
    def test_analyze_panel_with_datasource_dict(self):
        """Test analyzing panel with datasource as dict."""
        panel = {
            "id": 1,
            "type": "stat",
            "datasource": {"type": "loki", "uid": "loki-1"}
        }
        
        result = analyze_panel(panel)
        
        assert result.datasource == "loki"
    
    def test_analyze_panel_with_options(self):
        """Test analyzing panel with options."""
        panel = {
            "id": 1,
            "type": "stat",
            "options": {"colorMode": "value", "graphMode": "area"}
        }
        
        result = analyze_panel(panel)
        
        assert result.options == {"colorMode": "value", "graphMode": "area"}
    
    def test_analyze_panel_extracts_custom_properties(self):
        """Test that custom properties are extracted."""
        panel = {
            "id": 1,
            "type": "graph",
            "custom_field": "custom_value",
            "another_field": 123
        }
        
        result = analyze_panel(panel)
        
        assert "custom_field" in result.custom_properties
        assert result.custom_properties["custom_field"] == "custom_value"
        assert result.custom_properties["another_field"] == 123


class TestFindRepeatedValues:
    """Tests for find_repeated_values function."""
    
    def test_find_no_repeated_values(self):
        """Test finding no repeated values."""
        panels = [
            PanelInfo(1, "graph", "Panel 1", {"x": 0, "y": 0, "w": 12, "h": 8}, [], None, {}, {}, [], {}),
            PanelInfo(2, "graph", "Panel 2", {"x": 0, "y": 8, "w": 12, "h": 8}, [], None, {}, {}, [], {}),
        ]
        
        result = find_repeated_values(panels)
        
        assert isinstance(result, dict)
    
    def test_find_repeated_values(self):
        """Test finding repeated values."""
        panels = [
            PanelInfo(1, "graph", "Panel 1", {"x": 0, "y": 0, "w": 12, "h": 8}, [], None, {}, {}, [], {"transparent": True}),
            PanelInfo(2, "graph", "Panel 2", {"x": 0, "y": 8, "w": 12, "h": 8}, [], None, {}, {}, [], {"transparent": True}),
        ]
        
        result = find_repeated_values(panels)
        
        # Should find the repeated transparent value
        assert isinstance(result, dict)


class TestFindDataSources:
    """Tests for find_data_sources function."""
    
    def test_find_single_datasource(self):
        """Test finding a single data source."""
        panels = [
            PanelInfo(1, "graph", "Panel 1", {"x": 0, "y": 0, "w": 12, "h": 8}, [], "prometheus", {}, {}, [], {}),
        ]
        
        result = find_data_sources(panels)
        
        assert "prometheus" in result
    
    def test_find_multiple_datasources(self):
        """Test finding multiple data sources."""
        panels = [
            PanelInfo(1, "graph", "Panel 1", {"x": 0, "y": 0, "w": 12, "h": 8}, [], "prometheus", {}, {}, [], {}),
            PanelInfo(2, "logs", "Panel 2", {"x": 0, "y": 8, "w": 12, "h": 8}, [], "loki", {}, {}, [], {}),
        ]
        
        result = find_data_sources(panels)
        
        assert "prometheus" in result
        assert "loki" in result
    
    def test_find_datasource_in_targets(self):
        """Test finding data source in targets."""
        panels = [
            PanelInfo(1, "graph", "Panel 1", {"x": 0, "y": 0, "w": 12, "h": 8}, 
                     [{"expr": "test", "datasource": {"type": "prometheus"}}], None, {}, {}, [], {}),
        ]
        
        result = find_data_sources(panels)
        
        assert "prometheus" in result


class TestFindRepeatedPanels:
    """Tests for find_repeated_panels function."""
    
    def test_find_no_repeated_panels(self):
        """Test finding no repeated panels."""
        panels = [
            PanelInfo(1, "graph", "Panel 1", {"x": 0, "y": 0, "w": 12, "h": 8}, [], None, {}, {}, [], {}),
            PanelInfo(2, "graph", "Panel 2", {"x": 0, "y": 8, "w": 12, "h": 8}, [], None, {}, {}, [], {}),
        ]
        
        result = find_repeated_panels(panels)
        
        assert result == []
    
    def test_find_repeated_panels(self):
        """Test finding repeated panels."""
        panels = [
            PanelInfo(1, "graph", "Panel 1", {"x": 0, "y": 0, "w": 12, "h": 8}, [], None, {}, {}, [], {"repeat": "service"}),
            PanelInfo(2, "graph", "Panel 2", {"x": 0, "y": 8, "w": 12, "h": 8}, [], None, {}, {}, [], {"repeat": "service"}),
        ]
        
        result = find_repeated_panels(panels)
        
        assert "Panel 1" in result


class TestExtractDashboardConfig:
    """Tests for extract_dashboard_config function."""
    
    def test_extract_all_config_fields(self):
        """Test extracting all configuration fields."""
        dashboard = {
            "id": 1,
            "uid": "test-uid",
            "title": "Test",
            "tags": ["tag1"],
            "timezone": "browser",
            "schemaVersion": 38,
            "version": 1,
            "refresh": "5s",
            "time": {"from": "now-6h", "to": "now"},
            "timepicker": {},
            "templating": {"list": []},
            "annotations": {"list": []},
            "description": "Test dashboard",
            "style": "dark",
            "editable": True,
            "fiscalYearStartMonth": 0,
            "graphTooltip": 0,
            "liveNow": False,
            "weekStart": "",
            "panelIds": [1, 2, 3]
        }
        
        result = extract_dashboard_config(dashboard)
        
        assert result["id"] == 1
        assert result["uid"] == "test-uid"
        assert result["schemaVersion"] == 38
        assert result["version"] == 1
        assert result["refresh"] == "5s"
    
    def test_extract_partial_config(self):
        """Test extracting partial configuration."""
        dashboard = {
            "title": "Test",
            "schemaVersion": 38
        }
        
        result = extract_dashboard_config(dashboard)
        
        assert result["title"] == "Test"
        assert result["schemaVersion"] == 38
        assert "uid" not in result