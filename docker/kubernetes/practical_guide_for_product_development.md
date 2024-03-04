## link

- [プロダクト開発のための Kubernetes 入門](https://docs.wantedly.dev/fields/infrastructure/kubernetes-introduction#kubernetes-toha)
- [Kubernetes道場 1日目 - Kubernetesの概要](https://cstoku.dev/posts/2018/k8sdojo-01/)

# Kubernetes とは

- Kubernetesはコンテナオーケストレーションプラットフォーム。 自動的なコンテナのデプロイ、スケーリング、管理などをやってくれる。
  - つまりOrchestratorの一種か...!:thinking_face:
  - Googleが開発。

## Kubernetesで何ができるのか?

- 複数ホストへのコンテナの展開(=デプロイ)
- コンテナのhealth check(=コンテナの状態を監視すること)
- コンテナのscaling(=コンテナの数を増減させること)
- service discovery(?)
- 展開済みコンテナのローリングアップデート(=アプリケーションのアップデートを行うこと?)
- Monitoring と Logging
- Authn/Authz(=認証と認可)
- ストレージのmounting(=外部ストレージリソースをコンテナに取り付けること?)
- CronJobによるバッチ処理のスケジュール実行

## Kubernetesの構成要素

-

# KubernetesにおけるObject

## Objectとは?

- Object とは??

  - Kubernetesの管理下にあるlayerのリソース(Container, Network, Storage, etc.)を抽象化したもの。
    - 詳細は[Kubernetesオブジェクトを理解する](https://kubernetes.io/ja/docs/concepts/overview/working-with-objects/kubernetes-objects/)を参照。
  - Kubernetesクラスタ上の永続的なentity(リソース)。

- Objectを操作(ex. 作成、変更、削除)する際には、Kubernetes APIを使用する。

## Objectのspec(仕様)とstate(状態)

- Kubernetesの根本的な概念に「**Reconciliation Loopによって、Objectで宣言されたspec(i.e. desired state)に、操作対象リソースのstate(i.e. current state)を近づける**」というものがある。
- ex. Podを2つ起動しておきたいとspecで宣言してる状態で、Podが1つになってしまった(state)場合、KubernetesはPodを自動的にもう一つ起動してくれる。
- 詳細は[Kubernetes のしくみ やさしく学ぶ 内部構造とアーキテクチャー](https://www.slideshare.net/ToruMakabe/kubernetes-120907020)を参照

## Objectを記述する

- Objectを作成する場合、objectの基本的な情報(ex. 名前)とともに、望ましい状態を記述したObjectのspecを渡さなければならない。
- 必須field:
  - apiVersion:
    - どのバージョンのKubernetesAPIを利用してobjectを作成するか。
  - kind:
    - どの種類のObjectを作成するか。(Podとか?)
  - metadata:
    - オブジェクトを一意に特定するための情報
    - ex. Objectのname, UID, namespace、
  - `spec`:
    - Objectの望ましい状態を記述する。
- `spec`の正確なformatはObject(のkind?)毎に異なる。
  - 詳しくは[KubernetesAPIのリファレンス](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.29/)を参照。
  - ex.
    - Podオブジェクトのspecのformatは[PodSpec v1 core](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.29/#podspec-v1-core)
    - Deploymentオブジェクトのspecのformatは[DeploymentSpec v1 apps](https://kubernetes.io/docs/reference/generated/kubernetes-api/v1.29/#deploymentspec-v1-apps)

## 主要なObjectの役割(機能)

- Namespace:
  - Kubernetes上のリソースを分類する為の名前空間
  - 操作権限の境界
  - Objectのグルーピング
  - ClusterRole(Binding)などの一部のObject以外は、必ずどこかのNamespaceに属している。
    - Object作成時に所属するNamespaceを指定しない場合、`default`Namespaceが指定される。
  - ex. マイクロサービスごとにNamespaceを分ける。
- Pod:
  - Kubernetesにおけるアプリケーションの最小構成単位。
  - コンテナの集まり
    - **1つのPodにN個のContainer**が含まれる。
- Node:
  - VMもしくは物理マシンに相当するもの。
    - ex. AWS上の1つのEC2インスタンス
  - Node上には複数のPodがデプロイされる。
- ReplicaSet:
  - Poｄの管理を行うObject
  - 指定した数のPodを複製・維持する。
    - ex. 2つのPodを起動してほしいと宣言しておくと、ReplicaSetはPodが1つになった場合、勝手にもう1つPodを起動してくれる。
- Deployment:
  - ReplicaSetの世代管理を行うObject
    - (世代管理 = versioningのことっぽい?:thinking:)
  - PodのRolling Update。
    - (=新しいバージョンのPodを段階的に安全にデプロイする事っぽい = rollout??)
  - 以前のReplicaSetまでのRollback
- Job:
  - Podを起動して、指定されたOne Shotなコマンドを実行する。
- CronJob:
  - 指定した時刻にJobを起動する。
  - (batch処理のスケジューラ的な役割か...!:thinking:)
- Service:
  - Podへの通信を管理する。
  - Podに対する L4(TCP/IP) Load Balancer。(??)
  - Podに対して通信しようと思ったら、Serviceを追加する必要がある。
- Ingress:
  - Pod(Services)への通信を管理する。
  - Pod(Services)に対する L7(HTTP) Load Balancer。(??)
    - URL 上の Path でルーティングを切り替えるとかはこのレイヤでないと出来ない
  -
