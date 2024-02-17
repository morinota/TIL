## link

- [プロダクト開発のための Kubernetes 入門](https://docs.wantedly.dev/fields/infrastructure/kubernetes-introduction#kubernetes-toha)
- [Kubernetes道場 1日目 - Kubernetesの概要](https://cstoku.dev/posts/2018/k8sdojo-01/)

# Kubernetes とは

- Kubernetesはコンテナオーケストレーションプラットフォーム。 自動的なコンテナのデプロイ、スケーリング、管理などをやってくれる。
  - Orchestratorの一種か...!:thinking_face:
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

##
