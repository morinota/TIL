"use strict";
exports.__esModule = true;
var math = require("mathjs");
var message = "Hello World hogehoge??";
console.log(message);
function add_nums(num_1, num_2) {
    return num_1 + num_2;
}
function main() {
    console.log("hello, world!");
    var ratingMatrix;
    var inversedRatingMatrix;
    console.log(add_nums(1, 10));
    ratingMatrix = math.matrix([
        [5, 3, 0, 1],
        [4, 0, 3, 1],
        [1, 1, 0, 5],
        [1, 0, 3, 4],
    ]);
    console.log(ratingMatrix);
    //   逆行列を計算
    inversedRatingMatrix = math.inv(ratingMatrix);
    console.log(inversedRatingMatrix);
}
main();
