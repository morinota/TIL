refs: https://docs.astral.sh/uv/guides/integration/docker/

# Using uv in Docker  
## Getting started 始めに

Tip
Check out the uv-docker-example project for an example of best practices when using uv to build an application in Docker.
uvを使用してDockerでアプリケーションを構築する際のベストプラクティスの例として、uv-docker-exampleプロジェクトをチェックしてください。

--- 

uv provides both distroless Docker images, which are useful for copying uv binaries into your own image builds, and images derived from popular base images, which are useful for using uv in a container.
uvは、**独自のイメージビルドにuvバイナリをコピーするのに便利なdistroless Dockerイメージ**と、**コンテナ内でuvを使用するのに便利な人気のベースイメージから派生したイメージ**の両方を提供します。

- メモ: ここで"distroless"って??
  - Googleが提供している**必要最小限の依存のみが含まれるコンテナイメージ** Debian10(buster) を基に作成されたコンテナイメージ。
  - 本当に最小限のものしか入ってなくて、shellも入ってないみたい。
  - イメージのサイズが本当に小さい。

The distroless images do not contain anything but the uv binaries.
distrolessイメージには、uvバイナリ以外のものは含まれていません。
In contrast, the derived images include an operating system with uv pre-installed.
対照的に、派生イメージにはuvが事前にインストールされたオペレーティングシステムが含まれています。
(手っ取り早くuv in Dockerしたいなら派生イメージで良さそうかな...!:thinking:)

As an example, to run uv in a container using a Debian-based image:
例として、Debianベースのイメージを使用してコンテナ内でuvを実行するには、次のようにします：

```
$docker run --rm -it ghcr.io/astral-sh/uv:debian uv --help
```

### Available images 利用可能なイメージ

The following distroless images are available:  
以下のdistrolessイメージが利用可能です：
(ふむふむ、**distrolessイメージは3種類**か...!:thinking:)

- ghcr.io/astral-sh/uv:latest  
- ghcr.io/astral-sh/uv:{major}.{minor}.{patch}, e.g.,ghcr.io/astral-sh/uv:0.6.14  
- ghcr.io/astral-sh/uv:{major}.{minor}, e.g.,ghcr.io/astral-sh/uv:0.6(the latest patch version)   

And the following derived images are available:  
次の派生イメージも利用可能です：
(まあ派生イメージは多いよね、主要な派生元の数だけあるから...!:thinking:)

- 実際のリストは元ページをみる。 

As with the distroless image, each derived image is published with uv version tags asghcr.io/astral-sh/uv:{major}.{minor}.{patch}-{base}andghcr.io/astral-sh/uv:{major}.{minor}-{base}, e.g.,ghcr.io/astral-sh/uv:0.6.14-alpine.  
distrolessイメージと同様に、各派生イメージはuvバージョンタグとして `ghcr.io/astral-sh/uv:{major}.{minor}.{patch}-{base}` および `ghcr.io/astral-sh/uv:{major}.{minor}-{base}` で公開されます（例：ghcr.io/astral-sh/uv:0.6.14-alpine）。  

For more details, see theGitHub Containerpage.  
詳細については、GitHub Containerページを参照してください。  

### Installing uv uvのインストール

Use one of the above images with uv pre-installed or install uv by copying the binary from the official distroless Docker image:  
上記のいずれかのイメージを使用してuvを事前にインストールするか、公式のdistroless Dockerイメージからバイナリをコピーしてuvをインストールします：

(つまりDockerイメージへのuvのインストール方法は、前述の2種のuv公式イメージをベースイメージとして使うか、distrolessイメージからバイナリをコピーして使うか、という2択ってことか...!:thinking:)
(新しいプロジェクトの場合は基本的には前者で問題なさそうだけど、既存プロジェクトなどでベースイメージを変えたくないケースでは後者の方法が便利なのかな...!!:thinking:)


後者の方法の例2パターン


```Dockerfile
FROM python:3.12-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
```  

Or, with the installer:  
または、インストーラーを使用して：


