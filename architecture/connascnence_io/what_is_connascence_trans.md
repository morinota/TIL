## Link リンク

- https://connascence.io/ https

> Two software components are connascent if a change in one would require the other to be modified in order to maintain the overall correctness of the system.
>
> システム全体の正しさを維持するために、一方を変更すると他方も変更する必要がある場合、2つのソフトウェアコンポーネントは"conascent"(結合?)している.

# What is COnnascence? COnnascenceとは何か？

Connascence is a software quality metric & a taxonomy for different types of coupling..
Connascenceは、ソフトウェアの品質指標であり、**さまざまなタイプのカップリングのための分類法**でもある.

This site is a handy reference to the various types of connascence, with examples to help you improve your code..
本サイトは、様々な種類のconnascence を、例題を交えて紹介し、コードの改良に役立てることを目的とした便利なリファレンスである.

## Subject to Change Subject to Change

All code is subject to change.
すべてのコードは変更される可能性がある.
As the real world changes, so too must our code.
現実の世界が変化するにつれて、私たちのコードも変化していかなければならない.
Connascence gives us an insight into the long-term impact our code will have on flexibility, as we write it.
Connascenceは、私たちのコードが柔軟性に与える長期的な影響について、それを書きながら洞察してくれる.
Maintaining a flexible codebase is essential for maintaining long-term development velocity..
**柔軟なコードベースを維持することは、長期的な開発速度を維持するために不可欠**である.

## A Flexible Metric A Flexible Metric.

Connascence is a metric, and like all metrics is an imperfect measure.
Connascenceは指標であり、他の指標と同様、不完全な尺度である.
However, connascence takes a more holistic approach, where each instance of connascence in a codebase must be considered on three separate axes:.
しかし、connascenceはより全体的なアプローチをとり、コードベース内のconnascenceの各インスタンスを次の**3つの軸**で考慮する必要がある.

- 1. **Strength**. Stronger connascences are harder to discover, or harder to refactor. 1. 強さです。 強力なコネクションは発見しにくい、あるいはリファクタリングしにくい。

- 2. **Degree**. An entity that is connascent with thousands of other entities is likely to be a larger issue than one that is connascent with only a few. 度です。 何千もの他のエンティティとつながっているエンティティは、数個のエンティティとつながっているエンティティよりも大きな問題になる可能性が高いです。

- 3. **Locality**. Connascent elements that are close together in a codebase are better than ones that are far apart. ロカリティ コードベースの中で近い位置にあるconnascenceの方が、遠い位置にあるものよりも優れているのである.

The three properties of Strength, Degree, and Locality give the programmer all the tools they need in order to make informed decisions about when they will permit certain types of coupling, and when the code ought to be refactored..
Strength、Degree、Localityの3つの特性は、プログラマが、**ある種の結合をいつ許すか、いつコードをリファクタリングすべきか**について、情報に基づいた決定を下すために必要なすべてのツールを提供する.

## A Vocabulary for Coupling

Arguably one of the most important benefits of connascence is that it gives developers a vocabulary to talk about different types of coupling.
connascenceの最も重要な利点の1つは、**開発者に異なるタイプのカップリングについて話すための語彙を与えること**であると思われる.
Connascence codifies what many experienced engineers have learned by trial and error: Having a common set of nouns to refer to different types of coupling allows us to share that experience more easily..
Connascenceは、多くの経験豊かなエンジニアが試行錯誤の末に学んだことを体系化したものである. **異なるタイプのカップリングを指す共通の名詞を持つことで、その経験をより簡単に共有することができる**のである.
