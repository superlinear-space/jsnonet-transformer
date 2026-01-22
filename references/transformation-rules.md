# Transformation Rules

This document describes how the transformer converts Grafana dashboard JSON to Jsonnet.

## Rule 1: Extract Repeated Values

Repeated values (colors, thresholds, etc.) are extracted into local variables when they appear multiple times.

### Before (JSON)

```json
{
  "panels": [
    {
      "id": 1,
      "type": "stat",
      "fieldConfig": {
        "defaults": {
          "thresholds": {
            "mode": "absolute",
            "steps": [
              { "color": "green", "value": null },
              { "color": "yellow", "value": 70 },
              { "color": "red", "value": 90 }
            ]
          }
        }
      }
    },
    {
      "id": 2,
      "type": "stat",
      "fieldConfig": {
        "defaults": {
          "thresholds": {
            "mode": "absolute",
            "steps": [
              { "color": "green", "value": null },
              { "color": "yellow", "value": 70 },
              { "color": "red", "value": 90 }
            ]
          }
        }
      }
    }
  ]
}
```

### After (Jsonnet)

```jsonnet
// Threshold configurations
local defaultThresholds = {
  mode: 'absolute',
  steps: [
    { color: 'green', value: null },
    { color: 'yellow', value: 70 },
    { color: 'red', value: 90 },
  ],
};

{
  panels: [
    {
      id: 1,
      type: 'stat',
      fieldConfig: {
        defaults: {
          thresholds: defaultThresholds,
        },
      },
    },
    {
      id: 2,
      type: 'stat',
      fieldConfig: {
        defaults: {
          thresholds: defaultThresholds,
        },
      },
    },
  ],
}
```

### Configuration

- **Minimum occurrences**: 2 (configurable via `min_pattern_occurrences`)
- **Priority**: High-frequency patterns are extracted first
- **Naming**: Variable names are derived from the pattern type (e.g., `colors`, `thresholds`, `datasources`)

## Rule 2: Create Panel Templates

Common panel configurations become template functions when multiple panels share similar structures.

### Before (JSON)

```json
{
  "panels": [
    {
      "type": "stat",
      "title": "Cluster CPU Usage",
      "colorMode": "value",
      "graphMode": "area",
      "justifyMode": "auto",
      "textMode": "auto",
      "transparent": false
    },
    {
      "type": "stat",
      "title": "Cluster Memory Usage",
      "colorMode": "value",
      "graphMode": "area",
      "justifyMode": "auto",
      "textMode": "auto",
      "transparent": false
    }
  ]
}
```

### After (Jsonnet)

```jsonnet
// Panel template functions
local statPanel(title, gridPos, targets, datasource) = {
  type: 'stat',
  title: title,
  gridPos: gridPos,
  targets: targets,
  datasource: { type: datasource, uid: '${datasource}' },
  colorMode: 'value',
  graphMode: 'area',
  justifyMode: 'auto',
  textMode: 'auto',
  transparent: false,
};

{
  panels: [
    statPanel(
      'Cluster CPU Usage',
      { x: 0, y: 1, w: 8, h: 8 },
      [{ expr: '...', refId: 'A' }],
      'prometheus'
    ),
    statPanel(
      'Cluster Memory Usage',
      { x: 8, y: 1, w: 8, h: 8 },
      [{ expr: '...', refId: 'A' }],
      'prometheus'
    ),
  ],
}
```

### Template Parameters

| Parameter | Description |
|-----------|-------------|
| `title` | Panel title |
| `gridPos` | Panel position and size `{x, y, w, h}` |
| `targets` | Array of query targets |
| `datasource` | Data source type (e.g., 'prometheus') |

### Supported Panel Templates

- `statPanel` - Single value display
- `timeseriesPanel` - Time series chart
- `graphPanel` - Legacy graph panel
- `barchartPanel` - Bar chart
- `tablePanel` - Table panel
- `piechartPanel` - Pie chart
- `gaugePanel` - Gauge panel
- `heatmapPanel` - Heatmap panel
- `logsPanel` - Logs panel
- `textPanel` - Text panel

## Rule 3: Data Source Extraction

Data source configurations are extracted into a local variable.

### Before (JSON)

```json
{
  "panels": [
    {
      "datasource": { "type": "prometheus", "uid": "${datasource}" }
    },
    {
      "datasource": { "type": "prometheus", "uid": "${datasource}" }
    }
  ]
}
```

### After (Jsonnet)

```jsonnet
// Data source configurations
local datasources = {
  prometheus: { type: 'prometheus', uid: '${datasource}' },
};

{
  panels: [
    { datasource: datasources.prometheus },
    { datasource: datasources.prometheus },
  ],
}
```

### Configuration

- **Pattern**: Same data source type and UID
- **Naming**: Derived from data source type (e.g., `prometheus`, `loki`, `elasticsearch`)

## Rule 4: Color Extraction

