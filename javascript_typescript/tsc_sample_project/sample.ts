let message: string = "Hello World hogehoge??";
console.log(message);

import * as math from "mathjs";

function add_nums(num_1: number, num_2: number): number {
  return num_1 + num_2;
}

function main() {
  console.log("hello, world!");
  let ratingMatrix: math.Matrix;
  let inversedRatingMatrix: math.Matrix;

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

  //   DOMでhtmlを宣言する
  const list: HTMLUListElement = document.createElement("ul");
  const apple: HTMLLIElement = document.createElement("li");
  apple.innerText = "りんごだ...!";
  list.append(apple);
  const orrange: HTMLLIElement = document.createElement("li");
  orrange.innerText = "オレンジだ...!";
  list.append(orrange);
  const grape: HTMLLIElement = document.createElement("li");
  grape.innerText = "ぶどうだ...!";
  list.append(grape);
}

main();
