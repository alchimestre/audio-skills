# audio-skills

Three `SKILL.md` workflows for agents that work on sound: measure a chain or a room, balance a mix, deliver a master to a loudness target. Each one asks for the number before it touches a fader.

## Skills

| Skill | What it covers | Use when |
|---|---|---|
| mixing-and-gain-staging | Nominal operating level, meter choice per question, bus structure, masking by subtraction, mono and phase checks, headroom, stems that null against the mix | Building or fixing a mix, or handing headroom to mastering |
| loudness-and-mastering | Published loudness targets, measure-then-gain, oversampled limiting and true peak, dither and sample-rate discipline, delivery record | A master has to hit a platform or broadcast spec |
| audio-measurement-and-analysis | Question-first measurement, FFT and window settings, null tests with a threshold, RT60 and axial modes, distortion harmonics | A sound question needs a number, or a room or chain needs assessing |

## Install

1. Point the harness at the skill directory:

```yaml
skills:
  customDirectories:
    - /path/to/audio-skills/skills
```

2. Restart the harness.

With the skills CLI:

```sh
npx skills add alchimestre/audio-skills
```

## Evals

`evals/cases/` holds one case per skill: positive prompts that must rank the skill in the top 3, negative prompts owned by another skill, and an execution case graded against `expectations[]`. The schema is the one used by [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills).

`evals/fixtures/` holds the audio each execution case runs on. It is synthetic and deterministic; regenerate it with:

```sh
python3 scripts/make-audio-fixtures.py
```

The runner is vendored from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (MIT, commit `aeac41d`). `scripts/run-evals.js` is unchanged apart from one import path, so upstream diffs stay readable; the frontmatter parser it needs lives in `scripts/lib/frontmatter.js`.

## Tests

```sh
npm test                                              # tier 2: trigger, routing, schema
node scripts/run-evals.js --min-rank1 95               # fail under a routing floor
node scripts/run-evals.js --behavioral mixing-and-gain-staging --dry-run
python3 scripts/make-audio-fixtures.py                # regenerate the WAVs
```

Tier 2 is deterministic and spends no tokens: every positive prompt must rank its skill in the top 3, no negative prompt may rank it first, two descriptions may not collide, and every case file must be schema-complete. Tier 3 runs an execution case through headless `claude`, materializes its fixtures in a throwaway workspace, and grades the trace against `expectations[]`; it costs tokens and needs `claude` on `PATH`.

## Limits

- Fixtures are 48 kHz WAVs, 44 KB to 576 KB. No commercial material is included.
- The skills assume a measured workflow. Without a target and a pass threshold, the workflow has nothing to verify against.
- Negative prompts owned by a skill outside this repo carry no `owner` field, so they assert "not ranked first" rather than a pairwise routing check.
- Skill anatomy follows addyosmani/agent-skills, MIT licensed.
