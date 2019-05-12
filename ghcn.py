"""Supports access and processing of GHCN data.

"""

# pylint: disable=invalid-name, locally-disabled
# pylint: disable=pointless-string-statement, locally-disabled

import sys
import os
import time
import datetime
import math
import pandas as pd

import analysis as anly


def _valsfromstr(line):
    """Create tuple of values parsed from a line in a DLY data file.

    Intended to be private to this module.
    Commented-out lines are useful for testing and debugging.

    """
    vals = ()
    for i in range(31):
        col = 21 + i * 8
        value = int(line[col:col + 5])
        # vals += (value, )
        # continue
        mflag = line[col + 5:col + 6]
        qflag = line[col + 6:col + 7]
        sflag = line[col + 7:col + 8]
        vals += (value, mflag, qflag, sflag)
        # print(str(value) + mflag + qflag + sflag)
    # print(vals)
    return vals


def _create_data_desc(data, elems):
    """Convert list of tuples from data file into data 'dictionary'.

    Intended to be private to this module.
    The returned object looks something like this...
        [
            {
                'TMAX': {
                    1944: [value1, value2, ... value366],
                },
            },
        ]

    """
    data_list = []
    for x in data:
        if x not in elems:
            continue

        keys = list(data[x])  # same as list(data[x].keys())
        if not keys:
            continue

        # Gotta be smart about filling in missing values...
        months = ((1, 31), (2, 29), (3, 31), (4, 30), (5, 31), (6, 30),
                  (7, 31), (8, 31), (9, 30), (10, 31), (11, 30), (12, 31))

        df = {}
        for y in keys:
            year_rec = data[x][y]
            df[y] = []
            for m in months:
                n_days = m[1]
                try:
                    mnth_rec = year_rec[m[0]]
                    for d in range(0, n_days * 4, 4):
                        val = int(mnth_rec[d])
                        # Replace 'bad' value with NaN or convert good value to ºF.
                        val = float('nan') if val == -9999 else round(
                            val * 0.18 + 32, 2)
                        df[y].append(val)
                except KeyError:
                    for d in range(0, n_days):
                        df[y].append(float('nan'))

            while len(df[y]) < 366:
                df[y].append(-9999)

        data_list.append({x: df})

    return {'id': data['id'], 'metadata': data['metadata'], 'data': data_list}


