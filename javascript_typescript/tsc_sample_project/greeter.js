var Student = /** @class */ (function () {
    function Student(firstName, middleInitial, lastName) {
        this.firstName = firstName;
        this.middleInitial = middleInitial;
        this.lastName = lastName;
        this.fullName = firstName + " " + middleInitial + " " + lastName;
    }
    return Student;
}());
function greeter(person) {
    return "Hello, " + person.firstName + " " + person.lastName;
}
var user = new Student("Jane", "M", "User");
// document.body.textContent = greeter(user);
console.log(greeter(user));
console.log(typeof user);
var message = "Hello World";
message.toLowerCase();
function flipCoin() {
    return Math.random() < 0.5;
}
var value = Math.random() < 0.5 ? "a" : "b";
console.log(value);
function greet(person, date) {
    console.log("Hello ".concat(person.toUpperCase(), ", today is ").concat(date.toDateString(), "!"));
}
greet("Maddison", new Date());
var names = ["ALice", "Bob", "Eve"];
names.forEach(function (s) {
    console.log(s.toUpperCase());
});
names.forEach(function (s) {
    console.log(s.toUpperCase());
});
function printCoord(pt) {
    console.log("The coordinate's x value is " + pt.x);
    console.log("The coordinate's y value is " + pt.y);
}
printCoord({ x: 3, y: 7 });
function printName(obj) {
    var _a;
    if (obj.last !== undefined) {
        console.log(obj.last.toUpperCase());
    }
    //   上と同じ処理
    console.log((_a = obj.last) === null || _a === void 0 ? void 0 : _a.toUpperCase());
}
printName({ first: "Bob" });
printName({ first: "Alice", last: "Alisson" });
function printId(id) {
    if (typeof id === "string") {
        console.log(id.toUpperCase());
    }
    else {
        console.log(id);
    }
}
function welcomePeople(x) {
    if (Array.isArray(x)) {
        // Here: 'x' is 'string[]'
        console.log("Hello, " + x.join(" and "));
    }
    else {
        // Here: 'x' is 'string'
        console.log("Welcome lone traveler " + x);
    }
}
// Return type is inferred as number[] | string
function getFirstThree(x) {
    return x.slice(0, 3);
}
var changingString = "Hello World";
changingString = "Olá Mundo";
// Because `changingString` can represent any possible string, that
// is how TypeScript describes it in the type system
changingString;
var constantString = "Hello World";
constantString;
function printText(s, alignment) {
    console.log(s);
}
printText("Hello, world", "left");
// printText("G'day, mate", "centre");
// 数値 literal 型も同じように動作する
function compare(a, b) {
    return a === b ? 0 : a > b ? 1 : -1;
}
// constとしてtype assertionすると、オブジェクト全体をliteral typeに変換できる.
// (i.e.すべてのプロパティが文字列や数値のような一般的なバージョンではなく、literal typeに割り当てられる.)
var req = { url: "https://example.com", method: "GET" };
// handleRequest(req.url, req.method);
function doSomething(x) {
    if (x === null) {
        // do nothing
    }
    else {
        console.log("Hello, " + x.toUpperCase());
    }
}
