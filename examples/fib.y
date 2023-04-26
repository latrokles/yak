IN: examples.fib

DEFER: fib
: fib ( n -- n )
      dup 2 <
      [ ]
      [ dup 1 - fib swap 2 - fib + ] 
      if-else ;

: main ( -- ) 30 fib print ;
