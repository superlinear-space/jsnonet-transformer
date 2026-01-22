"""
Panel Template Functions

Reusable template functions for common Grafana panel types.
"""

from typing import Any, Dict, List, Optional


def graph_panel(
    title: str,
    gridPos: Dict[str, int],
    targets: Optional[List[Dict[str, Any]]] = None,
    datasource: Optional[str] = None,
    legend: Optional[Dict[str, Any]] = None,
    tooltip: Optional[Dict[str, Any]] = None,
    colors: Optional[List[str]] = None,
    thresholds: Optional[Dict[str, Any]] = None,
    lines: bool = True,
    fill: int = 1,
    linewidth: int = 1,
    pointradius: int = 2,
    bars: bool = False,
    percentage: bool = False,
    stepped_line: bool = False,
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Create a graph panel configuration.
    
    Args:
        title: Panel title.
        gridPos: Grid position {x, y, w, h}.
        targets: Query targets.
        datasource: Data source type.
        legend: Legend configuration.
        tooltip: Tooltip configuration.
        colors: Line colors.
        thresholds: Threshold configuration.
        lines: Show lines.
        fill: Fill opacity (0-10).
        linewidth: Line width.
        pointradius: Point radius.
        bars: Show bars.
        percentage: Show as percentage.
        stepped_line: Use stepped line.
        **kwargs: Additional properties.
        
    Returns:
        Panel configuration dictionary.
    """
    return {
        'type': 'graph',
        'title': title,
        'gridPos': gridPos,
        'targets': targets or [],
        'datasource': _datasource(datasource),
        'legend': legend or {
            'show': True,
            'values': False,
            'min': False,
            'max': False,
            'current': False,
            'total': False,
            'avg': False,
        },
        'tooltip': tooltip or {
            'shared': True,
            'sort': 0,
            'include_null': False,
        },
        'colors': colors or ['#5794f2', '#b877d9', '#f2495c'],
        'thresholds': thresholds or {
            'mode': 'absolute',
            'steps': [
                {'color': 'green', 'value': None},
                {'color': 'green', 'value': 80},
                {'color': 'red', 'value': 90},
            ],
        },
        'lines': lines,
        'fill': fill,
        'linewidth': linewidth,
        'pointradius': pointradius,
        'bars': bars,
        'percentage': percentage,
        'steppedLine': stepped_line,
        **kwargs,
    }


def timeseries_panel(
    title: str,
    gridPos: Dict[str, int],
    targets: Optional[List[Dict[str, Any]]] = None,
    datasource: Optional[str] = None,
    legend: Optional[Dict[str, Any]] = None,
    colors: Optional[List[str]] = None,
    fillOpacity: int = 80,
    showPoints: str = 'auto',
    unit: str = 'short',
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Create a timeseries panel configuration.
    
    Args:
        title: Panel title.
        gridPos: Grid position {x, y, w, h}.
        targets: Query targets.
        datasource: Data source type.
        legend: Legend configuration.
        colors: Line colors.
        fillOpacity: Fill opacity (0-100).
        showPoints: When to show points ('always', 'never', 'auto').
        unit: Unit to display.
        **kwargs: Additional properties.
        
    Returns:
        Panel configuration dictionary.
    """
    return {
        'type': 'timeseries',
        'title': title,
        'gridPos': gridPos,
        'targets': targets or [],
        'datasource': _datasource(datasource),
        'legend': legend or {
            'show': True,
            'displayMode': 'list',
            'placement': 'bottom',
            'calcs': [],
        },
        'colors': colors or ['#5794f2', '#b877d9', '#f2495c'],
        'fillOpacity': fillOpacity,
        'showPoints': showPoints,
        'unit': unit,
        **kwargs,
    }


def stat_panel(
    title: str,
    gridPos: Dict[str, int],
    targets: Optional[List[Dict[str, Any]]] = None,
    datasource: Optional[str] = None,
    colorMode: str = 'value',
    graphMode: str = 'area',
    justifyMode: str = 'auto',
    textMode: str = 'auto',
    unit: str = 'short',
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Create a stat panel configuration.
    
    Args:
        title: Panel title.
        gridPos: Grid position {x, y, w, h}.
        targets: Query targets.
        datasource: Data source type.
        colorMode: Color mode ('value', 'background').
        graphMode: Graph mode ('none', 'area').
        justifyMode: Justify mode ('auto', 'left', 'right').
        textMode: Text mode ('auto', 'value', 'title', 'name').
        unit: Unit to display.
        **kwargs: Additional properties.
        
    Returns:
        Panel configuration dictionary.
    """
    return {
        'type': 'stat',
        'title': title,
        'gridPos': gridPos,
        'targets': targets or [],
        'datasource': _datasource(datasource),
        'colorMode': colorMode,
        'graphMode': graphMode,
        'justifyMode': justifyMode,
        'textMode': textMode,
        'unit': unit,
        **kwargs,
    }


def gauge_panel(
    title: str,
    gridPos: Dict[str, int],
    targets: Optional[List[Dict[str, Any]]] = None,
    datasource: Optional[str] = None,
    min: int = 0,
    max: int = 100,
    thresholds: Optional[Dict[str, Any]] = None,
    showThresholdLabels: bool = False,
    showThresholdMarkers: bool = True,
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Create a gauge panel configuration.
    
    Args:
        title: Panel title.
        gridPos: Grid position {x, y, w, h}.
        targets: Query targets.
        datasource: Data source type.
        min: Minimum value.
        max: Maximum value.
        thresholds: Threshold configuration.
        showThresholdLabels: Show threshold labels.
        showThresholdMarkers: Show threshold markers.
        **kwargs: Additional properties.
        
    Returns:
        Panel configuration dictionary.
    """
    return {
        'type': 'gauge',
        'title': title,
        'gridPos': gridPos,
        'targets': targets or [],
        'datasource': _datasource(datasource),
        'min': min,
        'max': max,
        'thresholds': thresholds or {
            'mode': 'absolute',
            'steps': [
                {'color': 'green', 'value': None},
                {'color': 'green', 'value': 80},
                {'color': 'red', 'value': 90},
            ],
        },
        'showThresholdLabels': showThresholdLabels,
        'showThresholdMarkers': showThresholdMarkers,
        **kwargs,
    }


def table_panel(
    title: str,
    gridPos: Dict[str, int],
    targets: Optional[List[Dict[str, Any]]] = None,
    datasource: Optional[str] = None,
    showHeader: bool = True,
    sortBy: Optional[str] = None,
    columnStyles: Optional[List[Dict[str, Any]]] = None,
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Create a table panel configuration.
    
    Args:
        title: Panel title.
        gridPos: Grid position {x, y, w, h}.
        targets: Query targets.
        datasource: Data source type.
        showHeader: Show column header.
        sortBy: Default sort column.
        columnStyles: Column styling rules.
        **kwargs: Additional properties.
        
    Returns:
        Panel configuration dictionary.
    """
    return {
        'type': 'table',
        'title': title,
        'gridPos': gridPos,
        'targets': targets or [],
        'datasource': _datasource(datasource),
        'showHeader': showHeader,
        'sortBy': sortBy,
        'columnStyles': columnStyles or [],
        **kwargs,
    }


def piechart_panel(
    title: str,
    gridPos: Dict[str, int],
    targets: Optional[List[Dict[str, Any]]] = None,
    datasource: Optional[str] = None,
    pieType: str = 'pie',
    displayLabels: Optional[List[str]] = None,
    legend: Optional[Dict[str, Any]] = None,
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Create a pie chart panel configuration.
    
    Args:
        title: Panel title.
        gridPos: Grid position {x, y, w, h}.
        targets: Query targets.
        datasource: Data source type.
        pieType: Pie type ('pie', 'donut').
        displayLabels: Labels to display.
        legend: Legend configuration.
        **kwargs: Additional properties.
        
    Returns:
        Panel configuration dictionary.
    """
    return {
        'type': 'piechart',
        'title': title,
        'gridPos': gridPos,
        'targets': targets or [],
        'datasource': _datasource(datasource),
        'pieType': pieType,
        'displayLabels': displayLabels or ['name', 'percent'],
        'legend': legend or {
            'displayMode': 'list',
            'placement': 'right',
            'values': ['value'],
        },
        **kwargs,
    }


def barchart_panel(
    title: str,
    gridPos: Dict[str, int],
    targets: Optional[List[Dict[str, Any]]] = None,
    datasource: Optional[str] = None,
    orientation: str = 'auto',
    barWidth: int = 0.97,
    groupWidth: int = 0.7,
    lineWidth: int = 1,
    fillOpacity: int = 80,
    gradientMode: str = 'none',
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Create a bar chart panel configuration.
    
    Args:
        title: Panel title.
        gridPos: Grid position {x, y, w, h}.
        targets: Query targets.
        datasource: Data source type.
        orientation: Bar orientation ('auto', 'horizontal', 'vertical').
        barWidth: Bar width (0-1).
        groupWidth: Group width (0-1).
        lineWidth: Line width.
        fillOpacity: Fill opacity (0-100).
        gradientMode: Gradient mode ('none', 'opacity', 'hue', 'scheme').
        **kwargs: Additional properties.
        
    Returns:
        Panel configuration dictionary.
    """
    return {
        'type': 'barchart',
        'title': title,
        'gridPos': gridPos,
        'targets': targets or [],
        'datasource': _datasource(datasource),
        'orientation': orientation,
        'barWidth': barWidth,
        'groupWidth': groupWidth,
        'lineWidth': lineWidth,
        'fillOpacity': fillOpacity,
        'gradientMode': gradientMode,
        **kwargs,
    }


def heatmap_panel(
    title: str,
    gridPos: Dict[str, int],
    targets: Optional[List[Dict[str, Any]]] = None,
    datasource: Optional[str] = None,
    colorScale: str = 'spectral',
    cards: Optional[Dict[str, int]] = None,
    colorScheme: str = 'interpolateSpectral',
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Create a heatmap panel configuration.
    
    Args:
        title: Panel title.
        gridPos: Grid position {x, y, w, h}.
        targets: Query targets.
        datasource: Data source type.
        colorScale: Color scale.
        cards: Card configuration.
        colorScheme: Color scheme.
        **kwargs: Additional properties.
        
    Returns:
        Panel configuration dictionary.
    """
    return {
        'type': 'heatmap',
        'title': title,
        'gridPos': gridPos,
        'targets': targets or [],
        'datasource': _datasource(datasource),
        'colorScale': colorScale,
        'cards': cards or {'padding': 1, 'spacing': 1},
        'colorScheme': colorScheme,
        **kwargs,
    }


def logs_panel(
    title: str,
    gridPos: Dict[str, int],
    targets: Optional[List[Dict[str, Any]]] = None,
    datasource: Optional[str] = None,
    showLabels: bool = False,
    showCommonLabels: bool = False,
    wrapLogMessage: bool = False,
    prettifyLogMessage: bool = False,
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Create a logs panel configuration.
    
    Args:
        title: Panel title.
        gridPos: Grid position {x, y, w, h}.
        targets: Query targets.
        datasource: Data source type.
        showLabels: Show labels.
        showCommonLabels: Show common labels.
        wrapLogMessage: Wrap log messages.
        prettifyLogMessage: Prettify log messages.
        **kwargs: Additional properties.
        
    Returns:
        Panel configuration dictionary.
    """
    return {
        'type': 'logs',
        'title': title,
        'gridPos': gridPos,
        'targets': targets or [],
        'datasource': _datasource(datasource),
        'options': {
            'showLabels': showLabels,
            'showCommonLabels': showCommonLabels,
            'wrapLogMessage': wrapLogMessage,
            'prettifyLogMessage': prettifyLogMessage,
        },
        **kwargs,
    }


def text_panel(
    title: str,
    gridPos: Dict[str, int],
    content: str = '',
    mode: str = 'markdown',
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Create a text panel configuration.
    
    Args:
        title: Panel title.
        gridPos: Grid position {x, y, w, h}.
        content: Text content.
        mode: Display mode ('markdown', 'html', 'text').
        **kwargs: Additional properties.
        
    Returns:
        Panel configuration dictionary.
    """
    return {
        'type': 'text',
        'title': title,
        'gridPos': gridPos,
        'options': {
            'content': content,
            'mode': mode,
        },
        **kwargs,
    }


def create_panel_template(
    panel_type: str,
    title: str,
    gridPos: Dict[str, int],
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Create a panel configuration based on type.
    
    Args:
        panel_type: Type of panel.
        title: Panel title.
        gridPos: Grid position {x, y, w, h}.
        **kwargs: Additional panel-specific options.
        
    Returns:
        Panel configuration dictionary.
    """
    panel_functions = {
        'graph': graph_panel,
        'timeseries': timeseries_panel,
        'stat': stat_panel,
        'gauge': gauge_panel,
        'table': table_panel,
        'piechart': piechart_panel,
        'barchart': barchart_panel,
        'heatmap': heatmap_panel,
        'logs': logs_panel,
        'text': text_panel,
    }
    
    func = panel_functions.get(panel_type)
    if func:
        return func(title, gridPos, **kwargs)
    else:
        # Generic panel
        return {
            'type': panel_type,
            'title': title,
            'gridPos': gridPos,
            **kwargs,
        }


def _datasource(datasource: Optional[str]) -> Optional[Dict[str, str]]:
    """Format datasource for Jsonnet."""
    if datasource:
        return {'type': datasource, 'uid': '${datasource}'}
    return None