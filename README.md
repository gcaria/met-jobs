# met-jobs
Searches through the jobs advertised until 01/10/2020 via the [Met-jobs mailing list](https://www.lists.rdg.ac.uk/mailman/listinfo/met-jobs) and
display the most appropriate results.

## Installation
Simply clone this git repository:
```
git clone https://github.com/gcaria/met-jobs.git
```
and install all packages specified in the `requirements.txt` file.

The code has only been tested with Python 3.

## Usage
To search a particular string in the database of Met-jobs ads, use:
```
python search.py -q "mesoscale convective"
```
Output:
```
----------------------------------------------------------------------
1) Mesoscale meteorologist - Mon, 2 Mar 2020 14:25:07 +1100
https://www.lists.rdg.ac.uk/archives/met-jobs/2020-03/msg00002.html
----------------------------------------------------------------------
2) Mesoscale Modelling Research Scientist Post - Mon, 8 Oct 2012 12:32:50 +0100
https://www.lists.rdg.ac.uk/archives/met-jobs/2012-10/msg00016.html
----------------------------------------------------------------------
3) Postdoctoral position in mesoscale weather modeling - Tue, 11 Apr 2017 15:48:15 +0000
https://www.lists.rdg.ac.uk/archives/met-jobs/2017-04/msg00043.html
----------------------------------------------------------------------
4) Postdoc in Mesoscale Meteorological Modeling - Mon, 13 Jun 2011 11:03:59 -0700
https://www.lists.rdg.ac.uk/archives/met-jobs/2011-06/msg00028.html
----------------------------------------------------------------------
5) PhD position in convective cloud modeling - Mon, 01 Jul 2013 10:48:11 +0200
https://www.lists.rdg.ac.uk/archives/met-jobs/2013-07/msg00001.html
----------------------------------------------------------------------
6) Research Fellow in Convective Cloud Dynamics - Fri, 13 Dec 2013 15:03:20 +0000 (GMT)
https://www.lists.rdg.ac.uk/archives/met-jobs/2013-12/msg00048.html
----------------------------------------------------------------------
7) PhD project in tropical convective dynamics - Fri, 24 Nov 2017 09:37:01 +0000
https://www.lists.rdg.ac.uk/archives/met-jobs/2017-11/msg00101.html
----------------------------------------------------------------------
8) Postdoctoral position,	ocean mesoscale/submesoscale dynamics - Tue, 23 Feb 2016 11:25:43 +0100
https://www.lists.rdg.ac.uk/archives/met-jobs/2016-02/msg00070.html
----------------------------------------------------------------------
9) “Mesoscale Modelling” at Goethe-University Frankfurt (Germany) - Wed, 31 Oct 2012 21:45:51 +0100
https://www.lists.rdg.ac.uk/archives/met-jobs/2012-11/msg00001.html
----------------------------------------------------------------------
10) Assistant Professor, Mesoscale Meteorology,	Florida State University - Fri, 2 Oct 2015 14:18:36 +0000
https://www.lists.rdg.ac.uk/archives/met-jobs/2015-10/msg00005.html
```

On a Mac you can simply just use `cmd`+`click` on the ad's URL to open it in
your browser.

To discover all available self-explanatory arguments run:
```
python search.py --help
```
