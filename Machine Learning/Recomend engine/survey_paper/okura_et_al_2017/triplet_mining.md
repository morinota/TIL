## link

https://omoindrot.github.io/triplet-loss

## title

Triplet Loss and Online Triplet Mining in TensorFlow

## abstruct

In face recognition, triplet loss is used to learn good embeddings (or “encodings”) of faces. If you are not familiar with triplet loss, you should first learn about it by watching this coursera video from Andrew Ng’s deep learning specialization.

Triplet loss is known to be difficult to implement, especially if you add the constraints of building a computational graph in TensorFlow.

In this post, I will define the triplet loss and the different strategies to sample triplets. I will then explain how to correctly implement triplet loss with online triplet mining in TensorFlow.

About two years ago, I was working on face recognition during my internship at Reminiz and I answered a question on stackoverflow about implementing triplet loss in TensorFlow. I concluded by saying:
2年ほど前、Reminizのインターンシップで顔認識の研究をしていたとき、stackoverflowでTensorFlowでトリプレットロスを実装するという質問に答えたことがあります。その際、私はこう締めくくりました。

> Clearly, implementing triplet loss in Tensorflow is hard, and there are ways to make it more efficient than sampling in python but explaining them would require a whole blog post !
> Tensorflowでトリプレットロスを実装するのは難しいのは明らかで、pythonでサンプリングするよりも効率的にする方法がありますが、それを説明するにはブログ記事全体が必要になります !

Two years later, here we go.

