## link

- https://arxiv.org/abs/2105.08318

## title

Zero-Shot Recommender Systems

## abstract

Performance of recommender systems (RS) relies heavily on the amount of training data available. This poses a chicken-and-egg problem for early-stage products, whose amount of data, in turn, relies on the performance of their RS. On the other hand, zero-shot learning promises some degree of generalization from an old dataset to an entirely new dataset. In this paper, we explore the possibility of zero-shot learning in RS. We develop an algorithm, dubbed ZEro-Shot Recommenders (ZESRec), that is trained on an old dataset and generalize to a new one where there are neither overlapping users nor overlapping items, a setting that contrasts typical cross-domain RS that has either overlapping users or items. Different from categorical item indices, i.e., item ID, in previous methods, ZESRec uses items' natural-language descriptions (or description embeddings) as their continuous indices, and therefore naturally generalize to any unseen items. In terms of users, ZESRec builds upon recent advances on sequential RS to represent users using their interactions with items, thereby generalizing to unseen users as well. We study three pairs of real-world RS datasets and demonstrate that ZESRec can successfully enable recommendations in such a zero-shot setting, opening up new opportunities for resolving the chicken-and-egg problem for data-scarce startups or early-stage products.
