#!/usr/bin/env python3
"""
Package the Grafana Dashboard JSON to Jsonnet Transformer skill.

This script validates the skill structure and creates a distributable zip file.
"""

import os
import zipfile
import json
import sys
from pathlib import Path
from datetime import datetime


class SkillPackager:
    """Package a skill for distribution."""
    
    def __init__(self, skill_path: str = ".", output_dir: str = "./dist"):
        self.skill_path = Path(skill_path)
        self.output_dir = Path(output_dir)
        self.errors = []
        self.warnings = []
    
    def validate(self) -> bool:
        """Validate the skill structure."""
        print("Validating skill structure...")
        
        # Check for SKILL.md
        skill_md = self.skill_path / "SKILL.md"
        if not skill_md.exists():
            self.errors.append("SKILL.md not found")
        else:
            print("  ✓ SKILL.md found")
            self._validate_skill_md(skill_md)
        
        # Check for skill.json
        skill_json = self.skill_path / "skill.json"
        if not skill_json.exists():
            self.warnings.append("skill.json not found (optional)")
        else:
            print("  ✓ skill.json found")
            self._validate_skill_json(skill_json)
        
        # Check for scripts directory
        scripts_dir = self.skill_path / "scripts"
        if not scripts_dir.exists():
            self.errors.append("scripts/ directory not found")
        else:
            print("  ✓ scripts/ directory found")
        
        # Check for references directory
        references_dir = self.skill_path / "references"
        if not references_dir.exists():
            self.warnings.append("references/ directory not found (optional)")
        else:
            print("  ✓ references/ directory found")
        
        # Check for assets directory
        assets_dir = self.skill_path / "assets"
        if not assets_dir.exists():
            self.warnings.append("assets/ directory not found (optional)")
        else:
            print("  ✓ assets/ directory found")
        
        # Report results
        if self.errors:
            print("\nErrors:")
            for error in self.errors:
                print(f"  ✗ {error}")
        
        if self.warnings:
            print("\nWarnings:")
            for warning in self.warnings:
                print(f"  ⚠ {warning}")
        
        return len(self.errors) == 0
    
    def _validate_skill_md(self, path: Path):
        """Validate SKILL.md format."""
        content = path.read_text()
        
        # Check for YAML frontmatter
        if not content.startswith("---"):
            self.errors.append("SKILL.md missing YAML frontmatter")
            return
        
        # Parse frontmatter
        lines = content.split("\n")
        frontmatter_lines = []
        in_frontmatter = False
        
        for i, line in enumerate(lines):
            if line.strip() == "---":
                if not in_frontmatter:
                    in_frontmatter = True
                    continue
                else:
                    frontmatter_lines = lines[1:i]
                    break
        
        if not frontmatter_lines:
            self.errors.append("SKILL.md empty or malformed frontmatter")
            return
        
        # Check for required fields
        frontmatter = "\n".join(frontmatter_lines)
        if "name:" not in frontmatter:
            self.errors.append("SKILL.md missing 'name' in frontmatter")
        if "description:" not in frontmatter:
            self.errors.append("SKILL.md missing 'description' in frontmatter")
        
        print("  ✓ SKILL.md frontmatter valid")
    
    def _validate_skill_json(self, path: Path):
        """Validate skill.json format."""
        try:
            with open(path) as f:
                data = json.load(f)
            
            # Check for required fields
            if "name" not in data:
                self.errors.append("skill.json missing 'name'")
            if "description" not in data:
                self.errors.append("skill.json missing 'description'")
            
            print("  ✓ skill.json format valid")
        except json.JSONDecodeError as e:
            self.errors.append(f"skill.json invalid JSON: {e}")
    
    def package(self, skill_name: str = None) -> str:
        """Package the skill into a zip file."""
        if not self.validate():
            print("\nValidation failed. Fix errors before packaging.")
            sys.exit(1)
        
        # Determine skill name
        if not skill_name:
            skill_name = self.skill_path.name
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Create zip file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_name = f"{skill_name}_{timestamp}.zip"
        zip_path = self.output_dir / zip_name
        
        print(f"\nPackaging skill to {zip_path}...")
        
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            # Add SKILL.md
            skill_md = self.skill_path / "SKILL.md"
            if skill_md.exists():
                zipf.write(skill_md, "SKILL.md")
                print("  ✓ Added SKILL.md")
            
            # Add skill.json
            skill_json = self.skill_path / "skill.json"
            if skill_json.exists():
                zipf.write(skill_json, "skill.json")
                print("  ✓ Added skill.json")
            
            # Add scripts directory
            scripts_dir = self.skill_path / "scripts"
            if scripts_dir.exists():
                for file in self._iterate_directory(scripts_dir):
                    arcname = file.relative_to(self.skill_path)
                    zipf.write(file, str(arcname))
                print(f"  ✓ Added scripts/ ({len(list(scripts_dir.rglob('*')))} files)")
            
            # Add references directory
            references_dir = self.skill_path / "references"
            if references_dir.exists():
                for file in self._iterate_directory(references_dir):
                    arcname = file.relative_to(self.skill_path)
                    zipf.write(file, str(arcname))
                print(f"  ✓ Added references/ ({len(list(references_dir.rglob('*')))} files)")
            
            # Add assets directory
            assets_dir = self.skill_path / "assets"
            if assets_dir.exists():
                for file in self._iterate_directory(assets_dir):
                    arcname = file.relative_to(self.skill_path)
                    zipf.write(file, str(arcname))
                print(f"  ✓ Added assets/ ({len(list(assets_dir.rglob('*')))} files)")
        
        print(f"\n✓ Skill packaged successfully: {zip_path}")
        return str(zip_path)
    
    def _iterate_directory(self, path: Path):
        """Iterate over all files in a directory."""
        for file in path.rglob("*"):
            if file.is_file():
                yield file


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Package a skill for distribution")
    parser.add_argument(
        "--path", "-p", default=".", help="Path to skill directory"
    )
    parser.add_argument(
        "--output", "-o", default="./dist", help="Output directory for zip file"
    )
    parser.add_argument(
        "--name", "-n", help="Name for the packaged skill"
    )
    parser.add_argument(
        "--validate-only", action="store_true", help="Only validate, don't package"
    )
    
    args = parser.parse_args()
    
    packager = SkillPackager(args.path, args.output)
    
    if args.validate_only:
        success = packager.validate()
        sys.exit(0 if success else 1)
    else:
        zip_path = packager.package(args.name)
        print(f"\nPackaged skill: {zip_path}")


if __name__ == "__main__":
    main()