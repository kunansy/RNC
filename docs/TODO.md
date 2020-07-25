%2C – &
%7C – |
%28 – (
%29 – )
%3A – :


* Написать предупреждения в документах, чего стоит и не стоит делать:
 вот это или тот факт, что нужно передавать при lexgram начальную форму
&spd=1 убивает остальные примеры слова, которые могли быть в этом документе; т.е. если
всего примеров слова 5 на 3 документах: 2 в первом документе, 1 – во втором, 2 – в третьем,
то это значение позволит получить всего 3 примера, по одному на документ.
Например, слова parse или васкуляризация
 
* ParalleCorpus, req in English 'fair', doc =
https://processing.ruscorpora.ru/search.xml?sort=i_grtagging&lex1=fair&env=alpha
&mysize=28363771&max2=1&mysentsize=1608212&mycorp=JSONeyJkb2NfbGFuZyI6IFsiZW5nIl0sICJpc19wYXJhX2JvdGhfcGFpcnMiOiBbdHJ1ZV19
&level1=0&level2=0&mode=para&parent1=0&text=lexgramm&min2=1&parent2=0
&docid=L3BsYWNlL3J1c2NvcnBvcmEvdGV4dHMvZmluYWxpemVkL3BhcmEvcGFyYS9lbmctcnVzL25hYm9rb3YvcGFsZV92ZXJhLnhtbCMxNTcz
Skip the doc, where l1 == l2 (пока что)
Parse doc by <table class='para'>. Язык одинаковый – суммируем в очередной пример,
другой – завершаем первый пример, работаем с новым.