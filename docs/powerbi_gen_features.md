## Using Filters

The filters at the bottom of each page allow you to focus the dashboard on specific parts of the AGS dataset.

Common filters include:

- **Project ID** – filters the report to a specific project.
- **Location Cluster** – filters by location cluster if this field is present in the AGS data.
- **Source File** – filters by the original AGS source file.
- **Location Type** – filters by investigation type, such as CP, DP, RC, WS or other recorded hole types.
- **GEOL_GEOL** – filters by the primary geology code.
- **GEOL_GEO2** – filters by the interpreted geology or second geology code.
- **Location ID** – filters by individual borehole or investigation location.

Filters can be used to narrow the dashboard down to one borehole, one geological unit, one investigation type or one source file.

For example, you may want to:

- View only one borehole.
- Compare SPT results in clay only.
- Check all records from one source AGS file.
- View only rotary core holes.
- Look at PSD curves from a small number of selected locations.

!!! tip
    If a chart is very busy, apply filters to reduce the number of records shown. This is especially useful on pages such as Particle Size Distribution, where many curves can overlap.


## Dynamic Units and Axis Labels

A key feature of the dashboard is that units and axis labels are shown dynamically where possible.

This means the dashboard reads unit information from the imported AGS data, rather than relying only on fixed hard-coded labels.

This helps users understand:

- What measurement is being plotted.
- Which unit is being used.
- Whether the displayed values match the source AGS file.
- Which axis has been selected on charts where the user can switch between depth and elevation.

Units are shown in small units tables or panels on the report pages.

For example, a plot may show:

- X-axis: `N Value`
- Y-axis: `Elevation (mAOD)`

or:

- X-axis: `Liquid Limit (%)`
- Y-axis: `Plasticity Index`

This is useful because AGS files can vary between projects, and users need to be confident that values are being interpreted with the correct units.


