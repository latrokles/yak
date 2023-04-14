# performance

Doing some off the cuff tests on `examples/while.yak` I saw that `yak` runs about 20 times slower than python code that does the same. This isn't all that surprising with all the copying and reference chasing `yak` is doing, but it would be nice if I can bring it down to about a factor of 5 so I want to do some more in-depth profiling to see if there's something I can do to get there, I have an inkling that there may be a handful of changes that I could make to get within 10X. Still this needs some more profiling.

## preliminaries

Originally I was getting runtimes that were about 100+ times slower than python. Doing some cursory profiling with `py-spy` and `cProfile`+`snakeviz` I found that the interpreter was spending a lot of time logging the callstack and callframe (one reason to not have logging in your interpreter) and after removing them we got to the 20x above.

A little more digging shows some codepaths that - while not taking long per call - get called a lot:

- `quotation.py`'s `empty`, `count`, `head`, `tail`.
- `stack.py`'s `check_available` and `pop`.
- `interpreter.py`'s `fetch_word`
- `codebase.py`'s `get_word`

Some of these are needed, but maybe we can optimize a few things.

For example, the reason `(fetch/get)_word` get called is because `yak` doesn't "compile" word definitions into the parse tree, but instead uses word references so that the definition gets fetched at evaluation time. This makes `DEFER`s easy and simplifies redefining words at runtime, but the flipside is that `yak` spends a lot of time going after these.

Not sure what to do about `quotation` since that's just how the callstack works... it gets called for everything.

Anyway, the idea here is just to keep track of some pointers to come back to later.

## some resources:

- [py-spy](https://github.com/benfred/py-spy)
- [yappi](https://github.com/sumerc/yappi/)
- [snakeviz](https://jiffyclub.github.io/snakeviz/)
- [how to profile your code in python](https://towardsdatascience.com/how-to-profile-your-code-in-python-e70c834fad89)
- [hyperfine](https://github.com/sharkdp/hyperfine) more of a benchmarking tool, but it'd be helpful for comparisons.
