## link リンク

https://netflixtechblog.com/decision-making-at-netflix-33065fa06481
https://netflixtechblog.com/decision-making-at-netflix-33065fa06481

# Decision Making at Netflix ネットフリックスにおける意思決定

This introduction is the first in a multi-part series on how Netflix uses A/B tests to make decisions that continuously improve our products, so we can deliver more joy and satisfaction to our members.
この紹介は、NetflixがどのようにA/Bテストを使用して意思決定を行い、継続的に製品を改善し、会員の皆様にさらなる喜びと満足をお届けできるかを紹介する複数回シリーズの第1回目です。
Subsequent posts will cover the basic statistical concepts underpinning A/B tests, the role of experimentation across Netflix, how Netflix has invested in infrastructure to support and scale experimentation, and the importance of the culture of experimentation within Netflix.
その後の記事では、A/Bテストの基礎となる基本的な統計的概念、Netflixにおける実験の役割、Netflixが実験をサポートし拡大するためのインフラにどのように投資してきたか、Netflixにおける実験文化の重要性について取り上げる予定だ。

Netflix was created with the idea of putting consumer choice and control at the center of the entertainment experience, and as a company we continuously evolve our product offerings to improve on that value proposition.
Netflixは、エンターテインメント体験の中心に消費者の選択とコントロールを置くという理念のもとに誕生し、企業として、その価値提案を改善するために提供する製品を継続的に進化させています。
For example, the Netflix UI has undergone a complete transformation over the last decade.
例えば、ネットフリックスのUIはこの10年で完全に変貌を遂げた。
Back in 2010, the UI was static, with limited navigation options and a presentation inspired by displays at a video rental store.
2010年当時のUIは静的で、ナビゲーションのオプションも限られており、レンタルビデオ店のディスプレイをイメージしたものだった。
Now, the UI is immersive and video-forward, the navigation options richer but less obtrusive, and the box art presentation takes greater advantage of the digital experience.
現在では、UIは没入感があり、映像が前面に押し出され、ナビゲーション・オプションはより豊富でありながら邪魔にならず、ボックスアートの表現もデジタル体験をより活かしている。

Transitioning from that 2010 experience to what we have today required Netflix to make countless decisions.
2010年の経験から現在の状況への移行には、Netflixは数え切れないほどの決断を迫られた。
What’s the right balance between a large display area for a single title vs showing more titles? Are videos better than static images? How do we deliver a seamless video-forward experience on constrained networks? How do we select which titles to show? Where do the navigation menus belong and what should they contain? The list goes on.
1つのタイトルを大きく表示することと、より多くのタイトルを表示することの適切なバランスは？静止画像よりも動画の方が良いのか？制約のあるネットワーク上でシームレスなビデオ転送体験を提供するには？表示するタイトルをどのように選択するか？ナビゲーション・メニューはどこに属し、何を含むべきか？挙げればきりがない。

Making decisions is easy — what’s hard is making the right decisions.
決断を下すのは簡単だ。難しいのは正しい決断を下すことだ。
How can we be confident that our decisions are delivering a better product experience for current members and helping grow the business with new members? There are a number of ways Netflix could make decisions about how to evolve our product to deliver more joy to our members:
自分たちの決断が、現会員にとってより良い製品体験を提供し、新規会員によるビジネスの成長に役立っていると確信するにはどうすればいいのだろうか。ネットフリックスが、会員により多くの喜びを提供するために、商品をどのように進化させるかについて決断する方法はいくつもある：

Let leadership make all the decisions.
リーダーシップにすべての決断を委ねる。

Hire some experts in design, product management, UX, streaming delivery, and other disciplines — and then go with their best ideas.
デザイン、製品管理、UX、ストリーミング配信、その他の分野の専門家を雇い、彼らの最高のアイデアを採用する。

Have an internal debate and let the viewpoints of our most charismatic colleagues carry the day.
社内で議論し、最もカリスマ性のある同僚の視点に任せる。

Copy the competition.
競争相手をコピーする。

In each of these paradigms, a limited number of viewpoints and perspectives contribute to the decision.
いずれのパラダイムにおいても、限られた数の視点や観点が意思決定に貢献する。
The leadership group is small, group debates can only be so big, and Netflix has only so many experts in each domain area where we need to make decisions.
リーダーシップ・グループは小さく、グループ討論はそれほど大きくできないし、ネットフリックスには意思決定が必要な各領域の専門家が限られている。
And there are maybe a few tens of streaming or related services that we could use as inspiration.
そして、私たちがインスピレーションとして使えるようなストリーミングや関連サービスは、おそらく数十はあるだろう。
Moreover, these paradigms don’t provide a systematic way to make decisions or resolve conflicting viewpoints.
さらに、これらのパラダイムは、意思決定や対立する視点を解決する体系的な方法を提供しない。

At Netflix, we believe there’s a better way to make decisions about how to improve the experience we deliver to our members: we use A/B tests.
Netflixでは、会員に提供する体験を改善する方法について、より良い決定方法があると信じています： それはA/Bテストです。
Experimentation scales.
実験の規模。
Instead of small groups of executives or experts contributing to a decision, experimentation gives all our members the opportunity to vote, with their actions, on how to continue to evolve their joyful Netflix experience.
少人数の経営幹部や専門家が意思決定に貢献するのではなく、実験的な試みにより、すべての会員が、楽しいNetflix体験を進化させ続ける方法について、自らの行動で投票する機会が与えられます。

More broadly, A/B testing, along with other causal inference methods like quasi-experimentation are ways that Netflix uses the scientific method to inform decision making.
より広く言えば、A/Bテストは、準実験のような他の因果関係推論手法とともに、ネットフリックスが意思決定に情報を提供するために科学的手法を用いる方法である。
We form hypotheses, gather empirical data, including from experiments, that provide evidence for or against our hypotheses, and then make conclusions and generate new hypotheses.
私たちは仮説を立て、その仮説の根拠となる実証的なデータ（実験を含む）を集め、結論を出し、新たな仮説を生み出す。
As explained by my colleague Nirmal Govind, experimentation plays a critical role in the iterative cycle of deduction (drawing specific conclusions from a general principle) and induction (formulating a general principle from specific results and observations) that underpins the scientific method.
私の同僚であるニルマル・ゴビンドが説明しているように、科学的方法を支える演繹（一般原理から具体的な結論を導き出すこと）と帰納（具体的な結果や観察から一般原理を定式化すること）の反復サイクルにおいて、実験は重要な役割を果たしている。

Curious to learn more? Follow the Netflix Tech Blog for future posts that will dive into the details of A/B tests and how Netflix uses tests to inform decision making.
もっと知りたいですか？Netflix Tech Blogでは、A/Bテストの詳細や、Netflixがどのようにテストを使って意思決定を行っているかをご紹介します。
Part 2 is already available.
パート2はすでに公開されている。