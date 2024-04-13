import abc
import pydantic
from datetime import datetime
from pathlib import Path
from typing import Final, Optional
import sagemaker
import boto3
from sagemaker.pytorch.estimator import PyTorch
from sagemaker.inputs import TrainingInput
from sagemaker.processing import ProcessingInput, ProcessingOutput
from sagemaker.pytorch import PyTorchProcessor


class BatchJobResult(pydantic.BaseModel):
    batch_job_name: str  # バッチジョブの名前
    result_s3_uri: str  # 成果物のS3 URI


class BatchJobExecutorInterface(abc.ABC):

    @abc.abstractmethod
    def run(self) -> BatchJobResult:
        raise NotImplementedError


class SagemakerTrainingJobExecutor(BatchJobExecutorInterface):
    def __init__(
        self,
        training_job_name: str,
        entry_point_script_path: Path,
        output_s3_uri: str,
        source_dir_path: Optional[Path] = None,
        instance_type: str = "ml.m5.large",
        instance_count: int = 1,
        hyperparameters: dict[str, str] = None,
    ) -> None:
        """
        entry_point_script_pathは、source_dir_pathからの相対パスで指定する必要がある。
        source_dir_pathは、指定したディレクトリ以下の全てが、実行インスタンスのopt/ml/code以下にコピーされる。
        """
        assert training_job_name is not None, "training_job_nameは必須です"
        self.training_job_name = training_job_name

        if source_dir_path:
            assert (
                source_dir_path / entry_point_script_path
            ).exists(), "entry_point_script_pathは、source_dir_pathからの相対パスで指定する必要がある"

        boto3_session = boto3.Session(profile_name=self.PROFILE_NAME)
        self.sagemaker_session = sagemaker.Session(boto_session=boto3_session)

        # sagemaker SDKでは学習処理を管理するクラスをestimatorと呼ぶ
        self.estimator = PyTorch(
            entry_point=str(entry_point_script_path),
            role=self.SERVICE_ROLE,
            instance_count=instance_count,
            instance_type=instance_type,
            framework_version="2.1.0",
            py_version="py310",
            sagemaker_session=self.sagemaker_session,
            # source_dir_pathがNoneでない場合はstrに変換して渡す
            source_dir=str(source_dir_path) if source_dir_path else None,
            output_path=output_s3_uri,
            volume_size=30,
            hyperparameters=hyperparameters,
        )

    def run(self, input_s3uri_by_dataname: dict[str, str] = {}) -> BatchJobResult:
        execution_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
        job_name = f"{self.training_job_name}-{execution_datetime}"
        # channell名を残しておく
        inputs = {
            channel: TrainingInput(s3_data=input_s3uri) for channel, input_s3uri in input_s3uri_by_dataname.items()
        }
        print(inputs)
        self.estimator.fit(inputs, job_name=job_name)
        print("fitting")
        return BatchJobResult(
            batch_job_name=job_name,
            result_s3_uri=f"{self.estimator.output_path}{job_name}/output",
        )


def run_sagemaker_training_job(
    job_name: str,
    source_code_dir_path: Path,
    entry_point_script_path: Path,
    output_s3_uri: str,
    input_s3uri_by_dataname: dict[str, str] = {},
    instance_type: str = "ml.m5.large",
    instance_count: int = 1,
    volume_size_in_gb: int = 30,
    hyperparameters: dict[str, str] = None,
) -> str:
    """Training Jobを実行し、返り値にmodel artifact (i.e. model.tar.gz) のS3 URIを返す。"""
    executor = SagemakerTrainingJobExecutor(
        training_job_name=job_name,
        entry_point_script_path=entry_point_script_path,
        source_dir_path=source_code_dir_path,
        output_s3_uri=output_s3_uri,
        instance_type=instance_type,
        instance_count=instance_count,
        hyperparameters=hyperparameters,
    )
    result_obj = executor.run(input_s3uri_by_dataname=input_s3uri_by_dataname)
    model_artifact_s3uri = result_obj.result_s3_uri
    return model_artifact_s3uri


def run_sagemaker_processing_job(
    job_name: str,
    entry_point_script_path: Path,
    input_s3uri_by_dataname: dict[str, str],
    output_s3uri_by_dataname: dict[str, str],
    source_code_dir_path: Optional[Path] = None,
    instance_type: str = "ml.m5.large",
    instance_count: int = 1,
    volume_size_in_gb: int = 30,
    is_wait: bool = False,
):
    """sagemaker processing jobを実行する。
    - entry_point_script_pathは、source_dir_pathからの相対パスで指定する必要がある。
    - source_dir_pathは、指定したディレクトリ以下の全てが、実行インスタンスのopt/ml/code以下にコピーされる。
    """
    if source_code_dir_path:
        assert (
            source_code_dir_path / entry_point_script_path
        ).exists(), "entry_point_script_pathは、source_dir_pathからの相対パスで指定してください"

    boto3_session = boto3.Session(profile_name=PROFILE_NAME)
    sagemaker_session = sagemaker.Session(boto_session=boto3_session)

    pytorch_processor = PyTorchProcessor(
        role=SERVICE_ROLE,
        instance_count=instance_count,
        instance_type=instance_type,
        framework_version="2.1.0",
        py_version="py310",
        sagemaker_session=sagemaker_session,
        volume_size_in_gb=volume_size_in_gb,
        env={"AWS_DEFAULT_REGION": "ap-northeast-1"},
    )

    inputs = [
        ProcessingInput(
            source=input_s3uri,
            destination=f"/opt/ml/processing/input/{dataname}",
            input_name=dataname,
        )
        for dataname, input_s3uri in input_s3uri_by_dataname.items()
    ]
    outputs = [
        ProcessingOutput(
            source=f"/opt/ml/processing/output/{dataname}",
            destination=output_s3uri,
            output_name=dataname,
        )
        for dataname, output_s3uri in output_s3uri_by_dataname.items()
    ]

    execution_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    pytorch_processor.run(
        code=str(entry_point_script_path),
        source_dir=str(source_code_dir_path) if source_code_dir_path else None,
        inputs=inputs,
        outputs=outputs,
        arguments=[
            "--input",
            "/opt/ml/processing/input",
            "--output",
            "/opt/ml/processing/output",
        ],  # スクリプトに渡すコマンドライン引数
        wait=is_wait,
        logs=True,
        job_name=f"{job_name}-{execution_datetime}",
    )