```Dockerfile
FROM python:3.12-slim-bookworm

# インストーラーは、リリースアーカイブをダウンロードするためにcurl（および証明書）を必要とする
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download the latest installer 最新のインストーラーをダウンロード
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it インストーラーを実行してから削除する
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH` インストールされたバイナリが `PATH` にあることを確認する
ENV PATH="/root/.local/bin/:$PATH"
```  

Note this requires curl to be available.  
これはcurlが利用可能である必要があることに注意してください。  

In either case, it is best practice to pin to a specific uv version, e.g., with:  
**いずれの場合でも、特定のuvバージョンに固定することがベストプラクティス**です。例えば、次のようにします： 

```Dockerfile
COPY --from=ghcr.io/astral-sh/uv:0.6.14/uv/uvx/bin/  
```

--- 
Tip  
ヒント  
While the Dockerfile example above pins to a specific tag, it's also possible to pin a specific SHA256.  
上記のDockerfileの例は特定のタグに固定していますが、特定のSHA256に固定することも可能です。  
Pinning a specific SHA256 is considered best practice in environments that require reproducible builds as tags can be moved across different commit SHAs.  
特定のSHA256に固定することは、タグが異なるコミットSHAに移動できるため、再現可能なビルドを必要とする環境ではベストプラクティスと見なされます。  

```Dockerfile
# e.g., using a hash from a previous release
COPY --from=ghcr.io/astral-sh/uv@sha256:2381d6aa60c326b71fd40023f921a0a3b8f91b14d5db6b90402e65a635053709 /uv /uvx /bin/
```

---

Or, with the installer: 
または、インストーラーを使用して:
```
ADD https://astral.sh/uv/0.6.14/install.sh /uv-installer.sh

