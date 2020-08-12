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
Searching with gramm params fixed – **Issue 3** closed.


#### 0.3.2 – 06.08.2020
#### Changed
* Default filename contains letters and digits, len = 8.

#### Added
* Corpora classes to `rnc.`
* Working with file: validating, that the Corpus type in the file
is equal to the Corpus class type.   
* Requesting two or more words with one str – **Issue 5** closed.
* Deleting the example by the index – **Issue 6** closed.
* Method `filter` to Corpus – **Issue 9** closed. 


#### Fixed
* Distance between words set – **Issue 7** closed. 
* Order of texts in the ParallelCorpus – **Issue 8** closed.

Other minor fixes and improvements.


#### 0.4 – 08.08.2020
#### Changed
* Docs changed, extended.
* Corpora were renamed.
 
#### Added
* MultilingualParaCorpus
* TutoringCorpus

#### Fixed
* Some Corpora inherited from MainCorpus didn't work.

Minor fixes and improvements.


#### 0.4.1 – 12.08.2020 
#### Changed
* Examples improved and fixed.
* Docs fixed.
* Setting loggers/handlers levels. 

#### Added
* Some features to Example.

Minor fixes and improvements.