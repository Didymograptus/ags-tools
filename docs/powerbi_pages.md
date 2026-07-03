
The following sections explain each page in the template and how to use it. Use the index on the right to jump to the area of interest.

## Project Summary Page

The **Project Summary** page is the first page shown after the AGS CSV folder has been loaded.

This page gives an overview of the imported dataset and helps confirm that the correct project has been loaded.

It answers four important questions:

1. Which project has been loaded?
2. Which AGS source file has been imported?
3. Where are the investigation locations?
4. Which AGS tables contain data?

==Screenshot Placeholder – Project Summary Page==

==Paste screenshot here:==

==![Project Summary page](path/to/screenshot.png)==


### Folder Name / Report Title

The large title at the top of the page is generated from the selected folder name.

This helps users quickly confirm which AGS CSV folder is currently being visualised.

### Project Information Table

The project information table summarises key project metadata from the AGS data.

It typically includes:

- **Project ID**
- **Project Name**
- **Location**
- **Source File**

This provides a quick check that the correct AGS file and project have been loaded.

### Borehole Location Map

The map shows the investigation locations contained in the AGS dataset.

Each point represents a borehole or investigation location from the `LOCA` table.

The map uses latitude and longitude values generated from the northing and easting coordinates during the AGS to CSV conversion process.

The points are coloured by **Hole Type** or **Location Type**, allowing users to distinguish between different investigation methods, such as cable percussion, dynamic probing, rotary core, window sample or other recorded types.

Users can:

- Zoom in and out.
- Pan around the site.
- Hover over points to view location information.
- Select points to filter related information on the page.

### AGS Data Loaded Table

The **AGS Data Loaded** table shows which AGS groups were imported from the CSV folder.

For each AGS group, it displays information such as:

- AGS group name.
- Number of rows imported.
- Whether the table contains data.
- Export date.
- Source file.

This table is useful for checking whether the expected AGS tables are present.

For example, if the SPT page is empty, the user can check whether the `ISPT` table contains data.

### Location Details Table

The **Location Details** table provides a summary of the investigation locations.

It typically includes:

- **Hole ID**
- **Hole Type**
- **Final Hole Depth**
- **Source File**

This allows users to quickly review which boreholes or investigation points are available in the dataset.

### Report-Wide Filters

The filters at the bottom of the Project Summary page are also used throughout the report.

Selections made here can be used to focus the dashboard on a specific project, source file, hole type, geological unit or location ID.

---

## SPT Analysis Page

The **SPT Analysis** page displays Standard Penetration Test results from the AGS data.

It allows users to review how SPT N-values vary with depth or elevation, and how those values relate to the recorded geology.

==Screenshot Placeholder – SPT Analysis Page==

==Paste screenshot here:==

==![SPT Analysis page](path/to/screenshot.png)==


### SPT N-Value Plot

The main scatter plot shows SPT results.

Each point represents one SPT record.

The points are coloured by geology, allowing users to compare SPT values across different geological units.

### X-Axis Selection

The X-axis can be changed depending on what value the user wants to plot.

Available options may include:

- **N Value** – the recorded SPT N-value.
- **N60 Value** – the energy-corrected N-value, where available.

If N60 values are not present in the AGS dataset, the N60 option may not provide useful results.

### Y-Axis Selection

The Y-axis can be changed to show either:

- **SPT Depth** – depth below ground level.
- **SPT Elevation** – elevation in metres above ordnance datum, where available.

Elevation is useful when comparing results across boreholes with different ground levels. Depth is useful when reviewing data relative to the ground surface.

### Summary Cards

The summary cards provide quick statistics for the currently selected data.

They typically show:

- **Average N** – the average SPT N-value.
- **Number of SPT Tests** – the total number of SPT records currently displayed.
- **Maximum Depth** – the deepest SPT record in the current selection.

These values update automatically when filters are applied.

### SPT Results Table

The table lists the SPT records used in the plot.

It may include:

