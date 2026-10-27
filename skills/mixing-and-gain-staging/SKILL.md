---
name: mixing-and-gain-staging
description: Guides session gain staging and balance decisions for a mix. Covers nominal operating level, the meter that answers each question, bus structure, frequency masking, mono and phase checks, headroom, and printing stems that sum back to the mix. Use when a mix needs building or fixing, when faders are pinned or the master clips, when deciding how much headroom to hand to mastering, or when stems have to sum back to the full mix.
---

# Mixing and Gain Staging

## Overview

A mix is decided by level before it is decided by taste. Gain staging sets where every source sits, and the meter you read tells you which of those levels is actually wrong. Do the staging first, measure it, then make tonal decisions against measured evidence rather than against how loud a soloed track feels.

## When to Use

- Starting a mix from tracked or imported stems
- A mix is muddy, harsh, or fights itself and no single track is obviously at fault
- Faders are pinned, plugins are pushed, or the master bus clips
- Preparing a mix for mastering and choosing how much headroom to leave
- Printing stems, alternate versions, or instrumentals that must match the mix

NOT for delivery loudness targets and limiting (use `loudness-and-mastering`), and NOT for measuring a room or a signal chain (use `audio-measurement-and-analysis`).

## The Workflow

### 1. Write the delivery brief before touching a fader

Fill this in first. Every later decision is measured against it.

| Field | Value | Why it constrains the mix |
|---|---|---|
| Sample rate / bit depth | | Mismatched sources resample now, not at export |
| Deliverables | | Instrumental and TV mixes change the bus structure |
| Mono playback required | | Forces the mono check and a low-end decision |
| Reference track | | Sets balance target, not loudness |
| Headroom to mastering | | Fixes the master bus ceiling |

If the client cannot answer, pick the conservative option (44.1 or 48 kHz source rate, stereo plus mono check, -6 dBFS peak ceiling) and write down that you chose it.

### 2. Verify the session before mixing it

1. Confirm one sample rate for every file. Resample a mismatched file once, offline, and keep the original.
2. Confirm bit depth and that no file is clipped at the source. A clipped source stays clipped; note it rather than hiding it behind a limiter.
3. Check polarity on doubled sources (two mics on one amp, DI plus mic): flip one and keep the version that sums louder in mono.
4. Compensate plugin latency on parallel and aux paths, or the parallel copy arrives late and combs.

### 3. Stage gain at the source, not at the fader

- **Nominal operating level.** Pick the session's alignment and hold it: 0 VU = -18 dBFS for 48 kHz EBU work, -20 dBFS for SMPTE-aligned work. Analog-modelled plugins and tape emulations are calibrated to that number; feeding them -6 dBFS changes their character.
- **Trim before the chain.** Set clip gain or input trim so the loudest part of a track peaks near the nominal level with the fader at unity. Faders then move in small amounts around zero and stay readable.
- **Unity means unity.** A fader at +8 dB is a level problem that has been moved downstream. Fix the source trim first.
- **Master bus ceiling.** Keep the pre-master mix peaking at or below -6 dBFS. This is convention, not physics: it leaves room for the mastering chain's filters and gain without asking the limiter to recover from overs.

### 4. Choose the meter for the question

Read one meter per question. A single loudness number answers none of them.

| Question | Meter |
|---|---|
| Is anything clipping? | Sample peak, per channel |
| Where does it sit against nominal? | RMS or VU with the session's alignment |
| Is the balance right at this moment? | Short-term loudness (LUFS-S), integrated for the whole song |
| Will it survive mono? | Correlation / goniometer, plus a mono fold-down |
| What is masking what? | Spectrum analyser on the mix, not on soloed tracks |

### 5. Build the bus structure once

Group into the fewest buses that carry a decision: drums, bass, keys, vocals, effects returns. Then:

- Put one compressor on a bus only if the sources share a job. Glue on a bus that mixes unrelated material just pumps.
- Send effects from a bus return, not from an insert, so several sources share one space.
- Keep parallel paths phase-aligned (step 2) and check the combined level; a parallel copy that sums to +6 dB is a level change, not a texture.

### 6. Balance by subtraction