class Ghcn:
    """Wrapper class for Global Historical Climatology Network Daily.

    Loads list of files from local "ghcnd_all" folder and supports subsequent access.
    Each files holds data for one station
    The caaller specifies paths to data and docs folders.

    See:
    https://www.ncdc.noaa.gov/ghcnd-data-access
    Original data from: ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/

    """

    def __init__(self, root, data, docs, elems=('TMAX', )):
        """Caller passes source folder root and subdir paths.

        """
        self.elements = elems
        self.histogram = None
        self.year_added = None
        self.n_lines = 0
        self.station_metadata = {}

        self.data_path = os.path.join(root, data)
        self.docs_path = os.path.join(root, docs)
        self.files = os.listdir(self.data_path)
        # (!) Also checkout os.walk() for alternative implementations.

        self.mkstation()  # mkstation() must preceed mkhistogram() ...

        now = datetime.datetime.now()
        self.year_1st = 1763
        self.year_lst = now.year
        self.mkhistogram()  # ... mkstation() must preceed mkhistogram()

        # Remove extraneous files from the list.
        i = 0
        while i < len(self.files):
            if not self.files[i].endswith('.dly'):
                self.files.pop(i)
            else:
                i += 1

    def listfiles(self):
        """Return the list of all (found) data files.

        """
        return self.files

    def mkstation(self):
        """Capture station metadata.

        """
        filepath = os.path.join(self.docs_path, "ghcnd-stations.txt")
        print("reading '" + filepath + "'...")
        n_lines = 0
        with open(filepath) as infile:
            for line in infile:
                id_ = line[0:11]
                lat = float(line[12:20])
                lng = float(line[21:30])
                self.station_metadata[id_] = {
                    'id': id_,
                    'lat': lat,
                    'lng': lng,
                    'elv': float(line[31:37]),
                    'elems': {},
                    # 'name': line[41:71],
                }

                n_lines += 1
                if (n_lines % 1000) == 0:
                    sys.stdout.write('mkstation n_lines = ' + str(n_lines) +
                                     '\r')
                    sys.stdout.flush()

        print('mkstation n_lines = ' + str(n_lines))

    def mkhistogram(self):
        """Create a histogram of valid stations by year.

        (!) Better to create the histogram from samples in the DLY files.
            So, let's start with this and maybe update it later, too.

        """
        self.histogram = [0] * (self.year_lst - self.year_1st + 1)
        year_1st = self.year_1st
        year_lst = self.year_lst
        filepath = os.path.join(self.docs_path, "ghcnd-inventory.txt")
        print("reading '" + filepath + "'...")
        n_lines = 0
        with open(filepath) as infile:
            for line in infile:
                id_ = line[0:11]
                elem = line[31:35]
                year_bgn = int(line[36:40])
                year_end = int(line[41:45])

                if elem in self.elements:
                    year_1st = year_bgn if year_bgn < year_1st else year_1st
                    year_lst = year_end if year_end > year_lst else year_lst

                    for i in range(year_bgn - year_1st,
                                   year_end - year_1st + 1):
                        self.histogram[i] += 1

                # Each element gets its own 'years-active'.
                self.station_metadata[id_]['elems'][elem] = {
                    'yearBgn': year_bgn,
                    'yearEnd': year_end
                }

                n_lines += 1
                if (n_lines % 10000) == 0:
                    sys.stdout.write('mkhistogram n_lines = ' + str(n_lines) +
                                     '\r')
                    sys.stdout.flush()

        print('mkhistogram n_lines = ' + str(n_lines))
        #
        # Now shave off the bgn and end of the histogram if possible.
        # ...
        self.year_1st = year_1st
        self.year_lst = year_lst

    def update_histogram(self, year=-1):
        """Re-creates the stations-per-year histogram.

        Builds the histogram using only the element rows from each
        station's data file that we actually use.

        Args:
            year: The year to add to the histogram, or, if -1, a flag
                causing the histogram to be initialized.

        """
        if year == -1:
            self.histogram = [0] * (self.year_lst - self.year_1st + 1)
            return

        i = year - self.year_1st
        if not self.year_added[i] and i >= 0 and i < len(self.histogram):
            self.histogram[i] += 1
            self.year_added[i] = True

    def stations_per_year(self):
        """Return stations' histogram, etc.

        """
        return {
            'firstYear': self.year_1st,
            'lastYear': self.year_lst,
            'histo': self.histogram
        }

    def get_stations(self, elem_name, min_yrs=0, must_include=-1):
        """Get list (metadata) of qualifying stations.

        """
        stations = []
        for i in self.files:
            id_ = os.path.splitext(i)
            mdata = self.station_metadata[id_[0]]

            try:
                yr_bgn = mdata['elems'][elem_name]['yearBgn']
                yr_end = mdata['elems'][elem_name]['yearEnd']
            except KeyError:
                continue

            span = yr_end - yr_bgn + 1
            if span >= min_yrs and (must_include == -1 or
                                    (yr_bgn <= must_include
                                     and must_include <= yr_end)):
                stations.append(mdata)

        return stations

    def file_to_data(self, file, elems, mk_histo=False, min_yrs=0):
        """Read station file and convert to (local format) data dictionary.

        Some stations may not have the element type(s) we're interested in.
        If so, should we kill that station's occurence for this session?

        Args:
            file: Name of data file to read.
            elems: Tuple of elements to load and process, e.g.:
                ('TMAX', 'TMIN', 'PRCP', 'SNOW', 'SNWD')
                Note that almost all stations capture TMAX, PRCP, or both.

        """
        with open(os.path.join(self.data_path, file)) as infile:
            if mk_histo:
                self.year_added = [False] * (self.year_lst - self.year_1st + 1)

            self.n_lines = 0
            data = {}
            for e in elems:
                data[e] = {}

            for line in infile:
                elem = line[17:21]
                if self.n_lines == 0:
                    data['id'] = line[:11]
                    data['metadata'] = self.station_metadata[data['id']]

                    # Only return data for statons that cover at least min_yrs.
                    try:
                        span = data['metadata'][elem]['yearEnd'] - data[
                            'metadata'][elem]['yearBgn']
                    except KeyError:
                        span = min_yrs  # Let's see what happens...

                    if span < min_yrs:
                        # See _create_data_desc() return, too.
                        return {
                            'id': data['id'],
                            'yearBgn': data['metadata'][elem]['yearBgn'],
                            'yearEnd': data['metadata'][elem]['yearEnd'],
                            'data': []
                        }

                try:
                    data[elem]
                except KeyError:
                    continue

                self.n_lines += 1
                # continue

                year = int(line[11:15])
                mnth = int(line[15:17])  # 1-12
                try:
                    data[elem][year]
                except KeyError:
                    data[elem][year] = {}

                data[elem][year][mnth] = _valsfromstr(line)

        return _create_data_desc(data, elems)


