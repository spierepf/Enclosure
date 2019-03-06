function tail(list) = len(list) < 2 ? [] : [ for(i=[1:len(list)-1]) list[i] ];
function cat(L1, L2) = [for(L=[L1, L2], a=L) a];
function mapGet(map, key) = map[search([key],map,1,0)[0]][1];
function mapRemove(map, key) = len(map) == 0 ? [] : (map[0][0] == key ? tail(map) : cat([map[0]], mapRemove(tail(map), key)));
function mapSet(map, key, value) = cat([[key, value]], mapRemove(map, key));
