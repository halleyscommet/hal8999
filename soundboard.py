import av
import numpy as np
import sounddevice as sd
from globals import AUDIO_DEVICE

filename = "fard.ogg"
container = av.open(filename)

# Find the first audio stream
stream = next(s for s in container.streams if s.type == 'audio')

# Decode audio frames
frames = []
for packet in container.demux(stream):
    for frame in packet.decode():
        # Convert frame to NumPy array (float32, planar or interleaved)
        frames.append(frame.to_ndarray())

# Stack all frames into one array
audio = np.concatenate(frames, axis=1 if stream.layout.name != "mono" else 0).T

# Get sample rate and channels
samplerate = stream.rate
channels = stream.codec_context.channels

# Reshape if needed for stereo
if channels > 1:
    audio = audio.reshape(-1, channels)

# Play the audio
sd.play(audio, samplerate, device=AUDIO_DEVICE)
sd.wait()
