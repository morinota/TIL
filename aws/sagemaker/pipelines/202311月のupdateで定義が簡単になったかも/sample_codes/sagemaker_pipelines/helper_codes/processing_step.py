from pathlib import Path
from typing import Optional
from sagemaker.processing import ScriptProcessor, ProcessingInput, ProcessingOutput
from sagemaker.workflow.steps import ProcessingStep
from sagemaker.workflow.pipeline_context import PipelineSession
from sagemaker.pytorch import PyTorchProcessor

# ScriptProcessorはsource_dir引数が利用不可。(なぜなら単一の.pyを実行することを想定してるから??)
## 参照: https://github.com/aws/sagemaker-python-sdk/issues/2117


def define_processing_step(
    step_name: str,
    pipeline_session: PipelineSession,
    source_dir_path: Path,
    entrypoint_path: Path,
    input_name_by_s3uri: dict[str, str],
    output_name_by_s3uri: dict[str, str],
    instance_type: Optional[str] = None,
    command_line_args: list[str] = [],
    instance_count: int = 1,
    volume_size_in_gb: int = 30,
) -> ProcessingStep:
    """SagemakerProcessingを実行するstepを作成する
    - imageはAWS公式のPyTorchのものを利用する。
        - (全然他のやつでも良さそう)
        - 依存関係をinstallする時間がオーバーヘッドになるのであれば、依存関係をwrapした自作imageを1つ用意して使い回すのはアリ。
    """
    assert source_dir_path.exists(), f"{source_dir_path=}が存在しません"
    assert (
        source_dir_path / entrypoint_path
    ).exists(), f"{entrypoint_path=}は、source_dir_pathからの相対パスで指定してください"

    # create a ScriptProcessor
    pytorch_processor = PyTorchProcessor(
        instance_type=instance_type,
        instance_count=instance_count,
        framework_version="2.1.0",
        py_version="py310",
        sagemaker_session=pipeline_session,
        volume_size_in_gb=volume_size_in_gb,
    )

    # create ProcessingInputs
    processing_inputs = [
        ProcessingInput(
            input_name=input_name,
            source=input_s3uri,
            destination=f"/opt/ml/processing/input/{input_name}",
        )
        for input_s3uri, input_name in input_name_by_s3uri.items()
    ]
    # create ProcessingOutputs
    processing_outputs = [
        ProcessingOutput(
            output_name=output_name,
            source=f"/opt/ml/processing/output/{output_name}",
        )
        for output_name in output_name_by_s3uri.values()
    ]

    # create a ProcessingStep
    return ProcessingStep(
        name=step_name,
        # PipelineSession内で実行しているため、定義時点ではrun()を呼び出しても実行されない。
        step_args=pytorch_processor.run(
            code=str(entrypoint_path),
            source_dir=str(source_dir_path),
            inputs=processing_inputs,
            outputs=processing_outputs,
            arguments=command_line_args,
        ),
    )
