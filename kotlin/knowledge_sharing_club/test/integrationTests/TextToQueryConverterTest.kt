package integrationTests

import TextToQueryConverter
import kotlin.test.Test
import kotlin.test.assertEquals

class TextToQueryConverterTest {
    @Test
    fun WhenUserSayRequestAboutCategoryItConvertToSQLQuery() {
        // Arrange
        val userChat = "私は金融の記事を読みたいです...!"
        val sut = TextToQueryConverter()

        // Act
        val query = sut.convert(userChat)

        // Assert
        assertEquals("SELECT * FROM items WHERE category = 'finance'", query)
    }
}