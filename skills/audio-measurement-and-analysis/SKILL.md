---
name: audio-measurement-and-analysis
description: Guides choosing, configuring, and interpreting audio measurements. Covers level and loudness meters, spectrum and FFT settings, transfer functions, impulse responses for RT60 and room modes, distortion, and null tests that prove whether a chain changed the signal. Use when a sound question needs a number, when a room or monitor setup has to be assessed, when a plugin or chain must be shown transparent, or when two measurements disagree.
---

# Audio Measurement and Analysis

## Overview

A measurement is an answer to one written question, taken with settings that do not change the answer. Choose the measurement from the question, state the settings, then compare the number against a threshold. Without the question and the settings, a spectrum display is decoration.

## When to Use

- A sound question needs a number: how loud, how bright, how long does the room ring, how much does this chain distort
- Assessing a room, monitor placement, or a treatment change
- Proving whether a plugin, converter, or processing chain is transparent
- Diagnosing a symptom someone described in adjectives ("boomy", "harsh", "phasey")
- Two measurements disagree and one of them is configured wrong

NOT for delivery loudness targets (use `loudness-and-mastering`) and NOT for balance decisions in a mix (use `mixing-and-gain-staging`).

## The Workflow

### 1. Write the question and the threshold first

One sentence, with the decision it informs:

- "Is the decay at 60 Hz longer than 0.6 s, which would mean the corner needs treatment?"
- "Does this chain null below -60 dBFS, which would mean it is transparent?"
- "Is the third harmonic below -50 dB relative to the fundamental at operating level?"

A question without a threshold cannot fail, and a measurement that cannot fail is not evidence.

### 2. Choose the measurement from the question

| Question | Measurement | Needs |
|---|---|---|
| How loud is it? | RMS, LUFS, sample peak, true peak | One channel at a time, calibrated gain |
| Where is the energy? | Spectrum / RTA | Known FFT size, window, averaging |
| Does the room ring, and where? | Impulse response: RT60, ETC, waterfall | Sweep or balloon pop, measurement mic with calibration file |
| Did this chain change the signal? | Null test | Sample-aligned paths, one inverted |
| How much distortion? | THD+N, harmonic series | Sine at a known level, bandwidth stated |
| How much delay? | Loopback timing | Same converter in and out, or a known reference |

### 3. Configure the rig so it does not change the answer

- Keep levels below clipping and well above the noise floor; record the operating level.
- Put nothing in the measurement path that is not under test. Bypass EQ, dynamics, and any "enhancement".
- Use the microphone's calibration file, and calibrate SPL with a 94 dB / 1 kHz calibrator (94 dB SPL = 1 Pa). Level in dBFS is not level in dB SPL until that is done.
- Hold one sample rate through the whole chain. A rate mismatch silently resamples and moves every frequency slightly.
- For room work, place the mic where a listener's head goes, and keep the source and mic positions documented so the measurement can be repeated.

### 4. Set the FFT honestly

- **Bin width** = sample rate / FFT size. 48 kHz over 4096 points is about 11.7 Hz per bin. Say the resolution out loud; a 0.1 Hz claim from a 1 s capture is not resolving anything.
- **Window** by signal type: rectangular for impulses and synchronous signals, Hann for music and noise, Blackman-Harris where a wide dynamic range inside one frame matters, flat-top when amplitude accuracy matters more than leakage.
- **Averaging**: at least eight averages for noise-like material, exponential averaging for a live RTA. State the count.
- **Overlap** of 50-75% when averaging, or the tail of each frame is thrown away.
- A longer window buys frequency resolution and loses time resolution. Both directions are real costs.

### 5. Null test: prove a chain is transparent

1. Route the same source through the chain and through a bypass path.
2. Align the two paths to the sample. One sample of offset leaves a comb, not a null.
3. Invert one path, sum, and measure the residual.

Read the residual as a decision:

