"""
Panel Templates Module

Provides reusable panel template functions for Grafana dashboards.
"""

from .panels import (
    graph_panel,
    timeseries_panel,
    stat_panel,
    gauge_panel,
    table_panel,
    piechart_panel,
    barchart_panel,
    heatmap_panel,
    logs_panel,
    text_panel,
    create_panel_template,
)

from .mixins import (
    legend_mixin,
    tooltip_mixin,
    axis_mixin,
    thresholds_mixin,
    colors_mixin,
    apply_mixin,
)

__all__ = [
    'graph_panel',
    'timeseries_panel',
    'stat_panel',
    'gauge_panel',
    'table_panel',
    'piechart_panel',
    'barchart_panel',
    'heatmap_panel',
    'logs_panel',
    'text_panel',
    'create_panel_template',
    'legend_mixin',
    'tooltip_mixin',
    'axis_mixin',
    'thresholds_mixin',
    'colors_mixin',
    'apply_mixin',
]