import java.time.LocalDateTime
import java.time.ZoneId
import java.time.ZonedDateTime
import java.time.format.DateTimeFormatter

fun main(){
    println("Hello World!")

    val input = "2023-03-17 01:36:46.853569"
    val datetime = parseDatetime(input)
    println(datetime)
    println(datetime ::class)
    return
}

fun parseDatetime(datetime_str : String):ZonedDateTime{
    val formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss.SSSSSS")
    val parsedDateTime = LocalDateTime.parse(datetime_str, formatter)
    return parsedDateTime.atZone(ZoneId.of("UTC"))
}