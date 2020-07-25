### API for [National Russian Corpus](http://ruscorpora.ru) 

### Corpora
[All corpora](docs/RNC_API.md)

### Installation
```bash
pip install rnc
```

### Usage

---
```python
import rnc

ru = rnc.corpus_name(
    query='корпус', # word to found, one should give in default case the vocabulary form of it
    p_count=5, # count of PAGES
    file='filename.csv', # name of local csv file, optional
    **kwargs # additional params
)

ru.request_examples()
```

#### Full version of query
```python
query = {
    'word1': {
        'gramm': 'acc', # grammar tags for lexgramm search
        'flags': 'bdot' # additional tags for lexgramm search
    },
    # you can get as a value one string or dict of params
    # params are: any name of dict key, name of tag (you can see them below) by one str or list of str  
    'word2': {
        'gramm': { 
            # the NAMES of these keys may be any
            'pos (any name)': 'S' or ['S', 'A'], 
            'case (any name)': 'acc' or ['acc', 'nom'], # one value or list of values,
        },
        'flags': {}, # all the same to here
        # distance between first and second words
        'min': 1,  
        'max': 5
    },  
}
``` 

```python
ru = rnc.corpus_name(
    query=query,
    p_count=5,
    file='filename.csv',
    **kwargs
)

ru.reques_examples()
```
[Lexgramm search params](docs/Lexgram%20search%20params)


##### Don't forget to call this function
```python
ru.reques_examples()
```

#### All params
These params are additional, you can ignore them. 
```python
ru = rnc.corpus_name(
    query=query, 
    p_count=5,
    file='filename.csv',
    marker=str.upper, # function, with which found wordforms'll be marked
    dpp=5, # documents per page
    spd=1, # sentences per document
    text='lexgramm' or 'lexform', # way to search
    out='normal' or 'kwic', # output format
    kwsz=5, # if out=kwic, count of words in context
    sort='sort_key', # way to sort the results
    subcorpus='', # see below how to set it
    accent=0, # with accentology (1) or without (0), if it is available
)
```

#### API can works with local base too
```python
ru = rnc.corpus_name(file='local_database.csv') # it must exist
print(ru)
```

#### Working with corpora
```python
corp = rnc.corpus_name(...) 
```
* `corp.request_examples()` – request examples. 
There're exceptions if:
    * Data still exists. 
    * No results found.
    * Requested page doesn't exist (if there're 10 pages in the Corpus, but you've requested > 10).
    * There's a mistake in the request.
    * You have no access to Internet.
    * There's a problem while getting access to Corpus.
* `corp()` – the same as `request_examples()`.
* `corp.data` – list of examples.
* `corp.found_wordforms` – dict with found wordforms and their frequency.
* `corp.dump()` – write two files: csv file with all data and json file with request params.
* `corp.copy()` – create a copy.
* `corp.shuffle()` – shuffle data.
* `corp.pop(index)` – remove example at the index from the data list and return it.
* `corp.sort(key=, reverse=)` – sort the list of examples. Here HTTP keys doesn't work.  
* `corp.url` – URl to first page of the Corpus result.
* `corp.open_url()` – open first page of the Corpus result.
* `corp.add_pages()` – in developing...
* `str(corp)`
* `len(corp)` – count if examples.
* `bool(corp)`
* `for r in corp`
* `corp.dpp` or another request param.
* `corp[]`
* `corp > `
* `corp >= `
* `corp < `
* `corp <= `


### ATTENTION
429



### How to
#### How to set sort?
[Here](docs/HTTP%20params.md) you can find sort keys and their descriptions.


#### How to set subcorpus?
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

![1](docs/HOWTO%20set%20subcorpus/1.png)
![2](docs/HOWTO%20set%20subcorpus/2.png)
![3](docs/HOWTO%20set%20subcorpus/3.png)
![4](docs/HOWTO%20set%20subcorpus/4.png)

[docs](docs/Lexgram%20search%20params)


[Why](docs/Why.md)