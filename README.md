# yakdraw

> **Warning**
>
> **DO NOT USE**
> **this 2D graphics "library" is for personal learning purposes.**

This repository tracks some personal experiments with 2D graphics, mainly implementing some basic 2D graphics primitives and a simple software based 2D raster graphics library.

The main idea is to simulate a framebuffer as an array of pixel values and draw to it using software implementations of 2D graphics algorithms (all CPU, NO graphics hardware).

Since - at the end of the day - I want to display these experiments I have to take a dependency on something that can put things on a OS window (and, thus, the screen). I've chosen SDL2 for its portability, but this could be anything that can take an array of pixels (integer values) and write display them on the screen (a NSWindow + NSImage in macos, a X11 window in linux, not sure about Windows tho).

I'm also using python as the implementation language in the interest of expediency despite the performance penalty it incurs with this type of software. I've been doing a lot of python programming the past couple of years at work so it's really fresh in my head and I know at least one other person who may actually read and play with this code if it's in python. There are a couple other languages I'd like to implement this on, but I'd be learning too many things... I can always re-implemented in other languages later.


## setting up

these are notes for myself.

- clone this repo.
- install with `pip install -e` (use virtual envs)
- run examples with `yak-examples`

## inspiration and references

I'm drawing from stuff that is quite old and perhaps out of date because - quite frankly - more recent resources on graphics bring with them the advances (and let's be honest, the complexity) of modern graphics hardware.

- Plan9's libdraw
- Smalltalk 80's BitBlt
- Fundamentals of Interactive Computer Graphics, J.D. Foley, A. Van Dam,  
- Graphics Gems, Andrew S. Galssner (editor)