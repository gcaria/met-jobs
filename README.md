# met-jobs
Searches through the jobs advertised until 27/01/2021 via the [Met-jobs mailing list](https://www.lists.rdg.ac.uk/mailman/listinfo/met-jobs) and
display the most appropriate results.

## Installation
Simply clone this git repository:
```
git clone https://github.com/gcaria/met-jobs.git
```
and install the packages (simply `pandas`, `sklearn` and their respective dependencies) specified in the `requirements.txt` file.
Additional packages are required should you wish to create a new database for the queries.

The code has only been tested with Python 3.

## Usage
To search a particular string (e.g. "mesoscale") in the database of Met-jobs ads, use:
```
search_met "mesoscale" -n 5
```
where in this case we have limited the output to the 5 most relevant results (see below about query options).

Output:
```
----------------------------------------------------------------------
1) Mesoscale meteorologist - 02-03-2020
https://www.lists.rdg.ac.uk/archives/met-jobs/2020-03/msg00002.html
----------------------------------------------------------------------
2) Mesoscale Modelling Research Scientist Post - 08-10-2012
https://www.lists.rdg.ac.uk/archives/met-jobs/2012-10/msg00016.html
----------------------------------------------------------------------
3) Postdoctoral position in mesoscale weather modeling - 11-04-2017
https://www.lists.rdg.ac.uk/archives/met-jobs/2017-04/msg00043.html
----------------------------------------------------------------------
4) Postdoc in Mesoscale Meteorological Modeling - 13-06-2011
https://www.lists.rdg.ac.uk/archives/met-jobs/2011-06/msg00028.html
----------------------------------------------------------------------
5) “Mesoscale Modelling” at Goethe-University Frankfurt (Germany) - 31-10-2012
https://www.lists.rdg.ac.uk/archives/met-jobs/2012-11/msg00001.html
```

On a Mac you can simply just use `cmd`+`click` on the ad's URL to open it in
your browser, or if you are on Linux just use `ctrl`+`click`

To discover all available self-explanatory arguments run:
```
search_met --help
```
