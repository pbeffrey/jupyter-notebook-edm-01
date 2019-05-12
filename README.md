# GHCN Analysis Getting Started

The Global Historical Climate Network (GHCN) 
comprises stations in 180 countries and territories collecting daily climate data summaries including: maximum and minimum temperature, precipitation, snowfall, etc. The current size of the uncompressed text-based data is almost 30GB.

This project attempts to take the grunt work out of loading and processing the 'raw' data into a form that's easier to access using NumPy and Pandas within a Jupyter Notebook. It consists of a small Python library for loading data from a *local* copy of the GHCN-Daily repository along with a sample Jupyter Notebook illustrating its use.

A description of GHCN-D can be found [here](https://www.ncdc.noaa.gov/ghcn-daily-description) and the FTP site for downloading the data is [here](ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/).

This Python library requires that the *ghcnd_all.tar.gz* file be downloaded from the FTP site and unpacked to a local folder—it will expand to almost 30GB—and that the following files are also downloaded to a nearby folder: *ghcnd-inventory.txt* and *ghcnd-stations.txt*. See [Data Downloading Instructions](#data-downloading-instructions) for more information.

#### You will undoubtedly find the *readme.txt* file on the FTP site very informative and helpful. And please be aware of the data usage rules described [here](https://www.ncdc.noaa.gov/ghcnd-data-access).

---

## Data Downloading Instructions

> **TODO** Create precise instructions here.

---

## Library Description and Overview

> **TODO** Create a general overview of the library and how it's used.

---

## Author

Phil Beffrey

pbeffrey@gmail.com