- Location ID.
- Elevation.
- N-value.
- Geological legend.
- Geological unit.
- Other available AGS fields.

This table is useful when the user wants to inspect the actual values behind the plotted points.

### Notes Section

The notes section provides important interpretation notes.

For example, the dashboard may state that values shown in the table are raw N-values unless corrected values are specifically selected.

Users should check this note before using the results for interpretation or reporting.

---

## Atterberg Limits Page

The **Atterberg Limits** page displays Liquid Limit and Plasticity Index results from laboratory testing.

It allows users to view test results on a standard plasticity chart and compare results by geological unit.

==Screenshot Placeholder – Atterberg Limits Page==

==Paste screenshot here:==

==![Atterberg Limits page](path/to/screenshot.png)==

### Plasticity Chart

The main chart plots:

- **X-axis:** Liquid Limit (%)
- **Y-axis:** Plasticity Index (%)

Each point represents one Atterberg Limits test.

The points are coloured by interpreted geology, allowing users to see how plasticity varies between geological units.

### Static Plasticity Chart Background

The plasticity chart includes a static background image showing standard classification boundaries.

This includes features such as:

- A-line.
- Clay and silt regions.
- Low, intermediate, high, very high and extremely high plasticity zones.

The background is provided as a visual aid. The dashboard plots the AGS data onto the chart but does not replace engineering interpretation.

### Summary Cards

The summary cards provide an overview of the filtered Atterberg Limits data.

They typically include:

- **Average Liquid Limit**
- **Number of Tests**
- **Average Plasticity Index**

These update automatically as filters are applied.

### Atterberg Limits Table

The table lists the laboratory records used in the plot.

It typically includes:

- Location ID.
- Liquid Limit.
- Plasticity Index.
- Sample top depth.
- Geological unit.

This allows users to check the source values behind the chart.

### Units Panel

The units panel confirms the variables and units used on the plot, such as Liquid Limit (%) and Plasticity Index.

---

## Geology Summary Page

The **Geology Summary** page provides a project-wide overview of the geological units recorded in the AGS dataset.

It is useful for checking stratigraphy, reviewing layer thicknesses and comparing top elevations across boreholes.

==Screenshot Placeholder – Geology Summary Page==

==Paste screenshot here:==

==![Geology Summary page](path/to/screenshot.png)==


### GEOL_GEOL Stratigraphy Summary

This table summarises the primary geology codes from the `GEOL_GEOL` field.

For each geology code, the table may show:

- Minimum layer thickness.
- Average layer thickness.
- Maximum layer thickness.
- Minimum top elevation.
- Average top elevation.
- Maximum top elevation.

This gives a quick overview of the thickness and elevation range of each primary geological unit.

### GEOL_GEO2 Stratigraphy Summary

This table provides a similar summary using the interpreted geology field, `GEOL_GEO2`.

This is helpful where `GEOL_GEO2` has been used to simplify or standardise geology descriptions across the dataset.

### Stratigraphy by Hole – GEOL_GEOL Top Elevations

This table compares geology across boreholes using the primary geology code.

Each row represents a location ID, and each column represents a geology code.

The values show the top elevation at which that geological unit is encountered.

This helps users compare the relative level of strata across the site.

### Stratigraphy by Hole – GEOL_GEO2 Top Elevations

This table provides the same type of comparison using the interpreted geology field.

It is useful for quickly reviewing simplified stratigraphic trends across the site.

### Geological Map

The map shows the investigation locations, coloured by geology.

This allows users to review the spatial distribution of geological units across the project area.

---

## Undrained Shear Strength Cu Page

The **Undrained Shear Strength Cu** page compares measured undrained shear strength values with estimated values derived from SPT correlations.

This allows users to review laboratory triaxial test results alongside empirical estimates from SPT data.

==Screenshot Placeholder – Undrained Shear Strength Cu Page==

==Paste screenshot here:==

==![Undrained Shear Strength Cu page](path/to/screenshot.png)==

