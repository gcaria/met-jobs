# met-jobs
met-jobs lets you search through the jobs advertised from January 2011 until July 2021 (around 12,000 entries) via the [Met-jobs mailing list](https://www.lists.rdg.ac.uk/mailman/listinfo/met-jobs) and
display the most appropriate results.

It also provides a tool to quickly scrape
the Met-jobs website and produce a database that includes the latest job ads,
which then can be used as input for the search engine.

----

## Installation
Simply pip it:
```
pip install met-jobs
```

If you want to build a new database of job ads, it is necessary to install
additional dependencies that deal with the web scraping part. You can do so, by using:
```
pip install met-jobs[scrape]
```

The code has only been tested with Python 3.8.

----

## Usage

### Search through the Met-jobs database

To search a particular string (e.g. "mesoscale") in the database of Met-jobs ads, use:
```
search_met mesoscale -n 5
```
where in this case we have limited the output to the 5 most relevant results (see below about query options).

Output:
```
1)   Mesoscale meteorologist                                                     - 02-03-2020
https://www.lists.rdg.ac.uk/archives/met-jobs/2020-03/msg00002.html


2)   Mesoscale Modelling Research Scientist Post                                 - 08-10-2012
https://www.lists.rdg.ac.uk/archives/met-jobs/2012-10/msg00016.html


3)   Postdoctoral position in mesoscale weather modeling                         - 11-04-2017
https://www.lists.rdg.ac.uk/archives/met-jobs/2017-04/msg00043.html


4)   Postdoc in Mesoscale Meteorological Modeling                                - 13-06-2011
https://www.lists.rdg.ac.uk/archives/met-jobs/2011-06/msg00028.html


5)   “Mesoscale Modelling” at Goethe-University Frankfurt (Germany)              - 31-10-2012
https://www.lists.rdg.ac.uk/archives/met-jobs/2012-11/msg00001.html
```

On a Mac you can simply use `cmd`+`click` on the ad's URL to open it in
your browser, or if you are on Linux just use `ctrl`+`click`

Options:

```
usage: search_met [-h] [-d DATABASE] [-n N_RESULTS] [-s START] [-e END] [--by {best,newest,oldest}] QUERY

Search in the met-jobs ads database.

positional arguments:
  QUERY                 String for search query

optional arguments:
  -h, --help            show this help message and exit
  -d DATABASE, --database DATABASE
                        Path of database used for search query (default is built-in database)
  -n N_RESULTS, --n_results N_RESULTS
                        Number of results displayed
  -s START, --start START
                        Start date for search
  -e END, --end END     End date for search
  --by {best,newest,oldest}
                        Criterium for order of results
```
### Scrape the Met-jobs website and create a database of job ads

A fast parallelized tool to scrape the website and retrieve information of the
job ads is provided. It can be useful to use this tool when you want to create a new database which
includes the latest job ads (as of now job ads until July 2021 are included in the built-in database).

This is achieved running:

```
create_db output_path.csv
```

Options:

```
usage: create_db [-h] [-s START] [-e END] PATH_CSV

Scrape the met-jobs website and create a database of job ads.

positional arguments:
  PATH_CSV              The output path for the database csv file

optional arguments:
  -h, --help            show this help message and exit
  -s START, --start START
                        Start date for database (format: YYYY-MM)
  -e END, --end END     End date for database (format: YYYY-MM)
```
