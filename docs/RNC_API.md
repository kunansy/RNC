#### Corpora
* Main 
  * bigrams
  * threegrams
  * 4-grams
  * 5-grams
* Syntax
* Paper
  * Media 2000 years
  * Local media
* Parallel
  * English 
  * Armenian
  * Bashkir
  * Belarusian
  * Bulgarian
  * Buryatian 
  * Spanish
  * Italian
  * Chinese
  * Latvian
  * Lithuanian
  * German
  * Russian classics in German translations
  * Polish
  * Ukrainian
  * French
  * Finnish
  * Czech
  * Swedish
  * Estonian 
  * Multilingual 
* Tutoring
* Dialect
* Poetry
* Speech
* Accentology
* Multimedia
* Multipark
  * «Ревизор»
  * English-Russian
* Historical
  * Age-Old Russian
  * bounty letters
  * old Russian
  * Church Slavonic



### TODO
* Прочитать всю документацию на сайте корпуса.

* Запрос всех примеров: известно кол-во вхождений, примерно рассчитывать номер последней 
страницы, запрашивать 5-6 страниц, близких к ориентировочной, проверять, какая из них оказалась 
действительно последней, затем основной запрос страниц до неё
* Mаркировка слов: re, \W вокруг слова, group. Поставить assert, что слово в group == слову из списка искомых. 
* Пространство имён subcorpus со стандартными подкорппусами: тексты А.С. Пушкина (Л.Н. Толстого, Ф.М. Достоевского etc), снятая/неснятая грамматическая омонимия.
i, *** etc для маркировки примеров.
* Некоторые примеры теряются: запрос 'лексема', dpp=5, spd=10, 4th page, 16 example. 
В.В. Седов. Этногенез ранних славян.
* Неверная работа маркера, где есть ударение: запрос 'ты', dpp=5, spd=10, 2684-й пример – 
«Не чай у тебя́ в голове́, ― сказа́л И́влев, ― Всё лошадей жале́ешь».
* В синтаксическом: открытьвать PDF файл со структурой или скачивать его (тоже асинхронщина). Опция: скачать все файлы структуры.
* multiprocessing.Pool.map_async для запросов. Будет ли работать и будет ли это лучше текущего решения?



### Completed