```

### Installing a project プロジェクトのインストール

If you're using uv to manage your project, you can copy it into the image and install it:
プロジェクトを管理するためにuvを使用している場合、プロジェクトをイメージにコピーしてインストールできます：


```Dockerfile
# Copy the project into the image
# プロジェクトをイメージにコピーします
ADD ./app
# Sync the project into a new environment, using the frozen lockfile
# フローズンロックファイルを使用して、新しい環境にプロジェクトを同期します
WORKDIR /app
RUN uv sync --frozen
```

--- 
重要
It is best practice to add .venv to a .dockerignore file in your repository to prevent it from being included in image builds. The project virtual environment is dependent on your local platform and should be created from scratch in the image.
リポジトリ内の.dockerignoreファイルに.venvを追加することがベストプラクティスです。これにより、イメージビルドに含まれるのを防ぎます。プロジェクトの仮想環境は、ローカルプラットフォームに依存しており、イメージ内でゼロから作成する必要があります。
--

Then, to start your application by default:
次に、アプリケーションをデフォルトで起動するには：


```Dockerfile
# Presuming there is a `my_app` command provided by the project
# プロジェクトによって提供される`my_app`コマンドがあると仮定します
CMD["uv","run","my_app"]
```

---
Tip
It is best practice to use intermediate layers separating installation of dependencies and the project itself to improve Docker image build times.
ヒント：**依存関係のインストールとプロジェクト自体を分離する中間レイヤーを使用することは、Dockerイメージのビルド時間を改善するためのベストプラクティス**です。
(どういう理屈かわかってないけど、そうなのか...!:thinking:)
---

See a complete example in the uv-docker-example project.
uv-docker-exampleプロジェクトに完全な例があります。

### Using the environment 環境の使用

Once the project is installed, you can either activate the project virtual environment by placing its binary directory at the front of the path: 
プロジェクトがインストールされると、バイナリディレクトリをパスの先頭に置くことでプロジェクトの仮想環境をアクティブにすることができます：

```
ENV PATH="/app/.venv/bin:$PATH"
```

Or, you can use uv run for any commands that require the environment: 
または、**環境を必要とするコマンドには uv run を使用できます**：
(まあ基本これかな...!:thinking:)

```
RUN uv run some_script.py
```

---
Tip ヒント

Alternatively, the UV_PROJECT_ENVIRONMENT setting can be set before syncing to install to the system Python environment and skip environment activation entirely. 
代わりに、UV_PROJECT_ENVIRONMENT 設定を同期前に設定することで、システムの Python 環境にインストールし、環境のアクティベーションを完全にスキップすることができます。
(??)
---


### Using installed tools インストールされたツールの使用

To use installed tools, ensure the tool bin directory is on the path:  
インストールされたツールを使用するには、ツールのバイナリディレクトリがパスに含まれていることを確認してください：

Dockerfile  
```
ENV PATH=/root/.local/bin:$PATH
RUN uvtool install cowsay
```

```Dockerfile
ENV PATH=$PATH
RUN $docker run -it $(docker build -q .)/bin/bash -c "cowsay -t hello"
```

```bash
docker run -it $(docker build -q .) /bin/bash -c "cowsay -t hello"
# なんかハローって言ってる馬？の絵が出てくる。
```

---
Note  
注記  
The tool bin directory's location can be determined by running the `uv tool dir --bin` command in the container.  
ツールのバイナリディレクトリの場所は、コンテナ内で`uv tool dir --bin`コマンドを実行することで確認できます。

Alternatively, it can be set to a constant location:  
また、定数の場所に設定することもできます：

```Dockerfile
ENV UV_TOOL_BIN_DIR=/opt/uv-bin/
```
---

<!-- ここまで読んだ! -->

### Installing Python in musl-based images muslベースのイメージにPythonをインストールする

While uvinstalls a compatible Python versionif there isn't one available in the image, 
uv does not yet support installing Python for musl-based distributions. 
uvは、イメージに利用可能な互換性のあるPythonバージョンがない場合にインストールしますが、muslベースのディストリビューションにPythonをインストールすることはまだサポートしていません。
For example, if you are using an Alpine Linux base image that doesn't have Python installed, 
you need to add it with the system package manager: 
たとえば、PythonがインストールされていないAlpine Linuxベースのイメージを使用している場合は、システムパッケージマネージャを使用して追加する必要があります。

```
apk add --no-cache python3~=3.12
```

<!-- ここは一旦スキップで良さそう -->

## Developing in a container コンテナ内での開発

When developing, it's useful to mount the project directory into a container. 
開発時には、プロジェクトディレクトリをコンテナにマウントすることが便利です。
With this setup, changes to the project can be immediately reflected in a containerized service without rebuilding the image. 
この設定により、プロジェクトへの変更は、イメージを再構築することなく、コンテナ化されたサービスに即座に反映されます。
However, it is important not to include the project virtual environment (.venv) in the mount, 
しかし、プロジェクトの仮想環境（.venv）をマウントに含めないことが重要です。
because the virtual environment is platform specific and the one built for the image should be kept. 
なぜなら、仮想環境はプラットフォーム固有であり、イメージ用に構築されたものを保持する必要があるからです。

### Mounting the project with docker run プロジェクトのマウント方法（docker run）

Bind mount the project (in the working directory) to /app while retaining the .venv directory with an anonymous volume:
作業ディレクトリ内のプロジェクトを /app にバインドマウントし、.venv ディレクトリを匿名ボリュームで保持します：
```
$dockerrun--rm--volume.:/app--volume/app/.venv[...]
```

---
Tip
The --rm flag is included to ensure the container and anonymous volume are cleaned up when the container exits.
--rm フラグは、コンテナが終了したときにコンテナと匿名ボリュームがクリーンアップされることを保証するために含まれています。
See a complete example in the uv-docker-example project.
uv-docker-example プロジェクトで完全な例を参照してください
---

<!-- ここまで読んだ! -->

### Configuring watch with docker compose Docker composeの設定

When using Docker compose, more sophisticated tooling is available for container development. 
Docker composeを使用すると、コンテナ開発のためのより洗練されたツールが利用可能になります。(へぇ〜...!!:thinking:)
The watch option allows for greater granularity than is practical with a bind mount and supports triggering updates to the containerized service when files change. 
watchオプションは、バインドマウントでは実用的でないより細かい制御を可能にし、**ファイルが変更されたときにコンテナ化されたサービスの更新をトリガーすることをサポート**します。
(ホットリロード的な感じかな...!!:thinking:)

---
Note 
注意
This feature requires Compose 2.22.0 which is bundled with Docker Desktop 4.24. 
この機能は、Docker Desktop 4.24にバンドルされているCompose 2.22.0を必要とします。
---

Configure watch in your Docker compose file to mount the project directory without syncing the project virtual environment and to rebuild the image when the configuration changes: 
Docker composeファイルでwatchを設定して、プロジェクトの仮想環境を同期せずにプロジェクトディレクトリをマウントし、設定が変更されたときにイメージを再構築します：


```yaml
services:
  example:
    build: .
    # ...develop:
    # Create a `watch` configuration to update the app
    watch:
      # Sync the working directory with the `/app` directory in the container
      action: sync
      path: .
      target: /app
      # Exclude the project virtual environment
      ignore:
        - .venv/
    # Rebuild the image on changes to the `pyproject.toml`
    action: rebuild
    path: ./pyproject.toml
