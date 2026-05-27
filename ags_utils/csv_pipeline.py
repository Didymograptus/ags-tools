"""
Unified CSV export pipeline for AGS data.

This module provides a single, reusable CSV export function that can be called
from any source (AGS file, database, etc.) that has been transformed via AGSTransformer.

Used by:
- ags_2_csv.py: AGS file → CSV
- ags_2_db_algorithm.py: AGS file → DB + CSV
- db_2_csv_algorithm.py: Database → CSV
"""

from .exporter import CSVExporter
from .column_metadata import build_ags_column_metadata_df


def export_ags_to_csv(transformer, output_dir, append_mode=False, feedback=None):
    """
    Generic CSV export from any AGSTransformer instance.

    Handles:
    - Table discovery
    - Transformation (elevation, filters, samp_id)
    - CSV writing with dedup/append logic
    - Manifest generation

    Args:
        transformer: AGSTransformer instance with source_file set
        output_dir: Output directory for CSV files
        append_mode: If True, append to existing CSVs; if False, overwrite
        feedback: Optional QGIS feedback object for logging (with pushInfo/reportError)

    Returns:
        Dict with export statistics: {"tables_exported": int, "total_rows": int}
    """
    if feedback is None:
        feedback = _NoOpFeedback()

    exporter = CSVExporter(output_dir, append_mode=append_mode)
    stats = {"tables_exported": 0, "total_rows": 0}
    exported_tables = {}

    try:
        # Discover all tables from transformer
        tables = transformer.available_tables()
        feedback.pushInfo(f"Exporting {len(tables)} table(s) to CSV...")

        for table in tables:
            # Allow cancellation via feedback object (QGIS-specific)
            if hasattr(feedback, 'isCanceled') and feedback.isCanceled():
                feedback.pushInfo("CSV export cancelled by user.")
                break

            try:
                # Transform the table (adds samp_id, elevation, filters as needed)
                df = transformer.transform_table(table)

                # Write to CSV with dedup/append logic
                exporter.write(table, df, transformer.source_file)
                exported_tables[table] = df

                stats["tables_exported"] += 1
                stats["total_rows"] += len(df)
                feedback.pushInfo(f"  Transformed {table}.csv ({len(df)} rows)")

            except Exception as e:
                feedback.reportError(f"Error transforming {table}: {str(e)}")

        # Write column metadata CSV (one row per exported column)
        parser_column_metadata = getattr(transformer.parser, "column_metadata", {})
        metadata_df = build_ags_column_metadata_df(
            exported_tables=exported_tables,
            fallback_source_file=transformer.source_file,
            parser_column_metadata=parser_column_metadata,
        )
        exporter.write_column_metadata(metadata_df)

        # Write manifest
        exporter.write_manifest()
        feedback.pushInfo("CSV export complete — manifest.csv and ags_column_metadata.csv written")

    except Exception as e:
        feedback.reportError(f"CSV export failed: {str(e)}")
        raise

    return stats


class _NoOpFeedback:
    """Fallback feedback object for non-QGIS contexts."""
    def pushInfo(self, msg):
        print(msg)

    def reportError(self, msg):
        print(f"ERROR: {msg}")
