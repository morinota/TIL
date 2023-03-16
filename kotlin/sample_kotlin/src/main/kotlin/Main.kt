fun main(args: Array<String>) {
    val fruits = listOf("banana", "avocado", "apple", "kiwifruit")
    fruits.filter { it.startsWith("a") }.sortedBy { it }.map { it.uppercase() }.forEach {
        println(it)
    }
    println("hoge $fruits")
}
fun getStringLength(obj:Any):Int?{
    if (obj is String) {
        // `obj` is automatically cast to `String` in this branch
        return obj.length
    }
    // `obj` is still of type `Any` outside of the type-checked branch
    return  null
}