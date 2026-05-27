# Copyright (C) 2020-2026  Asitha Senanayake
#
# This file is part of python_ags4.
#
# python_ags4 is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# https://github.com/asitha-sena/python-ags4
# https://gitlab.com/ags-data-format-wg/ags-python-library

import logging

logger = logging.getLogger(__name__)


# Read functions #

def AGS4_to_dict(filepath_or_buffer, encoding='utf-8', get_line_numbers=False, rename_duplicate_headers=True):
    """Load all the data in an AGS4 file to a dictionary of dictionaries.

    Each GROUP in the AGS4 file is assigned its own dictionary.

    'AGS4_to_dataframe()' function uses this function to load AGS4 data in to
    Pandas dataframes.

    Parameters
    ----------
    filepath_or_buffer : File path (str, pathlib.Path), or StringIO.
        Path to AGS4 file or any object with a read() method (such as an open
        file or StringIO).
    encoding : str, default='utf-8'
        Encoding of text file. This can be set to 'utf-8-sig' to read files that
        begin with a byte-order-mark.
    get_line_numbers : bool, default=False
        Add line number column to each table (for UNIT, TYPE, and DATA rows) and
        return a dictionary with line numbers for GROUP and HEADING lines.
    rename_duplicate_headers: bool, default=True
        Rename duplicate headers if found. Neither AGS4 tables nor Pandas
        dataframes allow duplicate headers, therefore a number will be appended
        to duplicates to make them unique.

    Returns
    -------
    data : dict of dicts
        Dictionary populated with data from the AGS4 file with AGS4 headers as
        keys.
    headings : dict of lists
        Dictionary with the headings in the each GROUP (This will be needed to
        recall the correct column order when writing Pandas dataframes back to
        AGS4 files. i.e. input for 'dataframe_to_AGS4()' function)
    line_numbers : dict of int, only if get_line_numbers=True
        Dictionary with the starting line numbers of GROUP and HEADING rows.
        This is only required for checking a .ags file with 'check_file()'
        function.
    """

    import csv
    from io import StringIO

    if _is_file_like(filepath_or_buffer):
        f = filepath_or_buffer
        f.seek(0)
        if hasattr(f, 'encoding') and getattr(f, 'encoding', None) != encoding and hasattr(f, 'reconfigure'):
            f.reconfigure(encoding=encoding)
        close_file = False
    else:
        # Read file with errors="replace" to catch UnicodeDecodeErrors
        f = open(filepath_or_buffer, "r", encoding=encoding, errors="replace")
        close_file = True

    try:

        data = {}
        headings = {}
        line_numbers = {}

        # NOTE: The 'headings' dict is not really necessary for the read AGS4
        # function but will be needed to write the columns of Pandas dataframes
        # when writing them back to AGS4 files. (The HEADING column needs to be
        # the first column in order to preserve the AGS data format. Other
        # columns in certain groups have a preferred order as well)

        # Initialize variable to track current group
        group = None

        for i, line in enumerate(f, start=1):
            if _is_bytebuffer(line):
                line = line.decode(encoding)

            else:
                # Strip byte-order mark from line, if present
                line = _remove_byte_order_mark(line, encoding)

            line = list(csv.reader(StringIO(line), quotechar='"'))[0]

            if len(line) == 0:
                # This indicates a blank line so assume that the current group has ended
                group = None

                continue

            elif line[0] == 'GROUP':
                group = line[1]

                # Raise exception if duplicate group is found as previous copy
                # of that group will be overwritten
                if group in data.keys():
                    msg = f"{group} group duplicated in Line {i}. Cannot parse file without overwriting data, "\
                           "therefore please combine all duplicate groups first."

                    logger.error(msg)
                    raise AGS4Error(msg)

                else:
                    data[group] = {}

                # Store GROUP line number (A default 'HEADING' entry is added to
                # avoid KeyErrors in case of missing HEADING rows)
                line_numbers[group] = {'GROUP': i, 'HEADING': '-'}

            elif line[0] == 'HEADING':

                if group is None:
                    msg = f"HEADER row in Line {i} is not associated with a GROUP. "\
                        "Please ensure that the GROUP name is defined in the line immediately preceding the HEADER row."

                    logger.error(msg)
                    raise AGS4Error(msg)

                # Catch HEADER rows with duplicate entries as it will result in
                # a dictionary with arrays of unequal lengths and cause a
                # ValueError when trying to convert to a Pandas dataframe
                if len(line) != len(set(line)):

                    if rename_duplicate_headers is False:
                        raise AGS4Error(f"HEADER row in {group} (Line {i}) has duplicate entries")

                    logger.warning(f"HEADER row in {group} (Line {i}) has duplicate entries.")

                    # Rename duplicate headers by appending a number
                    item_count = {}

                    for i, item in enumerate(line):
                        if item not in item_count:
                            item_count[item] = {'i': i, 'count': 0}
                        else:
                            item_count[item]['i'] = i
                            item_count[item]['count'] += 1
                            count = item_count[item]['count']

                            line[i] = line[i]+'_'+str(item_count[item]['count'])

                            logger.info(f'Duplicate column {item} found and renamed as {item}_{count}. '
                                        'Automatically renamed columns do not conform to AGS4 Rules 19a and 19b. '
                                        'Therefore, please review the data and rename or drop duplicate columns as appropriate.')

                # Store HEADING line number
                line_numbers[group]['HEADING'] = i

                # Store UNIT, TYPE, and DATA line numbers
                if get_line_numbers is True:
                    line.append('line_number')

                headings[group] = line

                for item in line:
                    data[group][item] = []

            elif line[0] in ['TYPE', 'UNIT', 'DATA']:

                # Append line number
                if get_line_numbers is True:
                    line.append(i)

                # Check whether line has the same number of entries as the
                # number of headings in the group. If not, print error and exit.
                if len(line) != len(headings[group]):
                    logger.error(f"Line {i} does not have the same number of entries as the HEADING row in {group}.")
                    raise AGS4Error(f"Line {i} does not have the same number of entries as the HEADING row in {group}.")

                for i in range(0, len(line)):
                    data[group][headings[group][i]].append(line[i])

            else:
                continue
    finally:
        if close_file:
            f.close()

    if get_line_numbers is True:
        return data, headings, line_numbers

    return data, headings