| Residual RMS | Meaning |
|---|---|
| At or below -60 dBFS | Transparent for practical purposes; the difference will not be heard on programme material |
| -60 to -40 dBFS | Measurable change, usually level or phase, occasionally audible on exposed material |
| Above -40 dBFS | Audible difference; the chain is not transparent |

### 6. Impulse response: room and chain

- Decay time from the Schroeder backward integral, fitted between -5 and -35 dB (T30) or -5 and -25 dB (T20). RT60 is that slope extrapolated to 60 dB.
- EDT is the same slope fitted from 0 to -10 dB, and it tracks perceived reverberance better than RT60 in small rooms.
- Axial mode frequencies: `f = c / (2L)`, with c ≈ 343 m/s at 20 °C. Compute the first few for each room dimension and compare against the measured peaks.
- Below the Schroeder frequency, roughly `2000 * sqrt(RT60 / volume)`, the room behaves as separate modes and a spectrum display looks like a comb; above it, treat it statistically. Volume in m³.
- A waterfall shows which frequencies decay late. A single RT60 number hides the one ringing mode that is the actual complaint.

### 7. Distortion: identify the harmonics, not just the number

- THD+N includes noise. If you need distortion alone, measure the harmonic series individually.
- Even harmonics usually mean asymmetry (single-ended stages, uneven bias); odd harmonics usually mean symmetric nonlinearity or clipping. Which harmonics dominate tells you where to look.
- Sweep the level. Distortion that jumps at a particular level is a threshold problem, not a constant.
- State the bandwidth of the measurement; THD measured to 20 kHz is a different number from THD measured to 96 kHz.

### 8. Record it, then repeat it

A measurement log entry:

| Field | Example |
|---|---|
| Question | Is RT60 at 60 Hz above 0.6 s? |
| Signal and level | Sweep, 20 Hz-20 kHz, 75 dB SPL at 1 m |
| Rig | Measurement mic + calibration file, interface at 48 kHz, no processing |
| Settings | FFT 65536, Hann, 4 averages, 75% overlap |
| Result | RT60(60 Hz) = 0.78 s |
| Decision | Corner treatment before the next measurement |

Then run it again. A measurement that does not reproduce within its tolerance is not a result, whatever it says.

## Verification

- [ ] Question and threshold written before measuring
- [ ] Measurement chosen from the question, with its known limits stated
- [ ] Rig configured once: no processing in the path, calibration applied, one sample rate
- [ ] FFT size, window, averaging, and overlap recorded with the result
- [ ] Bin width stated when a frequency resolution is claimed
- [ ] Null test paths sample-aligned before inverting
- [ ] Room results compared against computed axial modes, not only against a picture
- [ ] Threshold cited with the number, in the same sentence as the conclusion
- [ ] Repeat run within tolerance

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The meter looks right" | Meters have time constants, weightings, and hold behaviour. Name the meter and its settings before trusting the reading. |
| "I trust my ears for this" | Ears are good at balance and bad at absolute level, 1 dB at 60 Hz, and anything about distortion below a couple of percent. |
| "More resolution is always better" | A 0.1 Hz bin takes a 10 s window and smears every transient across it. Resolution trades against time. |
| "Room correction software will handle it" | It needs a measurement to work from and a measurement to verify it worked. Both are your job. |
| "The plugin says it is linear phase, so it is transparent" | Linear phase constrains phase, not magnitude or latency. The null test answers transparency. |
| "One average is enough, the signal is steady" | Noise-like material needs averaging to separate signal from variance. Eight frames, minimum, stated. |
| "The screenshot is the evidence" | A screenshot reproduces neither the settings nor the run. Log the numbers. |

## Red Flags

- A spectrum shown without FFT size, window, or averaging
- Frequency claims finer than the bin width allows
- No calibration, so dBFS readings presented as dB SPL
- Null tests claimed without sample alignment
- Distortion quoted without bandwidth or level
- RT60 quoted without saying which fit range produced it
- A single measurement treated as a repeatable result

## Related Skills

- `loudness-and-mastering` for the loudness and true-peak targets this skill measures against
- `mixing-and-gain-staging` for the meter choices behind a mix's level decisions
