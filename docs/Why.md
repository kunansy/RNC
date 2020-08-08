#### Why do we wait for 24s?
100 reqs with 24s sleeping = 173s, 173s executing. <br>

100 reqs with 35s sleeping = 215s, 214s executing. <br>
100 reqs with 30s sleeping = 184s, 185s executing. <br>
100 reqs with 25s sleeping = 180s, 180s executing. <br>
100 reqs with 23s sleeping = 188s, 189s executing. <br>
100 reqs with 20s sleeping = 186s, 185s executing. <br>
More requests, operations <br>
100 reqs with 01s sleeping = 169s, 169s executing. <br>


#### Why asynchronous?
RNC returns 429 error even if the request was synchronous. It's better to use async.