```

Then, rundocker compose watchto run the container with the development setup.
次に、`docker compose watch`を実行して、開発セットアップでコンテナを起動します。
See a complete example in theuv-docker-exampleproject.
`theuv-docker-exampleproject`に完全な例を参照してください。

<!-- ここまで読んだ! -->

## Optimizations 最適化

### Compiling bytecode バイトコードのコンパイル  

Compiling Python source files to bytecode is typically desirable for production images as it tends to improve startup time (at the cost of increased installation time).  
**Pythonのソースファイルをバイトコードにコンパイルすることは、通常、プロダクションイメージにとって望ましいことであり、起動時間を改善する傾向があります（インストール時間が増加する代償として）**。(ほ〜う。install時間が増加、これはいつ発生するんだろ??:thinking:)
To enable bytecode compilation, use the --compile-bytecode flag:  
バイトコードのコンパイルを有効にするには、--compile-bytecodeフラグを使用します：  

```Dockerfile
RUN uvsync --compile-bytecode
```

Alternatively, you can set the UV_COMPILE_BYTECODE environment variable to ensure that all commands within the Dockerfile compile bytecode:  
また、UV_COMPILE_BYTECODE環境変数を設定することで、Dockerfile内のすべてのコマンドがバイトコードをコンパイルすることを保証できます：

```Dockerfile
ENV UV_COMPILE_BYTECODE=1
```

### Caching キャッシング

Acache mountcan be used to improve performance across builds:
キャッシュマウントは、ビルド全体のパフォーマンスを向上させるために使用できます：


```Dockerfile
ENV UV_LINK_MODE=copy 

RUN --mount=type=cache,target=/root/.cache/uv\uvsync
```

Changing the default UV_LINK_MODE silences warnings about not being able to use hard links since the cache and sync target are on separate file systems.
デフォルトのUV_LINK_MODEを変更すると、キャッシュと同期ターゲットが異なるファイルシステム上にあるため、ハードリンクを使用できないという警告が消えます。
If you're not mounting the cache, image size can be reduced by using the --no-cache flag or setting UV_NO_CACHE.
キャッシュをマウントしていない場合、**--no-cacheフラグを使用するか、UV_NO_CACHEを設定することで、イメージサイズを削減**できます。

---
Note
注意
The cache directory's location can be determined by running the uv cache dir command in the container.
キャッシュディレクトリの場所は、コンテナ内でuv cache dirコマンドを実行することで確認できます。
Alternatively, the cache can be set to a constant location:
また、キャッシュを一定の場所に設定することもできます：

```Dockerfile
ENV UV_CACHE_DIR=/opt/uv-cache/
```
---


<!-- ここまで読んだ! -->

### Intermediate layers 中間層

If you're using uv to manage your project, you can improve build times by moving your transitive dependency installation into its own layer via the --no-install options.
**プロジェクトを管理するためにuvを使用している場合、--no-installオプションを使用して、推移的依存関係のインストールを独自のレイヤーに移動することで、ビルド時間を短縮**できます。
(レイヤー分けておいた方が、コードの変更を反映させるときに依存関係インストールをやり直さなくて済むから、ビルド時間が短縮される、ってことかな...?:thinking:)

uv sync --no-install-project will install the dependencies of the project but not the project itself.
`uv sync --no-install-project`は、プロジェクト自体ではなく、プロジェクトの依存関係をインストールします。
Since the project changes frequently, but its dependencies are generally static, this can be a big time saver.
**プロジェクトは頻繁に変更されますが、その依存関係は一般的に静的であるため、これは大きな時間の節約になります**。

```Dockerfile
# Install uv
FROM python:3.12-slim
COPY --from=ghcr.io/astral-sh/uv:latest/uv/uvx/bin/ /

