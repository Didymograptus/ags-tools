# loading AGS file into memory as pandas DataFrames using python-ags4
# script defines a small AGSParser class that loads an AGS file into memory and makes its groups easy to access.
# once loaded it can then be transformed (in transformer.py) and exported as needed.

try:
    from python_ags4 import AGS4
except ModuleNotFoundError:
    try:
        from ags4 import AGS4
    except ModuleNotFoundError:
        AGS4 = None
from pathlib import Path


class AGSParser:
    # __init__ stores the input path, extracts the source filename, and prepares two dictionaries
    def __init__(self, filepath: str):
        self.filepath = filepath
        self.filename = Path(filepath).name
        self.tables = {}
        self.headings = {}

    # load uses python-ags4 to read the AGS file and populate the tables and headings dictionaries. It returns True if successful.
    def load(self) -> bool:
        if AGS4 is None:
            raise ModuleNotFoundError(
                "Missing AGS parser dependency. Install 'python-ags4' in the QGIS Python environment."
            )
        tables, headings = AGS4.AGS4_to_dataframe(self.filepath)
        # python-ags4 returns dicts of {GROUP_NAME: DataFrame}. Some AGS files
        # include UNIT/TYPE metadata rows in either index or HEADING column.
        # Remove these here so all downstream exports are consistently data-only.
        cleaned_tables = {}
        for group_name, df in tables.items():
            if df is None:
                cleaned_tables[group_name] = df
                continue

            out = df.copy()

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
        self.headings = headings
        return True

    # helper methods to access the loaded groups. get_group returns the DataFrame for a group or None if it doesn't exist, while has_group returns a boolean indicating whether the group is present.
    def get_group(self, group_name: str):
        """Returns DataFrame for group or None if not present."""
        return self.tables.get(group_name, None)

    def has_group(self, group_name: str) -> bool:
        return group_name in self.tables