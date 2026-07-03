![OpenLog logo](https://geolandia.gitlab.io/openlog/openlog-documentation/_static/logo.png)

==TD This process needs to be tested by someone new to it.==

OpenLog is a freely available QGIS plugin that enables the user to view legends, soil descriptions and graphical data with depth.
It is extremely useful for quickly viewing exploratory hole information. It is **not** intended to be a way of presenting logs in a report.

A sample output is shown below. The soil descriptions are dynamic, in that they become visible as the user zooms into the log.

![Example OpenLog layout](assets/ss_openlog_example.png)
/// caption
Screenshot of QGIS showing the OpenLog graphical logs and soil descriptions.
///


There is very useful guidance available via the [OpenLog user guide](https://geolandia.gitlab.io/openlog/openlog-documentation/usage/user_manual.html)

!!! note
    The OpenLog guidance is not reproduced here because the official guidance will always be more up to date. However please ignore the video at the top of the official guidance page. It refers to a database type that is not recommended.

OpenLog requires mapping of the GeoPackage data to their specific spatialite database. This is not a complicated process, but it does involve several steps.

1. Create a spatialite database [help](https://geolandia.gitlab.io/openlog/openlog-documentation/usage/user_manual.html#spatialite-standalone)

!!! note
    Use the [spatialite option](https://geolandia.gitlab.io/openlog/openlog-documentation/usage/user_manual.html#spatialite-standalone) , not the xplordb option when creating a database


2. After creating the spatialite database, [connect to it](https://geolandia.gitlab.io/openlog/openlog-documentation/usage/user_manual.html#to-spatialite) and

3. add data by following the guidance [here](https://geolandia.gitlab.io/openlog/openlog-documentation/usage/user_manual.html#importing-data)

4. Import tabular [downhole data](https://geolandia.gitlab.io/openlog/openlog-documentation/usage/user_manual.html#import-tabular-downhole-data)

!!! note
    There is no need to add survey data.

!!! tip
    Select 'depth' for Domain if in doubt.

    Select 'extended' for geology information and 'discrete' for test information e.g. SPT.

Add as much information as you wish, but note that space on a screen is limited, so keep it as simple as possible.

!!! tip
    In the Column definition part of the Downhole data import screen there are data type options. Normally these will be one of three:
    1. 'NOMINAL' - e.g. soil descriptions (GEOL_DESC)

    2. 'CATEGORICAL' e.g. Legend codes (GEOL_LEG) or

    3. 'NUMERICAL' e.g. SPT test results (SPT_NAL)

Once the data has been imported the logs are [ready for viewing](https://geolandia.gitlab.io/openlog/openlog-documentation/usage/user_manual.html#striplog-visualization)

The legend graphics can be changed using the functionality shown [here](https://geolandia.gitlab.io/openlog/openlog-documentation/usage/user_manual.html#extended-categorical-data)

!!! note
    The developers of OpenLog have made an [AGS file-friendly interface](https://geolandia.gitlab.io/openlog/openlog-documentation/usage/user_manual.html#import-ags-files), however this is part of their Premium (paid-for) offering. The use of the GeoPackage file created using the ags-tools plugin offers a very similar experience.