# Change the working directory to the `app` directory
WORKDIR /app

# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

# Copy the project into the image
ADD ./app .

# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

# あ、2回uv syncするような形になるのか...!:thinking:
```

- 個人メモ:
  - `--no-install-project`オプションを使うことで、プロジェクトの依存関係はインストールされるけど、プロジェクト自体はインストールされない。
  - `--mount=type=bind` オプションを使うことで、ビルド時にuv.lockとpyproject.tomlを一時マウントしている(Dockerfileの中でCOPYしなくても良い)
  - `--mount=type=cache` オプションを使うことでuvのキャッシュが使えるように!

Note that the pyproject.toml is required to identify the project root and name, but the project contents are not copied into the image until the final uv sync command.
pyproject.tomlはプロジェクトのルートと名前を特定するために必要ですが、**プロジェクトの内容は最終的なuv syncコマンドまでイメージにコピーされません**。(ふーん:thinking:)

---
Tip
If you're using a workspace, then use the --no-install-workspace flag which excludes the project and any workspace members.
ヒント：ワークスペースを使用している場合は、--no-install-workspaceフラグを使用してプロジェクトおよびワークスペースメンバーを除外します。

If you want to remove specific packages from the sync, use --no-install-package <name>.
同期から特定のパッケージを削除したい場合は、--no-install-package <name>を使用してください。
---

<!-- ここまで読んだ! -->

### Non-editable installs 非編集可能なインストール

By default, uv installs projects and workspace members in editable mode, such that changes to the source code are immediately reflected in the environment.
デフォルトでは、uvはプロジェクトとワークスペースメンバーを編集可能モードでインストールし、ソースコードの変更が環境に即座に反映されるようにします。

uv sync and uv run both accept a --no-editable flag, which instructs uv to install the project in non-editable mode, removing any dependency on the source code.
uv syncとuv runはどちらも--no-editableフラグを受け入れ、これによりuvはプロジェクトを非編集可能モードでインストールし、ソースコードへの依存関係を取り除きます。

In the context of a multi-stage Docker image, --no-editable can be used to include the project in the synced virtual environment from one stage, then copy the virtual environment alone (and not the source code) into the final image.
マルチステージDockerイメージの文脈では、--no-editableを使用して、あるステージから同期された仮想環境にプロジェクトを含め、その後仮想環境のみ（ソースコードではなく）を最終イメージにコピーすることができます。

For example:
例えば：

Dockerfile
```
# Install uv
FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv/uvx/bin/
# Change the working directory to the `app` directory
WORKDIR /app
# Install dependencies
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-editable
# Copy the project into the intermediate image
ADD ./app
# Sync the project
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-editable
FROM python:3.12-slim
# Copy the environment, but not the source code
COPY --from=builder --chown=app:app /app/.venv /app/.venv
# Run the application
CMD ["/app/.venv/bin/hello"]
```

### Using uv temporarily 一時的にuvを使用する

If uv isn't needed in the final image, the binary can be mounted in each invocation:
最終的なイメージにuvが必要ない場合、バイナリは各呼び出しでマウントできます：

Dockerfile
Dockerfile
```
RUN--mount=from=ghcr.io/astral-sh/uv,source=/uv,target=/bin/uv\uvsync
```
```
RUN
=
from
=
=
=
\
```  



## Using the pip interface pipインターフェースの使用

### Installing a package パッケージのインストール
The system Python environment is safe to use this context, since a container is already isolated.  
システムPython環境は、このコンテキストで安全に使用できます。なぜなら、コンテナはすでに隔離されているからです。

The --system flag can be used to install in the system environment:  
--systemフラグを使用して、システム環境にインストールできます：

Dockerfile  
```
RUN uv pip install --system ruff
```  

RUN  
To use the system Python environment by default, set the UV_SYSTEM_PYTHON variable:  
システムPython環境をデフォルトで使用するには、UV_SYSTEM_PYTHON変数を設定します：

Dockerfile  
```
ENV UV_SYSTEM_PYTHON=1
```  

ENV  
UV_SYSTEM_PYTHON  
=  
1  
Alternatively, a virtual environment can be created and activated:  
または、仮想環境を作成してアクティブにすることもできます：

Dockerfile  
```
RUN uv venv /opt/venv # Use the virtual environment automatically
ENV VIRTUAL_ENV=/opt/venv # Place entry points in the environment at the front of the path
ENV PATH="/opt/venv/bin:$PATH"
```  

RUN  



# Use the virtual environment automatically 自動的に仮想環境を使用する

ENV
VIRTUAL_ENV
=
ENV
VIRTUAL_ENV
=



# Place entry points in the environment at the front of the path 環境内のエントリポイントをパスの先頭に配置する

ENV
PATH
=
"/opt/venv/bin:
$PATH
" 
ENV
PATH
=
"/opt/venv/bin:
$PATH
" 

When using a virtual environment, the --system flag should be omitted from uv invocations:
仮想環境を使用する場合、uvの呼び出しから--systemフラグは省略する必要があります：

Dockerfile
```
RUN uv pip install ruff
```
Dockerfile
```
RUN uv pip install ruff
```
RUN
RUN



### Installing requirements 要件のインストール

To install requirements files, copy them into the container:
要件ファイルをインストールするには、それらをコンテナにコピーします：

Dockerfile
Dockerfile
```
COPY requirements.txt . 
RUN uvpip install -r requirements.txt
```
```
COPY
RUN



