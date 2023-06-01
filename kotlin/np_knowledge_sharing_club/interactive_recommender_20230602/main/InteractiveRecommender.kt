class InteractiveRecommender() {
    private val itemFilter = ItemFilter()
    private val textToQueryConverter = TextToQueryConverter()
    fun recommend(items: List<Item>, userChat: String): List<Item> {
        val sqlQuery = textToQueryConverter.convert(userChat)
        sqlQuery ?: return items
        return itemFilter.filterByQuery(sqlQuery, items)
    }

}

