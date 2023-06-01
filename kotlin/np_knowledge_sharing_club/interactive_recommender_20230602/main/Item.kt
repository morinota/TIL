data class Item(
    val id: String,
    val title: String,
    val score: Double,
    // 記事カテゴリ(business, finance, career, eduacition, technology, industry の6種)
    val category: String,
    val complexity: Double,
)
