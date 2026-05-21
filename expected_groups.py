# Configuration for AGS CSV export enrichment.
#
# AGS groups and columns are discovered dynamically from the parsed file.
# This module defines:
#   1. Which filter columns get appended to exported tables
#   2. Which groups get samp_id injected (lab tests + samples)
#   3. Which depth columns get ELEV_* calculations per table
#   4. Fixed schemas for plugin-generated tables (meta, manifest only)

# ================================================================ #
# Filter columns appended to most AGS group exports                 #
# ================================================================ #

COMMON_FILTER_COLUMNS = ["LOCA_CLST", "LOCA_TYPE", "GEOL_LEG", "GEOL_GEO2", "GEOL_GEOL"]

# ================================================================ #
# Groups that require samp_id injection (lab tests + samples)       #
# ================================================================ #

GROUPS_WITH_SAMP_ID = {
    "SAMP", "LDEN", "LHVN", "LPEN", "LVAN", "RDEN", "RPLT", "RUCS",
    "LPDN", "LLPL", "GRAT", "GRAG", "MCVG", "LNMC", "MCVT",
    "CBRG", "CBRT", "CMPG", "CMPT", "CONG", "CONS", "SHBG", "SHBT",
    "TRIG", "TRIT", "GCHM", "ERES", "SPEC",
}

# ================================================================ #
# Depth columns per table — used to calculate ELEV_* columns        #
# Formula: ELEV_<depth_col> = LOCA_GL - <depth_col>                #
# ================================================================ #

ELEVATION_DEPTH_COLUMNS = {
    "SAMP": ["SAMP_TOP", "SAMP_BASE", "SAMP_WDEP"],
    "SPEC": ["SPEC_DPTH", "SPEC_BASE"],
    "BKFL": ["BKFL_TOP", "BKFL_BASE"],
    "CDIA": ["CDIA_DPTH"],
    "CHIS": ["CHIS_FROM", "CHIS_TO"],
    "CORE": ["CORE_TOP", "CORE_BASE"],
    "DCPG": ["DCPG_DPTH"],
    "DETL": ["DETL_TOP", "DETL_BASE"],
    "DISC": ["DISC_TOP", "DISC_BASE"],
    "DLOG": ["DLOG_TOP", "DLOG_BASE"],
    "DOBS": ["DOBS_TOP", "DOBS_BASE"],
    "DPRB": ["DPRB_DPTH"],
    "DPRG": ["DPRG_TIP"],
    "DREM": ["DREM_TOP", "DREM_BASE"],
    "FGHG": ["FGHG_TOP", "FGHG_BASE", "FGHG_HBAS", "FGHG_CAS", "FGHG_PRWL", "FGHG_AWL"],
    "FLSH": ["FLSH_TOP", "FLSH_BASE"],
    "FRAC": ["FRAC_FROM", "FRAC_TO"],
    "GEOL": ["GEOL_TOP", "GEOL_BASE"],
    "HDIA": ["HDIA_DPTH"],
    "HDPH": ["HDPH_TOP", "HDPH_BASE"],
    "HORN": ["HORN_TOP", "HORN_BASE"],
    "ICBR": ["ICBR_DPTH"],
    "IDEN": ["IDEN_DPTH"],
    "IFID": ["IFID_DPTH"],
    "IPEN": ["IPEN_DPTH"],
    "IPID": ["IPID_DPTH"],
    "IPRG": ["IPRG_TOP", "IPRG_BASE", "IPRG_PRWL", "IPRG_SWAL", "IPRG_AWL"],
    "IPRT": ["IPRT_DPTH"],
    "IRDX": ["IRDX_DPTH"],
    "IRES": ["IRES_DPTH", "IRES_BASE"],
    "ISAG": ["ISAG_DPTS", "ISAG_DPTE"],
    "ISAT": ["ISAT_DPTH"],
    "ISPT": ["ISPT_TOP", "ISPT_CAS"],
    "IVAN": ["IVAN_DPTH"],
    "LOCA": ["LOCA_FDEP"],
    "PIPE": ["PIPE_TOP", "PIPE_BASE"],
    "PLTG": ["PLTG_DPTH"],
    "PMTG": ["PMTG_DPTH"],
    "PTIM": ["PTIM_DPTH", "PTIM_CAS"],
    "PUMT": ["PUMT_DPTH"],
    "RDEN": ["SAMP_TOP", "SPEC_DPTH"],
    "RPLT": ["SAMP_TOP", "SPEC_DPTH"],
    "RUCS": ["SAMP_TOP", "SPEC_DPTH"],
    "SCDG": ["SCDG_DPTH"],
    "SCPP": ["SCPP_TOP", "SCPP_BASE"],
    "SCPT": ["SCPT_DPTH"],
    "WADD": ["WADD_TOP", "WADD_BASE"],
    "LDEN": ["SAMP_TOP", "SPEC_DPTH"],
    "LHVN": ["SAMP_TOP", "SPEC_DPTH"],
    "LPEN": ["SAMP_TOP", "SPEC_DPTH"],
    "LVAN": ["SAMP_TOP", "SPEC_DPTH"],
    "WETH": ["WETH_TOP", "WETH_BASE"],
    "WGPG": ["WGPG_STRT", "WGPG_STOP", "WGPG_BHD"],
    "WGPT": ["WGPT_DPTH"],
    "WSTG": ["WSTG_DPTH", "WSTG_SEAL", "WSTG_CAS"],
    "WSTD": ["WSTD_POST"],
    "WINS": ["WINS_TOP"],
}

