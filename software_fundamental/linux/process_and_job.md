# プロセスとジョブ

## プロセス

- linuxコマンドの実体は、ディスク上に保存されたファイルである。
  - シェルからコマンドを実行すると、Linuxカーネルはディスク(=ストレージ?)から実行ファイルを読み出してメモリに格納し、そのメモリ内容に従ってCPUがプログラムを実行する。
  - ここで、**メモリ上で実行状態にあるプログラム**のことを「プロセス」と呼ぶ。
- `ps`コマンドで、現在動作しているプロセス一覧を確認できる。
  - Linuxはマルチタスク機能によって、さまざまなプロセスが同時に動作している。

## ジョブ

- プロセスは、Linuxカーネルから見た処理の単位である。対して、**シェルから見た処理の単位**を「ジョブ」と呼ぶ。
  - コマンドが1つだけの場合は、プロセスとジョブは同じ単位になる。
  - 一方で、**複数のコマンドをパイプで繋いで実行する場合には、プロセスはコマンドごとに生成されるのに対して、ジョブはコマンドライン全体で1つ**となる。
    - ex. `ls -l | cat ^n | less`の場合、3つのコマンドが実行されるのでプロセスは3つ生成されるが、ジョブは1つ。
- プロセスはシステム全体で一意のプロセスID(PID)を持つが、ジョブはシェルごとに一意なジョブ番号を持つ。
  - よって、複数のターミナルエミュレータを起動して2つ以上のシェルを同時に使ってる場合、ジョブ番号は重複し得る。
- ジョブ制御:
  - シェルの機能を使えば、ジョブを一時停止させたり、バックグラウンド実行させたりなど、ジョブ制御が可能になる。
    - **ジョブ制御を上手く使えば、さまざまな作業を並行して効率よく実行できる。**
- ジョブの状態:
  - フォアグラウンド(fg): ユーザが対話的に操作しながら処理が実行されている状態。
  - バックグラウンド(bg): ユーザが対話的に操作せずに処理が実行されている状態。
  - 一時停止(suspended): 処理を一時的に停止させている状態。
  - （各状態は、ctrl+z, fgコマンド、bgコマンドで遷移可能）
- ジョブという概念の利点:
  - プロセスはLinuxカーネルから見た処理単位。
    - 全てのプロセスにはプロセスIDが付与されてるので、本質的にはプロセスIDで操作すれば色々できる。
  - -> でも、ユーザは多くの場合シェルから操作する
    - プロセスという単位よりも、ジョブという単位の方が多くの場面で利便性が高い...!