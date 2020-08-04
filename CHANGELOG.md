# Changelog

#### 0.1 – 26.07.2020
First release
* `MainCorpus`


#### 0.2 – 26.07.2020
##### Added
* `Paper2000Corpus`
* `PaperRegionalCorpus`
* `DialectCorpus`
* `SpokenCorpus`
* `AccentologyCorpus`


#### 0.2.1 – 31.07.2020
#### Changed
* Marking found wordforms with re.
* Logging simplified.
* Exceptions catching and evaluating.
* Some methods became static.
* `__repr__` and `__str__` methods in `Example` and `Corpus`.
* Ex_type initting fixed. 
* Docs corrected.
* Now one can dump data to files even if they exist.


#### Added
##### To `Corpus`
* Set classmethods.
* Clear function.
* NotImplementedError in `Corpus._parse_doc`.
* Setitem method.
* `Restrict show` param: by default Corpus shows in print 50 examples. 
One can change this param or turn the restriction off.


##### To \_\_init__
* Func to set stream_handlers levels.
* Func to set file_handlers levels.
* Func to set loggers levels.

##### To `Example`
* `data` property, more changes with this.
* Setter methods.


#### 0.3 – 02.08.2020
#### Changed
* Parsing structure corrected.
* `is_http_request_correct` and `whether_result_found` joined, amount of operations deteriorated.
* Order of receiving pages corrected.
* Corpus init divided: _from_file, _from_Corpus.
 

#### Added
* ParallelCorpus.
* Adding found wordforms to the Corpus initting from file.


#### 0.3.1 – 04.08.2020
Searching with gramm params fixed. 