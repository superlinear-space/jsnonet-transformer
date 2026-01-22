# Jsonnet Syntax Guide

Jsonnet is a data templating language that extends JSON with features like variables, functions, and object composition.

## Basic Syntax

### Local Variables

Define local variables using the `local` keyword:

```jsonnet
local colors = {
  green: '#73bf69',
  red: '#f2495c',
  blue: '#5794f2',
};
```

### Strings

Strings can use single or double quotes:

```jsonnet
local title = 'My Dashboard';
local description = "Grafana Dashboard";
```

Multi-line strings use triple quotes:

```jsonnet
local multiline = |||
  This is a
  multi-line
  string
|||;
```

### Numbers

```jsonnet
local count = 42;
local pi = 3.14159;
local negative = -10;
```

### Booleans

```jsonnet
local enabled = true;
local disabled = false;
local null_value = null;
```

## Functions

### Basic Functions

Define functions with parameters:

```jsonnet
local add(a, b) = a + b;
local result = add(1, 2);  // result = 3
```

### Functions with Default Arguments

```jsonnet
local greet(name, greeting = 'Hello') = greeting + ' ' + name;
local hello = greet('World');           // Hello World
local hi = greet('Claude', 'Hi');       // Hi Claude
```

### Functions with Multiple Expressions

```jsonnet
local max(a, b) = if a > b then a else b;
```

## Object Composition

### Basic Objects

```jsonnet
{
  name: 'Dashboard',
  version: 1,
}
```

### Object Inheritance

Use `+` to merge objects:

```jsonnet
local base = {
  title: 'My Dashboard',
  timezone: 'browser',
};

local extended = base + {
  version: 2,
  tags: ['kubernetes'],
};
```

### Object Super

Use `+:` to override fields:

```jsonnet
local base = {
  panels: [],
};

local extended = base + {
  panels+: [
    { title: 'New Panel' },
  ],
};
```

## Arrays

### Array Literals

```jsonnet
local numbers = [1, 2, 3, 4, 5];
local mixed = [1, 'two', true, null];
```

### Array Comprehensions

```jsonnet
local squares = [x * x for x in [1, 2, 3, 4, 5]];  // [1, 4, 9, 16, 25]

local even_squares = [x * x for x in [1, 2, 3, 4, 5] if x % 2 == 0];  // [4, 16]
```

### Array Operations

```jsonnet
local first = [1, 2, 3][0];           // 1
local length = std.length([1, 2, 3]); // 3
local combined = [1, 2] + [3, 4];     // [1, 2, 3, 4]
```

## Standard Library

Jsonnet includes a standard library with useful functions:

### String Functions

```jsonnet
local upper = std.toUpper('hello');   // 'HELLO'
local lower = std.toLower('WORLD');   // 'world'
local split = std.split('a,b,c', ','); // ['a', 'b', 'c']
```

### Array Functions

```jsonnet
local sum = std.sum([1, 2, 3, 4, 5]);  // 15
local map_double = std.map(function(x) x * 2, [1, 2, 3]); // [2, 4, 6]
local filter_even = std.filter(function(x) x % 2 == 0, [1, 2, 3, 4]); // [2, 4]
```

### Type Functions

```jsonnet
local is_string = std.isString('hello');      // true
local is_number = std.isNumber(42);           // true
local type_of = std.type(42);                 // 'number'
```

### Other Functions

```jsonnet
local abs = std.abs(-5);                      // 5
local floor = std.floor(3.7);                 // 3
local ceil = std.ceil(3.2);                   // 4
local format = std.format('%.2f', 3.14159);   // '3.14'
```

## Imports

### Importing Jsonnet Files

```jsonnet
// Import a library file
local panels = import 'templates/panels.libsonnet';

// Import with alias
local utils = import 'lib/utils.jsonnet';
```

### Importing JSON Files

```jsonnet
// Import a JSON file (automatically parsed)
local config = import 'config.json';
```

## Conditionals

### If Statements

```jsonnet
local value = if x > 0 then 'positive' else 'non-positive';
```

### If-ElseIf-Else

```jsonnet
local grade = if score >= 90 then 'A'
              else if score >= 80 then 'B'
              else if score >= 70 then 'C'
              else 'F';
```

## Grafana-Specific Patterns

### Panel Template Function

```jsonnet
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
```

### Usage

```jsonnet
statPanel(
  'Cluster CPU Usage',
  { x: 0, y: 1, w: 8, h: 8 },
  [{ expr: '...', refId: 'A' }],
  'prometheus'
)
```

### Data Source Configuration

```jsonnet
local datasources = {
  prometheus: { type: 'prometheus', url: 'http://prometheus:9090' },
  loki: { type: 'loki', url: 'http://loki:3100' },
};
```

### Color Theme

```jsonnet
local colors = {
  green: '#73bf69',
  red: '#f2495c',
  blue: '#5794f2',
  orange: '#ff780a',
  purple: '#b877d9',
  yellow: '#ffab40',
};
```

### Threshold Configuration

```jsonnet
local defaultThresholds = {
  mode: 'absolute',
  steps: [
    { color: 'green', value: null },
    { color: 'yellow', value: 70 },
    { color: 'red', value: 90 },
  ],
};
```

## Common Patterns

### Conditional Field Addition

```jsonnet
{
  title: 'Dashboard',
  // Only include 'tags' if not empty
  [if std.length(tags) > 0 then 'tags']: tags,
}
```

### Dynamic Field Names

```jsonnet
{
  ['panel_' + std.toString(i)]: { title: 'Panel ' + std.toString(i) }
  for i in std.range(1, 4)
}
```

### Merge Defaults with Panel Config

```jsonnet
local defaults = {
  transparent: false,
  gridPos: { x: 0, y: 0, w: 12, h: 8 },
};

local panel = defaults + {
  title: 'My Panel',
  type: 'stat',
};