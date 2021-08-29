# Enclosure
OpenSCAD library for generating enclosures.

``` openscad
// Lets make the round bits pretty
$fn=64;

// Load the main library
use <Enclosure.scad>
use <PCB.scad>

// Start by describing the basic dimensions of your enclosure
myEnclosure = enclosure([80.0, 40.0, 25.0]); // define an enclosure that is 80.0mm x 40.0mm x 25.0mm

// This is our PCB
myPCB = pcb([70.0, 30.0], 4.0);

color("green", 0.1) pcb(myPCB);

// Now lets render the enclosure cover:
translate([0, 0, 10]) union() {
    difference() {
        // Basic shape for the enclosure cover
        enclosureCover(myEnclosure);

        // Need a hole on the left for the micro USB connector
        enclosureLeft(myEnclosure) shellScale(myEnclosure) {
            translate([-(11.0-7.0)/2, 15.5]) cylinder(d=7.0);
            translate([(11.0-7.0)/2, 15.5]) cylinder(d=7.0);
            translate([-(11.0-7.0)/2, 15.5-(7.0/2)]) cube([11.0-7.0, 7.0, 1]);
        }

        // Need a hole on the right for the NeoPixel lead
        enclosureRight(myEnclosure) shellScale(myEnclosure) translate([-4,7-1.5,0]) cube([8, 3, 1]);

        // And some holes on the top for the microphone
        enclosureTop(myEnclosure) shellScale(myEnclosure) {
            translate([2.54*(4), 0]) {
                cylinder();
                for (theta = [0, 60, 120, 180, 240, 300]) {
                    rotate([0,0,theta]) translate([0, 2.5, 0]) cylinder();
                }
            }
        }
    }
    coverStandoffs(myEnclosure, myPCB);
}

// Now lets render the snap on base:
translate([0, 0, -10]) union() {
    enclosureBase(myEnclosure);
    baseStandoffs(myEnclosure, myPCB);
}
```
