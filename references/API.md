# API Reference

## Main Module (`src.main`)

### Functions

#### `transform(input_file: str, options: Optional[TransformOptions] = None) -> TransformResult`

Transform a JSON file to Jsonnet.

**Parameters:**
- `input_file` (str): Path to the input JSON file
- `options` (TransformOptions, optional): Transformation options

**Returns:**
- `TransformResult`: Contains success status, generated code, analysis, patterns, errors, and warnings

**Example:**
```python
from src import transform, TransformOptions

result = transform('dashboard.json')
if result.success:
    print(result.jsonnet_code)
else:
    print(f"Errors: {result.errors}")
```

#### `transform_string(json_string: str, options: Optional[TransformOptions] = None) -> TransformResult`

Transform a JSON string to Jsonnet.

**Parameters:**
- `json_string` (str): The JSON string to transform
- `options` (TransformOptions, optional): Transformation options

**Returns:**
- `TransformResult`: Contains success status, generated code, analysis, patterns, errors, and warnings

**Example:**
```python
from src import transform_string

json_str = '{"dashboard": {"title": "Test", "panels": []}}'
result = transform_string(json_str)
print(result.jsonnet_code)
```

### Classes

#### `TransformOptions`

Configuration options for the transformation.

**Attributes:**
- `validate` (bool): Validate JSON structure (default: True)
- `min_pattern_occurrences` (int): Minimum occurrences for pattern detection (default: 2)
- `extract_repeated` (bool): Extract repeated values (default: True)
- `create_templates` (bool): Create panel templates (default: True)
- `add_comments` (bool): Add comments to output (default: True)
- `include_imports` (bool): Include import statements (default: False)
- `indent_size` (int): Spaces per indent level (default: 4)
- `max_line_length` (int): Maximum line length (default: 120)
- `output_file` (str): Output file path (default: None)
- `overwrite` (bool): Overwrite output file (default: False)

**Example:**
```python
from src import TransformOptions

options = TransformOptions(
    extract_repeated=True,
    create_templates=True,
    add_comments=True,
    indent_size=2,
    output_file='output.jsonnet'
)
```

#### `TransformResult`

Result of a transformation.

**Attributes:**
- `success` (bool): Whether the transformation succeeded
- `jsonnet_code` (str): The generated Jsonnet code
- `analysis` (DashboardAnalysis): Analysis of the dashboard
- `patterns` (list): Detected patterns
- `errors` (list): List of errors
- `warnings` (list): List of warnings
- `output_file` (str): Path to output file if written

---

## Parser Module (`src.parser`)

### Functions

#### `parse_json_string(json_string: str) -> Dict[str, Any]`

Parse a JSON string into a Python dictionary.

**Parameters:**
- `json_string` (str): The JSON string to parse

**Returns:**
- `Dict[str, Any]`: Parsed JSON data

**Raises:**
- `JSONParseError`: If the JSON is invalid

#### `parse_json(file_path: str) -> ParseResult`

Parse a JSON file into a Python dictionary.

**Parameters:**
- `file_path` (str): Path to the JSON file

**Returns:**
- `ParseResult`: Contains data, source path, and errors

#### `validate_grafana_dashboard(data: Dict[str, Any]) -> list[str]`

Validate that the parsed JSON is a valid Grafana dashboard.

**Parameters:**
- `data` (Dict[str, Any]): The parsed JSON data

**Returns:**
- `list[str]`: List of validation errors (empty if valid)

#### `extract_dashboard_data(data: Dict[str, Any]) -> Dict[str, Any]`

Extract the dashboard data from various possible structures.

**Parameters:**
- `data` (Dict[str, Any]): The parsed JSON data

**Returns:**
- `Dict[str, Any]`: The dashboard data dictionary

### Exceptions

#### `JSONParseError`

Exception raised when JSON parsing fails.

---

## Analyzer Module (`src.analyzer`)

### Functions

#### `analyze_dashboard(data: Dict[str, Any]) -> DashboardAnalysis`

Analyze a Grafana dashboard JSON structure.

**Parameters:**
- `data` (Dict[str, Any]): The dashboard JSON data

**Returns:**
- `DashboardAnalysis`: Analysis results

### Classes

#### `DashboardAnalysis`

Analysis results for a Grafana dashboard.

**Attributes:**
- `title` (str): Dashboard title
- `uid` (str): Dashboard UID
- `tags` (list): Dashboard tags
- `timezone` (str): Dashboard timezone
- `panels` (list[PanelInfo]): List of panel analyses
- `repeated_panels` (list): List of repeated panel titles
- `repeated_values` (dict): Dictionary of repeated values
- `data_sources` (set): Set of data source references
- `panel_types` (Counter): Counter of panel types
- `common_targets` (list): List of common query targets
- `dashboard_config` (dict): Dashboard configuration

#### `PanelInfo`

Information about a single panel.

**Attributes:**
- `panel_id` (int): Panel ID
- `type` (str): Panel type
- `title` (str): Panel title
- `grid_pos` (dict): Grid position
- `targets` (list): Query targets
- `datasource` (str): Data source
- `options` (dict): Panel options
- `field_config` (dict): Field configuration
- `transformations` (list): Transformations
- `custom_properties` (dict): Custom properties

