"""
Dashboard Analyzer Module

Analyzes Grafana dashboard structure and identifies patterns for transformation.
"""

from typing import Any, Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, field
from collections import Counter


@dataclass
class PanelInfo:
    """Information about a single panel."""
    panel_id: int
    type: str
    title: str
    grid_pos: Dict[str, int]
    targets: List[Dict[str, Any]]
    datasource: Optional[str]
    options: Dict[str, Any]
    field_config: Dict[str, Any]
    transformations: List[Dict[str, Any]]
    custom_properties: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DashboardAnalysis:
    """Analysis results for a Grafana dashboard."""
    title: str
    uid: Optional[str]
    tags: List[str]
    timezone: str
    panels: List[PanelInfo]
    repeated_panels: List[str]
    repeated_values: Dict[str, Any]
    data_sources: Set[str]
    panel_types: Counter
    common_targets: List[Dict[str, Any]]
    dashboard_config: Dict[str, Any]


def analyze_dashboard(data: Dict[str, Any]) -> DashboardAnalysis:
    """
    Analyze a Grafana dashboard JSON structure.
    
    Args:
        data: The parsed dashboard JSON data.
        
    Returns:
        A DashboardAnalysis object containing the analysis results.
    """
    # Extract dashboard data
    dashboard = data.get('dashboard', data)
    
    # Extract basic info
    title = dashboard.get('title', 'Untitled Dashboard')
    uid = dashboard.get('uid')
    tags = dashboard.get('tags', [])
    timezone = dashboard.get('timezone', 'browser')
    
    # Extract panels
    panels_raw = dashboard.get('panels', [])
    panels = []
    for panel in panels_raw:
        panel_info = analyze_panel(panel)
        panels.append(panel_info)
    
    # Analyze patterns
    repeated_values = find_repeated_values(panels)
    data_sources = find_data_sources(panels)
    panel_types = Counter(p.type for p in panels)
    repeated_panels = find_repeated_panels(panels)
    common_targets = find_common_targets(panels)
    
    # Extract dashboard config
    dashboard_config = extract_dashboard_config(dashboard)
    
    return DashboardAnalysis(
        title=title,
        uid=uid,
        tags=tags,
        timezone=timezone,
        panels=panels,
        repeated_panels=repeated_panels,
        repeated_values=repeated_values,
        data_sources=data_sources,
        panel_types=panel_types,
        common_targets=common_targets,
        dashboard_config=dashboard_config
    )


def analyze_panel(panel: Dict[str, Any]) -> PanelInfo:
    """
    Analyze a single panel.
    
    Args:
        panel: The panel JSON data.
        
    Returns:
        A PanelInfo object.
    """
    panel_id = panel.get('id', 0)
    panel_type = panel.get('type', 'unknown')
    title = panel.get('title', '')
    
    # Grid position
    grid_pos = panel.get('gridPos', {'x': 0, 'y': 0, 'w': 12, 'h': 8})
    
    # Targets (queries)
    targets = panel.get('targets', [])
    
    # Data source
    datasource = panel.get('datasource')
    if datasource and isinstance(datasource, dict):
        datasource = datasource.get('type', datasource.get('uid'))
    
    # Options
    options = panel.get('options', {})
    
    # Field config
    field_config = panel.get('fieldConfig', {})
    
    # Transformations
    transformations = panel.get('transformations', [])
    
    # Custom properties (not commonly used)
    custom_props = {}
    common_props = {
        'id', 'type', 'title', 'gridPos', 'targets', 'datasource',
        'options', 'fieldConfig', 'transformations', 'transparent',
        'description', 'repeat', 'repeatDirection', 'maxPerRow',
        'collapsed', 'panels', 'legend', 'tooltip', 'bars', 'lines',
        'fill', 'fillGradient', 'linewidth', 'dashLength', 'dashVector',
        'points', 'pointradius', 'percentage', 'steppedLine', 'nullPointMode',
        'aliasColors', 'seriesOverrides', 'thresholds', 'overrides',
        'xaxis', 'yaxes', 'yaxis', 'decimals', 'links', 'datasource'
    }
    for key, value in panel.items():
        if key not in common_props:
            custom_props[key] = value
    
    return PanelInfo(
        panel_id=panel_id,
        type=panel_type,
        title=title,
        grid_pos=grid_pos,
        targets=targets,
        datasource=datasource,
        options=options,
        field_config=field_config,
        transformations=transformations,
        custom_properties=custom_props
    )


