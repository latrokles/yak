# TODO

## fixes

- print_object
  - misnomer, it's returning a string
  - split into a representation and output string
    - like `__repr__` and `__str__` in python, but since I want to override `bool` and `None` (among others) I cannot leverage `repr()` and `str()`
	- Factor makes a distinction between `pprint` (in `prettyprint`) and `print` (in `io`).
  - ideas
    - `present`  returns string representation (as in `__repr__`)
	- `output`   returns string for printing (as in `__str__`)
	- `describe` returns object representation for inspection (custom implementation)
	- place these in `primitives.__init__`
	- have them use `repr` and `str` for all `YakPrimitive` values
	- `describe` calls a `__describe__` method in `YakPrimitive` that returns a `Descriptor` object (maybe this needs a new name).
	- implement `__repr__` and `__str__` in each YakPrimitive.
	- implement `io.print` and `io.pprint`
	  - will this require stream to write to?

## code & pkg structure:

## feature

- PRIMITIVE: parse word.
  - would allow `PRIMITIVE: kernel.dup ( x -- x x )` to do all the `def_primitive` under the hood.
  - this way the only two vocabs that have to be built in python code are:
    - bootstrap
	- syntax
  - the rest of the vocabularies can be defined in `yak/lang` as pure `.yak` files.

- control flow
  - will have to define `if-else` in python like I did with `rtkm` and `ruin`.
  - will need either recursion and/or stack combinators (`keep`, `dip`, etc.) to be able to implement looping.
    - `[ ... ] loop`
	- `[ ... ] [ ... ] while`
	- `[ ... ] [ ... ] until`
	- `X [ ... ] repeat`

- parse collections
  - parse assocs
  - parse tuples

- object system
  - classes
  - generic words
  - methods
  - orthogonal persistence of class instances

- codebase
  - ?

- stdlib
  - control flow combinators
    - if-then
	- loop
  - math
  - strings
  - io
  - net
  - http
  - web
  - random
  - test

- graphics
  - ?

- tests
  - ?
