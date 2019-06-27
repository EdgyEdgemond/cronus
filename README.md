Cronus
======

A crontab parser that renders the result to a simple table.


Usage
-----

```bash
$ cronparse '*/15 0 1,15 * 1-5 /usr/bin/find'
minute          0 45 30 15
hour            0
day of month    1 15
month           1 2 3 4 5 6 7 8 9 10 11 12
day_of_week     1 2 3 4 5
command         /usr/bin/find
```
