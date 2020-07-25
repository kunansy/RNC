#### Corpora
* Main – class **MainCorpus**
  * bigrams – **in developing...**
  * threegrams – **in developing...**
  * 4-grams – **in developing...**
  * 5-grams – **in developing...**
* Syntax – **in developing...**
* Paper – **in developing...**
  * Media 2000 years – **in developing...**
  * Local media – **in developing...**
* Parallel – **in developing...**
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
  * Polish
  * Ukrainian
  * French
  * Finnish
  * Czech
  * Swedish
  * Estonian 
* Russian classics in German translations – **in developing...**
* Multilingual – **in developing...**
* Tutoring – **in developing...**
* Dialect – **in developing...** 
* Poetry – **in developing...**
* Speech – **in developing...**
* Accentology – **in developing...**
* Multimedia – **in developing...**
* Multipark – **in developing...**
  * «Ревизор» – **in developing...**
  * English-Russian – **in developing...**
* Historical – **in developing...**
  * Age-Old Russian – **in developing...**
  * Bounty letters – **in developing...**
  * Old Russian – **in developing...**
  * Church Slavonic – **in developing...**



### TODO
* Прочитать всю документацию на сайте корпуса.

* Запрос всех примеров: известно кол-во вхождений, примерно рассчитывать номер последней 
страницы, запрашивать 5-6 страниц, близких к ориентировочной, проверять, какая из них оказалась 
действительно последней, затем основной запрос страниц до неё
* Mаркировка слов: re, \W вокруг слова, group. Поставить assert, что слово в group == слову из списка искомых. 
* Некоторые примеры теряются: запрос 'лексема', dpp=5, spd=10, 4th page, 16 example. 
В.В. Седов. Этногенез ранних славян.
* Неверная работа маркера, где есть ударение: запрос 'ты', dpp=5, spd=10, 2684-й пример – 
«Не чай у тебя́ в голове́, ― сказа́л И́влев, ― Всё лошадей жале́ешь».
* В синтаксическом: открытьвать PDF файл со структурой или скачивать его (тоже асинхронщина). Опция: скачать все файлы структуры.
* multiprocessing.Pool.map_async для запросов. Будет ли работать и будет ли это лучше текущего решения?



### Completed