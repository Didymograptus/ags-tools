
Use this workflow to generate cross-sections from your reviewed database.

This part of the workflow is where geotechnical interpretation becomes much more visual. A good section setup helps the team communicate strata relationships, depth trends, and ground model assumptions clearly.

## Purpose

DB to Cross-Sections creates geological section outputs for interpretation, design discussions, and reporting.

## Typical geotechnical workflow

1. Complete AGS2DB.
2. Review LOCA and GEOL content.
3. Run DB to Cross-Sections.
4. Define section line.
5. Review output visually.
6. Export PNG for issue, if required.

## Step-by-step UI guidance (DB to Cross-Sections)

1. Open Processing Toolbox.
2. Run DB to Cross-Sections.
3. Set Input DB to your GeoPackage.
4. Enter a clear section name, for example A-Ap.
5. Define Section Line using one method:
   - Leave blank for automatic line generation.
   - Enter coordinates as sx,sy,ex,ey.
   - Use interactive draw on map.
6. Set Section width buffer (m).
7. Optional: set LiDAR raster for ground profile.
8. Optional: set PNG report export.
9. Click Run.

If you are new to section work, run a first pass quickly, then refine the section line and buffer. Iteration is normal and usually improves the final output significantly.

## Practical interpretation tips

- Start with a broader buffer (500 m to 1000 m) and refine.
- Keep section names aligned with your drawing references.
- If the section is empty, first verify LOCA locations and GEOL depth data.
- If orientation is not useful, reverse or redraw the line.

It is good practice to save at least one preview PNG during drafting so project reviewers can comment on section positioning before final issue.

## Common issues and fixes

1. No section features:
   - Check LOCA and GEOL records exist.
   - Increase buffer width.
   - Ensure the section line crosses borehole extents.
2. Ground profile missing:
   - Confirm raster file path.
   - Test without raster to isolate the issue.
3. Section looks over-exaggerated:
   - Reduce vertical exaggeration and rerun.

==Screenshot Placeholders==

==[Insert screenshot: DB to Cross-Sections dialog]==

==[Insert screenshot: Section line drawing on map canvas]==

==[Insert screenshot: Generated section output window]==

==[Insert screenshot: Exported PNG preview]==




