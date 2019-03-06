use <_MapStructure.scad>

module assert(condition, errorMessage) {
    if(!condition) echo(errorMessage);
}

assert(mapGet([["key", "value"]], "key") == "value", "mapGet failed");
assert(mapGet([["key", "value"]], "missingKey") == undef, "mapGet failed");

assert(mapRemove([["key", "value"]], "key") == [], "mapRemove failed");
assert(mapRemove([["key", "value"]], "missingKey") == [["key", "value"]], "mapRemove failed");

assert(mapSet([], "key", "value") == [["key", "value"]], "mapSet failed");
assert(mapSet([["key", "oldValue"]], "key", "value") == [["key", "value"]], "mapSet failed");
assert(mapSet([["key", "value"]], "newKey", "newValue") == [["newKey", "newValue"],["key", "value"]], "mapSet failed");
