import java.time.LocalDatetime
fun main(args: Array<String>) {
    val fruits = listOf("banana", "avocado", "apple", "kiwifruit")
    fruits.filter { it.startsWith("a") }.sortedBy { it }.map { it.uppercase() }.forEach {
        println(it)
    }
    println("hoge $fruits")
    val sample_datetime = "2023-03-17 01:36:46.853569"
    val formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSSSSS")
    val parsedDateTime = LocalDateTime.parse(input, formatter)
    println(parsedDateTime)
    val utcDateTime = parsedDateTime.atZone(ZoneId.of("UTC"))
    println(utcDateTime)
}
fun getStringLength(obj:Any):Int?{
    if (obj is String) {
        // `obj` is automatically cast to `String` in this branch
        return obj.length
    }
    // `obj` is still of type `Any` outside of the type-checked branch
    return  null
}