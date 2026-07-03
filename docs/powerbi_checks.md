Before relying on the dashboard outputs, users should carry out a few simple checks.


- Confirm that the folder name, project ID, project name and source file are correct on the Project Summary page.
- Use the AGS Data Loaded table to confirm which AGS groups were imported and whether they contain records.
- Review the units panels on each page, especially before using plots for reporting or interpretation.
- If charts are difficult to read, apply filters to focus on specific boreholes, geology codes or location types.
- If a page has no data, check whether the relevant AGS table exists and contains records.


## Troubleshooting

### Empty pages

Some pages may appear empty if the imported AGS file does not contain the relevant test data.

This does not necessarily mean the dashboard has failed.

For example:

- If there are no SPT records, the **SPT Analysis** page may be empty.
- If there are no Atterberg Limits records, the **Atterberg Limits** page may be empty.
- If there are no rock testing records, the **Rock & Material Properties** page may be empty.
- If there are no PSD records, the **Particle Size Distribution** page may be empty.

The **Project Summary** page can be used to check which AGS groups have been imported and whether data is present.

### The Dashboard Opens but Charts Are Empty

Check that:

- The correct folder path was entered.
- The folder contains the generated CSV files.
- The files have not been renamed.
- The AGS to CSV conversion completed successfully.
- The relevant AGS tables contain data.

### The Wrong Project Appears

Check that the FolderPath points to the intended CSV output folder.

If needed, reopen the template or edit the parameter and load the correct folder.

### Some Pages Are Empty

This usually means the AGS dataset does not contain that type of data.

For example, the Rock & Material Properties page will be empty if there are no UCS, point load, density or moisture content records.

### A Plot Looks Too Busy

Apply filters at the bottom of the page to reduce the number of displayed records.

For example, filter by one borehole, one geological unit or one source file.

### Units Look Unexpected

Check the units stored in the source AGS file and review the dynamic units table on the relevant page.