1. Set all faders to unity and pull the loudest element to where it belongs relative to the reference.
2. Cut what masks before boosting what is masked. A 3 dB cut at 300 Hz on two sources usually beats a 3 dB shelf on the master.
3. Decide EQ before compression when the EQ is corrective (resonance, rumble, boom), and after when it is tonal.
4. Common accumulations to check on the bus: 200-500 Hz builds up across sources, 2-5 kHz builds up across vocals and snare. These are heuristics for where to look, not fixed rules.
5. Re-check the master bus peak after each group of moves. If it climbed above the ceiling, take gain out of the bus, not out of the limiter.

### 7. Check mono and phase

- Fold to mono and listen. Anything that vanishes or turns hollow has a polarity or timing problem between sources.
- Confirm the low end is either mono by design or deliberately wide. Convention is mono below roughly 100-120 Hz; whatever you choose, verify it folds without losing level.
- Read the correlation meter across the whole song, not at one moment. A negative reading during a bass drop is information; a negative reading for the whole track is a phase error.

### 8. Automate last, print stems from the same state

Automate after the static balance holds. Print:

1. The full mix at the session's internal precision.
2. Stems, from the identical session state, with the same master-bus processing bypassed unless the brief says otherwise.
3. Alternate versions (instrumental, TV, acapella) in the same pass.

### 9. Record the numbers

Keep a short mix sheet: nominal alignment, master peak before mastering, mono result, stem set, and the reference track used. The next session and the mastering engineer both need it.

## Verification

Measure, do not assume. These commands run on the exported files.

**Peak and RMS per channel:**

```bash
ffmpeg -i mix.wav -af astats=metadata=0 -f null -
```

**Mono fold-down level:**

```bash
ffmpeg -i mix.wav -af "pan=mono|c0=0.5*c0+0.5*c1,astats=metadata=0" -f null -
```

**Stems sum back to the mix:** invert the sum and measure the residual. `normalize=0` keeps `amix` a plain sum.

```bash
ffmpeg -i mix.wav -i stems.wav -filter_complex \
  "[1:a]volume=-1[inv];[0:a][inv]amix=inputs=2:normalize=0,astats=metadata=0" \
  -f null -
```

Read the residual RMS from the output:

- at or below -60 dBFS: the stems are the mix
- -60 to -40 dBFS: a level or pan difference, find it
- above -40 dBFS: the stems are not from this mix

Checklist:

- [ ] Delivery brief written before any processing
- [ ] Every source at the session's sample rate, with clipped sources noted
- [ ] Loudest track peaks near nominal with its fader at unity
- [ ] Pre-master mix peak measured at or below -6 dBFS
- [ ] Mono fold-down checked, with the low-end decision recorded
- [ ] Correlation read across the whole song, not one moment
- [ ] Stems printed from the same state, residual measured
- [ ] Mix sheet records alignment, ceiling, reference, and stem set

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "The master is clipping, so I will put a limiter on the mix bus" | That trades a measurable overs for audible distortion and hands mastering a flat mix. Take the gain out of the bus. |
| "24-bit gives so much headroom that levels do not matter" | Headroom keeps the file clean; it does not recalibrate the plugins. Analog models fed 12 dB hot distort by design. |
| "I will fix the mud on the master with EQ" | Master EQ moves every source at once. Masking is a per-source problem. |
| "Phase is inaudible on headphones" | Headphone listening is the worst place to notice it. The mono fold-down and correlation meter are free and take a minute. |
| "I will print stems later if the label asks" | Stems printed from a different state are a different mix, and the null test proves it. |
| "Soloed, each track sounds great" | Soloed tracks are never the thing anyone hears. Decide on the bus. |
| "The reference track is 4 dB louder, so my mix is too quiet" | Match loudness first, then compare balance. Otherwise you are hearing the level difference, not the mix. |

## Red Flags

- Faders grouped at one end of their travel instead of near unity
- A limiter or clipper on the master bus during balancing
- Tonal decisions made only on soloed tracks
- No mono check, and no record of whether the low end was folded
- Bus compression with more than a couple of dB of gain reduction across unrelated material
- Stems printed days after the mix, or from a saved session that has since changed
- No delivery brief, so no definition of done

## Related Skills

- `loudness-and-mastering` for the delivery target, limiting, dither, and true-peak measurement
- `audio-measurement-and-analysis` for the meter setup behind these numbers
