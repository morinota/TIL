package integrationTests

import InteractiveRecommender
import Item
import org.junit.jupiter.api.Test
import kotlin.test.assertEquals

class TestInteractiveRecommender {
    private val feedUpdates = listOf(
        Item("1", "政府、地方自治体に対しデジタル化支援金を交付", 0.8, "finance", 0.6),
        Item("2", "日銀、マイナス金利を維持", 0.7, "finance", 0.7),
        Item("3", "日本株式市場、急落", 0.6, "finance", 0.8),
        Item("4", "米中貿易戦争の影響、新興市場に拡大", 0.5, "business", 0.5),
        Item("5", "企業間の競争激化、IT業界にも波及", 0.9, "technology", 0.8),
        Item("6", "景気減速、デフレリスク増加", 0.4, "finance", 0.4),
        Item("7", "ブロックチェーン技術、急速に普及", 0.7, "technology", 0.6),
        Item("8", "日本、TPPに復帰", 0.6, "business", 0.7),
        Item("9", "ロボット革命により雇用機会が減少", 0.3, "industry", 0.4),
        Item("10", "新しい産業革命の波が到来", 0.9, "technology", 0.8)
    )

    @Test
    fun FilteringRecommendationItemsByCategoryWhenGotRequestAboutCategory() {
        // Arrange
        val userComment = "金融に関するニュースに興味があります!"
        val sut = InteractiveRecommender()

        // Act
        val filteredUpdates = sut.recommend(feedUpdates, userComment)

        // Assert
        val filteredUpdatesExpected = listOf(
            Item("1", "政府、地方自治体に対しデジタル化支援金を交付", 0.8, "finance", 0.6),
            Item("2", "日銀、マイナス金利を維持", 0.7, "finance", 0.7),
            Item("3", "日本株式市場、急落", 0.6, "finance", 0.8),
            Item("6", "景気減速、デフレリスク増加", 0.4, "finance", 0.4)
        )
        assertEquals(filteredUpdatesExpected, filteredUpdates)
    }
}
