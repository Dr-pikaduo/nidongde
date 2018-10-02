# nidongde
nidongde is a Chinese phrase for "you know". Please control yourself!

Make sure you are older than 18!

## Requirement
requests
bs4
fake-useragent


## Scripts

### load.py (deprecated)
load vedios

### search.py (deprecated)
search vedios with keywords (and styles)

### load_novels.py
load novels.

### load_movies.py (recommended)
Load movies with OOP, integrate load.py and search.py.
```
Movie.load  == load in load.py
Movie.search == search in search.py

# Examples
# load 29960, 29961, 29963, 29964-29971, 34538-34543
Moive.load([29960, [29961, 29963], (29964, 29971), (34538, 34543)])

# search movies with '人妻'
for m in Movie.search('人妻')：
    print(m)
```

## clt

```bash
script.py load -i [index]
script.py search -k keyword -s style
```

## misc
I get first `✭star` in my github-life.
