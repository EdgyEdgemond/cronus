Cronus
======

A crontab parser that renders the result to a simple table.

Installation
------------

Clone this repo and then run the following from the new directory:

```bash
$ pip install -e .
```

To run tests:

```bash
$ pip install -e .[test]
$ pytest
```

Usage
-----

The `'`s in the command line are important to prevent any `*`s converting to
the contents of the current directory.

```bash
$ cronparse '*/15 0 1,15 * 1-5' /usr/bin/find
minute          0 45 30 15
hour            0
day of month    1 15
month           1 2 3 4 5 6 7 8 9 10 11 12
day_of_week     1 2 3 4 5
command         /usr/bin/find
```