### Measured Cu from Triaxial Tests

The left-hand plot shows measured undrained shear strength values from triaxial testing.

Each point represents a laboratory test result, typically extracted from the `TRIT` table.

The plot shows:

- **X-axis:** Measured Cu, usually in kPa.
- **Y-axis:** Sample depth or sample elevation.

The points are coloured by geology.

### Estimated Cu from SPT Correlation

The right-hand plot shows estimated undrained shear strength values calculated from SPT results.

These values are based on an empirical correlation using the selected **F1 factor**.

This allows users to compare estimated Cu values with measured laboratory results where both datasets are available.

### F1 Factor

The **F1 factor** control allows the user to adjust the correlation used to estimate Cu from SPT data.

Changing the F1 factor updates the estimated Cu plot automatically.

For example, where the dashboard uses a relationship such as:

```text
Estimated Cu = F1 × SPT N-value
```

increasing the F1 factor will increase the estimated Cu values shown on the plot.

> **Important**
> Estimated Cu values are indicative and depend on the selected empirical factor. They should be used with engineering judgement and compared with measured laboratory data where available.

### Axis Selection

Both plots allow the Y-axis to be changed between depth and elevation.

This allows users to review strength values either relative to ground level or relative to a common elevation datum.

---

## Rock & Material Properties Page

The **Rock & Material Properties** page displays laboratory rock and material test results where these are present in the AGS file.

This page may appear empty if the example AGS dataset or user-selected AGS file does not contain rock testing data.

==Screenshot Placeholder – Rock & Material Properties Page==

==Paste screenshot here:==

==![Rock and Material Properties page](path/to/screenshot.png)==

### Uniaxial Compressive Strength

The Uniaxial Compressive Strength plot displays UCS results, typically from the `RUCS` table.

The plot shows UCS values against either sample depth or sample elevation.

### Point Load Strength Index

The Point Load plot displays point load test results, typically from the `RPLT` table.

It allows users to review point load strength index values against depth or elevation.

### Dry Density

The Dry Density plot displays dry density values, typically from the relevant density testing table such as `RDEN`.

Results can be viewed against sample depth or sample elevation.

### Moisture Content

The Moisture Content plot displays moisture content results from laboratory testing.

Results can also be viewed against depth or elevation.

### Axis Selection

Each chart includes a selector allowing the user to choose whether the vertical axis shows:

- **Sample Depth**
- **Sample Elevation**

### Dynamic Units

The units table beneath the plots shows the units and axis labels for the displayed test results.

These are read from the AGS data where available.

---

## Particle Size Distribution Page

The **Particle Size Distribution** page displays laboratory particle size distribution curves.

It allows users to compare grading curves between samples, boreholes and geological units.

==Screenshot Placeholder – Particle Size Distribution Page==

==Paste screenshot here:==

==![Particle Size Distribution page](path/to/screenshot.png)==


### PSD Chart

The main chart plots PSD curves using data from AGS particle size distribution tables, such as `GRAG` and `GRAT`.

The chart shows:

- **X-axis:** Particle size, usually in millimetres.
- **Y-axis:** Percentage passing.

Each line represents an individual PSD test.

The legend identifies each curve using the location ID and sample depth, allowing users to identify which sample each curve relates to.

### Static PSD Background

The chart uses a static Particle Size Distribution background image as an underlay.

This background provides familiar grading chart context, including:

- Clay.
- Silt.
- Sand.
- Gravel.
- Cobbles.
- Standard sieve size divisions.

The plotted lines are overlaid onto this background.

> **Note**
> The PSD background is a visual guide. The dashboard plots the imported AGS laboratory data onto the chart but does not alter or reinterpret the source data.

### Filtering PSD Curves

PSD charts can become difficult to read when many curves are shown at once.

For clearer review, users should filter by:

- Location ID.
- Geological unit.
- Location type.
- Source file.
- Project ID.

This allows smaller groups of curves to be compared more clearly.