---

## Generator Module (`src.generator`)

### Classes

#### `JsonnetGenerator`

Generates Jsonnet code from analyzed dashboard data.

**Constructor:**
```python
JsonnetGenerator(options: Optional[GeneratorOptions] = None)
```

**Methods:**
- `generate(analysis: DashboardAnalysis) -> str`: Generate Jsonnet code

#### `GeneratorOptions`

Options for Jsonnet code generation.

**Attributes:**
- `indent_size` (int): Spaces per indent (default: 4)
- `max_line_length` (int): Maximum line length (default: 120)
- `extract_repeated` (bool): Extract repeated values (default: True)
- `create_templates` (bool): Create templates (default: True)
- `add_comments` (bool): Add comments (default: True)
- `include_imports` (bool): Include imports (default: True)
- `template_style` (str): Template style (default: "function")

---

## Templates Module (`src.templates`)

### Panel Templates (`src.templates.panels`)

#### `graph_panel(title, gridPos, targets=None, datasource=None, legend=None, tooltip=None, colors=None, thresholds=None, lines=True, fill=1, linewidth=1, pointradius=2, bars=False, percentage=False, stepped_line=False, **kwargs)`

Create a graph panel configuration.

#### `timeseries_panel(title, gridPos, targets=None, datasource=None, legend=None, colors=None, fillOpacity=80, showPoints='auto', unit='short', **kwargs)`

Create a timeseries panel configuration.

#### `stat_panel(title, gridPos, targets=None, datasource=None, colorMode='value', graphMode='area', justifyMode='auto', textMode='auto', unit='short', **kwargs)`

Create a stat panel configuration.

#### `gauge_panel(title, gridPos, targets=None, datasource=None, min=0, max=100, thresholds=None, showThresholdLabels=False, showThresholdMarkers=True, **kwargs)`

Create a gauge panel configuration.

#### `table_panel(title, gridPos, targets=None, datasource=None, showHeader=True, sortBy=None, columnStyles=None, **kwargs)`

Create a table panel configuration.

#### `piechart_panel(title, gridPos, targets=None, datasource=None, pieType='pie', displayLabels=None, legend=None, **kwargs)`

Create a pie chart panel configuration.

#### `barchart_panel(title, gridPos, targets=None, datasource=None, orientation='auto', barWidth=0.97, groupWidth=0.7, lineWidth=1, fillOpacity=80, gradientMode='none', **kwargs)`

Create a bar chart panel configuration.

#### `heatmap_panel(title, gridPos, targets=None, datasource=None, colorScale='spectral', cards=None, colorScheme='interpolateSpectral', **kwargs)`

Create a heatmap panel configuration.

#### `logs_panel(title, gridPos, targets=None, datasource=None, showLabels=False, showCommonLabels=False, wrapLogMessage=False, prettifyLogMessage=False, **kwargs)`

Create a logs panel configuration.

#### `text_panel(title, gridPos, content='', mode='markdown', **kwargs)`

Create a text panel configuration.

#### `create_panel_template(panel_type, title, gridPos, **kwargs)`

Create a panel configuration based on type.

### Mixins (`src.templates.mixins`)

#### `legend_mixin(show=True, displayMode='list', placement='bottom', values=None, min=False, max=False, avg=False, current=False, total=False, **kwargs)`

Create a legend configuration mixin.

#### `tooltip_mixin(shared=True, sort=0, include_null=False, **kwargs)`

Create a tooltip configuration mixin.

#### `axis_mixin(show=True, label=None, min=None, max=None, logBase=1, unit=None, decimals=None, **kwargs)`

Create an axis configuration mixin.

#### `thresholds_mixin(mode='absolute', steps=None, **kwargs)`

Create a thresholds configuration mixin.

#### `colors_mixin(scheme='standard', colors=None, **kwargs)`

Create a colors configuration mixin.

#### `apply_mixin(panel, mixin, overwrite=False)`

Apply a mixin to a panel configuration.

#### `grid_pos_mixin(x=0, y=0, w=12, h=8)`

Create a grid position mixin.

#### `datasource_mixin(type, uid='${datasource}')`

Create a datasource mixin.

#### `targets_mixin(expr, legendFormat=None, interval=None, refId='A', datasource=None)`

Create a query target mixin.

---

## Patterns Module (`src.patterns`)

### Classes

#### `PatternDetector`

Detects common patterns in Grafana dashboards.

**Constructor:**
```python
PatternDetector(min_occurrences: int = 2)
```

**Methods:**
- `detect(data: Dict[str, Any]) -> List[PatternMatch]`: Detect patterns in dashboard data
- `get_template_suggestions() -> List[str]`: Get suggestions for creating panel templates
- `get_extraction_suggestions() -> List[str]`: Get suggestions for extracting local variables

#### `PatternMatch`

A detected pattern match.

**Attributes:**
- `pattern_type` (str): Type of pattern
- `value` (Any): Pattern value
- `occurrences` (int): Number of occurrences
- `path` (str): JSON path where pattern was found
- `suggestion` (str): Suggested transformation