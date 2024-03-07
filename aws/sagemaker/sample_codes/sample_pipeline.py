from psutil import Process
from sagemaker.workflow.parameters import (
    ParameterInteger,
    ParameterString,
    ParameterFloat,
)
from sagemaker.processing import Processor
from sagemaker.processing import ProcessingInput, ProcessingOutput
from sagemaker.workflow.steps import ProcessingStep

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
preprocessor = Processor()
# preprocessor_args = preprocessor.run(
#     inputs=[ProcessingInput(source=input_data_s3uri, destination="/opt/ml/processing/input")],
#     outputs=[ProcessingOutput(output_name="train", source="/opt/ml/processing/train")],
# )
preprocsss_step = ProcessingStep(
    name="HogehogeProcess",
    processor=preprocessor,
    inputs=[ProcessingInput(source=input_data_s3uri, destination="/opt/ml/processing/input")],
    outputs=[ProcessingOutput(output_name="train", source="/opt/ml/processing/train")],
)
