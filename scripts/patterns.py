"""
Pattern Detection Module

Detects common patterns in Grafana dashboards for extraction and templating.
"""

from typing import Any, Dict, List, Set, Tuple, Optional
from dataclasses import dataclass
from collections import Counter, defaultdict


@dataclass
class PatternMatch:
    """A detected pattern match."""
    pattern_type: str
    value: Any
    occurrences: int
    path: str
    suggestion: str


class PatternDetector:
    """
    Detects common patterns in Grafana dashboards.
    """
    
    # Threshold for considering a value as "repeated"
    REPEAT_THRESHOLD = 2
    
    # Common panel types
    PANEL_TYPES = [
        'timeseries', 'timeseries', 'graph', 'stat', 'gauge', 'bargauge',
        'table', 'table-old', 'heatmap', 'worldmap', 'piechart', 'grafana-clock-panel',
        'pluginlist', 'news', 'logs', 'traces', 'flamegraph', 'histogram',
        'candlestick', 'status-history', 'canvas', 'geomap', 'xychart'
    ]
    
    # Common color schemes
    COLOR_SCHEMES = [
        {'name': 'Green', 'colors': ['#73bf69', '#73bf69', '#73bf69']},
        {'name': 'Blue', 'colors': ['#5794f2', '#5794f2', '#5794f2']},
        {'name': 'Red', 'colors': ['#f2495c', '#f2495c', '#f2495c']},
        {'name': 'Orange', 'colors': ['#ff780a', '#ff780a', '#ff780a']},
    ]
    
    def __init__(self, min_occurrences: int = 2):
        """
        Initialize the pattern detector.
        
        Args:
            min_occurrences: Minimum occurrences to consider a pattern.
        """
        self.min_occurrences = min_occurrences
        self.matches: List[PatternMatch] = []
    
    def detect(self, data: Dict[str, Any]) -> List[PatternMatch]:
        """
        Detect patterns in dashboard data.
        
        Args:
            data: The dashboard JSON data.
            
        Returns:
            A list of detected pattern matches.
        """
        self.matches = []
        dashboard = data.get('dashboard', data)
        panels = dashboard.get('panels', [])
        
        # Detect various patterns
        self._detect_color_patterns(panels)
        self._detect_threshold_patterns(panels)
        self._detect_legend_patterns(panels)
        self._detect_axis_patterns(panels)
        self._detect_tooltip_patterns(panels)
        self._detect_grid_patterns(panels)
        self._detect_datasource_patterns(panels)
        self._detect_panel_type_patterns(panels)
        
        return self.matches
    
    def _detect_color_patterns(self, panels: List[Dict[str, Any]]) -> None:
        """Detect repeated color configurations."""
        color_values = []
        for panel in panels:
            colors = panel.get('colors', [])
            if colors:
                color_values.append(tuple(colors))
        
        # Count occurrences
        color_counts = Counter(color_values)
        for colors, count in color_counts.items():
            if count >= self.min_occurrences:
                self.matches.append(PatternMatch(
                    pattern_type='colors',
                    value=list(colors),
                    occurrences=count,
                    path='panels[].colors',
                    suggestion=f'Extract to local variable: local colors = {list(colors)}'
                ))
    
    def _detect_threshold_patterns(self, panels: List[Dict[str, Any]]) -> None:
        """Detect repeated threshold configurations."""
        threshold_values = []
        for panel in panels:
            thresholds = panel.get('thresholds')
            if thresholds:
                threshold_values.append(json.dumps(thresholds, sort_keys=True))
        
        threshold_counts = Counter(threshold_values)
        for thresh_json, count in threshold_counts.items():
            if count >= self.min_occurrences:
                thresh = json.loads(thresh_json)
                self.matches.append(PatternMatch(
                    pattern_type='thresholds',
                    value=thresh,
                    occurrences=count,
                    path='panels[].thresholds',
                    suggestion='Extract to local variable for consistent threshold styling'
                ))
    
    def _detect_legend_patterns(self, panels: List[Dict[str, Any]]) -> None:
        """Detect repeated legend configurations."""
        legend_values = []
        for panel in panels:
            legend = panel.get('legend')
            if legend and isinstance(legend, dict):
                legend_values.append(json.dumps(legend, sort_keys=True))
        
        legend_counts = Counter(legend_values)
        for legend_json, count in legend_counts.items():
            if count >= self.min_occurrences:
                legend = json.loads(legend_json)
                self.matches.append(PatternMatch(
                    pattern_type='legend',
                    value=legend,
                    occurrences=count,
                    path='panels[].legend',
                    suggestion='Extract to local variable for consistent legend configuration'
                ))
    
    def _detect_axis_patterns(self, panels: List[Dict[str, Any]]) -> None:
        """Detect repeated axis configurations."""
        axis_values = []
        for panel in panels:
            xaxis = panel.get('xaxis')
            yaxes = panel.get('yaxes')
            if xaxis:
                axis_values.append(('xaxis', json.dumps(xaxis, sort_keys=True)))
            if yaxes:
                axis_values.append(('yaxes', json.dumps(yaxes, sort_keys=True)))
        
        axis_counts = Counter(axis_values)
        for (axis_type, axis_json), count in axis_counts.items():
            if count >= self.min_occurrences:
                axis = json.loads(axis_json)
                self.matches.append(PatternMatch(
                    pattern_type='axis',
                    value=axis,
                    occurrences=count,
                    path=f'panels[].{axis_type}',
                    suggestion=f'Extract {axis_type} configuration to local variable'
                ))
    
    def _detect_tooltip_patterns(self, panels: List[Dict[str, Any]]) -> None:
        """Detect repeated tooltip configurations."""
        tooltip_values = []
        for panel in panels:
            tooltip = panel.get('tooltip')
            if tooltip:
                tooltip_values.append(json.dumps(tooltip, sort_keys=True))
        
        tooltip_counts = Counter(tooltip_values)
        for tooltip_json, count in tooltip_counts.items():
            if count >= self.min_occurrences:
                tooltip = json.loads(tooltip_json)
                self.matches.append(PatternMatch(
                    pattern_type='tooltip',
                    value=tooltip,
                    occurrences=count,
                    path='panels[].tooltip',
                    suggestion='Extract tooltip configuration to local variable'
                ))
    
    def _detect_grid_patterns(self, panels: List[Dict[str, Any]]) -> None:
        """Detect repeated grid configurations."""
        grid_values = []
        for panel in panels:
            grid = panel.get('grid')
            if grid:
                grid_values.append(json.dumps(grid, sort_keys=True))
        
        grid_counts = Counter(grid_values)
        for grid_json, count in grid_counts.items():
            if count >= self.min_occurrences:
                grid = json.loads(grid_json)
                self.matches.append(PatternMatch(
                    pattern_type='grid',
                    value=grid,
                    occurrences=count,
                    path='panels[].grid',
                    suggestion='Extract grid configuration to local variable'
                ))
    
    def _detect_datasource_patterns(self, panels: List[Dict[str, Any]]) -> None:
        """Detect data source usage patterns."""
        datasource_usage = defaultdict(list)
        for i, panel in enumerate(panels):
            ds = panel.get('datasource')
            if ds:
                if isinstance(ds, dict):
                    ds = ds.get('type', ds.get('uid', 'unknown'))
                datasource_usage[ds].append(i)
        
        for ds, indices in datasource_usage.items():
            if len(indices) >= self.min_occurrences:
                self.matches.append(PatternMatch(
                    pattern_type='datasource',
                    value=ds,
                    occurrences=len(indices),
                    path='panels[].datasource',
                    suggestion=f'Extract {ds} to datasources local variable'
                ))
    
    def _detect_panel_type_patterns(self, panels: List[Dict[str, Any]]) -> None:
        """Detect panel type usage patterns."""
        panel_types = [p.get('type', 'unknown') for p in panels]
        type_counts = Counter(panel_types)
        
        for panel_type, count in type_counts.items():
            if count >= self.min_occurrences:
                self.matches.append(PatternMatch(
                    pattern_type='panel_type',
                    value=panel_type,
                    occurrences=count,
                    path='panels[].type',
                    suggestion=f'Create template function for {panel_type} panels'
                ))
    
    def get_template_suggestions(self) -> List[str]:
        """
        Get suggestions for creating panel templates.
        
        Returns:
            A list of template suggestions.
        """
        suggestions = []
        panel_types = Counter(m.value for m in self.matches if m.pattern_type == 'panel_type')
        
        for panel_type, count in panel_types.items():
            if count >= 2:
                suggestions.append(
                    f"Create {panel_type}Panel template function for {count} panels"
                )
        
        return suggestions
    
    def get_extraction_suggestions(self) -> List[str]:
        """
        Get suggestions for extracting local variables.
        
        Returns:
            A list of extraction suggestions.
        """
        return [m.suggestion for m in self.matches if m.pattern_type != 'panel_type']


# Import json for JSON serialization in pattern detection
import json