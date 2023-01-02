import interleaving

a = [1, 2, 3, 4, 5]  # Ranking 1
b = [4, 3, 5, 1, 2]  # Ranking 2

method = interleaving.TeamDraft(lists=[a, b])  # initialize an interleaving method
ranking = method.interleave()  # interleaving

print(ranking)
