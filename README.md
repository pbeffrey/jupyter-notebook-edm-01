# GHCN Analysis Getting Started

The Global Historical Climate Network (GHCN) 
comprises over 100,000 stations in 180 countries and territories collecting daily climate data summaries including: maximum and minimum temperature, precipitation, snowfall, etc. The current total size of the uncompressed text-based data is almost 30GB.

This project attempts to take the grunt work out of loading and processing the 'raw' data into a form that's easier to access using NumPy and Pandas within a Jupyter Notebook. It consists of a small Python library for loading data from a *local* copy of the GHCN-Daily repository along with a sample Jupyter Notebook illustrating its use—see [*edm_01.ipynb*](https://github.com/pbeffrey/jupyter-notebook-edm-01/blob/master/edm_01.ipynb) for a static version of that Notebook.

A description of GHCN-D can be found [here](https://www.ncdc.noaa.gov/ghcn-daily-description) and you can download the data from [here](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/), or from ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/

This Python library requires that the *ghcnd_all.tar.gz* file be downloaded from the data website and unpacked to a local folder—it will expand to almost 30GB—and that the following files be downloaded to a nearby folder: *ghcnd-inventory.txt* and *ghcnd-stations.txt*. See [Data Downloading Instructions](#data-downloading-instructions) for more information.

#### You will undoubtedly find the *readme.txt* file on the data website very informative and helpful. And please be aware of the data usage rules described [here](https://www.ncdc.noaa.gov/ghcnd-data-access).

---

## Data Downloading Instructions

I suggest downloading both the data and doc files to different folders with a common root. The data tarball (*ghcnd_all.tar.gz*) will expand to create a folder with over 100,000 files (one for each GHCN station), so you might want to avoid opening that folder with a file browser.

On my linux system the folders are arranged like this:
- /media/data/GHCN/ghcnd_all/..data files..
- /media/data/GHCN/docs/..doc files..

Do something like the following:

1. Create the common root folder—e.g., 'GHCN'—and create the docs folder under it.

2. Download *ghcnd-inventory.txt* and *ghcnd-stations.txt* from the data website directly to the docs folder.

3. Download *ghcnd_all.tar.gz* from the data website directly to the GHCN folder—it will create the ghcnd_all folder when extracted.

4. On linux or macOS use `'tar -xzf ghcnd_all.tar.gz'` to extract all of the data files; on Windows I find that [7-Zip](https://www.7-zip.org/) works very well.

---

## Library Description and Overview

> **TODO** Create a general overview of the library and how it's used.

[MIT License](https://github.com/pbeffrey/jupyter-notebook-edm-01/blob/master/LICENSE.md)

---

## Performance

> **TODO** Describe the performance advantages of this library.

---

## Future Improvements

> **TODO** Describe planned improvements, including C++ components.

---

## Author

Phil Beffrey

pbeffrey@gmail.com
