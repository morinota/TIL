plugins {
    kotlin("jvm") version "1.8.0"
    kotlin("plugin.serialization").version("1.6.21")
    application
}

group = "org.example"
version = "1.0-SNAPSHOT"

repositories {
    mavenCentral()
}
repositories {
    mavenCentral()
}
dependencies {
    testImplementation(kotlin("test"))
    implementation("com.github.jsqlparser:jsqlparser:4.6")
    implementation("org.jetbrains.kotlinx:dataframe:0.10.0")
    implementation("com.aallam.openai:openai-client:3.2.3")
    implementation("io.ktor:ktor-client-java:2.3.0")
    implementation("com.squareup.okhttp3:okhttp:4.9.0")
    implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.5.0")

}

tasks.test {
    useJUnitPlatform()
}

kotlin {
    jvmToolchain(8)
}

application {
    mainClass.set("MainKt")
}

