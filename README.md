# my Sweet Cache
This project let make fast and simply cache 

## autors
Bartłomiej Chwiłkowski (github: chwilko)


# Structure
mySweetCache:
    mySweetCache.py:
        main functions
    utils.py:
        other function usefull to 


## Functions 

cache:
    decorator to cache the result of the function
use_par:
    decorator to set first function argument
use_pars:
    decorator to set first function arguments

# How to use

```python3
@cache("key")
def long_counting_function():
    ...

long_counting_function()
```

After first call this function result is saved in .MScache_files/key
In next call instead recount value will be read from cache.
To recount call `long_counting_function(use_cache=False)` then cache will be overwrited
or delete .MScache_files/try file.

WARNING!
If you define two function with the same key, there two functions will share the same cache file.



# Licence
MIT
