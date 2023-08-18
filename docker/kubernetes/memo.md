## refs

- https://udemy.benesse.co.jp/development/system/kubernetes.html
- https://kubernetes.io/ja/docs/tutorials/

## めちゃざっくりKubernetesって?

- Kubernetesはコンテナオーケストレーションツールのひとつ。
  - "コンテナオーケストレーション"=複数のコンテナを管理・運用する為の技術。
- “クバーネティス”や“クーべネティス”と読む。ギリシャ語に由来する言葉で、**操縦士やパイロットという意味**らしい。
  - K8s(ケーエイツ)やkubeと略される事もある。
- 例えば、本番環境でサービスを提供しているコンテナがダウンした場合、他のコンテナを起動する必要がある。Kubernetesは、この様な動作の管理を助けてくれる。

### Kubernetes のCompornents

Pod, Node, Clusterという3種の Componentがあるっぽい。

- Kubernetes Clusterは、コンテナ化されたアプリケーションを実行する、Node(=worker machine)の集合

![]https://udemy.benesse.co.jp/wp-content/uploads/Kubernetes-e1604986289452.png