Color values are extracted into a local variable.

### Before (JSON)

```json
{
  "fieldConfig": {
    "defaults": {
      "color": { "mode": "palette-classic" }
    }
  }
}
```

### After (Jsonnet)

```jsonnet
// Common color definitions
local colors = {
  green: '#73bf69',
  red: '#f2495c',
  blue: '#5794f2',
  orange: '#ff780a',
  purple: '#b877d9',
  yellow: '#ffab40',
};
```

## Rule 5: Dashboard Configuration

Dashboard metadata is preserved as-is with minimal transformation.

### Before (JSON)

```json
{
  "dashboard": {
    "title": "Kubernetes Cluster Overview",
    "uid": "kubernetes-cluster",
    "tags": ["kubernetes", "cluster", "monitoring"],
    "timezone": "browser",
    "schemaVersion": 38,
    "version": 1,
    "refresh": "5s",
    "time": {
      "from": "now-6h",
      "to": "now"
    }
  }
}
```

### After (Jsonnet)

```jsonnet
{
  title: 'Kubernetes Cluster Overview',
  uid: 'kubernetes-cluster',
  tags: ['kubernetes', 'cluster', 'monitoring'],
  timezone: 'browser',
  schemaVersion: 38,
  version: 1,
  refresh: '5s',
  time: { from: 'now-6h', to: 'now' },
}
```

## Rule 6: Panel Comments

Comments are added to panels for documentation.

### Output

```jsonnet
{
  panels: [
    {
      // Cluster Health
      id: 1,
      type: 'row',
      title: 'Cluster Health',
      gridPos: { x: 0, y: 0, w: 24, h: 1 },
      collapsed: false,
    },
    {
      // Cluster CPU Usage
      id: 2,
      type: 'stat',
      title: 'Cluster CPU Usage',
      // ...
    },
  ],
}
```

### Configuration

- **Enabled by default**: `add_comments: true`
- **Comment format**: `// <panel_title>` for named panels
- **Row panels**: Comments indicate section headers

## Rule 7: Query Target Extraction

Repeated query patterns can be extracted into local variables.

### Before (JSON)

```json
{
  "targets": [
    { "expr": "rate(cpu_usage[5m])", "legendFormat": "CPU", "refId": "A" },
    { "expr": "rate(cpu_usage[5m])", "legendFormat": "Memory", "refId": "B" }
  ]
}
```

### After (Jsonnet)

```jsonnet
// Common query targets
local cpuQuery = { expr: 'rate(cpu_usage[5m])', refId: 'A' };
local memoryQuery = { expr: 'rate(memory_usage[5m])', refId: 'A' };

{
  targets: [
    cpuQuery + { legendFormat: 'CPU' },
    memoryQuery + { legendFormat: 'Memory' },
  ],
}
```

## Rule 8: Indentation and Formatting

Output is formatted with consistent indentation.

### Configuration

| Option | Default | Description |
|--------|---------|-------------|
| `indent_size` | 4 | Spaces per indent level |
| `max_line_length` | 120 | Maximum line length |

### Example

```jsonnet
{
  title: 'Dashboard',
  panels: [
    {
      id: 1,
      type: 'stat',
      title: 'Panel',
    },
  ],
}
```

## Rule 9: Import Statements

Optional import statements can be added for external libraries.

### Configuration

- **Enabled by default**: `include_imports: false`
- **When enabled**: Adds import statements for referenced template files

### Example

```jsonnet
import 'templates/panels.libsonnet';

{
  panels: [
    panels.statPanel('Title', { x: 0, y: 0, w: 12, h: 8 }, [], 'prometheus'),
  ],
}
```

## Transformation Options

### TransformOptions

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `validate` | `bool` | `True` | Validate JSON structure |
| `min_pattern_occurrences` | `int` | `2` | Minimum occurrences for pattern detection |
| `extract_repeated` | `bool` | `True` | Extract repeated values |
| `create_templates` | `bool` | `True` | Create panel templates |
| `add_comments` | `bool` | `True` | Add comments to output |
| `include_imports` | `bool` | `False` | Include import statements |
| `indent_size` | `int` | `4` | Spaces per indent level |
| `max_line_length` | `int` | `120` | Maximum line length |

## Transformation Pipeline

```
JSON Input
    ↓
Parser (validate and parse JSON)
    ↓
Analyzer (extract dashboard data)
    ↓
Pattern Detector (find repeated patterns)
    ↓
Code Generator (create Jsonnet output)
    ↓
Jsonnet Output
```

### Step 1: Parse JSON

- Validate JSON structure
- Extract dashboard object
- Handle errors gracefully

### Step 2: Analyze Dashboard

- Extract panel data
- Identify panel types
- Collect metadata

### Step 3: Detect Patterns

- Find repeated values
- Identify common configurations
- Calculate pattern frequency

### Step 4: Generate Code

- Create local variables
- Build panel templates
- Format output