import sagemaker
from sagemaker import image_uris
from sagemaker.workflow.parameters import (
    ParameterInteger,
    ParameterString,
    ParameterFloat,
)
from sagemaker.processing import Processor
from sagemaker.processing import ProcessingInput, ProcessingOutput
from sagemaker.workflow.steps import ProcessingStep

# sessionなどの定数の準備
from sagemaker.workflow.pipeline_context import PipelineSession

sagemaker_session = sagemaker.session.Session()
region = sagemaker_session.boto_region_name
role = sagemaker.get_execution_role()
pipeline_session = PipelineSession()

# pipeline parametersの定義
processing_instance_count = ParameterInteger(name="ProcessingInstanceCount", default_value=1)
instance_type = ParameterString(name="TrainingInstanceType", default_value="ml.m5.xlarge")
model_approval_status = ParameterString(name="ModelApprovalStatus", default_value="PendingManualApproval")
input_data_s3uri = ParameterString(
    name="InputData",
    default_value="s3://sagemaker-sample-data-us-west-2/processing/census/census-income.csv",
)
batch_data_s3uri = ParameterString(
    name="BatchData",
    default_value="s3://sagemaker-sample-data-us-west-2/processing/census/census-income.csv",
)
mse_threshold = ParameterFloat(name="MSEThreshold", default_value=6.0)

# 最初のstepの定義
preprocessor = Processor(
    sagemaker_session=pipeline_session,
)
preprocessor_args = preprocessor.run(
    inputs=[ProcessingInput(source=input_data_s3uri, destination="/opt/ml/processing/input")],
    outputs=[ProcessingOutput(output_name="train", source="/opt/ml/processing/train")],
)
preprocsss_step = ProcessingStep(
    name="HogehogeProcess",
    processor=preprocessor,
    inputs=[ProcessingInput(source=input_data_s3uri, destination="/opt/ml/processing/input")],
    outputs=[ProcessingOutput(output_name="train", source="/opt/ml/processing/train")],
)


# 2番目のstepの定義
from sagemaker.estimator import Estimator
from sagemaker.inputs import TrainingInput
from sagemaker.workflow.steps import TrainingStep

model_path = f"s3://sagemaker-sample-data-us-west-2/AbaloneTrain"
image_uri = image_uris.retrieve(
    framework="xgboost",
    region="us-west-2",
    version="1.0-1",
    py_version="py3",
)
xgb_estimator = Estimator(
    image_uri=image_uri,
    instance_type=instance_type,
    instance_count=1,
    output_path=model_path,
    role="arn:aws:iam::123456789012:role/SageMakerHogeRole",
    sagemaker_session=pipeline_session,
)
xgb_estimator.set_hyperparameters(
    objective="reg:linear",
    num_round=50,
    max_depth=5,
    eta=0.2,
    gamma=4,
    min_child_weight=6,
    subsample=0.7,
)

xgb_train_step = TrainingStep(
    name="XGBoostTrain",
    estimator=xgb_estimator,
    inputs={
        "train": TrainingInput(
            s3_data=preprocsss_step.properties.ProcessingOutputConfig.Outputs["train"].S3Output.S3Uri,
            content_type="text/csv",
        ),
        "validation": TrainingInput(
            s3_data=preprocsss_step.properties.ProcessingOutputConfig.Outputs["validation"].S3Output.S3Uri,
            content_type="text/csv",
        ),
    },
)


# 3番目のstepの定義(モデルの評価)
from sagemaker.processing import ScriptProcessor

eval_processor = ScriptProcessor(
    image_uri=image_uri,
    command=["python3"],
    instance_type="ml.m5.xlarge",
    instance_count=1,
    base_job_name="script-processor",
    role=role,
    sagemaker_session=pipeline_session,
)
eval_processor_args = eval_processor.run(
    inputs=[
        ProcessingInput(
            source=xgb_train_step.properties.ModelArtifacts.S3ModelArtifacts,
            destination="/opt/ml/processing/model",
        ),
        ProcessingInput(
            source=preprocsss_step.properties.ProcessingOutputConfig.Outputs["test"].S3Output.S3Uri,
            destination="/opt/ml/processing/test",
        ),
    ],
    outputs=[
        ProcessingOutput(output_name="evaluation", source="/opt/ml/processing/evaluation"),
    ],
    code="code/evaluation.py",
)

from sagemaker.model import Model

model = Model(
    image_uri=image_uri,
    model_data=xgb_train_step.properties.ModelArtifacts.S3ModelArtifacts,
    sagemaker_session=pipeline_session,
    role=role,
)