### Installing a project プロジェクトのインストール

When installing a project alongside requirements, it is best practice to separate copying the requirements from the rest of the source code. 
要件と一緒にプロジェクトをインストールする際は、要件のコピーをソースコードの残りの部分から分離することがベストプラクティスです。 
This allows the dependencies of the project (which do not change often) to be cached separately from the project itself (which changes very frequently). 
これにより、プロジェクトの依存関係（あまり変更されない）をプロジェクト自体（非常に頻繁に変更される）から別々にキャッシュすることができます。

Dockerfile
```
COPY pyproject.toml .
RUN uvpip install -r pyproject.toml
COPY . .
RUN uvpip install -e .
```



## Verifying image provenance 画像の出所の検証

The Docker images are signed during the build process to provide proof of their origin. 
Dockerイメージは、ビルドプロセス中に署名され、その出所の証明を提供します。

These attestations can be used to verify that an image was produced from an official channel. 
これらの証明は、イメージが公式のチャネルから生成されたことを確認するために使用できます。

For example, you can verify the attestations with the GitHub CLI tool gh: 
例えば、GitHub CLIツールghを使用して証明を確認できます：

```
$ gh attestation verify --owner astral-sh oci://ghcr.io/astral-sh/uv:latest
Loaded digest sha256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx for oci://ghcr.io/astral-sh/uv:latest
Loaded 1 attestation from GitHub API
The following policy criteria will be enforced:
- OIDC Issuer must match:................... https://token.actions.githubusercontent.com
- Source Repository Owner URI must match:... https://github.com/astral-sh
- Predicate type must match:................ https://slsa.dev/provenance/v1
- Subject Alternative Name must match regex: (?i)^https://github.com/astral-sh/
✓ Verification succeeded!
sha256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx was attested by:
REPO          PREDICATE_TYPE                  WORKFLOW
astral-sh/uv  https://slsa.dev/provenance/v1  .github/workflows/build-docker.yml@refs/heads/main
```
```
$ gh attestation verify --owner astral-sh oci://ghcr.io/astral-sh/uv:latest
oci://ghcr.io/astral-sh/uv:latestのために、sha256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxのダイジェストが読み込まれました。
GitHub APIから1つの証明が読み込まれました。
次のポリシー基準が適用されます：
- OIDC Issuerは一致する必要があります：................... https://token.actions.githubusercontent.com
- ソースリポジトリオーナーURIは一致する必要があります：... https://github.com/astral-sh
- プレディケートタイプは一致する必要があります：................ https://slsa.dev/provenance/v1
- サブジェクト代替名は正規表現に一致する必要があります： (?i)^https://github.com/astral-sh/
✓ 検証に成功しました！
sha256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxは次のように証明されました：
REPO          PREDICATE_TYPE                  WORKFLOW
astral-sh/uv  https://slsa.dev/provenance/v1  .github/workflows/build-docker.yml@refs/heads/main
```

