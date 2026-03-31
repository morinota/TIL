## これは何?

- モバイル開発の基本くらいは理解しておきたいので、Kotlin Coroutines と Flow の基礎をまとめる。

## ざっくりChatGPTと壁打ち

- 前提知識:
  - Android開発における基本的な設計思想: MVVM
    - Model-View-ViewModelの略。**別にAndroidに限った話ではなく、UIアーキテクチャの一般的な設計思想の1つ。**
      - 一言で言うと、責務を分けてるだけ! 
  - MVVMをAndroid開発の実装レベルに落とすと...
    - 例えば [Repository] → [UseCase] → [ViewModel] → [UI]
      - Repository層とUseCase層はMVVMでいうところのModel層にあたる。
      - データの流れとしては...
        - バックエンドAPI -> Repository層 → UseCase層 → ViewModel層 → UI層 ←→ UI操作
    - Repository層
      - データの取得や保存を担当する層。ネットワーク通信やデータベース操作など、データに関する処理を行う。
    - UseCase層
      - ビジネスロジックを担当する層。Repositoryからデータを取得し、必要な処理を行ってViewModelに提供する役割を持つ。
    - ViewModel層
      - UIに表示するデータの管理や、UIからのイベント処理を担当する層。ViewModelはUseCaseからデータを受け取り、UIに提供する役割を持つ。
    - UI層
      - ユーザーインターフェースを担当する層。ViewModelから提供されたデータを表示し、ユーザーの操作をViewModelに伝える役割を持つ。
    

- CoroutinesとFlow:
  - 
