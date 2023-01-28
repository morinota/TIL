class Student {
  fullName: string;
  constructor(
    public firstName: string,
    public middleInitial: string,
    public lastName: string
  ) {
    this.fullName = firstName + " " + middleInitial + " " + lastName;
  }
}

interface Person {
  firstName: string;
  lastName: string;
} // 引数に渡すオブジェクトのinterfaceを定義: こういう形のobjectが渡される、と明示的にできる.

function greeter(person: Person) {
  return "Hello, " + person.firstName + " " + person.lastName;
}
let user = new Student("Jane", "M", "User");

// document.body.textContent = greeter(user);
console.log(greeter(user));
console.log(typeof user);

const message = "Hello World";
message.toLowerCase();

function flipCoin() {
  return Math.random() < 0.5;
}

const value = Math.random() < 0.5 ? "a" : "b";
console.log(value);

function greet(person: string, date: Date) {
  console.log(
    `Hello ${person.toUpperCase()}, today is ${date.toDateString()}!`
  );
}

greet("Maddison", new Date());

const names = ["ALice", "Bob", "Eve"];

names.forEach(function (s) {
  console.log(s.toUpperCase());
});

names.forEach((s) => {
  console.log(s.toUpperCase());
});

type Point = {
  x: number;
  y: number;
};

function printCoord(pt: Point) {
  console.log("The coordinate's x value is " + pt.x);
  console.log("The coordinate's y value is " + pt.y);
}
printCoord({ x: 3, y: 7 });

function printName(obj: { first: string; last?: string }) {
  if (obj.last !== undefined) {
    console.log(obj.last.toUpperCase());
  }
  //   上と同じ処理
  console.log(obj.last?.toUpperCase());
}

printName({ first: "Bob" });
printName({ first: "Alice", last: "Alisson" });

type ID = number | string;

function printId(id: ID) {
  if (typeof id === "string") {
    console.log(id.toUpperCase());
  } else {
    console.log(id);
  }
}

function welcomePeople(x: string[] | string) {
  if (Array.isArray(x)) {
    // Here: 'x' is 'string[]'
    console.log("Hello, " + x.join(" and "));
  } else {
    // Here: 'x' is 'string'
    console.log("Welcome lone traveler " + x);
  }
}

// Return type is inferred as number[] | string
function getFirstThree(x: number[] | string) {
  return x.slice(0, 3);
}

let changingString = "Hello World";
changingString = "Olá Mundo";
// Because `changingString` can represent any possible string, that
// is how TypeScript describes it in the type system
changingString;
const constantString = "Hello World";
constantString;

function printText(s: string, alignment: "left" | "right" | "center") {
  console.log(s);
}
printText("Hello, world", "left");
// printText("G'day, mate", "centre");

// 数値 literal 型も同じように動作する
function compare(a: string, b: string): -1 | 0 | 1 {
  return a === b ? 0 : a > b ? 1 : -1;
}

// constとしてtype assertionすると、オブジェクト全体をliteral typeに変換できる.
// (i.e.すべてのプロパティが文字列や数値のような一般的なバージョンではなく、literal typeに割り当てられる.)
const req = { url: "https://example.com", method: "GET" } as const;
// handleRequest(req.url, req.method);
