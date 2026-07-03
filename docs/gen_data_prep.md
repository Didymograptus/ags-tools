
In order to make the most of the ags-tools suite of applications the AGS data file must be valid and of sufficient data quality for the type of analysis and visualisation that needs to be undertaken.

Checking the AGS file format for validity is explained [here](/ags-nh-data-vis-docs/ags_tools_validator/).

For example if markers of all exploratory holes are to be plotted on a map, or aerial photo then 100% of the exploratory hole co-ordinated (LOCA_NATE and LOCA_NATN) must be populated, with values that reflect the real-wold position of the exploratory holes and 100% of the exploratory holes must have the correct ID (LOCA_ID). However, for the purposes of this visualisation, the data started, or the sample information is not needed.

On the other hand if the user wished to create a plot of SPT vs Depth. then the exploratory co-ordinate information is not useful, but the insitu test depth and results are. (ISPT_DPTH and ISPT_NVAL)

Data quality therefore should be considered in the context of the use of the data.

!!! warning
    GDMS only requires **75%** population of the co-ordinate data, so do not assume that the AGS data held has the level of data quality required for all purposes.

## Data quality

When assessing the quality of data it is useful to consider different aspects of data that together provide a measure of data quality.
These aspects are termed 'dimensions' and are:

- Accuracy
- Completeness
- Uniqueness
- Consistency
- Timeliness
- Validity
- Integrity
- Currency
- Reasonableness

The definitions are set out in the DAMA DMBOK publication.

The main dimensions that are relevant to AGS data used in analysis are: Completeness, Validity Integrity, Uniqueness and Reasonableness. Examples are given below:

|Term|Example|
|----|-------|
|Validity|Is the final depth of the hole (LOCA_FDEP a positive number)|
|Completeness|Have all the exploratory holes been assigned co-ordinates (LOCA_NATE and LOCA_NATN)|
|Integrity|Does the base depth of a strat match the top depth of the one below it (GEOL_BASE, GEOL_TOP)|
|Uniqueness|Do all the top depth of strata in a single exploratiory hole have a unique value (GEOL_TOP)|
|Reasonableness|Does a sample described as stiff clay have a strength test that matches the description (SAMP_DESC)|

!!! note
    The AGS file format checks for some of the dimensions, such as Uniqueness and Validity, however it only checks against the format requirements (keysets and data types) It does not check the data itself.

The AGS has created a tool to enable the dimensions to be quantified against criteria and assessed. Further information about the tool can be found [here](https://ags4-validator-desktop-app-43aa52.gitlab.io/data_quality_assessments/)

The visualisation summary tool in the ags-tools plugin provides an immediate, graphical way of looking at the data. It can flag any obvious outliers of data (Reasonablenss and/or Validity) and missing data (Completeness).

!!! note
    Note that the Accuracy of data can only be assessed where the real world values are known. e.g. Location ID.
