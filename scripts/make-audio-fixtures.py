"""Generate the audio fixtures for the three sound-engineering skills.

Deterministic: every value comes from math, no randomness seeded from the clock.
Run from the repository root with `python3`.
"""

import math
import os
import struct
import wave

RATE = 48000
ROOT = "evals/fixtures"


def write_mono(path, samples, rate=RATE, width=2, normalize=True):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    peak = max(1e-9, max(abs(v) for v in samples)) if normalize else 1.0
    with wave.open(path, "wb") as out:
        out.setnchannels(1)
        out.setsampwidth(width)
        out.setframerate(rate)
        out.writeframes(b"".join(pcm(v, peak, width) for v in samples))


def write_stereo(path, left, right, rate=RATE, width=2):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    peak = max(1e-9, max(abs(v) for v in left + right))
    with wave.open(path, "wb") as out:
        out.setnchannels(2)
        out.setsampwidth(width)
        out.setframerate(rate)
        out.writeframes(b"".join(pcm(a, peak, width) + pcm(b, peak, width) for a, b in zip(left, right)))


def pcm(value, peak, width):
    full = 32767 if width == 2 else 8388607
    scaled = int(round(value / peak * 0.9 * full))
    scaled = max(-full, min(full, scaled))
    if width == 2:
        return struct.pack("<h", scaled)
    return scaled.to_bytes(3, "little", signed=True)


def kick(duration=2.0, hits=(0.0, 0.5, 1.0, 1.5)):
    out = []
    for n in range(int(RATE * duration)):
        t = n / RATE
        value = 0.0
        for hit in hits:
            d = t - hit
            if 0 <= d < 0.35:
                value += math.sin(2 * math.pi * 60 * d) * math.exp(-d / 0.09)
                if d < 0.004:
                    value += 0.6 * math.sin(2 * math.pi * 1800 * d)
        out.append(value)
    return out


def bass(duration=2.0):
    return [math.sin(2 * math.pi * 55 * n / RATE) * (0.7 + 0.3 * math.sin(2 * math.pi * 0.5 * n / RATE))
            for n in range(int(RATE * duration))]


def pad(duration=2.0):
    return [0.6 * math.sin(2 * math.pi * 220 * n / RATE) + 0.4 * math.sin(2 * math.pi * 330 * n / RATE)
            for n in range(int(RATE * duration))]


def vocal(duration=2.0):
    out = []
    for n in range(int(RATE * duration)):
        t = n / RATE
        vibrato = 1 + 0.01 * math.sin(2 * math.pi * 5 * t)
        gate = 1.0 if math.sin(2 * math.pi * 0.8 * t) > -0.2 else 0.0
        out.append(0.5 * math.sin(2 * math.pi * 440 * vibrato * t) * gate)
    return out


def norm(track, target=0.25):
    peak = max(abs(v) for v in track) or 1.0
    return [v / peak * target for v in track]


def mixing_fixture():
    base = f"{ROOT}/mixing-and-gain-staging/session"
    write_mono(f"{base}/stems/kick.wav", norm(kick(), 0.25))
    write_mono(f"{base}/stems/bass.wav", norm(bass(), 0.18))
    left, right = norm(pad(), 0.22), norm(pad(), 0.22)
    write_stereo(f"{base}/stems/pad.wav", left, [-v for v in right])
    write_mono(f"{base}/stems/vocal.wav", norm(vocal(), 0.20))

    bounce_left = [a + b + l + v for a, b, l, v in zip(norm(kick(), 0.25), norm(bass(), 0.18), left, norm(vocal(), 0.20))]
    bounce_right = [a + b + r + v for a, b, r, v in zip(norm(kick(), 0.25), norm(bass(), 0.18), [-x for x in right], norm(vocal(), 0.20))]
    write_stereo(f"{base}/mix-v1.wav", bounce_left, bounce_right)


def loudness_fixture():
    base = f"{ROOT}/loudness-and-mastering/album"
    duration = 3.0
    left, right = [], []
    for n in range(int(RATE * duration)):
        t = n / RATE
        body = (0.9 * math.sin(2 * math.pi * 60 * t)
                + 0.5 * math.sin(2 * math.pi * 220 * t)
                + 0.35 * math.sin(2 * math.pi * 440 * t)
                + 0.2 * math.sin(2 * math.pi * 880 * t))
        pulse = math.exp(-((t % 0.5) / 0.08)) * 0.6
        left.append(body + pulse)
        right.append(body * 0.95 + pulse * 1.05)
    write_stereo(f"{base}/mix-master.wav", left, right)


def room_ir(duration=2.0, rt60=0.55):
    decay = math.log(1000.0) / rt60
    out = []
    for n in range(int(RATE * duration)):
        t = n / RATE
        body = math.exp(-decay * t)
        signal = (body * math.sin(2 * math.pi * 1200 * t) * math.exp(-t / 0.02)
                  + 0.45 * body * math.sin(2 * math.pi * 59 * t)
                  + 0.3 * body * math.sin(2 * math.pi * 118 * t))
        if n == 0:
            signal += 1.0
        out.append(signal)
    return out


def measurement_fixture():
    base = f"{ROOT}/audio-measurement-and-analysis/lab"
    write_mono(f"{base}/room-ir.wav", room_ir())
    reference = [0.12 * math.sin(2 * math.pi * 1000 * n / RATE) for n in range(RATE)]
    write_mono(f"{base}/chain-in.wav", reference, normalize=False)
    # The chain under test adds 3 dB and nothing else: the null test should show
    # a full-level residual, which reads as "level change, not transparent".
    write_mono(f"{base}/chain-out.wav", [v * 1.41 for v in reference], normalize=False)


if __name__ == "__main__":
    mixing_fixture()
    loudness_fixture()
    measurement_fixture()
    for root, _, files in os.walk(ROOT):
        for name in sorted(files):
            if name.endswith(".wav"):
                path = os.path.join(root, name)
                print(f"{path} {os.path.getsize(path)} bytes")
