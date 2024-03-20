import dataclasses

import json
import os
from pathlib import Path

from sagemaker.workflow.pipeline import Pipeline
import sagemaker
from sagemaker.workflow.pipeline_context import PipelineSession
from sagemaker.workflow.steps import ProcessingStep
from sagemaker.processing import ScriptProcessor, FrameworkProcessor
from sagemaker.processing import ProcessingInput, ProcessingOutput
from sagemaker.pytorch.processing import PyTorchProcessor
from sagemaker.workflow.parameters import (
    ParameterInteger,
    ParameterString,
    ParameterFloat,
)

ROOT_DIR = Path(__file__).parent


@dataclasses.dataclass
class PipelineParams:
    processing_instance_count: ParameterInteger
    instance_type: ParameterString
    mse_threshold: ParameterFloat


def define_pipeline_parameters() -> PipelineParams:
    processing_instance_count = ParameterInteger(name="ProcessingInstanceCount", default_value=1)
    instance_type = ParameterString(name="TrainingInstanceType", default_value="ml.t3.medium")
    mse_threshold = ParameterFloat(name="MSEThreshold", default_value=6.0)

    return PipelineParams(processing_instance_count, instance_type, mse_threshold)


def define_preprocessing_step_1(
    pipeline_params: PipelineParams,
    pipeline_session: PipelineSession,
    input_data_s3uri: str,
    source_dir: Path,
    entry_point: Path,
) -> ProcessingStep:
    preprocessor = PyTorchProcessor(
        framework_version="1.8.1",
        role="arn:aws:iam::123456789012:role/service-role/AmazonSageMaker-ExecutionRole-20210601T000001",
        instance_count=pipeline_params.processing_instance_count,
        instance_type=pipeline_params.instance_type,
        sagemaker_session=pipeline_session,
    )
    preprocessor_args = preprocessor.run(
        code=str(entry_point),
        source_dir=str(source_dir),
        inputs=[ProcessingInput(source=input_data_s3uri, destination="/opt/ml/processing/input")],
        outputs=[ProcessingOutput(output_name="train", source="/opt/ml/processing/train")],
    )
    preprocsss_step = ProcessingStep(
        name="HogehogeProcess",
        step_args=preprocessor_args,
    )
    return preprocsss_step


sagemaker_session = sagemaker.Session()


def define_pipeline() -> Pipeline:
    sagemaker_session = sagemaker.Session()
    pipeline_session = PipelineSession()

    pipeline_parameters = define_pipeline_parameters()
    processing_step_1 = define_preprocessing_step_1(
        pipeline_parameters,
        pipeline_session,
        "s3://sagemaker-sample-data-us-west-2/processing/census/census-income.csv",
        source_dir=ROOT_DIR / "sample_source_dir",
        entry_point=Path("entry_point.py"),
    )

    return Pipeline(
        name="HogehogePipeline",
        parameters=[
            pipeline_parameters.processing_instance_count,
            pipeline_parameters.instance_type,
            pipeline_parameters.mse_threshold,
        ],
        steps=[processing_step_1],
    )


if __name__ == "__main__":
    pipeline = define_pipeline()

    pipeline_definition = pipeline.definition()
    definition = json.loads(pipeline_definition)
    print(json.dumps(definition, indent=2))
