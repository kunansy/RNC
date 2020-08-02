### API for [Russian National Corpus](http://ruscorpora.ru) 

#### Installation
```bash
pip install rnc
```

#### Structure

---
Corpus object contains list of obtained examples.
There're two types:
![](https://github.com/FaustGoethe/RNC/blob/master/docs/Two_ex_types.png?raw=true) <br> 
* If `out` is `normal`, API uses normal example, which name is equal to the Corpus class name:
```python
ru = MainCorpus(...)
ru.request_examples()

print(type(ru[0]))
>>> MainExample
```
* if `out` is `kwic`, API uses `KwicExample`.

Examples' objects [fields](https://github.com/FaustGoethe/RNC/blob/master/docs/Examples.md)   

#### Usage

---
```python
import rnc

ru = rnc.corpus_name(
    query='корпус', 
    p_count=5,
    file='filename.csv',
    marker=str.upper,
    **kwargs
)

ru.request_examples()
```
* query – one str or dict with tags. Word to found, one should give the vocabulary form of it.
* p_count – count of PAGES.
* file – name of local csv file, optional.
* marker – function, with which found wordforms'll be marked. 
* kwargs – additional params.

[Corpora](https://github.com/FaustGoethe/RNC/blob/master/docs/Corpora.md) you can use.

##### Full version of query
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
            # the NAMES of these keys may be any
            'pos (any name)': 'S' or ['S', 'A'], # one value or list of values,
            'case (any name)': 'acc' or ['acc', 'nom'],
        },
        'flags': {}, # all the same to here
        # distance between first and second words
        'min': 1,  
        'max': 3
    },  
}

corp = rnc.corpus_name(
    query=query,
    p_count=5,
    file='filename.csv',
    marker=str.upper,
    **kwargs
)
corp.reques_examples()
```
[Lexgramm search params](https://github.com/FaustGoethe/RNC/tree/master/docs/Lexgram%20search%20params)



##### Additional request params
These params are optional, you can ignore them. Here the default values is shown.
```python
ru = rnc.corpus_name(
    query=query, 
    p_count=5,
    file='filename.csv',
    marker=str.upper, # function, with which found wordforms'll be marked
    
    dpp=5, # documents per page
    spd=10, # sentences per document
    text='lexgramm' or 'lexform', # way to search
    out='normal' or 'kwic', # output format
    kwsz=5, # if out=kwic, count of words in context
    sort='i_grtagging', # way to sort the results
    subcorpus='', # see below how to set it
    accent=0, # with accentology (1) or without (0), if it's available
)
```

##### API can works with local base too
```python
ru = rnc.corpus_name(file='local_database.csv') # it must exist
print(ru)
```
If the file exists, API works with it and you can't request new examples.

##### Working with corpora
```python
corp = rnc.corpus_name(...) 
```
* `corp.request_examples()` – request examples. 
There's an exception if:
    * Data still exist. 
    * No results found.
    * Requested page doesn't exist (if there're 10 pages in the Corpus, but you've requested > 10).
    * There's a mistake in the request.
    * You have no access to Internet.
    * There's a problem while getting access to Corpus.
    * another problems...
* `corp()` – the same as `request_examples()`.
* `corp.data` – list of examples.
* `corp.found_wordforms` – dict with found wordforms and their frequency.
* `corp.dump()` – write two files: csv file with all data and json file with request params.
* `corp.copy()` – create a copy.
* `corp.shuffle()` – shuffle data.
* `corp.pop(index)` – remove and return the example at the index from the data list.
* `corp.sort(key=, reverse=)` – sort the list of examples. Here HTTP keys doesn't work.  
* `corp.url` – URl to first page of the Corpus result.
* `corp.open_url()` – open first page of the Corpus result.
* `str(corp) or print(corp)` – str with info about Corpus, enumerated examples. By default Corpus shows 
first 50 examples, but you can change this value or turn restriction off. 
* `len(corp)` – count if examples.
* `bool(corp)` – whether data exist.
* `corp.dpp` or another request param.
* `corp[index or slice]` – get element at the index or create new obj with sliced data:
```python
first_ten = corp[:10]
``` 
Compare corp length with length of another obj or int.  
* `corp > `
* `corp >= `
* `corp < `
* `corp <= `

Set default values to the all objects you'll create 
* `corpus_name.set_dpp(value)` – change default `document per page` value.
* `corpus_name.set_spd(value)` – change default `sentences per document` value.
* `corpus_name.set_text(value)` – change default search way.
* `corpus_name.set_sort(value)` – change default sort key.
* `corpus_name.set_min(value)` – change default min distance between words.
* `corpus_name.set_max(value)` – change default max distance between words.
* `corpus_name.set_restrict_show(value)` – change default amount of shown example in print. 
If is is equal to `False`, Corpus shows all examples. 

Also you can use cycle for. For example we want to see only left context (out=kwic) and source:
```python
corp = rnc.corpus_name('корпус', 5, out='kwic', kwsz=7)
corp.request_examples()
for r in corp:
    print(r.left)
    print(r.src)
```


#### ATTENTION
* Don't forget to call this function
```python
corp.request_examples()
```
* If you've requested more than 10 pages, Corpus returns 429 error (Too many requests).
For example requesting 100 pages you should wait about 3 minutes: 
![100 pages](https://github.com/FaustGoethe/RNC/blob/master/docs/100_pages.png?raw=true)
* If you want to see messages like that:
```python
rnc.set_stream_handlers_level('DEBUG')
```


#### How to
##### How to set sort?
[Here](https://github.com/FaustGoethe/RNC/blob/master/docs/HTTP%20params.md) you can find sort keys and their descriptions.


##### How to set language in ParallelCorpus?
```python
en = rnc.ParallelCorpus('get', 5, rnc.Subcorpus.Parallel.English)
```
If you want to search something by several languages, choose them and set the subcorpus. 


##### How to set subcorpus?
There're default keys in rnc.Subcorpus.Person – Russian writers and poets: 
* Pushkin
* Dostoyevsky
* TolstoyLN
* Chekhov
* Gogol
* Turgenev

Example:
```python
ru = rnc.MainCorpus('нету', 1, subcorpus=rnc.Subcorpus.Person.Pushkin)
```

**OR**

 
![1](https://raw.githubusercontent.com/FaustGoethe/RNC/master/docs/How%20to%20set%20subcorpus/1.png)
![2](https://raw.githubusercontent.com/FaustGoethe/RNC/master/docs/How%20to%20set%20subcorpus/2.png)
![3](https://raw.githubusercontent.com/FaustGoethe/RNC/master/docs/How%20to%20set%20subcorpus/3.png)
![4](https://raw.githubusercontent.com/FaustGoethe/RNC/master/docs/How%20to%20set%20subcorpus/4.png)

---
[Documentation](https://github.com/FaustGoethe/RNC/tree/master/docs) <br>
[Source](https://github.com/FaustGoethe/RNC)
---
If you found a bug or have an idea to improve the API write to me – alniconim@gmail.com.  

P.S. If your native is Russian or you know it well, please write me in Russian.