def AGS4_to_dataframe(filepath_or_buffer, encoding='utf-8', get_line_numbers=False, rename_duplicate_headers=True,
                      only_groups=None):
    """Load all the tables in an AGS4 file to a dictionary of Pandas dataframes.

    The output is a dictionary of dataframes with the name of each AGS4 table
    (i.e. GROUP) as the primary key.

    Parameters
    ----------
    filepath_or_buffer : str, StringIO
        Path to AGS4 file or any file like object (open file or StringIO).
    encoding : str, default='utf-8'
        Encoding of text file. This can be set to 'utf-8-sig' to read files that
        begin with a byte-order-mark.
    get_line_numbers : bool, default=False
        Add line number column to each table (for UNIT, TYPE, and DATA rows) and
        return a dictionary with line numbers for GROUP and HEADING lines.
    rename_duplicate_headers: bool, default=True
        Rename duplicate headers if found. Neither AGS4 tables nor Pandas
        dataframes allow duplicate headers, therefore a number will be appended
        to duplicates to make them unique.
    only_groups : list or None (default=None)
        An optional list of groups to convert instead of converting all the
        groups in the input file.

    Returns
    -------
    tables : dict of dataframes
        Dictionary populated with Pandas dataframes. Each GROUP in the AGS4
        files is assigned to its a dataframe.
    headings : dict of lists
        Dictionary with the headings in the each GROUP (This will be needed to
        recall the correct column order when writing Pandas dataframes back to
        AGS4 files. i.e. input for 'dataframe_to_AGS4()' function)
    line_numbers : dict of int, only if get_line_numbers=True
        Dictionary with the starting line numbers of GROUP and HEADING rows.
        This is only required for checking a .ags file with 'check_file()'
        function.

    """

    from pandas import DataFrame

    # Extract AGS4 file into a dictionary of dictionaries. A dictionary with
    # group line numbers is returned, in addition to data and headings, for
    # checking purposes.
    if get_line_numbers is True:
        data, headings, line_numbers = AGS4_to_dict(filepath_or_buffer, encoding=encoding, get_line_numbers=get_line_numbers,
                                                    rename_duplicate_headers=rename_duplicate_headers)

        # Convert dictionary of dictionaries to a dictionary of Pandas
        # dataframes
        tables = {}
        for key in data:
            tables[key] = DataFrame(data[key])

        return tables, headings, line_numbers

    # Otherwise only the data and the headings are returned
    data, headings = AGS4_to_dict(filepath_or_buffer, encoding=encoding,
                                  rename_duplicate_headers=rename_duplicate_headers)

    # Convert dictionary of dictionaries to a dictionary of Pandas dataframes
    tables = {}

    if only_groups:
        for key in only_groups:
            tables[key] = DataFrame(data[key])
    else:
        for key in data:
            tables[key] = DataFrame(data[key])

    return tables, headings


