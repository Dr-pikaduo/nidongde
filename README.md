# nidongde
🔞nidongde is a Chinese phrase for "you know". Please control yourself!

Make sure you are older than 18!

## Requirement

requests

bs4

fake-useragent (Optional）

## Featrues

- A mature framework
- multi-threads, use `threading` to load data
- extensible, define `website` to operate the urls

## Framework

![](https://github.com/Freakwill/nidongde/blob/master/framework.png)


## Scripts

### load.py (deprecated)
load vedios

### search.py (deprecated)
search vedios with keywords (and styles)

### load_novels.py
search and load novels.

### load_movies.py (recommended)
Load movies with OOP, integrate load.py and search.py.

```python
from nidongde import *

Movie.load  == load in load.py
Movie.search == search in search.py

# Examples
# load 29960, 29961, 29963, 29964-29971, 34538-34543
Moive.load([29960, [29961, 29963], (29964, 29971), (34538, 34543)])

# search movies with '人妻'
for m in Movie.search('人妻')：
    print(m)

# search novels with '人妻'
for m in Novel.search('人妻')：
    print(m)
```

## clt

```bash
script.py load -i [index] (-v)
script.py search -k keyword -s style -m (mask method)
```

Example:
```bash
script.py search -k 人妻 [-s 人妻]
script.py load -i 39818-39822
```
mask method: `mask`, a float number (probability to mask any character) or any integer for Caesar

## TO DO

- crawl new websites
- multi-threading
- load novels

## misc
I get first `✭star` in my github-life.

## Similar projects
* [Porndl](https://github.com/Ybow/porndl)
* [FBIWarning](https://github.com/nusr/FBIWarning)
* [Pornsearch](https://github.com/LucasLeandro1204/Pornsearch)
