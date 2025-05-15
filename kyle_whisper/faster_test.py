from faster_whisper import WhisperModel

def load_model_safe(model_size="small"):
    try:
        print(f"🚀 正在尝试用GPU加载 {model_size} 模型...")
        model = WhisperModel(model_size, device="cuda", compute_type="float16")
        print("✅ 成功使用GPU加载")
    except Exception as e:
        print(f"❌ GPU加载失败，错误: {e}")
        print("⚙️ 切换到CPU加载（慢一点）...")
        model = WhisperModel(model_size, device="cpu", compute_type="int8")
    return model

if __name__ == "__main__":
    model = load_model_safe("tiny")
    segments, info = model.transcribe("./audio_recording/61-70970-0000.flac",language="zh",  task="transcribe",)
    for segment in segments:
        print(f"[{segment.start:.2f} --> {segment.end:.2f}] {segment.text}")

    # segments =None,
    # info = None
    # segments, info = model.transcribe("./video/1.mp3",language="zh", task="translate",)
    # for segment in segments:
    #     print(f"[{segment.start:.2f} --> {segment.end:.2f}] {segment.text}")
