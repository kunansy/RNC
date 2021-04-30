# API for [Russian National Corpus](http://ruscorpora.ru) 

## Installation
```bash
pip install rnc
```

## Structure
Corpus object contains list of obtained examples.
There are two types of examples:
![](https://github.com/kunansy/RNC/blob/master/docs/Two_ex_types.png?raw=true) <br> 
* If `out` is `normal`, API uses normal example, which name is equal to the Corpus class name:

```python
ru = rnc.MainCorpus(...)
ru.request_examples()

print(type(ru[0]))
>>> MainExample
```
* if `out` is `kwic`, API uses `KwicExample`.

Examples' objects [fields](https://github.com/kunansy/RNC/blob/master/docs/Examples.md)   


## Usage
```python
import rnc

ru = rnc.MainCorpus(
    query='корпус', 
    p_count=5,
    file='filename.csv',
    marker=str.upper,
    **kwargs
)

ru.request_examples()
```
* `query` – one str or dict with tags. Words to find, you should give the vocabulary form of them.
* `p_count` – count of **PAGES**.
* `file` – path to local csv file, optional. Example: `file='data\\filename.csv'`. 
* `marker` – function, with which found wordforms will be marked, optional. 
* `kwargs` – additional params.

[Corpora](https://github.com/kunansy/RNC/blob/master/docs/Corpora.md) you can use.


### Full query form
```python
query = {
    'word1': {
        'gramm': 'acc', # grammar tags for lexgramm search
        'flags': 'bdot' # additional tags for lexgramm search
    },
    # you can get as a value one string or dict of params
    # params are: any name of dict key, name of tag (you can see them below)  
    'word2': {
        'gramm': { 
            # the NAMES of these keys might be any
            'pos (any name)': 'S' or ['S', 'A'], # one value or list of values,
            'case (any name)': 'acc' or ['acc', 'nom'],
        },
        'flags': {}, # all the same to here
        # distance between first and second words
        'min': 1,  
        'max': 3
    },  
}

corp = rnc.MainCorpus(
    query, 5, file='filename.csv', marker=str.upper, **kwargs)
corp.reques_examples()
```
[Lexgramm search params](https://github.com/kunansy/RNC/tree/master/docs/Lexgram%20search%20params)


### String as a query
Also you can pass as a query a string with the **vocabulary forms** of the 
words, divided by space: `query = 'get down'` or `query = 'я получить'`. 
Distance between them will be default.


### Additional request params
These params are optional, you can ignore them. Here are the default values.
```python
corp = rnc.ParallelCorpus(
    query=query, 
    p_count=5,
    file='filename.csv',
    marker=str.upper,
    
    dpp=5, # documents per page
    spd=10, # sentences per document (<= than spd)
    text='lexgramm' or 'lexform', # way to search
    out='normal' or 'kwic', # output format
    kwsz=5, # if out=kwic, count of words in context
    sort='i_grtagging', # way to sort the results, see HOWTO section below
    mycorp='', # see HOWTO section below
    accent=0, # with accentology (1) or without (0), if it is available
)
```
[Sort keys](https://github.com/kunansy/RNC/blob/master/docs/HTTP%20params.md)


### API can work with a local file too
```python
ru = rnc.SpokenCorpus(file='local_database.csv') # it must exist
print(ru)
```
If the file exists, API works with it. If the data list is not empty you 
cannot request new examples. <br>

If you work with a file, it is not demanded to pass any argument to Corpus 
except for the file name (`file=...`).


### Working with corpora
```python
corp = rnc.corpus_name(...) 
```
* `corp.request_examples()` – request examples. 
There is an exception if:
    * Data still exist. 
    * No results found.
    * A requested page does not exist (if there are 10 pages in the RNC, but 
      you have requested > 10).
    * There is a mistake in the request.
    * You have no access to the Internet.
    * There is a problem while getting access to RNC.
    * another problems...
* `corp.data` – list of examples (only getter)
* `corp.query` – query (only getter).
* `corp.forms_in_query` – requested wordforms (only getter).
* `corp.p_count` – requested count of pages (only getter). 
* `corp.file` – path to the local csv file (only getter).
* `corp.marker` – marker (only getter).
* `corp.params` – dict, HTTP tags (only getter). 
* `corp.found_wordforms` – dict with found wordforms and their frequency (only getter).
* `corp.ex_type` – type of example (only getter).
* `corp.amount_of_docs` – amount of docs where the query was found.
* `corp.amount_of_contexts` – amount of contexts where the query was found.
* `corp.graphic_link` – link to the graphic of the distribution of query occurrences by years.
* `corp.dump()` – write two files: csv file with all data and json file with config.
* `corp.copy()` – create a copy.
* `corp.shuffle()` – shuffle data list.
* `corp.sort_data(key=, reverse=)` – sort the list of examples. Here HTTP keys do not work,
key is applied to Example objects.  
* `corp.pop(index)` – remove and return the example at the index.
* `corp.clear()` – empty the data list.
* `corp.filter(key)` – filter the data list, remove some examples using the key. 
Key is applied to the `Example` objects.
* `corp.url` – URL of the first RNC page (only getter).
* `corp.findall(pattern, args)` – get all examples where the pattern found and 
  the match.
* `corp.finditer(pattern, args)` – get all examples where the pattern found and 
  the match.

Magic methods: 
* `corp.dpp` or another request param (only getter).
* `corp()` – all the same to `request_examples()`.
* `str(corp) or print(corp)` – str with info about Corpus, enumerated examples.
By default, Corpus shows first 50 examples, but you can change it 
or turn the restriction off. 

    Info about Corpus:
    ```
    Russian National Corpus (https://ruscorpora.ru)
    Class: CorpusName, len = amount of examples 
    Pages: n of 'words' requested
    ```
* `len(corp)` – count of examples.
* `bool(corp)` – whether data exist.
* `corp[index or slice]` – get element at the index or create a new object 
  with sliced data:
```python
from_2_to_10 = corp[2:10:2]
```
* `del corp[10]` or `del corp[:10]` – remove some examples from the data list.

* Also you can use cycle `for`. For example we want to see only left 
  context (`out=kwic`) and source:
```python
corp = rnc.ParallelCorpus(
    'corpus', 5, 
    out='kwic', kwsz=7, 
    mycorp=rnc.mycorp.en
)
corp.request_examples()

for r in corp:
    print(r.left)
    print(r.src)
```

Set default values to all objects you will create:
* `corpus_name.set_dpp(value)` – change default `document per page` value.
* `corpus_name.set_spd(value)` – change default `sentences per document` value.
* `corpus_name.set_text(value)` – change default search way.
* `corpus_name.set_sort(value)` – change default sort key.
* `corpus_name.set_min(value)` – change default min distance between words.
* `corpus_name.set_max(value)` – change default max distance between words.
* `corpus_name.set_restrict_show(value)` – change default amount of shown examples in print. 
If it is equal to `False`, the Corpus shows all examples. 


### Corpora features
#### ParallelCorpus
* The query might be both in the original language and in the language of 
  translation. 

#### MultilingualParaCorpus
* Working with files is removed.
* Param `mycorp` is not demanded by default, but it might be passed, see 
  **HOWTO** section below.

#### MultimodalCorpus
* `corp.download_all()` – download all media files. **It is recommended** to use 
this method instead of `expl.download_file()`.


## Logger
* See all log messages
```python
rnc.set_stream_handler_level('debug')
```
* See less than all messages
```python
rnc.set_stream_handler_level('info')
```
* Turn the logger off
```python
rnc.set_logger_level('critical')
```
* Turn off all messages in the stream, but dump logs to file
```python
rnc.set_stream_handler_level('critical')
```
* Turn off dumping logs to file
```python
rnc.set_file_handler_level('critical')
```


## ATTENTION
* Do not forget to call this function
```python
corp.request_examples()
```
* If you have requested more than 10 pages, RNC returns 429 error 
  (Too many requests).
For example requesting 100 pages you should wait about 3 minutes: 
![100 pages](https://github.com/kunansy/RNC/blob/master/docs/100_pages.png?raw=true)
* **Do not call** the marker you pass

**RIGHT:**
```python
ru = rnc.MainCorpus(...,  marker=str.upper)
```
**WRONG:**
```python
ru = rnc.MainCorpus(..., marker=str.upper())
```
* Pass an empty string as a param if you do not want to set them
```python
query = {
    'word1': '',
    'word2': {'min': 2, 'max': 5}
}
```
* If `accent=1`, marker does not work.

---

## HOWTO
You can ask any question you want [here](https://github.com/kunansy/RNC/discussions).

### How to set sort?
There are some sort keys:
1. `i_grtagging` – by default.
2. `random` – randomly.
3. `i_grauthor` – by author.
4. `i_grcreated_inv` – by creation date.
5. `i_grcreated` – by creation date in reversed order.
6. `i_grbirthday_inv` – by author's birth date.
7. `i_grbirthday` – by author's birth date in reversed order.

[Some of HTTP params](https://github.com/kunansy/RNC/blob/master/docs/HTTP%20params.md).


### How to set language in ParallelCorpus?
```python
en = rnc.ParallelCorpus('get', 5, mycorp=rnc.mycorp.en)
```
**OR**
```python
en = rnc.ParallelCorpus('get', 5, mycorp=rnc.mycorp['en'])
```
Language keys list:
1. Armenian – 'arm'
1. Bashkir – 'bas'
1. Belarusian – 'bel'
1. Bulgarian – 'bul'
1. Buryatian – 'bur'
1. Chinese – 'ch'
1. Czech – 'cz'
1. English – 'en'
1. Estonian – 'es'
1. Finnish – 'fin'
1. French – 'fr'
1. German – 'ger'
1. Italian – 'it'
1. Latvian – 'lat'
1. Lithuanian – 'lit'
1. Polish – 'pol'
1. Spanish – 'sp'
1. Swedish – 'sw'
1. Ukrainian – 'ukr'

If you want to search something by several languages, choose and set the 
`mycorp` in the site, pass this param to Corpus. 


### How to set subcorpus?
Means specify the sample where you want to search the query. <br>

There are default keys in `rnc.mycorp` (working checked in 
**MainCorpus**) – Russian writers and poets: 
* Pushkin
* Dostoyevsky
* TolstoyLN
* Chekhov
* Gogol
* Turgenev

Example:
```python
ru = rnc.MainCorpus('нету', 1, mycorp=rnc.mycorp['Pushkin'])
```


**OR**

```python
ru = rnc.MainCorpus('нету', 1, mycorp=rnc.mycorp.Pushkin)
```


**OR**

 
![1](https://raw.githubusercontent.com/kunansy/RNC/master/docs/How%20to%20set%20subcorpus/1.png)
![2](https://raw.githubusercontent.com/kunansy/RNC/master/docs/How%20to%20set%20subcorpus/2.png)
![3](https://raw.githubusercontent.com/kunansy/RNC/master/docs/How%20to%20set%20subcorpus/3.png)
![4](https://raw.githubusercontent.com/kunansy/RNC/master/docs/How%20to%20set%20subcorpus/4.png)


## Links
* [Russian National Corpus](https://ruscorpora.ru)
* [Docs](https://github.com/kunansy/RNC/tree/master/docs)
* Examples' objects [fields](https://github.com/kunansy/RNC/blob/master/docs/Examples.md)
* [Corpora](https://github.com/kunansy/RNC/blob/master/docs/Corpora.md) you can use.
* [Lexgramm search params](https://github.com/kunansy/RNC/tree/master/docs/Lexgram%20search%20params)
* [Sort keys](https://github.com/kunansy/RNC/blob/master/docs/HTTP%20params.md)
---


## Requirements
* Python >= 3.7


## Licence
`rnc` is offered under MIT licence.


## Source code
The project is hosted on [Github](https://github.com/kunansy/RNC)

---

Please file an issue in the [bug tracker](https://github.com/kunansy/RNC/issues) 
if you have found a bug or have some suggestions to improve the library.
