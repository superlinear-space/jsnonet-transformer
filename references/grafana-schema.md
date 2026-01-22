# Grafana Dashboard Schema Reference

This document describes the Grafana dashboard schema used by the transformer.

## Dashboard Structure

A Grafana dashboard JSON file has the following top-level structure:

```json
{
  "dashboard": {
    "id": null,
    "uid": "string",
    "title": "string",
    "tags": ["string"],
    "timezone": "browser",
    "schemaVersion": 38,
    "version": 1,
    "refresh": "5s",
    "panels": []
  },
  "overwrite": true,
  "message": "Update message"
}
```

## Dashboard Properties

| Property | Type | Description |
|----------|------|-------------|
| `id` | number \| null | Dashboard ID (null for new dashboards) |
| `uid` | string | Unique dashboard identifier |
| `title` | string | Dashboard title |
| `tags` | string[] | Dashboard tags |
| `timezone` | string | Timezone (e.g., "browser", "utc") |
| `schemaVersion` | number | Grafana schema version |
| `version` | number | Dashboard version |
| `refresh` | string | Auto-refresh interval |
| `panels` | Panel[] | Array of panel objects |

## Panel Types

The transformer supports all standard Grafana panel types:

| Type | Description |
|------|-------------|
| `graph` | Line/area chart |
| `timeseries` | Modern time series chart |
| `stat` | Single value display |
| `gauge` | Gauge visualization |
| `table` | Tabular data |
| `piechart` | Pie/donut chart |
| `barchart` | Bar chart |
| `heatmap` | Heatmap visualization |
| `logs` | Log viewer |
| `text` | Text panel |
| `row` | Container panel |

## Common Panel Properties

```json
{
  "id": 1,
  "type": "graph",
  "title": "Panel Title",
  "gridPos": { "x": 0, "y": 0, "w": 12, "h": 8 },
  "datasource": { "type": "prometheus", "uid": "${datasource}" },
  "targets": []
}
```

### Grid Position

```json
{
  "gridPos": {
    "x": 0,      // X position (0-24)
    "y": 0,      // Y position
    "w": 12,     // Width (1-24)
    "h": 8       // Height (2-?)
  }
}
```

### Data Source

```json
{
  "datasource": {
    "type": "prometheus",
    "uid": "${datasource}"
  }
}
```

### Targets (Queries)

```json
{
  "targets": [
    {
      "expr": "rate(cpu_usage[5m])",
      "legendFormat": "{{pod}}",
      "refId": "A"
    }
  ]
}
```

## Field Configuration

```json
{
  "fieldConfig": {
    "defaults": {
      "color": { "mode": "thresholds" },
      "mappings": [],
      "thresholds": {
        "mode": "absolute",
        "steps": [
          { "color": "green", "value": null },
          { "color": "yellow", "value": 70 },
          { "color": "red", "value": 90 }
        ]
      },
      "unit": "percent"
    },
    "overrides": []
  }
}
```

## Panel Options

```json
{
  "options": {
    "colorMode": "value",
    "graphMode": "area",
    "justifyMode": "auto",
    "orientation": "auto",
    "reduceOptions": {
      "calcs": ["lastNotNull"],
      "fields": "",
      "values": false
    },
    "textMode": "auto"
  }
}
```

## Time Picker

```json
{
  "timepicker": {
    "refresh_intervals": ["5s", "10s", "30s", "1m", "5m", "15m", "30m", "1h", "2h", "1d"],
    "time_options": ["5m", "15m", "1h", "6h", "12h", "24h", "2d", "7d", "30d"]
  }
}
```

## Templating

```json
{
  "templating": {
    "list": [
      {
        "name": "datasource",
        "type": "datasource",
        "query": "prometheus",
        "refresh": 1
      },
      {
        "name": "cluster",
        "type": "query",
        "datasource": "${datasource}",
        "query": "label_values(kube_pod_info, cluster)",
        "refresh": 2
      }
    ]
  }
}
```

## Annotations

```json
{
  "annotations": {
    "list": [
      {
        "builtIn": 1,
        "datasource": "${datasource}",
        "enable": true,
        "hide": true,
        "iconColor": "rgba(0, 211, 255, 0.945)",
        "name": "Annotations & Alerts",
        "type": "dashboard"
      }
    ]
  }
}