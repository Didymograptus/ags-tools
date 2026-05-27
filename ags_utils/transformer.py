# Schema mapping for all AGS groups found in sample_file.ags.
# Each transform method reads the raw AGS group, passes all native columns through
# unchanged, and injects plugin-generated fields (source_file, samp_id, lat, lon).
# Column names in output CSVs match the AGS headings exactly (uppercase) so that
# Power BI relationships and column references never break across files.

import pandas as pd
from .geo_utils import bng_to_wgs84
from ..expected_groups import (
    GROUPS_WITH_SAMP_ID,
    ELEVATION_DEPTH_COLUMNS,
    GEOLOGY_INTERVAL_DEPTH_COLUMNS,
)


class AGSTransformer:
    # All constants imported from expected_groups as the single source of truth
    ELEVATION_DEPTH_COLUMNS = ELEVATION_DEPTH_COLUMNS
    GROUPS_WITH_SAMP_ID = GROUPS_WITH_SAMP_ID
    GEOLOGY_INTERVAL_DEPTH_COLUMNS = GEOLOGY_INTERVAL_DEPTH_COLUMNS

    def __init__(self, parser, source_file: str):
        self.parser = parser
        self.source_file = source_file
        (
            self.geol_leg_lookup,
            self.geol_geo2_lookup,
            self.geol_geol_lookup,
            self.loca_gl_lookup,
        ) = self._build_filter_lookups()
        self.geol_intervals_lookup = self._build_geol_intervals_lookup()

    # ------------------------------------------------------------------ #

    def _empty_df(self, table_name: str) -> pd.DataFrame:
        """Returns an empty DataFrame for a group that has no data in the AGS file."""
        return pd.DataFrame()

    def _safe_float(self, val):
        try:
            return float(val)
        except (ValueError, TypeError):
            return None

    def _build_lookup(self, group_name: str, value_col: str) -> dict:
        df = self.parser.get_group(group_name)
        if df is None or "LOCA_ID" not in df.columns or value_col not in df.columns:
            return {}
        lookup_df = (
            df[["LOCA_ID", value_col]]
            .dropna(subset=["LOCA_ID"])
            .drop_duplicates(subset=["LOCA_ID"])
        )
        lookup_df["LOCA_ID"] = lookup_df["LOCA_ID"].astype(str)
        return lookup_df.set_index("LOCA_ID")[value_col].to_dict()

    def _build_filter_lookups(self):
        return (
            self._build_lookup("GEOL", "GEOL_LEG"),
            self._build_lookup("GEOL", "GEOL_GEO2"),
            self._build_lookup("GEOL", "GEOL_GEOL"),
            self._build_lookup("LOCA", "LOCA_GL"),
        )

    def _build_geol_intervals_lookup(self):
        df = self.parser.get_group("GEOL")
        if df is None or not {"LOCA_ID", "GEOL_TOP", "GEOL_BASE"}.issubset(df.columns):
            return {}

        cols = ["LOCA_ID", "GEOL_TOP", "GEOL_BASE"] + \
               [c for c in ["GEOL_GEO2", "GEOL_LEG", "GEOL_GEOL"] if c in df.columns]
        geol_df = df[cols].copy()
        geol_df["LOCA_ID"] = geol_df["LOCA_ID"].astype(str)
        geol_df["GEOL_TOP"] = geol_df["GEOL_TOP"].apply(self._safe_float)
        geol_df["GEOL_BASE"] = geol_df["GEOL_BASE"].apply(self._safe_float)
        geol_df = geol_df.dropna(subset=["LOCA_ID", "GEOL_TOP", "GEOL_BASE"])

        return {
            loca_id: sorted(
                group.to_dict("records"),
                key=lambda x: (x["GEOL_TOP"], x["GEOL_BASE"])
            )
            for loca_id, group in geol_df.groupby("LOCA_ID")
        }

    def _map_geol_value_by_interval(self, out: pd.DataFrame, table_name: str, value_column: str):
        depth_col = self.GEOLOGY_INTERVAL_DEPTH_COLUMNS.get(table_name)
        if depth_col is None or depth_col not in out.columns:
            return None
        if "LOCA_ID" not in out.columns or not self.geol_intervals_lookup:
            return None

        loca_ids = out["LOCA_ID"].where(out["LOCA_ID"].notna(), "").astype(str)
        depths = out[depth_col].apply(self._safe_float)
        values = []

        for loca_id, depth in zip(loca_ids, depths):
            matched_value = None
            if depth is not None:
                for interval in self.geol_intervals_lookup.get(loca_id, []):
                    geol_top = interval.get("GEOL_TOP")
                    geol_base = interval.get("GEOL_BASE")
                    if geol_top is None or geol_base is None:
                        continue
                    if geol_top <= depth < geol_base:
                        matched_value = interval.get(value_column)
                        break
            values.append(matched_value)

        return pd.Series(values, index=out.index)

    def _inject_elevation(self, out: pd.DataFrame, table_name: str) -> pd.DataFrame:
        """
        Calculate and inject ELEV_* columns for all depth columns in this table.
        Formula: ELEV_<depth_col> = LOCA_GL - <depth_col>

        Creates one ELEV_* column for each depth column found in the table.
        """
        depth_cols = self.ELEVATION_DEPTH_COLUMNS.get(table_name, [])
        if not depth_cols:
            return out

        if "LOCA_ID" not in out.columns:
            return out

        loca_ids = out["LOCA_ID"].where(out["LOCA_ID"].notna(), "").astype(str)
        loca_gl = loca_ids.map(self.loca_gl_lookup).apply(self._safe_float)

        # For each depth column in this table, create an ELEV_* column
        for depth_col in depth_cols:
            elev_col_name = f"ELEV_{depth_col}"

            # Only calculate if the depth column exists in the dataframe
            if depth_col in out.columns:
                depth = out[depth_col].apply(self._safe_float)
                out[elev_col_name] = [
                    round(gl - d, 2) if (gl is not None and d is not None) else None
                    for gl, d in zip(loca_gl, depth)
                ]

        return out

    def _inject_filter_columns(self, out: pd.DataFrame, table_name: str = None) -> pd.DataFrame:
        """
        Injects calculated filter columns (e.g., GEOL_LEG, GEOL_GEO2, GEOL_GEOL) into the DataFrame.
        """
        tables_with_geology = {
            "GEOL", "CORE", "DLOG", "DETL", "SAMP", "SPEC", "DOBS", "DISC",
            "SCPT", "ISPT", "TRIT", "CBRT", "DCPT", "DPRG",
            "WETH", "FRAC", "FGHG", "FLSH", "IDEN", "ISAG"
        }
        if table_name not in tables_with_geology or "LOCA_ID" not in out.columns:
            return out

        loca_ids = out["LOCA_ID"].where(out["LOCA_ID"].notna(), "").astype(str)
        lookups = {"GEOL_LEG": self.geol_leg_lookup, "GEOL_GEO2": self.geol_geo2_lookup, "GEOL_GEOL": self.geol_geol_lookup}

        for col_name, lookup in lookups.items():
            mapped = self._map_geol_value_by_interval(out, table_name, col_name)
            if mapped is None:
                mapped = loca_ids.map(lookup)
            if col_name in out.columns:
                out[col_name] = out[col_name].where(out[col_name].notna(), mapped)
            else:
                out[col_name] = mapped

        return out

    def _pass_through(self, df: pd.DataFrame, table_name: str,
                      extra_cols: dict = None) -> pd.DataFrame:
        """
        Generic pass-through: takes all columns from the raw AGS DataFrame,
        drops FILE_FSET, injects source_file and any extra_cols, then
        injects elevation and filter columns.
        
        Column order is not enforced — raw AGS column order is preserved.
        """
        out = df.copy()
        out.drop(columns=[c for c in ["FILE_FSET"] if c in out.columns], inplace=True)
        out.insert(0, "source_file", self.source_file)
        if extra_cols:
            for col, values in extra_cols.items():
                out.insert(0, col, values)
        out = self._inject_elevation(out, table_name)
        return self._inject_filter_columns(out, table_name)

    def _samp_id_series(self, df: pd.DataFrame) -> pd.Series:
        """Builds the composite samp_id for sample-linked tables."""
        return df.get("LOCA_ID", "").astype(str) + "_" + \
               df.get("SAMP_REF", "").astype(str) + "_" + \
               df.get("SAMP_TOP", "").astype(str)

    def available_tables(self) -> list:
        """Return AGS groups discovered in the loaded file, in file order."""
        return [name for name, df in self.parser.tables.items() if df is not None]

    def transform_table(self, table_name: str) -> pd.DataFrame:
        """
        Transform any AGS table with best-effort strategy:
        1. Check for explicit special-case method (e.g., transform_loca)
        2. Else use generic pass-through with samp_id injection if applicable

        Args:
            table_name: AGS group name in original uppercase (e.g. 'LOCA', 'SAMP', 'ISPT')

        Returns:
            Transformed DataFrame with source_file, samp_id, ELEV_*, filters injected
        """
        # Special case: LOCA has custom coordinate handling
        if table_name == "LOCA":
            return self.transform_loca()

        # Generic path: get raw data, inject samp_id if needed, pass through
        df = self.parser.get_group(table_name)
        if df is None:
            return self._empty_df(table_name)

        extra_cols = None
        if table_name in self.GROUPS_WITH_SAMP_ID:
            extra_cols = {"samp_id": self._samp_id_series(df)}

        return self._pass_through(df, table_name, extra_cols=extra_cols)

    # ================================================================== #
    # Special case: LOCA transformation with BNG→WGS84 conversion        #
    # ================================================================== #

    def transform_loca(self) -> pd.DataFrame:
        """Special handling for LOCA: derives WGS84 lat/lon from BNG coords."""
        df = self.parser.get_group("LOCA")
        if df is None:
            return self._empty_df("LOCA")

        out = df.drop(columns=[c for c in ["FILE_FSET"] if c in df.columns], inplace=False)
        out.insert(0, "source_file", self.source_file)

        eastings = out.get("LOCA_NATE", pd.Series(dtype=object)).apply(self._safe_float)
        northings = out.get("LOCA_NATN", pd.Series(dtype=object)).apply(self._safe_float)
        latlon = [
            bng_to_wgs84(e, n) if (e and n) else (None, None)
            for e, n in zip(eastings, northings)
        ]
        out["lat"] = [ll[0] for ll in latlon]
        out["lon"] = [ll[1] for ll in latlon]
        return self._inject_filter_columns(out, "LOCA")