All the code can be found on this [github repository](https://github.com/omoindrot/tensorflow-triplet-loss).

# Triplet Loss and Triplet Mining

## Why not just use softmax?

The triplet loss for face recognition has been introduced by the paper FaceNet: A Unified Embedding for Face Recognition and Clustering from Google. They describe a new approach to train face embeddings using online triplet mining, which will be discussed in the next section.
顔認識における三重項損失は、FaceNetという論文で紹介されています。A Unified Embedding for Face Recognition and Clustering from Googleという論文で紹介されています。彼らは**オンライントリプレットマイニング**を用いて顔埋め込みを学習する新しいアプローチについて述べています。

Usually in supervised learning we have a fixed number of classes and train the network using the softmax cross entropy loss. However in some cases we need to be able to have a variable number of classes. In face recognition for instance, we need to be able to compare two unknown faces and say whether they are from the same person or not.
通常、教師あり学習では、**固定数のクラス**があり、ソフトマックス・クロスエントロピー・ロスを用いてネットワークを学習する。しかし、場合によっては、**クラスの数を可変にする必要**があります。例えば、顔認識では、2つの未知の顔を比較して、同一人物の顔かどうかを判断する必要があります。

Triplet loss in this case is a way to learn good embeddings for each face. In the embedding space, faces from the same person should be close together and form well separated clusters.
この場合の三重項損失は、**各顔の良い埋め込み**を学習するための方法である。**埋め込み空間では、同一人物の顔は近く**にあり、**よく分離したクラスタを形成**しているはずです。
(つまり、同じ人のいろんな顔写真の埋め込みベクトルは、似ているように！違う人同士の埋込ベクトル達は似ていないように！)

## Definition of the loss

![](https://omoindrot.github.io/assets/triplet_loss/triplet_loss.png)

fig. Triplet loss on two positive faces (Obama) and one negative face (Macron)

The goal of the triplet loss is to make sure that: Triplet Lossを適用する目的は、生成される埋め込みベクトル達が以下の条件を満たすようにすることである.

- Two examples with the same label have their embeddings close together in the embedding space. 同じラベルを持つ2つの例は、埋め込み空間においてその埋め込みが近接している
- Two examples with different labels have their embeddings far away. ラベルが異なる2つの例では、埋め込みが離れている。

To formalise this requirement, the loss will be defined over triplets of embeddings:
この要件を定式化するために、損失は以下の埋め込みの三つ組に対して定義される：

- an anchor
- a positive of the same class as the anchor
- a negative of a different class

For some distance on the embedding space $d$, , the loss of a triplet $(a, p, n)$ is:

$$
L = \max(d(a,p) - d(a, n) + \text{margin}, 0)
$$

We minimize this loss, which pushes $d(a,p)$ to 0 and $(a,n)$ to be greater than $d(a,p) + \text{margin}$.
この損失を最小にすることで、$d(a,p)$を0に押し上げ、$(a,n)$が$d(a,p) + \text{margin}$ よりも大きくなるようにします。

As soon as $n$ becomes an “easy negative”, the loss becomes zero.
$n$(negative)が「簡単な負」になると同時に、損失は0になります。 (???)

## Triplet mining

Based on the definition of the loss, there are three categories of triplets:
損失の定義に基づき、三つ組には3つのカテゴリーがあります。

- easy triplets:
  - triplets which have a loss of 0, because $d(a,p) + \text{margin} < d(a,n)$
  - 損失が0になるtriplet。
- hard triplets:
  - triplets where **the negative is closer to the anchor than the positive**, i.e $d(a,n) <d(a,p)$
- semi-hard triplets:
  - triplets where the negative is not closer to the anchor than the positive, but which still have positive loss:
  - 三重で、マイナスがプラスよりアンカーに近くないが、それでもプラスの損失があるもの。
  - : $d(a,p) < d(a,n) < d(a,p) + \text{margin}$

Each of these definitions depend on where the negative is, relatively to the anchor and positive. We can therefore extend these three categories to the negatives: hard negatives, semi-hard negatives or easy negatives.
これらの定義はそれぞれ、**アンカーとポジに対するネガティブの相対的な位置関係**によって決まります。したがって、**これらの3つのカテゴリーをネガティブに拡張**して、ハードネガティブ、セミハードネガティブ、イージーネガティブとすることができる。

The figure below shows the three corresponding regions of the embedding space for the negative.
下図は、ネガに対応する埋め込み空間の3つの領域を示しています。

![](https://omoindrot.github.io/assets/triplet_loss/triplets.png)

fig. The three types of negatives, given an anchor and a positive アンカーとポジティブが与えられたときの3種類のネガティブ

Choosing what kind of triplets we want to train on will greatly impact our metrics. In the original Facenet paper, they pick a random semi-hard negative for every pair of anchor and positive, and train on these triplets.
**どのようなトリプレットで学習させるか**は、測定値に大きく影響します。オリジナルのFacenet論文では、**アンカーとポジティブのペアごとにランダムにセミハードなネガティブを選び**、これらのトリプレットで学習しています。

## Offline and online triplet mining

We have defined a loss on triplets of embeddings, and have seen that some triplets are more useful than others. The question now is how to sample, or “mine” these triplets.
我々は、埋め込みのトリプレットに対する損失を定義し、あるトリプレットは他のトリプレットより有用であることを見てきました。問題は、**これらのトリプレットをどのようにサンプリングする**か、つまり「**マイニング**」するかである。

### Offline triplet mining

The first way to produce triplets is to find them offline, at the beginning of each epoch for instance. We compute all the embeddings on the training set, and then only select hard or semi-hard triplets. We can then train one epoch on these triplets.
トリプレットを生成する最初の方法は、例えば各エポックの最初に、オフラインでトリプレットを見つけることである。**学習セット上のすべての埋め込みを計算**し、**ハードまたはセミハードなトリプレットのみを選択**します。そして、これらの**トリプレットを用いて1つのエポックを学習する**ことができます。

Concretely, we would produce a list of triplets $(i,j,k)$. We would then create batches of these triplets of size $B$, which means we will have to compute $3B$ embeddings to get the $B$ triplets, compute the loss of these $B$ triplets and then backpropagate into the network.
具体的には、トリプレットのリスト$(i,j,k)$を作成する。つまり、$B$個のトリプレットを得るために$3B$個の埋め込みを計算し、これらの$B$個のトリプレットの損失を計算し、ネットワークにバックプロパゲートする必要があります。

Overall this technique is not very efficient since we need to do a full pass on the training set to generate triplets. It also requires to update the offline mined triplets regularly.
この手法は、トリプレットを生成するために**トレーニングセットをフルパスする(i.e. パラメータ更新の度に全レコードを一旦モデルに通して埋込を取得するってこと??)必要がある**ため、全体としてあまり効率的ではありません。また、オフラインでマイニングされたトリプレットを定期的に更新する必要があります。

### Online triplet mining

Online triplet mining was introduced in Facenet and has been well described by Brandon Amos in his blog post OpenFace 0.2.0: Higher accuracy and halved execution time.
オンライントリプレットマイニングはFacenetで導入され、Brandon Amosのブログ記事[OpenFace 0.2.0: Higher accuracy and halved execution time](http://bamos.github.io/2016/01/19/openface-0.2.0/)でよく説明されています。

The idea here is to compute useful triplets on the fly, for each batch of inputs. Given a batch of $B$ examples (for instance $B$ images of faces), we compute the $B$ embeddings and we then can find a maximum of $B^3$ triplets. Of course, most of these triplets are not **valid** (i.e. they don’t have 2 positives and 1 negative).
このアイデアは、入力のバッチごとに、有用なトリプレットをその場で計算することである。B$個の例（例えば顔の画像）が与えられたら、B$個の埋め込みを計算し、最大$B^3$個の三つ組を見つけることができる。もちろん、これらの三つ組のほとんどは、**有効**ではない（つまり、2つの正と1つの負を持たない）。

This technique gives you more triplets for a single batch of inputs, and doesn’t require any offline mining. It is therefore much more efficient. We will see an implementation of this in the last part.
この手法では、1つの入力バッチに対してより多くのトリプレットを得ることができ、オフラインマイニングを必要としない。そのため、より効率的です。最終回では、この手法の実装を紹介します。

![](https://omoindrot.github.io/assets/triplet_loss/online_triplet_loss.png)

fig. Triplet loss with online mining: triplets are computed on the fly from a batch of embeddings オンラインマイニングによるトリプレットの損失：トリプレットは埋め込みのバッチからオンザフライで計算される

## Strategies in online mining

In online mining, we have computed a batch of $B$ embeddings from a batch of $B$ inputs. Now we want to generate triplets from these $B$ embeddings.
オンラインマイニングでは、$B$個の入力から$B$個の埋め込みを一括して計算した。次に、これらの$B$個の埋め込みから三つ組を生成したい。

Whenever we have three indices $i,j,k \in [1,B]$, if examples $i$ and $j$ have the same label but are distinct, and example $k$ has a different label, we say that $(i,j,k)$ is a valid triplet. What remains here is to have a good strategy to pick triplets among the valid ones on which to compute the loss.
i,j,kの3つのインデックスがあるとき、**$i$と$j$が同じラベルで区別でき、$k$が異なるラベルであれば、$(i,j,k)$は有効な三つ組である**と言う。ここで残るのは、有効な三つ組の中から損失を計算する三つ組を選ぶ良い方法である。

A detailed explanation of two of these strategies can be found in section 2 of the paper In Defense of the Triplet Loss for Person Re-Identification.
これらの戦略のうち2つについては、論文「[In Defense of the Triplet Loss for Person Re-Identification](https://arxiv.org/abs/1703.07737)」の第2節に詳しい説明がある。

They suppose that you have a batch of faces as input of size $B = PK$, composed of $P$ different persons with $K$ images each. A typical value is $K=4$. The two strategies are:
入力として、$B = PK$の大きさの顔のバッチがあり、$P$人の異なる人物からなり、それぞれ$K$枚の画像があると仮定する。典型的な値は$K=4$である。このとき、2つの戦略がある。

- **batch all**:
  - select all the valid triplets, and average the loss on the hard and semi-hard triplets.**有効なトリプレットをすべて選択**し、ハードおよびセミハードトリプレットの損失を平均化します。
    - a crucial point here is to not take into account the easy triplets (those with loss $0$), as averaging on them would make the overall loss very small. ここで重要なのは，**easy triplets（損失 $0$ のもの）を考慮しないこと**である．なぜなら，これらの3連単を平均化すると，全体の損失が非常に小さくなるからである．
    - this produces a total of $PK(K-1)(PK-K)$ triplets ($PK$ anchors, $K-1$ possible positives per anchor, $PK-K$ possible negatives). これにより、合計 $PK(K-1)(PK-K)$ 個のトリプレットが生成される ($PK$ 個のアンカー、アンカーあたり $K-1$ 個のpossibleなポジティブ、 $PK-K$ 個のpossibleなネガティブ)。
- **batch hard:**
  - for each anchor, select the hardest positive (biggest distance $d(a,p)$) and the hardest negative among the batch. **各アンカーについて、バッチの中で最もハードなポジティブ**（距離 $d(a,p)$ が最大）、最もハードなネガティブを選択する。
  - this produces $PK$ triplets
  - 選択されたトリプレットは、バッチの中で最もhardである

According to the paper cited above, the batch hard strategy yields the best performance:上記の論文によると、バッチハード戦略が最も良い性能を発揮するとのことです:

> Additionally, the selected triplets can be considered moderate triplets, since they are the hardest within a small subset of the data, which is exactly what is best for learning with the triplet loss.
> さらに、選択されたトリプレットは、データの小さなサブセット内で最もhardであるため、適度なトリプレットとみなすことができ、これはまさに**トリプレットロスによる学習に最適なもの**である。(i.e. 明らかに間違えてる問題を復習する！事で一番成長できる！みたいなイメージ！)

However it really depends on your dataset and should be decided by comparing performance on the dev set.
しかし、↑の結論は**データセットに依存**するものであり、**開発セットでのパフォーマンスを比較することによって決定されるべき**ものです。

# A naive implementation of triplet loss トリプレットロスの素朴な実装

In the stackoverflow answer, I gave a simple implementation of triplet loss for offline triplet mining:

# A better implementation with online triplet mining オンライントリプレットマイニングを用いたより良い実装

## Compute the distance matrix

## Batch all strategy

## Batch hard strategy

## Testing our implementation

# Experience with MNIST

# Conclusion

# Resources