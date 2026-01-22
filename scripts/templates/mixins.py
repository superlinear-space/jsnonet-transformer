"""
Mixin Functions

Reusable configuration mixins for Grafana panels.
"""

from typing import Any, Dict, List, Optional


def legend_mixin(
    show: bool = True,
    displayMode: str = 'list',
    placement: str = 'bottom',
    values: Optional[List[str]] = None,
    min: bool = False,
    max: bool = False,
    avg: bool = False,
    current: bool = False,
    total: bool = False,
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Create a legend configuration mixin.
    
    Args:
        show: Show legend.
        displayMode: Display mode ('list', 'table', 'hidden').
        placement: Legend placement ('bottom', 'right').
        values: Values to show.
        min: Show minimum.
        max: Show maximum.
        avg: Show average.
        current: Show current value.
        total: Show total.
        **kwargs: Additional properties.
        
    Returns:
        Legend configuration dictionary.
    """
    config = {
        'show': show,
        'displayMode': displayMode,
        'placement': placement,
    }
    
    if values:
        config['values'] = values
    
    calcs = []
    if min:
        calcs.append('min')
    if max:
        calcs.append('max')
    if avg:
        calcs.append('avg')
    if current:
        calcs.append('last')
    if total:
        calcs.append('sum')
    
    if calcs:
        config['calcs'] = calcs
    
    return {**config, **kwargs}


def tooltip_mixin(
    shared: bool = True,
    sort: int = 0,
    include_null: bool = False,
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Create a tooltip configuration mixin.
    
    Args:
        shared: Show shared tooltip.
        sort: Sort order (0: none, 1: ascending, 2: descending).
        include_null: Include null values.
        **kwargs: Additional properties.
        
    Returns:
        Tooltip configuration dictionary.
    """
    return {
        'shared': shared,
        'sort': sort,
        'include_null': include_null,
        **kwargs,
    }


def axis_mixin(
    show: bool = True,
    label: Optional[str] = None,
    min: Optional[float] = None,
    max: Optional[float] = None,
    logBase: int = 1,
    unit: Optional[str] = None,
    decimals: Optional[int] = None,
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Create an axis configuration mixin.
    
    Args:
        show: Show axis.
        label: Axis label.
        min: Minimum value.
        max: Maximum value.
        logBase: Logarithmic base (1 = linear).
        unit: Unit to display.
        decimals: Decimal places.
        **kwargs: Additional properties.
        
    Returns:
        Axis configuration dictionary.
    """
    config = {'show': show}
    
    if label is not None:
        config['label'] = label
    if min is not None:
        config['min'] = min
    if max is not None:
        config['max'] = max
    if logBase > 1:
        config['logBase'] = logBase
    if unit is not None:
        config['unit'] = unit
    if decimals is not None:
        config['decimals'] = decimals
    
    return {**config, **kwargs}


def thresholds_mixin(
    mode: str = 'absolute',
    steps: Optional[List[Dict[str, Any]]] = None,
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Create a thresholds configuration mixin.
    
    Args:
        mode: Threshold mode ('absolute', 'percentage').
        steps: Threshold steps.
        **kwargs: Additional properties.
        
    Returns:
        Thresholds configuration dictionary.
    """
    default_steps = [
        {'color': 'green', 'value': None},
        {'color': 'green', 'value': 80},
        {'color': 'red', 'value': 90},
    ]
    
    return {
        'mode': mode,
        'steps': steps or default_steps,
        **kwargs,
    }


def colors_mixin(
    scheme: str = 'standard',
    colors: Optional[List[str]] = None,
    **kwargs: Any,
) -> List[str]:
    """
    Create a colors configuration mixin.
    
    Args:
        scheme: Color scheme ('standard', 'green-blue', 'red-yellow-green').
        colors: Custom colors list.
        **kwargs: Unused (for compatibility).
        
    Returns:
        List of colors.
    """
    if colors:
        return colors
    
    schemes = {
        'standard': ['#5794f2', '#b877d9', '#f2495c', '#fffa35', '#73bf69'],
        'green-blue': ['#73bf69', '#5794f2', '#b877d9', '#f2495c'],
        'red-yellow-green': ['#f2495c', '#ffab40', '#73bf69', '#5794f2'],
        'dark': ['#8e8e8e', '#8e8e8e', '#8e8e8e'],
        'light': ['#8e8e8e', '#8e8e8e', '#8e8e8e'],
    }
    
    return schemes.get(scheme, schemes['standard'])


def apply_mixin(
    panel: Dict[str, Any],
    mixin: Dict[str, Any],
    overwrite: bool = False,
) -> Dict[str, Any]:
    """
    Apply a mixin to a panel configuration.
    
    Args:
        panel: Panel configuration.
        mixin: Mixin configuration to apply.
        overwrite: Overwrite existing values.
        
    Returns:
        Modified panel configuration.
    """
    result = panel.copy()
    
    for key, value in mixin.items():
        if key not in result or overwrite:
            result[key] = value
    
    return result


def grid_pos_mixin(
    x: int = 0,
    y: int = 0,
    w: int = 12,
    h: int = 8,
) -> Dict[str, int]:
    """
    Create a grid position mixin.
    
    Args:
        x: X position.
        y: Y position.
        w: Width.
        h: Height.
        
    Returns:
        Grid position dictionary.
    """
    return {'x': x, 'y': y, 'w': w, 'h': h}


def datasource_mixin(
    type: str,
    uid: str = '${datasource}',
) -> Dict[str, str]:
    """
    Create a datasource mixin.
    
    Args:
        type: Datasource type (e.g., 'prometheus', 'loki').
        uid: Datasource UID variable.
        
    Returns:
        Datasource configuration dictionary.
    """
    return {'type': type, 'uid': uid}


def targets_mixin(
    expr: str,
    legendFormat: Optional[str] = None,
    interval: Optional[str] = None,
    refId: str = 'A',
    datasource: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Create a query target mixin.
    
    Args:
        expr: Query expression.
        legendFormat: Legend format template.
        interval: Query interval.
        refId: Query reference ID.
        datasource: Datasource type override.
        
    Returns:
        Target configuration dictionary.
    """
    target = {
        'expr': expr,
        'refId': refId,
    }
    
    if legendFormat:
        target['legendFormat'] = legendFormat
    if interval:
        target['interval'] = interval
    if datasource:
        target['datasource'] = datasource_mixin(datasource)
    
    return target