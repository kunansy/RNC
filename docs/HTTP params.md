### Some of Corpus HTTP keys:


**I.** Sorting, key &sort
1. i_grtagging – by default.
2. random – randomly.
3. i_grauthor – by author.
4. i_grcreated_inv – by creation date.
5. i_grcreated – by creation date in reversed order.
6. i_grbirthday_inv – by author's birth date.
7. i_grbirthday – by author's birth date in reversed order.


**II.** Subcorpus type, key &mode
1. main – main (Russian) subcorpus.
2. para – parallel subcorpus (all of them).
3. paper – paper subcorpus.
etc...


**III.** Searching method, key &text:
1. lexgramm – lexical and grammatical search.
2. lexform – search for exact forms, words via &req.


**IV.** Showing format, key &out: 
1. normal – usual.
2. kwic – Key Word In Context.
   2.1 &kwsz – amount of words in context.


**V.** Amount of examples in the document, key &spd
1. &spd – int value


**VI.** Docs per page, key &dpp
1. &dpp – int value


**VII.** Page number, key &p
1. &p – int value
 
 
**VIII.** Distance between n and (n + 1) word, keys &min(n + 1), &max(n + 1)
1. &min(n + 1) – int value
2. &max(n + 1) – int value
 
 
**IX.** &mycorp
1. %28lang%3A%22eng%22%7Clang_trans%3A%22eng%22%29 – for English parallel subcorpus
 
**X.** Nodia=1 – without accentology <br>

**XI.** Unknown keys:
1. &seed=any int, optionally
2. &env=alpha, optionally
3. &level_n=0, optionally
4. &parent_n=0, optionally 
5. &mysentsize=1608212, optionally
6. &mysize=28363771, optionally
