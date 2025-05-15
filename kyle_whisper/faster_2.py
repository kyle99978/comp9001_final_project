import os

os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
from faster_whisper import WhisperModel
import torch


def kyle_faster_whisper_1(model_type: str = "tiny",
                          abs_path: str = "",
                          task: str = "transcribe",
                          compute_type: str = "float16",
                          device: str = "cuda" if torch.cuda.is_available() else "cpu"
                          ) -> tuple[list[str], list[str]]:

    if not abs_path:
        raise ValueError("abs_path is required!")
    if not os.path.isfile(abs_path):
        raise FileNotFoundError(f"The file at {abs_path} was not found!")

    valid_model_types = ["tiny", "base", "small", "medium", "large-v2", "large-v3"]
    if model_type not in valid_model_types:
        raise ValueError(f"Invalid model_type: {model_type}. \nValid options are: {valid_model_types}")
    print("000000000000000000000000")
    if device == "cuda" and torch.cuda.is_available() and compute_type in ["int8_float16", "float16", "float32", "int8"]:
        model = WhisperModel(model_type, device="cuda", compute_type=compute_type)
    elif device == "cpu" and compute_type in ["float32", "int8"]:
        model = WhisperModel(model_type, device="cpu", compute_type=compute_type)
    elif device == "cpu" and compute_type in ["float16", "int8_float16"]:
        print(r"cpu: int8_float16 and float16 not support, int8 will be used")
        model = WhisperModel(model_type, device="cpu", compute_type="int8")
    else:
        raise ValueError(f"Unsupported device={device} compute_type={compute_type}")

    print("1111111111111111111111111111111111")
    segments, _ = model.transcribe(
        audio=abs_path,
        task=task,  # transcribe OR translate
        # vad_filter=True,
    )
    print("333333333333333333333")
    for segment in segments:
        print(segment)
        start = segment.start
        end = segment.end
        text = segment.text
        print(f"[{start:.2f}s --> {end:.2f}s] {text}")


    # print(f"[{segment.start:.2f} --> {segment.end:.2f}] {segment.text}")
    print("444444444444444444444")


if __name__ == "__main__":
    # kyle_faster_whisper_1(
    #     model_type="tiny",
    #     abs_path="./video/1.mp3",
    #     task="translate",
    #     # compute_type="float32",
    #     # device="cuda",
    # )

    kyle_faster_whisper_1(
        model_type="tiny",
        abs_path="./video/1.mp3",
        task="transcribe",
        compute_type="float32",
        # device="cuda",
    )


