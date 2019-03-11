# Enclosure
OpenSCAD library for generating enclosures.

``` openscad
// Lets make the round bits pretty
$fn=64;

// Load the main library
use <Enclosure.scad>

// Start by describing the basic dimensions of your enclosure
myEnclosure = enclosure([80.0, 40.0, 20.0]); // define an enclosure that is 80.0mm x 40.0mm x 20.0mm


// Now lets render the enclosure cover:
difference() {
    // Basic shape for the enclosure cover
    enclosureCover(myEnclosure);

    // Need some holes in the top for a couple of potentiometers
    enclosureTop(myEnclosure) translate([-18, 0]) rotate(60) potentiometer();

    enclosureTop(myEnclosure) translate([ 18, 0]) rotate(60) potentiometer();
}

// Now lets render the snap on base:
translate([0, 0, -10]) enclosureBase(myEnclosure);
```
