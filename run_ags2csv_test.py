"""
Standalone test: AGS → CSV workflow (no QGIS required).
Exports test/data/Esholt.ags to 'ESHOLT TEST3/' in the repo root.
"""

import os
import sys
from pathlib import Path

# Ensure repo root is on the path so 'core' imports work
repo_root = Path(__file__).parent
sys.path.insert(0, str(repo_root))

import importlib, importlib.util, types

# The repo root has an __init__.py and core/ uses relative imports (..expected_groups).
# Register the repo root as package 'ags_tools' so those relative imports resolve.
parent_dir = str(repo_root.parent)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Load the repo root folder as package 'ags_tools' (folder name has a hyphen so
# we load it manually rather than relying on the import system's name resolution).
spec = importlib.util.spec_from_file_location(
    "ags_tools", str(repo_root / "__init__.py"),
    submodule_search_locations=[str(repo_root)]
)
pkg = importlib.util.module_from_spec(spec)
pkg.__path__ = [str(repo_root)]
pkg.__package__ = "ags_tools"
sys.modules["ags_tools"] = pkg
spec.loader.exec_module(pkg)

from ags_tools.core.parser import AGSParser
from ags_tools.core.transformer import AGSTransformer
from ags_tools.core.csv_pipeline import export_ags_to_csv

AGS_FILE = repo_root / "test" / "data" / "Esholt.ags"
OUTPUT_DIR = repo_root / "ESHOLT TEST3"

def main():
    print(f"Input:  {AGS_FILE}")
    print(f"Output: {OUTPUT_DIR}")

    # 1. Parse
    parser = AGSParser(str(AGS_FILE))
    loaded = parser.load()
    print(f"Parser loaded: {loaded}, groups found: {list(parser.tables.keys())}")

    # 2. Build source_file lineage string (mimics the QGIS algorithm)
    csv_folder_name = OUTPUT_DIR.name
    proj_id = ""
    if "PROJ" in parser.tables and parser.tables["PROJ"] is not None:
        proj_df = parser.tables["PROJ"]
        if "PROJ_ID" in proj_df.columns and len(proj_df) > 0:
            proj_id = str(proj_df["PROJ_ID"].iloc[0])
    source_file = f"{AGS_FILE.name}|{csv_folder_name}|{proj_id}"
    print(f"source_file tag: {source_file}")

    # 3. Transform
    transformer = AGSTransformer(parser, source_file)

    # 4. Export
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    stats = export_ags_to_csv(transformer, str(OUTPUT_DIR), append_mode=False)
    print(f"\nDone. tables_exported={stats['tables_exported']}, total_rows={stats['total_rows']}")
    print(f"CSVs written to: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
