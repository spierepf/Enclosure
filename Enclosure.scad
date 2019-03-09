use <_MapStructure.scad>

function enclosure(size, shell=2.0, fillet=3.0, gap=0.1, nubWidth=-1, lipDepth=-1, lipHeight=-1) =
    [
        ["width", size[0]],
        ["depth", size[1]],
        ["height", size[2]],
        ["shell", shell],
        ["fillet", fillet],
        ["gap", gap],
        ["nubWidth", nubWidth == -1 ? 0.50*size[0] : nubWidth],
        ["lipDepth", lipDepth == -1 ? 1.0*shell : lipDepth],
        ["lipHeight", lipHeight == -1 ? 1.5*shell : lipHeight]
    ];

module roundedBox (width, depth, height, fillet) {
    if(fillet > 0) {
        translate([fillet-width/2, fillet-depth/2, 0]) {
            minkowski() {
                cube([width-fillet*2, depth-fillet*2, height-fillet]);
                difference() {
                    sphere(fillet, center=true);
                    translate([0, 0, -fillet])
                    cube(size=fillet * 2, center=true);
                }
            }
        }
    } else {
        translate([-width/2, -depth/2, 0]) cube([width, depth, height]);
    }
}

module roundedRectangle(width, depth, height, fillet) {
    if(fillet > 0) {
        translate([fillet-width/2, fillet-depth/2, 0])
        minkowski() {
            cube([width-fillet*2, depth-fillet*2, height/2]);
            cylinder(r=fillet, h=height/2);
        }
    } else {
         translate([-width/2, -depth/2, 0]) cube([width, depth, height]);
    }
} 

module nub(w, d, h) {
    polyhedron(
        points=[
            [-w/2,     0,   0],
            [-w/2,     0,   h],
            [-w/2+h/2, d, h/2],
            [w/2,      0,   0],
            [w/2,      0,   h],
            [w/2-h/2,  d, h/2]
        ],
        faces=[
            [0, 1, 2],
            [3, 5, 4],
            [0, 3, 4, 1],
            [1, 4, 5, 2],
            [2, 5, 3, 0]
        ]
    );
}

module enclosureCover(enclosure) {
    width = mapGet(enclosure, "width");
    depth = mapGet(enclosure, "depth");
    height = mapGet(enclosure, "height");
    fillet = mapGet(enclosure, "fillet");
    shell = mapGet(enclosure, "shell");
    nubWidth = mapGet(enclosure, "nubWidth");
    lipHeight = mapGet(enclosure, "lipHeight");

    difference() {
        roundedBox ( width, depth, height, fillet );
        translate([0, 0, -0.001])
        roundedBox ( width - 2*shell, depth - 2*shell, height-shell+0.001, fillet-shell);
    }
    rotate(0, [0, 0, 1]) translate([0, -depth/2+shell, 0]) nub(nubWidth, lipHeight/2, lipHeight);
    rotate(180, [0, 0, 1]) translate([0, -depth/2+shell, 0]) nub(nubWidth, lipHeight/2, lipHeight);
}

module enclosureBase(enclosure) {
    width = mapGet(enclosure, "width");
    depth = mapGet(enclosure, "depth");
    fillet = mapGet(enclosure, "fillet");
    shell = mapGet(enclosure, "shell");
    gap = mapGet(enclosure, "gap");
    nubWidth = mapGet(enclosure, "nubWidth");
    lipDepth = mapGet(enclosure, "lipDepth");
    lipHeight = mapGet(enclosure, "lipHeight");

    difference() {
        union() {
            translate([0, 0, -shell]) roundedRectangle(width, depth, shell, fillet);
            difference() {
                roundedRectangle(width-2*(shell+gap), depth-2*(shell+gap), lipHeight, fillet-(shell+gap));
                translate([0, 0, -0.001]) roundedRectangle(width-2*(shell+gap+lipDepth), depth-2*(shell+gap+lipDepth), lipHeight + 0.002, fillet-(2*shell+gap+lipDepth));
            }
        }
        union() {
            rotate(0, [0, 0, 1]) translate([0, -depth/2+shell+gap, 0]) nub(nubWidth, lipHeight/2, lipHeight);
            rotate(180, [0, 0, 1]) translate([0, -depth/2+shell+gap, 0]) nub(nubWidth, lipHeight/2, lipHeight);
            rotate(0, [0, 0, 1]) translate([0, -depth/2+shell+gap, lipHeight/2]) nub(nubWidth, lipHeight/2, lipHeight);
            rotate(180, [0, 0, 1]) translate([0, -depth/2+shell+gap, lipHeight/2]) nub(nubWidth, lipHeight/2, lipHeight);
        }
    }
}

module shellScale(enclosure) {
    shell = mapGet(enclosure, "shell");

    scale([1, 1, shell + 0.01]) children();
}

module enclosureTop(enclosure) {
    height = mapGet(enclosure, "height");
    shell = mapGet(enclosure, "shell");

    translate([0, 0, height-shell-0.01]) shellScale(enclosure) children();
}

module enclosureFront(enclosure) {
    height = mapGet(enclosure, "height");
    depth = mapGet(enclosure, "depth");
    shell = mapGet(enclosure, "shell");

    rotate([90, 0, 0]) translate([0, height/2, depth/2-shell-0.01]) shellScale(enclosure) children();
}

module enclosureBack(enclosure) {
    height = mapGet(enclosure, "height");
    depth = mapGet(enclosure, "depth");
    shell = mapGet(enclosure, "shell");

    rotate([90, 0, 0]) rotate([0, 180, 0]) translate([0, height/2, depth/2-shell-0.01]) shellScale(enclosure) children();
}

module enclosureRight(enclosure) {
    height = mapGet(enclosure, "height");
    width = mapGet(enclosure, "width");
    shell = mapGet(enclosure, "shell");

    rotate([90, 0, 0]) rotate([0, 90, 0]) translate([0, height/2, width/2-shell-0.01]) shellScale(enclosure) children();
}

module enclosureLeft(enclosure) {
    height = mapGet(enclosure, "height");
    width = mapGet(enclosure, "width");
    shell = mapGet(enclosure, "shell");

    rotate([90, 0, 0]) rotate([0, -90, 0]) translate([0, height/2, width/2-shell-0.01]) shellScale(enclosure) children();
}