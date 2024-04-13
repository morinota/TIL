## refs:

- [Track an experiment while training a Pytorch model with a SageMaker Training Job](https://sagemaker-examples.readthedocs.io/en/latest/sagemaker-experiments/sagemaker_job_tracking/pytorch_script_mode_training_job.html)
- [example一覧](https://docs.aws.amazon.com/sagemaker/latest/dg/experiments-tutorials.html)

# Track an experiment while training a Pytorch model with a SageMaker Training Job

- このexampleでは、2つの概念を紹介する:
  - 1. Experiment:
    - ExperimentはRunの集まり。
    - 1回の試行で`Run`を初期化するときには、そのRunが所属するExperiment名を指定する必要がある。
    - Experimentの名前は、AWSアカウント内で一意である必要がある。
  - 2. Run(=Trial?):
    - 1つのiterationの為の全ての入力、パラメータ、設定、結果で構成される。
- できる事:
  - 実験の成果物(artifacts)をtrackingできる!: (dataset, algorithm, hyperparameters, metrics, etc.)
    - **データセットをtrackingできるってことは、推薦結果一覧のテーブルもtrackingできるよね...! まあtrackingはできるとして、後はプレビュー表示してくれるか**...!?:thinking:

## setup

- Sagemaker Python SDKにて、Sagemaker Experimentsは`Run`クラスを提供しており、新しいexperiment runを作成できる。

```python
from sagemaker.pytorch import PyTorch
from sagemaker.experiments.run import Run
from sagemaker.session import Session
from sagemaker import get_execution_role
from sagemaker.utils import unique_name_from_base

role = get_execution_role()
region = Session().boto_session.region_name


# set new experiment configuration
experiment_name = unique_name_from_base("training-job-experiment")
run_name = "experiment-run-example"
print(experiment_name)
```

## 実験用のコードを実装

- Sagemaker ProcessingJobやTrainingJobで実行するコードを実装する。
- その際、`load_run`関数を使って、実験設定を自動的に検出できる。
  - (なるほど, sessionだけ渡して、experiment名やtrial名は指定しなくとも自動的に検出してくれるのか...!:thinking:)
  - `run.log_parameter`, `run.log_parameters`, `run.log_file`, `run.log_metric`, `run.log_confusion_matrix`等のメソッドを使って、モデルの学習をtrackingできる。

```python
session = Session(boto3.session.Session(region_name=args.region))
with load_run(sagemaker_session=session) as run:
    run.log_parameters(
        {"num_train_samples": len(train_set.data), "num_test_samples": len(test_set.data)}
    )
    ...
```

## TrainingJobの実行

- TrainingJob に **experiment run contextを渡して**実行する...!
  - context managerとして`Run`クラスを使って、with句の中でTrainingJobやProcessingJobを起動したらそれでOK??

```python
# Start training job with experiment setting
with Run(experiment_name=experiment_name, run_name=run_name, sagemaker_session=Session()) as run:
    est = PyTorch(
        entry_point="./script/mnist.py",
        role=role,
        model_dir=False,
        framework_version="1.12",
        py_version="py38",
        instance_type="ml.c5.xlarge",
        instance_count=1,
        hyperparameters={"epochs": 10, "hidden_channels": 5, "optimizer": "adam", "region": region},
        keep_alive_period_in_seconds=3600,
    )

    est.fit()
```

- ちなみに、context managerって...
  - with statement(句)のbodyに対して、前処理と後処理を実行するための概念。
  - context managerは `__enter__()` と`__exit__()`メソッドを持っていて、with句のbodyの実行前後にそれが実行される...!
    - だから`Run`クラスもcontext managerなのであれば、これらのメソッドが実装されているはず...!:thinking:
  - with statementは、毎回同じ様なtry/finally statementを書くのを止める為に導入されたやつ...!

後は、Sagemaker Experiments UIから、各experiment runの結果を確認できるはず...!(AWS ConsoleのSagemaker Studioからアクセスできるやつ...??)
