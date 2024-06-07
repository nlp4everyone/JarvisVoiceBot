from pvrecorder import PvRecorder
import wave,struct
from config import audio_params
audio_file = "audio_recording.wav"

def get_audio_device() -> list:
    return PvRecorder.get_available_devices()

def start_recording(device_index: int = -1) -> None:
    recorder = PvRecorder(device_index = device_index, frame_length = 512)

    audio = []

    try:
        recorder.start()

        while True:
            frame = recorder.read()
            audio.extend(frame)
    except KeyboardInterrupt:
        recorder.stop()

        with wave.open(audio_file,'w') as f:
            f.setparams((1,2,16000,512,"NONE","NONE"))
            f.writeframes(struct.pack("h"*len(audio),*audio))
    finally:
        recorder.delete()

def main():
    # Print selecting notification
    print("Here is list index of devices: ")
    # Print device
    list_devices = get_audio_device()
    for (i,device) in enumerate(list_devices):
        print(f"[{i}]: {device}")

    # Insert index
    index = input("\nPlease insert your index device: ")
    # Validate infor
    if not index.isnumeric():
        raise Exception("Index must be numberic")
    index = int(index)

    # Check if device existed in list
    if int(index) > len(list_devices) - 1:
        raise Exception("Index device must be inside list")
    # Inform state
    print(f"Connected to {list_devices[index]}")

    # Get response
    start_recording(device_index = index)

if __name__ == "__main__":
    main()