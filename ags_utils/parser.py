# loading AGS file into memory as pandas DataFrames using  a cut-down version of python-ags4.AGS4
# script defines a small AGSParser class that loads an AGS file into memory and makes its groups easy to access.
# once loaded it can then be transformed (in transformer.py) and exported as needed.

from .AGS4 import AGS4_to_dataframe
from pathlib import Path

class AGSParser:
    # __init__ stores the input path, extracts the source filename, and prepares two dictionaries
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.filename = Path(filepath).name
        self.tables = {}
        self.headings = {}
        # Per-group, per-column metadata extracted from AGS UNIT/TYPE rows.
        # Shape: {"GROUP": {"COLUMN": {"unit": "", "ags_type": ""}}}
        self.column_metadata = {}

    # load uses python-ags4 to read the AGS file and populate the tables and headings dictionaries. It returns True if successful.
    def load(self) -> bool:

        tables, headings = AGS4_to_dataframe(self.filepath)
        # python-ags4 returns dicts of {GROUP_NAME: DataFrame}. Some AGS files
        # include UNIT/TYPE metadata rows in either index or HEADING column.
        # Remove these here so all downstream exports are consistently data-only.
        cleaned_tables = {}
        column_metadata = {}
        for group_name, df in tables.items():
            if df is None:
                cleaned_tables[group_name] = df
                column_metadata[group_name] = {}
                continue

            out = df.copy()

            # Extract per-column metadata from AGS UNIT/TYPE rows before cleanup.
            unit_row = None
            type_row = None
            if "HEADING" in out.columns:
                heading = out["HEADING"].astype(str).str.strip().str.upper()
                unit_rows = out.loc[heading == "UNIT"]
                type_rows = out.loc[heading == "TYPE"]
                if not unit_rows.empty:
                    unit_row = unit_rows.iloc[0]
                if not type_rows.empty:
                    type_row = type_rows.iloc[0]

            group_meta = {}
            for col in out.columns:
                unit_val = ""
                type_val = ""
                if unit_row is not None and col in unit_row.index:
                    raw_unit = unit_row.get(col, "")
                    unit_val = "" if raw_unit is None else str(raw_unit).strip()
                if type_row is not None and col in type_row.index:
                    raw_type = type_row.get(col, "")
                    type_val = "" if raw_type is None else str(raw_type).strip()
                group_meta[col] = {"unit": unit_val, "ags_type": type_val}
            column_metadata[group_name] = group_meta

            # Drop metadata rows when they are encoded as index labels.
            if out.index is not None:
                idx = out.index.astype(str).str.strip().str.upper()
                out = out[~idx.isin(["UNIT", "TYPE"])]

            # Drop metadata rows when they are encoded in a HEADING column.
            if "HEADING" in out.columns:
                heading = out["HEADING"].astype(str).str.strip().str.upper()
                out = out[~heading.isin(["UNIT", "TYPE"])]

            cleaned_tables[group_name] = out.reset_index(drop=True)

        self.tables = cleaned_tables
        self.column_metadata = column_metadata
        self.headings = headings
        return True

    # helper methods to access the loaded groups. get_group returns the DataFrame for a group or None if it doesn't exist, while has_group returns a boolean indicating whether the group is present.
    def get_group(self, group_name: str):
        """Returns DataFrame for group or None if not present."""
        return self.tables.get(group_name, None)

    def has_group(self, group_name: str) -> bool:
        return group_name in self.tables