def format_numeric_column(dataframe, column_name, TYPE):
    '''Format column in dataframe to specified TYPE and convert to string.

    Parameters
    ----------
    dataframe : Pandas DataFrame
        Pandas DataFrame with AGS4 data
    column_name : str
        Name of column to be formatted
    TYPE : str
        AGS4 TYPE for specified column

    Returns
    -------
    Pandas DataFrame
        Dataframe with formatted data.
    '''

    df = dataframe.copy()
    col = column_name

    # Convert data type to 'object' since adding string values to numeric
    # columns raises a FutureWarning as it will not be supported in future
    # version of Pandas.
    df[col] = df[col].astype('object')

    try:
        if 'DP' in TYPE:
            i = int(TYPE.strip('DP'))
            # Apply formatting DATA rows with real numbers. NaNs will be avoided so that they will be exported
            # as "" rather than "nan"
            mask = (df.HEADING == "DATA") & df[col].notna()
            df.loc[mask, col] = df.loc[mask, col].apply(lambda x: f"{x:.{i}f}")

        elif 'SCI' in TYPE:
            i = int(TYPE.strip('SCI'))
            # Apply formatting DATA rows with real numbers. NaNs will be avoided so that they will be exported
            # as "" rather than "nan"
            mask = (df.HEADING == "DATA") & df[col].notna()
            df.loc[mask, col] = df.loc[mask, col].apply(lambda x: f"{x:.{i}E}")

        elif 'SF' in TYPE:

            # Apply formatting DATA rows with real numbers. NaNs will be avoided so that they will be exported
            # as "" rather than "nan"
            mask = (df.HEADING == "DATA") & df[col].notna()
            df.loc[mask, [col]] = df.loc[mask, [col]].map(lambda x: _format_SF(x, TYPE))

        else:
            pass

    except ValueError:
        logger.warning(f"Numeric data in {col:<9} not reformatted as it had one or more non-numeric entries.")

    except TypeError:
        logger.warning(f"Numeric data in {col:<9} not reformatted as it had one or more non-numeric entries.")

    return df


def _format_SF(value, TYPE):
    '''Format a value to specified number of significant figures
    and return a string.'''

    from math import log10, floor

    # Avoid log(0) as int(log(0)) will raise an OverflowError
    if value != 0:
        i = int(TYPE.strip('SF')) - 1 - int(floor(log10(abs(value))))

    else:
        return f"{value}"

    if i < 0:
        return f"{round(value, i):.0f}"

    else:
        return f"{value:.{i}f}"



def _is_file_like(obj):
    """Check if object is file like

    Returns
    -------
    bool
        Return True if obj is file like, otherwise return False
    """

    if not (hasattr(obj, 'read') or hasattr(obj, 'write')):
        return False

    if not hasattr(obj, "__iter__"):
        return False

    return True


def _is_bytebuffer(obj):
    """Check if object is buffer like

    Returns
    -------
    bool
        Return True if obj is buffer like, otherwise return False
    """

    if hasattr(obj, 'decode'):
        return True

    return False


def _remove_byte_order_mark(string, encoding):
    """Remove byte-order mark from string.
    """

    import codecs

    string_without_BOM = string.encode(encoding)\
                               .strip(codecs.BOM_UTF8)\
                               .strip(codecs.BOM)\
                               .strip(codecs.BOM_BE)\
                               .strip(codecs.BOM_LE)\
                               .decode(encoding)

    return string_without_BOM


class AGS4Error(Exception):
    """Exception class for AGS4 parsing errors.
    """
    pass
