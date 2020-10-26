# met-jobs
Searches through the jobs advertised via the [Met-jobs mailing list](https://www.lists.rdg.ac.uk/mailman/listinfo/met-jobs) and
return the most appropriate results.

## Installation
Simply clone this git repository:
```
git clone https://github.com/gcaria/met-jobs.git
```
and install all packages specified in the `requirements.txt` file.

The code can only be run with Python 3.

## Usage
To search a particular string in the database, use:
```
python search.py -q "mesoscale convective"
```

To discover all available self-explanatory arguments run:
```
python search.py --help
```
