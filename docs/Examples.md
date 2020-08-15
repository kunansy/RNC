### Examples
`expl = corp[0]`
#### MainExample
* `expl.txt` – example's text (getter and setter).
* `expl.src` – example's source (getter and setter).
* `expl.ambiguation` – example's ambiguation (getter and setter).
* `expl.doc_url` – example's URL (only getter).
* `expl.found_wordforms` – example's found wordforms (only getter). 
* `expl.data` – dict of fields' names and their values (only getter).  
There're all fields except for URL. 
* `expl.open_doc()` – open the example in new tab of the default browser.
* `expl.copy()` – create a copy.
* `bool(expl)` – validating that all fields (from `data`) exists.
* `expl == expl1` – are examples equal.
* `'text' in expl` – does expl.txt contain text. 
* print format: <br>
```
    TEXT: ...
    SOURCE: ...
    AMBIGUATION: ...
    FOUND WORDFORMS: ...
```

---

#### KwicExample
* `expl.left` – example's left context (getter and setter).
* `expl.center` – example's center context (getter and setter).
* `expl.right` – example's right context (getter and setter).
* `expl.txt` – example's text, sum all contexts (only getter).
* `expl.ambiguation` **isn't** supported.
* Other fields the same to `MainExample`.
* print format:
```
    LEFT: ...
    CENTER: ...
    RIGHT: ...
    SOURCE: ...
    FOUND WORDFORMS: ...
```

---

#### Paper2000Example
All the same to `MainExample`.

---

#### PaperRegionalExample
All the same to `MainExample`.

---

#### ParallelExample
* `expl.txt` – get dict with {lang: text in the lang} (only getter).
* `expl.sort(key, reverse)` – sort the dict, use the key to lang tags.
* `expl['lang']` – the text in the language (getter and setter).
* `expl.lang` – the text in the language (only getter).
* Other fields the same to `MainExample`.

---

#### MultilingualParaExample
All the same to `ParallelExample`.

---

#### DialectalExample
All the same to `MainExample`.

---

#### SpokenExample
All the same to `MainExample`.

---

#### AccentologicalExample
All the same to `MainExample`.

---

#### TutoringExample
All the same to `MainExample`.

---

#### MultimodalExample
* `expl.filepath` – path to the local media file (getter and setter).
* `expl.download_file()` – download the media file.
* Other the same to `MainExample`.