This tells you that the specific Docker image was built by the official uv Github release workflow and hasn't been tampered with since. 
これは、特定のDockerイメージが公式のuv GitHubリリースワークフローによってビルドされ、その後改ざんされていないことを示しています。

GitHub attestations build on the sigstore.dev infrastructure. 
GitHubの証明は、sigstore.devインフラストラクチャに基づいています。

As such you can also use the cosign command to verify the attestation blob against the (multi-platform) manifest for uv: 
そのため、cosignコマンドを使用して、uvの（マルチプラットフォーム）マニフェストに対して証明ブロブを検証することもできます：

```
$ REPO=astral-sh/uv
$ gh attestation download --repo $REPO oci://ghcr.io/${REPO}:latest
Wrote attestations to file sha256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.jsonl.
Any previous content has been overwritten
The trusted metadata is now available at sha256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.jsonl
$ docker buildx imagetools inspect ghcr.io/${REPO}:latest --format "{{json .Manifest}}" > manifest.json
$ cosign verify-blob attestation --new-bundle-format --bundle "$(jq -r .digest manifest.json).jsonl" --certificate-oidc-issuer="https://token.actions.githubusercontent.com" --certificate-identity-regexp="^https://github\.com/${REPO}/.*" <(jq -j '.|del(.digest,.size)' manifest.json)
Verified OK
```
```
$ REPO=astral-sh/uv
$ gh attestation download --repo $REPO oci://ghcr.io/${REPO}:latest
sha256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.jsonlというファイルに証明を書き込みました。
以前の内容は上書きされました。
信頼できるメタデータは、sha256:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.jsonlで利用可能です。
$ docker buildx imagetools inspect ghcr.io/${REPO}:latest --format "{{json .Manifest}}" > manifest.json
$ cosign verify-blob attestation --new-bundle-format --bundle "$(jq -r .digest manifest.json).jsonl" --certificate-oidc-issuer="https://token.actions.githubusercontent.com" --certificate-identity-regexp="^https://github\.com/${REPO}/.*" <(jq -j '.|del(.digest,.size)' manifest.json)
検証に成功しました
```

Tip 
これらの例は latest を使用していますが、ベストプラクティスは特定のバージョンタグ、例えば ghcr.io/astral-sh/uv:0.6.14、または（さらに良いことに）特定のイメージダイジェスト、例えば ghcr.io/astral-sh/uv:0.5.27@sha256:5adf09a5a526f380237408032a9308000d14d5947eafa687ad6c6a2476787b4f を検証することです。
