fun main() {
    println("Hello, Morita")
    for (i in 0..9) {
        print(i)
    }
    println("")
}

fun sum(a: Int, b: Int): Int {
    return a + b
}

fun sum(a: Int, b: Int) = a + b

fun printSum(a: Int, b: Int): Unit {
    println(a, b)
}

open class Shape

class Rectangle(var height: Double, var length: Double) : Shape() {
    var perimeter = (height + length) * 2
}