# ================================================================ #
# Fixed schemas for plugin-generated tables (not AGS groups)        #
# ================================================================ #

EXPECTED_CSVS = {
    "meta": [
        "source_file", "PROJ_ID", "PROJ_NAME", "PROJ_LOC", "PROJ_CLNT",
        "PROJ_CONT", "PROJ_ENG", "PROJ_MEMO", "exported_at", "exported_by",
    ],
    "manifest": [
        "source_file", "csv_name", "ags_group", "row_count", "has_data", "exported_at",
    ],
}

# ================================================================ #
# Depth column used to map geology intervals onto other tables      #
# Maps group name → the column that holds the top-of-interval depth #
# Used in transformer to look up GEOL_LEG/GEO2/GEOL by depth       #
# ================================================================ #

GEOLOGY_INTERVAL_DEPTH_COLUMNS = {
    "SAMP": "SAMP_TOP",
    "BKFL": "BKFL_TOP",
    "DETL": "DETL_TOP",
    "WETH": "WETH_TOP",
    "CORE": "CORE_TOP",
    "HDPH": "HDPH_TOP",
    "WINS": "WINS_TOP",
    "WSTG": "WSTG_DPTH",
    "WSTD": "WSTG_DPTH",
    "ISPT": "ISPT_TOP",
    "DCPG": "DCPG_DPTH",
    "DCPT": "DCPG_DPTH",
    "ICBR": "ICBR_DPTH",
    "IPID": "IPID_DPTH",
    "IVAN": "IVAN_DPTH",
    "PTIM": "PTIM_DPTH",
    "LPDN": "SAMP_TOP",
    "LLPL": "SAMP_TOP",
    "GRAT": "SAMP_TOP",
    "GRAG": "SAMP_TOP",
    "MCVG": "SAMP_TOP",
    "LNMC": "SAMP_TOP",
    "MCVT": "SAMP_TOP",
    "LDEN": "SAMP_TOP",
    "LHVN": "SAMP_TOP",
    "LPEN": "SAMP_TOP",
    "LVAN": "SAMP_TOP",
    "CBRG": "SAMP_TOP",
    "CBRT": "SAMP_TOP",
    "CMPG": "SAMP_TOP",
    "CMPT": "SAMP_TOP",
    "CONG": "SAMP_TOP",
    "CONS": "SAMP_TOP",
    "SHBG": "SAMP_TOP",
    "SHBT": "SAMP_TOP",
    "TRIG": "SAMP_TOP",
    "TRIT": "SAMP_TOP",
    "RDEN": "SAMP_TOP",
    "RPLT": "SAMP_TOP",
    "RUCS": "SAMP_TOP",
    "GCHM": "SAMP_TOP",
    "ERES": "SAMP_TOP",
}
