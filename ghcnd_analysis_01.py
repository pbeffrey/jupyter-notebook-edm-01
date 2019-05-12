"""Read and analyze GHCN data.

"""
# pylint: disable=invalid-name, locally-disabled
# pylint: disable=pointless-string-statement, locally-disabled

import time
import matplotlib.pyplot as plt

import ghcn
import mapping as map_
import analysis as anly

# Unused but nice to know about...
# from io import StringIO
# from six.moves import urllib

WORLD_MAP = map_.Mapping()


def report_station(data):
    """Report info about a station.

    """
    mdata = data['metadata']
    WORLD_MAP.add_location(mdata)
    """
    print(mdata['id'] + ' ' + str(mdata['yearBgn']) + ' to ' +
          str(mdata['yearEnd']))
    print('  lat, lng, elv = ' + str(mdata['lat']) + ', ' + str(mdata['lng']) +
          ', ' + str(mdata['elv']))
    print('  index = ' + str(mdata['index']))
    """


def report_all(obj):
    """Give a summary of every file processed.

    """
    print(
        str(obj['nValidStations']) + ' stations are valid out of ' +
        str(obj['nTotalStations']) + ' total, max_rows_per_station = ' +
        str(obj['maxRowsPerStation']))


def plot_histogram(per_year, elems):
    """Plot the 'active stations by year' histogram.

    Not used but handy to know about:
    years_series = pd.Series(per_year['histo'])

    """

    # Make years and labels lists for ALL years...
    years = []
    labels = []
    for i in range(per_year['firstYear'], per_year['lastYear'] + 1):
        years.append(i)
        if ((i - per_year['firstYear']) % 10) == 0:
            labels.append(str(i))
        else:
            labels.append('')

    # ... But let's skip plotting the first 130 years
    # 1893 is the first year when there were more than 1000 stations (1798 to be exact).
    year_bgn_plot = 130

    plt.figure(figsize=(15, 3))
    plt.title('Number of Active Stations per year recording: ' + ', '.join(elems))
    plt.bar(years[year_bgn_plot:],
            per_year['histo'][year_bgn_plot:],
            width=0.6,
            snap=False,
            alpha=0.65)
    plt.xticks(years[year_bgn_plot:], labels[year_bgn_plot:], rotation=90)
    # plt.show() # Comment out to allow the *next* show() to draw.


def process_a_bucket():
    """What it says.

    """


def for_each_bucket(t_bgn, ghcn_obj, stations, buckets):
    """What it says.

    """
    for bucket in buckets:
        if not bucket['list']:
            continue
        print(len(bucket['list']))
        '''
        for item in bucket['list']:
            print(item)
        '''


def python_main():
    """Main function.

    """
    t_bgn = time.time()
    this_elem = 'TMAX'

    ghcn_obj = ghcn.Ghcn('/media/data/GHCN', 'ghcnd_all', 'docs',
                         (this_elem, ))
    # Show histogram of stations; some are thrown away, see plot_histogram().
    per_year = ghcn_obj.stations_per_year()
    plot_histogram(per_year, (this_elem, ))

    # stations = ghcn_obj.get_stations(this_elem, min_yrs=50, must_include=2019)
    stations = ghcn_obj.get_stations(this_elem, 25, must_include=2015)
    # 'stations' is a list of metadata dictionaries.
    print("n stations = " + str(len(stations)))

    for station in stations:
        WORLD_MAP.add_location(station)
    WORLD_MAP.show()
    """
    # No longer necessary...
    removed = ghcn.remove_if_element_missing(stations, this_elem)
    print('removed ' + str(len(removed)) + ' stations')
    """
    # Sort to easily display the longest-active stations first.
    stations.sort(key=lambda e: e['elems'][this_elem]['yearBgn'] - e['elems'][
        this_elem]['yearEnd'])

    # Maybe helpful:
    # https://matplotlib.org/examples/pylab_examples/subplots_demo.html

    # plt.figure(figsize=(6, 2))
    f, axarr = plt.subplots(3, 3, sharex='col', sharey='row', figsize=(16, 9))
    f.subplots_adjust(hspace=0.25, wspace=0.1)

    anly.PLOT_LAYOUT = []
    anly.PLOT_LAYOUT_INDEX = 0
    for y in range(3):
        for x in range(3):
            anly.PLOT_LAYOUT.append(axarr[y, x])

    ghcn.for_each_station(ghcn_obj, stations[0:9], t_bgn)

    # for_each_bucket(t_bgn, ghcn_obj, stations, WORLD_MAP.buckets)

    plt.show()


python_main()