"""numpy genfromtxt() is an alternative for parsing lines.

    But testing with the first 30 files suggests that the pure Python code is over
    80 times faster than numpy genfromtxt(), for just that part of the processing.

    Something like...

        DELIM = (11, 4, 2, 4)
        for i in range(31):
            DELIM += (5, 1, 1, 1)

        DTYPE = ('U11', int, int, 'U4')
        for i in range(31):
            DTYPE += (int, 'U1', 'U1', 'U1')

        for line in infile:
            vals = np.genfromtxt(StringIO(line), delimiter=DELIM, dtype=DTYPE)  # (B)
            id = vals.item(0)[0]
            year = vals.item(0)[1]
            elem = vals.item(0)[3] # etc.

"""


def ghcndata_to_dataframe(gd, elem_name):
    """Convert GHCN data description to pandas DataFrame.

    (!) Handles 1 element at a time; i.e.,
        call with only 1 element in the list returned from Ghcn.file_to_data().

    Fills in NaNs with mean value computed for each column.
    'df = df_.fillna(df.mean())' is an alternative, but not what we want. (!)

    """
    try:
        elem_data = gd[elem_name]
    except KeyError:
        elem_data = gd[0][elem_name]

    df = pd.DataFrame(elem_data)

    for x in df.values:
        sum_ = 0
        n = 0
        for val in x:
            if not math.isnan(val):
                sum_ += val
                n += 1
        n = 1 if n == 0 else n  # Handle 'x' without any good values.
        sum_ = round(sum_ / n, 2)
        #
        # Compute full stats and reject 'bad data' here, too? (!)
        #...
        len_ = len(x)
        for i in range(0, len_):
            if math.isnan(x[i]):
                x[i] = sum_

    return df


def report_elapsed(t_bgn, n_files, n_lines):
    """Report progress when called.

    """
    print("elapsed = " + "{0:.2f}".format(round(time.time() - t_bgn, 2)) +
          " n_files = " + str(n_files) + " n_lines = " + str(n_lines))


def only_1st_and_lst(years):
    """Here's your missing docstring.

    """
    # print(str(years[0]) + '-' + str(years[len(years) - 1]))
    years_len = len(years)
    if years_len == 0:
        return False
    # Plot only 1st and last.
    return years if years_len == 1 else years[::years_len - 1]


def process_a_station(ghcn_obj, id_):
    """What it says.

    """
    filename = id_ + '.dly'
    ghcn_data = ghcn_obj.file_to_data(filename, ghcn_obj.elements, min_yrs=50)
    # Skip file if it doesn't have the data we're looking for.
    if not ghcn_data['data']:
        return False

    # (!!!) Only handling the first element here.
    df = ghcndata_to_dataframe(ghcn_data['data'][0], ghcn_obj.elements[0])
    years = [a for a in ghcn_data['data'][0][ghcn_obj.elements[0]]]
    if not years:
        return

    years = only_1st_and_lst(years)
    anly.plot_years(df, id_, years)
    # plt.show()

    return True


def for_each_station(ghcn_obj, stations, t_bgn=time.time()):
    """What it says.

    """
    n_files = 0
    n_lines = 0
    for item in stations:
        """
        if n_files > 3:
            break
        if n_files < 3:
            n_files += 1
            continue
        """

        if not process_a_station(ghcn_obj, item['id']):
            continue

        n_files += 1
        n_lines += ghcn_obj.n_lines
        if (n_files % 100) == 0:
            report_elapsed(t_bgn, n_files, n_lines)

    report_elapsed(t_bgn, n_files, n_lines)


def remove_if_element_missing(stations, elem_name):
    """Remove stations from list that don't have the element we're looking for.

    """
    removed = []
    i = 0
    while i < len(stations):
        station = stations[i]
        found = True
        try:
            station['elems'][elem_name]
        except KeyError:
            found = False

        if not found:
            removed.append(stations.pop(i))
        else:
            i += 1

    return removed
