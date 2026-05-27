import pandas as pd


def _extract_original_source_file(source_file_value: str) -> str:
    """Return original AGS filename from lineage value like 'ags|folder|proj'."""
    if source_file_value is None:
        return ""
    text = str(source_file_value).strip()
    if not text:
        return ""
    return text.split("|")[0].strip()


def _sources_for_table(df: pd.DataFrame, fallback_source_file: str) -> list:
    """Get unique original source filenames represented by this table."""
    if df is not None and "source_file" in df.columns:
        values = (
            df["source_file"]
            .fillna("")
            .astype(str)
            .str.strip()
        )
        values = values[values != ""]
        source_files = sorted({
            _extract_original_source_file(v)
            for v in values
            if _extract_original_source_file(v)
        })
        if source_files:
            return source_files

    source_name = _extract_original_source_file(fallback_source_file)
    return [source_name] if source_name else [""]


def build_ags_column_metadata_df(
    exported_tables: dict,
    fallback_source_file: str,
    parser_column_metadata: dict = None,
) -> pd.DataFrame:
    """
    Build one metadata row per exported column.

    Output columns:
    - table_name
    - column_name
    - unit
    - ags_type
    - source_file
    """
    parser_column_metadata = parser_column_metadata or {}
    rows = []

    for table_name, df in exported_tables.items():
        if df is None:
            continue

        table_meta = parser_column_metadata.get(table_name, {})
        source_files = _sources_for_table(df, fallback_source_file)

        # Preserve column order exactly as exported.
        for col_name in list(df.columns):
            meta = table_meta.get(col_name, {})
            unit_val = meta.get("unit", "") if isinstance(meta, dict) else ""
            ags_type_val = meta.get("ags_type", "") if isinstance(meta, dict) else ""

            unit_val = "" if unit_val is None else str(unit_val).strip()
            ags_type_val = "" if ags_type_val is None else str(ags_type_val).strip()

            for source_name in source_files:
                rows.append({
                    "table_name": table_name,
                    "column_name": col_name,
                    "unit": unit_val,
                    "ags_type": ags_type_val,
                    "source_file": source_name,
                })

    out = pd.DataFrame(
        rows,
        columns=["table_name", "column_name", "unit", "ags_type", "source_file"],
    )

    # Ensure empty strings, not None/NaN, for unit/type/source_file.
    for col in ["unit", "ags_type", "source_file", "table_name", "column_name"]:
        if col in out.columns:
            out[col] = out[col].fillna("").astype(str)

    return out
