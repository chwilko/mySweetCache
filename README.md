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
### cache
```python3
def cache(
    MSC_name: Optional[str] = None,
    *,
    header: Optional[str] = None,
    sep_in_data: str = "",
) -> Callable:
```
Wrapper add possibility caching function result to wrapped function

If file MSC_name exist in _CACHE_FILES
  wraped function return cache from right cache.
else
  make new cache
Wrapper add optional argument 'use_cache'.
If use_cache == False
  cache will overwrite.


Args:
  MSC_name (Optional[str], optional): cache key. Defaults to None.
  header (Optional[str], optional): data description. Defaults to None.
  sep_in_data (str, optional): Separator between array items
      for text output. If "" (empty), a binary file is written,
      equivalent to file.write(a.tobytes()). Defaults to "".

Returns:
    callable: Function with cache functionality.

### read_cache
```python3
def read_cache(MSC_name: str) -> Any:
``` 
Function to fast read MSC.

Args:
    MSC_name (str): cache key to read.

Raises:
    NameError: If this cache don't exist.

Returns:
    np.array: Previously saved data.

### save_cache
```python3
save_cache(
    MSC_name: str,
    data: ndarray,
    *,
    header: Optional[str] = None,
    sep_in_data: str = "",
)
```
Function to fast save MSC.

Args:
    MSC_name (str): cache key to save.
    data (ndarray): data to save
    sep_in_data (Optional[str], optional): Separator between array items
        for text output. If "" (empty), a binary file is written,
        equivalent to file.write(a.tobytes()).

### use_par
Decorator set self argument as first function argument.
```python3
def use_par(par):
```


### use_pars
Decorator set self arguments as first function arguments.
```python3
def use_pars(*pars):
```

# How to use
```python3
example use:
  @cache("key")
  def long_working_function() -> np.ndarray:
      # long code to work
      return ...

example use 2:
  @cache("key")
  @use_parms(11, 21)
  def long_working_function(arg1, arg2) -> np.ndarray:
      # long code to work
      return ...
```

After first call this function result is saved in .MScache_files/key
In next call instead recount value will be read from cache.
To recount call `long_counting_function(use_cache=False)` then cache will be overwrited
or delete .MScache_files/try file.

WARNING!
If you define two function with the same key, there two functions will share the same cache file.



# Licence
MIT
