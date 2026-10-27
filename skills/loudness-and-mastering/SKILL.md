---
name: loudness-and-mastering
description: Guides loudness measurement and mastering delivery. Covers choosing the platform or broadcast target, measuring integrated loudness and true peak before processing, setting limiter gain and ceiling, dithering on bit-depth reduction, resampling once, and verifying the exported file against the spec. Use when a master has to hit a loudness target, when exports are quieter or louder than a reference, when true-peak overs appear after limiting, or when preparing distribution and archive masters.
---

# Loudness and Mastering

## Overview

Loudness is a measured quantity with a published target, not a preference. Measure the mix, move gain, then limit, then verify the exported file against the number. Mastering decisions made by ear alone miss the two failures that matter most on delivery: integrated loudness off target, and inter-sample peaks above the ceiling.

## When to Use

- Delivering to a streaming platform, broadcast chain, or video platform with a published target
- Comparing a master against a commercial reference and finding it quieter or duller
- True-peak meters showing overs after a limiter
- Preparing archive master, distribution master, and lossy versions from one session
- A client says "make it louder" and the request needs a target and a ceiling

NOT for balancing a mix (use `mixing-and-gain-staging`) and NOT for measuring a room or a chain (use `audio-measurement-and-analysis`).

## The Workflow

### 1. Get the target in writing

Write the delivery spec down before mastering. Typical published targets:

| Delivery | Integrated | True peak | Note |
|---|---|---|---|
| Streaming (Spotify, YouTube, Tidal, Amazon) | -14 LUFS | -1 dBTP | Platform applies its own playback gain |
| Apple Music | -16 LUFS | -1 dBTP | Sound Check normalises at playback |
| EBU R128 broadcast | -23 LUFS ±0.5 LU | -1 dBTP | Also LRA limits by programme type |
| ATSC A/85 (US broadcast) | -24 LKFS ±2 | -2 dBTP | Dialogue-anchored |
| Cinema / theatrical | no LUFS target | per-print | Dialogue level is the anchor, not loudness normalisation |

Verify the current numbers against the platform's or broadcaster's own published spec before mastering: vendors change them, and a spec sheet from three years ago is not a target. Record the source and date of the number you used.

Platforms apply their own gain at playback. A master hotter than the target is turned down and gains nothing audible, while the limiting damage stays in the file. "Louder wins" is false on every normalising platform.

### 2. Measure before processing

```bash
ffmpeg -i mix.wav -af loudnorm=print_format=json -f null -
```

Read from the JSON: `input_i` (integrated LUFS), `input_tp` (true peak, dBTP), `input_lra` (loudness range, LU). Write all three down. They are the baseline you will compare the export against.

### 3. Move gain before dynamics

1. Compute the gain difference between `input_i` and the target.
2. Apply that as a static gain change, not as limiter drive. A master 4 LU below target needs 4 dB of gain, not 4 dB more limiting.
3. Only then ask how much limiting the material actually wants. If the static gain already hits the target, the remaining limiter work is tone and cohesion, not loudness.

### 4. Limit with a ceiling, not a hope

- Ceiling at -1.0 dBTP for anything that will be encoded to a lossy format. Codecs overshoot, and the ceiling is what survives encoding.
- Oversample the limiter (4× or more) so the ceiling constrains inter-sample peaks, not just sample peaks.
- Keep gain reduction modest. More than a few dB of sustained reduction starts to flatten transients; if the master needs more, the mix is too quiet and the answer is mix gain.
- Set release against tempo. A release shorter than a beat pumps on dense material; too long and the recovery lands after the next hit.

### 5. Fix tone after loudness, not before

Loudness changes perceived balance: louder reads brighter and tighter. Compare against the reference at matched loudness, or you are judging level, not tone. Gain-match with a meter, then decide.

### 6. Handle bit depth, dither, and sample rate once

- Work in 32-bit float. Nothing in the chain clips internally.
- Dither only when reducing bit depth to 16-bit, at the final step, TPDF at one LSB. A 24-bit master does not need dither.
- Resample once, at the end, with the highest-quality resampler available. Two resamples are one too many; a repeated 44.1/48 kHz round trip is audible on cymbals.
- Export the distribution master and the archive master from the same session: archive at the working sample rate and 24-bit, no limiter or with the ceiling documented.

### 7. Verify the exported file, not the export dialog

Run the measurement on the file that leaves the machine:

```bash
ffmpeg -i master.wav -af ebur128=peak=true -f null -
```

The summary block at the end reports integrated loudness, loudness range, and true peak. Compare against the target table.

### 8. Check the lossy version

Encode the distribution master to the delivery codec, decode it back, and measure again. Peaks above the sample-peak ceiling here mean the true-peak ceiling was set too high.

```bash
ffmpeg -i master.wav -c:a aac -b:a 256k /tmp/check.m4a
ffmpeg -i /tmp/check.m4a -af astats=metadata=0 -f null -
```

### 9. Write the delivery record

One line per deliverable: file name, sample rate, bit depth, integrated LUFS, true peak, LRA, and the target it was checked against. This is what a client query gets answered with.

## Verification

- [ ] Target recorded with its source and date
- [ ] Baseline `input_i`, `input_tp`, `input_lra` measured before processing
- [ ] Loudness reached by gain, not by limiter drive
- [ ] Limiter oversampled, ceiling at or below -1.0 dBTP
- [ ] Export measured: integrated within ±0.5 LU of target
- [ ] Export measured: true peak at or below -1.0 dBTP
- [ ] No sample at full scale in either channel
- [ ] Dither applied only on the 16-bit reduction, at the final step
- [ ] Sample rate converted once, at the end
- [ ] Lossy round trip measured and under ceiling
- [ ] Delivery record written for each deliverable

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "Louder is safer; platforms normalise it down anyway" | Normalising down leaves the limiter's distortion and removes the dynamics. Nothing is gained, something is lost. |
| "I can hear that it is close enough to the target" | ±0.5 LU is measurable in one command and inaudible by ear. Meters are free. |
| "The export dialog said -14, so it is -14" | The dialog reports the setting, not the file. Measure the exported file, always. |
| "Dither is not audible, so skip it" | True at 24-bit. At 16-bit it removes quantisation distortion that survives on quiet passages and fades. |
| "I will resample in the editor and again at export" | Each conversion filters the top octave. Convert once, at the end. |
| "The limiter meter shows no clipping" | Sample-peak meters miss inter-sample overs. Read true peak, oversampled. |
| "The reference track is -8 LUFS, so that is the target" | That reference was mastered for a format that normalises it. Your target comes from the delivery spec. |

## Red Flags

- Loudness reached by pushing the limiter instead of moving gain
- True peak measured only with a sample-peak meter
- Dither applied twice, or applied to a 24-bit master
- Two sample-rate conversions in the chain
- Master louder than the target "for safety"
- Comparing tone against a reference at a different loudness
- No delivery record, so the numbers are unreproducible

## Related Skills

- `mixing-and-gain-staging` for the mix's headroom, mono check, and stem set
- `audio-measurement-and-analysis` for meter configuration and measurement interpretation