def find_repeated_values(panels: List[PanelInfo]) -> Dict[str, Any]:
    """
    Find values that are repeated across panels.
    
    Args:
        panels: List of analyzed panels.
        
    Returns:
        A dictionary of repeated values.
    """
    repeated = {}
    
    # Collect all values
    all_values = {}
    for panel in panels:
        for key, value in panel.custom_properties.items():
            if isinstance(value, (str, int, float, bool)):
                key_path = f"panels.{key}"
                if key_path not in all_values:
                    all_values[key_path] = []
                all_values[key_path].append(value)
    
    # Find repeated values (appearing more than once)
    for key_path, values in all_values.items():
        if len(values) > 1:
            unique_values = set(str(v) for v in values)
            if len(unique_values) == 1:
                # All values are the same - extract as local
                repeated[key_path] = values[0]
    
    # Check for common panel configurations
    legend_configs = []
    tooltip_configs = []
    for panel in panels:
        if hasattr(panel, 'custom_properties'):
            for key, value in panel.custom_properties.items():
                if 'legend' in key.lower():
                    legend_configs.append((key, value))
                if 'tooltip' in key.lower():
                    tooltip_configs.append((key, value))
    
    return repeated


def find_data_sources(panels: List[PanelInfo]) -> Set[str]:
    """
    Find all unique data sources used in panels.
    
    Args:
        panels: List of analyzed panels.
        
    Returns:
        A set of unique data source references.
    """
    sources = set()
    for panel in panels:
        if panel.datasource:
            sources.add(panel.datasource)
        for target in panel.targets:
            if 'datasource' in target:
                ds = target['datasource']
                if isinstance(ds, dict):
                    ds = ds.get('type', ds.get('uid', ''))
                if ds:
                    sources.add(ds)
    return sources


def find_repeated_panels(panels: List[PanelInfo]) -> List[str]:
    """
    Find panels that are repeated (using repeat property).
    
    Args:
        panels: List of analyzed panels.
        
    Returns:
        A list of panel IDs that are repeated.
    """
    repeated = []
    for panel in panels:
        if panel.custom_properties.get('repeat'):
            repeated.append(panel.title)
    return repeated


def find_common_targets(panels: List[PanelInfo]) -> List[Dict[str, Any]]:
    """
    Find common query targets across panels.
    
    Args:
        panels: List of analyzed panels.
        
    Returns:
        A list of common target configurations.
    """
    all_targets = []
    for panel in panels:
        for target in panel.targets:
            # Create a hashable version for comparison
            target_key = tuple(sorted((k, str(v)) for k, v in target.items()))
            all_targets.append((target_key, target))
    
    # Count occurrences
    target_counts = Counter(t[0] for t in all_targets)
    
    # Return targets that appear more than once
    common = []
    for target_key, target in all_targets:
        if target_counts[target_key] > 1:
            if target not in common:
                common.append(target)
    
    return common


def extract_dashboard_config(dashboard: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract dashboard-level configuration.
    
    Args:
        dashboard: The dashboard JSON data.
        
    Returns:
        A dictionary of dashboard configuration.
    """
    config = {}
    
    # Core config fields
    core_fields = [
        'id', 'uid', 'title', 'tags', 'timezone', 'schemaVersion',
        'version', 'refresh', 'time', 'timepicker', 'templating',
        'annotations', 'description', 'style', 'editable', 'fiscalYearStartMonth',
        'graphTooltip', 'liveNow', 'weekStart', 'panelIds'
    ]
    
    for field in core_fields:
        if field in dashboard:
            config[field] = dashboard[field]
    
    return config