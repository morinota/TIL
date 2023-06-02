import net.sf.jsqlparser.expression.Expression
import net.sf.jsqlparser.expression.operators.conditional.AndExpression
import net.sf.jsqlparser.expression.operators.conditional.OrExpression
import net.sf.jsqlparser.expression.operators.conditional.XorExpression
import net.sf.jsqlparser.expression.operators.relational.ComparisonOperator
import net.sf.jsqlparser.expression.operators.relational.EqualsTo
import net.sf.jsqlparser.expression.operators.relational.GreaterThanEquals
import net.sf.jsqlparser.expression.operators.relational.MinorThanEquals
import net.sf.jsqlparser.parser.CCJSqlParserUtil
import net.sf.jsqlparser.statement.select.PlainSelect
import net.sf.jsqlparser.statement.select.Select
import net.sf.jsqlparser.statement.select.SelectBody

class ItemFilterByQuery {
    fun filter(sqlQuery: String, items: List<Item>): List<Item> {
        val statement = CCJSqlParserUtil.parse(sqlQuery)
        val select = statement as? Select
        val selectBody = select?.selectBody

        val whereClauseExpression = extractWhereClause(selectBody)
        if (whereClauseExpression == null) {
            println("This query doesn't include Comparison Operator. so return pure items.")
            return items
        }

        println("This query include Comparison Operator. so conduct items filtering.")
        return items.filter { isValidItemByExpression(it, whereClauseExpression) }
    }

    private fun extractWhereClause(selectBody: SelectBody?): Expression? {
        if (selectBody !is PlainSelect) {
            return null
        }
        return selectBody.where
    }

    private fun isValidItemByExpression(item: Item, whereClause: Expression): Boolean {
        return when (whereClause) {
            is AndExpression -> filterItemByAndExpression(item, whereClause)
            is OrExpression -> filterItemByOrExpression(item, whereClause)
            is XorExpression -> filterItemByXorExpression(item, whereClause)
            else -> filterItemBySingleExpression(item, whereClause)
        }
    }

    private fun filterItemByAndExpression(item: Item, andExpression: AndExpression): Boolean {
        val isValidLeft = isValidItemByExpression(item, andExpression.leftExpression)
        val isValidRight = isValidItemByExpression(item, andExpression.rightExpression)
        return isValidLeft and isValidRight
    }

    private fun filterItemByOrExpression(item: Item, orExpression: OrExpression): Boolean {
        val isValidLeft = isValidItemByExpression(item, orExpression.leftExpression)
        val isValidRight = isValidItemByExpression(item, orExpression.rightExpression)
        return isValidLeft or isValidRight
    }

    private fun filterItemByXorExpression(item: Item, xorExpression: XorExpression): Boolean {
        val isValidLeft = isValidItemByExpression(item, xorExpression.leftExpression)
        val isValidRight = isValidItemByExpression(item, xorExpression.rightExpression)
        return isValidLeft xor isValidRight
    }

    private fun filterItemBySingleExpression(item: Item, singleExpression: Expression): Boolean {
        if (singleExpression !is ComparisonOperator) {
            return true
        }
        val column = singleExpression.leftExpression.toString()
        val value = singleExpression.rightExpression.toString().replace("'", "") // 文字列に''が含まれてるので取り除く.

        when (singleExpression) {
            is EqualsTo -> return item.getProperty(column) == value

            is GreaterThanEquals -> {
                val property = item.getProperty(column)
                if (property !is Double) return false
                return property >= value.toDouble()
            }

            is MinorThanEquals -> {
                val property = item.getProperty(column)
                if (property !is Double) return false
                return property <= value.toDouble()
            }
        }
        return true
    }


}
