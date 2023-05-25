# yak

`yak` is a concatenative programming language that poorly draws ideas from `forth`, `factor`, `retroforth`, and others. It's mainly a personal experiment to see how far I can take this in my personal day to day computing.

## syntax

- series of space delimited tokens
- these tokens can be literals or words.
- `words` are akin to functions in other languages.
- syntax is in Reverse Polish Notation (rpn) (e.g. `1 2 +`).


## values

`yak` supports the following types:

| type identifier | type | description | example |
|-----------------|------|-------------|---------|
|`i`|`int`|integer values |`1`, `1_000`|
|`f`|`float`|floating point values|`2.5`|
|`b`|`bool`|boolean values `t` or `f`|`t` or `f`|
|`s`|`str`|sequences of characters enclosed in double quotes (`"`) |`"hello world!"`|
|`a`|`array`|collections of values|`a{ 1 2 3 5.6 }`|
|`m`|`map`|maps|`m{ "name" bob "age" 10 }`|
|`t`|`tuple`|tuples|`t{ 10 5 }`|
|`q`|`quot`|quotations collections of `words` that can be treated as values.|`[ 1 + ]`|
|`w`|`word`|words, the equivalent of functions or procedures|`add`, `dup`, `swap`|
|`d`|`date`|dates|`d:2023-05-24`, `d:2000-06-11`|
|`dt`|`datetime`|datetimes|`dt:2023-05-25T05:51:59.507975+00:00`|
|`v`|`vocabulary`|named collections of related `words`|...|
|`nil`|`nil`|`nil`|`nil`|
|`obj`|`objects`|user defined objects|...|
|`pob`|`python objects`|python native objects|...|

## running

- `yak` will launch a graphics capable version of yak.
- `yak-cli` will launch a console only version of yak, this is useful for running in systems without a desktop environment.

both of these commands take the same command line arguments.

```
--script FILEPATH	run a specific yak script.
--image  FILEPATH	start yak off a specific image file.
--port   PORT		the port for the interactive server to run in.
```
