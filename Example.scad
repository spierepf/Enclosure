// Lets make the round bits pretty
$fn=32;

// Load the main library
use <Enclosure.scad>

// Start by describing the basic dimensions of your enclosure
myEnclosure = enclosure([80.0, 40.0, 20.0]); // define an enclosure that is 80.0mm x 40.0mm x 20.0mm


// Now lets render the enclosure cover:
difference() {
    // Basic shape for the enclosure cover
    enclosureCover(myEnclosure);
    
    // Need a big hole in the top for the on off switch
    enclosureTop(myEnclosure) cylinder(d=16);
    
    // Add three holes in front to mount LEDs
    enclosureFront(myEnclosure) translate([-10, 0]) cylinder(d=5);
    enclosureFront(myEnclosure) translate([0, 0]) cylinder(d=5);
    enclosureFront(myEnclosure) translate([10, 0]) cylinder(d=5);
}

// Now lets render the snap on base:
translate([0, 0, -10]) enclosureBase(myEnclosure);
