"""
Main Transformation Pipeline

Orchestrates the JSON to Jsonnet transformation process.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from pathlib import Path

from .parser import parse_json, parse_json_string, extract_dashboard_data, validate_grafana_dashboard
from .analyzer import analyze_dashboard, DashboardAnalysis
from .patterns import PatternDetector
from .generator import JsonnetGenerator, GeneratorOptions


@dataclass
class TransformOptions:
    """Options for the transformation process."""
    # Parser options
    validate: bool = True
    
    # Analyzer options
    min_pattern_occurrences: int = 2
    
    # Generator options
    extract_repeated: bool = True
    create_templates: bool = True
    add_comments: bool = True
    include_imports: bool = False
    indent_size: int = 4
    max_line_length: int = 120
    
    # Output options
    output_file: Optional[str] = None
    overwrite: bool = False


@dataclass
class TransformResult:
    """Result of a transformation."""
    success: bool
    jsonnet_code: str
    analysis: Optional[DashboardAnalysis]
    patterns: List[Any]
    errors: List[str]
    warnings: List[str]
    output_file: Optional[str] = None


class TransformationError(Exception):
    """Exception raised when transformation fails."""
    pass


def transform(
    input_file: str,
    options: Optional[TransformOptions] = None,
) -> TransformResult:
    """
    Transform a JSON file to Jsonnet.
    
    Args:
        input_file: Path to the input JSON file.
        options: Transformation options.
        
    Returns:
        A TransformResult containing the result and metadata.
    """
    options = options or TransformOptions()
    errors = []
    warnings = []
    
    # Parse JSON
    parse_result = parse_json(input_file)
    if parse_result.errors:
        errors.extend(parse_result.errors)
        return TransformResult(
            success=False,
            jsonnet_code='',
            analysis=None,
            patterns=[],
            errors=errors,
            warnings=warnings,
        )
    
    data = parse_result.data
    
    # Validate if requested
    if options.validate:
        validation_errors = validate_grafana_dashboard(data)
        if validation_errors:
            errors.extend(validation_errors)
            # Don't fail on validation, just warn
            warnings.extend([f'Validation warning: {e}' for e in validation_errors])
    
    # Extract dashboard data
    dashboard_data = extract_dashboard_data(data)
    
    # Analyze dashboard
    analysis = analyze_dashboard(dashboard_data)
    
    # Detect patterns
    detector = PatternDetector(min_occurrences=options.min_pattern_occurrences)
    patterns = detector.detect(dashboard_data)
    
    # Generate Jsonnet
    generator_options = GeneratorOptions(
        indent_size=options.indent_size,
        max_line_length=options.max_line_length,
        extract_repeated=options.extract_repeated,
        create_templates=options.create_templates,
        add_comments=options.add_comments,
        include_imports=options.include_imports,
    )
    
    generator = JsonnetGenerator(generator_options)
    jsonnet_code = generator.generate(analysis)
    
    # Write output if specified
    output_file = None
    if options.output_file:
        output_path = Path(options.output_file)
        if output_path.exists() and not options.overwrite:
            warnings.append(f'Output file exists: {options.output_file}')
        else:
            try:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(jsonnet_code)
                output_file = str(output_path)
            except IOError as e:
                errors.append(f'Failed to write output file: {e}')
    
    return TransformResult(
        success=len(errors) == 0,
        jsonnet_code=jsonnet_code,
        analysis=analysis,
        patterns=patterns,
        errors=errors,
        warnings=warnings,
        output_file=output_file,
    )


def transform_string(
    json_string: str,
    options: Optional[TransformOptions] = None,
) -> TransformResult:
    """
    Transform a JSON string to Jsonnet.
    
    Args:
        json_string: The JSON string to transform.
        options: Transformation options.
        
    Returns:
        A TransformResult containing the result and metadata.
    """
    options = options or TransformOptions()
    errors = []
    warnings = []
    
    # Parse JSON string
    try:
        from .parser import parse_json_string
        data = parse_json_string(json_string)
    except Exception as e:
        errors.append(f'Failed to parse JSON: {e}')
        return TransformResult(
            success=False,
            jsonnet_code='',
            analysis=None,
            patterns=[],
            errors=errors,
            warnings=warnings,
        )
    
    # Validate if requested
    if options.validate:
        validation_errors = validate_grafana_dashboard(data)
        if validation_errors:
            errors.extend(validation_errors)
            warnings.extend([f'Validation warning: {e}' for e in validation_errors])
    
    # Extract dashboard data
    dashboard_data = extract_dashboard_data(data)
    
    # Analyze dashboard
    analysis = analyze_dashboard(dashboard_data)
    
    # Detect patterns
    detector = PatternDetector(min_occurrences=options.min_pattern_occurrences)
    patterns = detector.detect(dashboard_data)
    
    # Generate Jsonnet
    generator_options = GeneratorOptions(
        indent_size=options.indent_size,
        max_line_length=options.max_line_length,
        extract_repeated=options.extract_repeated,
        create_templates=options.create_templates,
        add_comments=options.add_comments,
        include_imports=options.include_imports,
    )
    
    generator = JsonnetGenerator(generator_options)
    jsonnet_code = generator.generate(analysis)
    
    return TransformResult(
        success=len(errors) == 0,
        jsonnet_code=jsonnet_code,
        analysis=analysis,
        patterns=patterns,
        errors=errors,
        warnings=warnings,
    )


def transform_with_templates(
    input_file: str,
    template_file: Optional[str] = None,
    options: Optional[TransformOptions] = None,
) -> TransformResult:
    """
    Transform a JSON file to Jsonnet with custom templates.
    
    Args:
        input_file: Path to the input JSON file.
        template_file: Optional path to custom template file.
        options: Transformation options.
        
    Returns:
        A TransformResult containing the result and metadata.
    """
    # For now, just use the standard transform
    # Custom templates can be added later
    return transform(input_file, options)


def create_dashboard_from_template(
    template_name: str,
    params: Dict[str, Any],
) -> str:
    """
    Create a dashboard from a built-in template.
    
    Args:
        template_name: Name of the template ('kubernetes', 'prometheus', etc.).
        params: Template parameters.
        
    Returns:
        Jsonnet code for the dashboard.
    """
    templates = {
        'kubernetes': _create_kubernetes_template,
        'prometheus': _create_prometheus_template,
        'empty': _create_empty_template,
    }
    
    if template_name not in templates:
        raise TransformationError(f'Unknown template: {template_name}')
    
    return templates[template_name](params)


def _create_kubernetes_template(params: Dict[str, Any]) -> str:
    """Create a Kubernetes dashboard template."""
    cluster_name = params.get('cluster_name', 'my-cluster')
    namespace = params.get('namespace', 'default')
    
    return f'''// Kubernetes Dashboard for {cluster_name}
// Generated by Grafana Dashboard JSON to Jsonnet Transformer

{{
  title: 'Kubernetes Cluster - {cluster_name}',
  uid: 'kubernetes-{cluster_name}',
  tags: ['kubernetes', 'cluster', '{namespace}'],
  timezone: 'browser',
  schemaVersion: 38,
  version: 1,
  
  panels: [
    // Cluster overview panels would go here
  ],
  
  time: {{
    from: 'now-6h',
    to: 'now'
  }},
  
  refresh: '5s'
}}
'''


def _create_prometheus_template(params: Dict[str, Any]) -> str:
    """Create a Prometheus metrics dashboard template."""
    job_name = params.get('job_name', 'prometheus')
    
    return f'''// Prometheus Dashboard for {job_name}
// Generated by Grafana Dashboard JSON to Jsonnet Transformer

{{
  title: 'Prometheus - {job_name}',
  uid: 'prometheus-{job_name}',
  tags: ['prometheus', 'metrics'],
  timezone: 'browser',
  schemaVersion: 38,
  version: 1,
  
  panels: [
    // Prometheus query panels would go here
  ],
  
  time: {{
    from: 'now-1h',
    to: 'now'
  }},
  
  refresh: '15s'
}}
'''


def _create_empty_template(params: Dict[str, Any]) -> str:
    """Create an empty dashboard template."""
    title = params.get('title', 'New Dashboard')
    
    return f'''// {title}
// Generated by Grafana Dashboard JSON to Jsonnet Transformer

{{
  title: '{title}',
  tags: [],
  timezone: 'browser',
  schemaVersion: 38,
  version: 1,
  
  panels: [],
  
  time: {{
    from: 'now-6h',
    to: 'now'
  }}
}}
'''