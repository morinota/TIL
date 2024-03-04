## refs

- [現在の MLOps に関わる課題とその解決法を考える](https://recruit.gmo.jp/engineer/jisedai/blog/mlops-far-far-far-best-practice/)
- [LayerXさんのVertexAI Pipelinesの活用例](https://tech.layerx.co.jp/entry/2023/11/16/185944#%E5%AE%9F%E9%9A%9B%E3%81%AE%E9%81%8B%E7%94%A8%E6%96%B9%E9%87%9D)
- 柏木さんのブログ[機械学習パイプラインの作り方を改めて考えてみる](https://masatakashiwagi.github.io/portfolio/post/how-to-recreate-ml-pipeline/)
- [Introducing End-to-End MLOps on AWS: Part1](https://medium.com/@datalab_70093/introducing-end-to-end-mlops-on-aws-part1-ae42dad5c487)
-

# orchestrator

- Sagemaker Pipelines もしくは Vertex AI Pipelines
  - booking.comはSagemaker Pipelinesを使っている。LayerXさんはVertex AI Pipelinesを使っている。
- マネージドのKubenetes(結構事例が多いっぽい。デファクトスタンダード?) (AWS EKSやGCP GKE)
  - wantedlyさんはEKSを使ってるっぽい。エムスリーさんはGKEを使ってるっぽい。
  - ZOZOさんもMLOps基盤にKubernetes & Kubeflowを使っているっぽい(https://techblog.zozo.com/entry/mlops-platform-kubeflow)
- その他OSS:
  - (ECSなどに自分でインスタンスを用意する感じ?)
  - Airflowなど
