# blog-post skill upgrades — inspired by Ametov lecture

**Date**: 2026-04-08
**Scope**: `~/.claude/skills/blog-post/` + new `~/.claude/skills/update-editorial/`
**Source material**: `ai-native-ops/derived/sessions/s2-w2-ametov/session-intel.md` (Алексей Амётов, "AI-контент для бизнеса", 2026-04-01)

## Context

Current `blog-post` skill runs a 7-phase pipeline (questions → research → related posts → brief → draft → deaify → titles → deploy) with GitHub issue persistence. It ships drafts through `deaify-text` as the only quality gate. There is no scoring against author voice / factual accuracy / AEO compliance before publish, and no feedback loop from post-publish edits.

Ametov's lecture introduced several patterns that map cleanly onto these gaps:

- Pipeline vs agent architecture, LLM-as-judge with explicit rubric
- `EDITORIAL.md` as canonical tone-of-voice file (Denis Smirnov's tip)
- Max 2 retries then HITL escalation
- Self-improving agents that update their own memory from QA corrections
- Inject current date to prevent "time traveler" hallucinations
- KISS / Karpathy — do not over-engineer

Five concrete improvements follow. All five are in scope.

## Decisions summary

| # | Question | Decision |
|---|----------|----------|
| Q1 | File structure for editorial canon | **B** — `EDITORIAL.md` (style, renamed from writing-guide.md) + `author-bible.md` (facts). Two files, clear split. |
| Q2 | Judge rubric shape | **C** — hybrid: 4 binary must-have criteria + 3 scale-1-3 nice-to-have criteria |
| Q3 | Retry mechanics on judge FAIL | **C** — Retry 1 = surgical patch (Sonnet), Retry 2 = full rewrite (Opus), then HITL via AskUserQuestion |
| Q4 | Self-improving loop trigger | **A** — after every post (new Phase 7), with shoist-gate for trivial edits |
| Q5 | Periodic corpus regeneration of EDITORIAL.md | **A** — drop it. Only per-post incremental updates. YAGNI. |

## Design

### 1. File structure — `~/.claude/skills/blog-post/`

**Rename:** `writing-guide.md` → `EDITORIAL.md`. Add new top section `## Judge rubric` (≤30 lines) before existing content. The rubric section is what the judge subagent reads as its primary contract; everything below is existing writing-guide content used by the draft subagent.

```
EDITORIAL.md
├── ## Judge rubric (must-have, binary)
│   1. Voice: вайбкодер, не разработчик
│   2. Facts: confirmed by research/brief/author-bible
│   3. AEO: first paragraph = direct answer
│   4. No AI clichés: zero hits from ai-terms-ru.md stop-list
├── ## Judge rubric (nice-to-have, 1-3 scale)
│   5. Concreteness (tools, numbers, names)
│   6. Structure (intro → problem → solution → takeaway)
│   7. NPS trick: would you recommend this draft to another agent?
├── ## Voice                    ← existing writing-guide content
├── ## Before/After             ← existing
└── ...                         ← existing
```

`author-bible.md` unchanged. `ai-terms-ru.md` unchanged.

All references to `writing-guide.md` in `SKILL.md` replaced with `EDITORIAL.md`.

### 2. Phase 4.5 — Judge

New phase between `deaify` (Phase 4) and `titles` (Phase 5). Sonnet subagent.

Inputs to judge prompt:
- First 30 lines of `EDITORIAL.md` (the rubric section)
- Full `author-bible.md`
- Full `ai-terms-ru.md`
- Brief from Phase 2.7 (fact source)
- Draft after deaify
- **Pre-computed clichés check**: grep draft against ai-terms-ru.md in Python/bash before invoking judge, inject results as `pre_computed_cliches: [...]`. Makes the `no_cliches` criterion deterministic instead of LLM-subjective.

Output: strict JSON.

```json
{
  "must_have": {
    "voice":      { "pass": bool, "evidence": "..." | null },
    "facts":      { "pass": bool, "evidence": "..." | null },
    "aeo":        { "pass": bool, "evidence": "..." | null },
    "no_cliches": { "pass": bool, "evidence": "..." | null }
  },
  "nice_to_have": {
    "concreteness": { "score": 1|2|3, "comment": "..." },
    "structure":    { "score": 1|2|3, "comment": "..." },
    "nps":          { "score": 1|2|3, "comment": "..." }
  },
  "verdict": "PASS" | "FAIL",
  "fail_reasons": ["voice", "aeo", ...]
}
```

Verdict rule: `PASS` iff all four must-have are `pass: true`. Nice-to-have is diagnostic only — logged for Phase 7, never blocks.

Result saved as a comment on the blog issue (Phase 4.5 slot). Retries append additional comments.

### 3. Retry state machine

```
judge: PASS → Phase 5
judge: FAIL (retry_count=0) → Retry 1: patch-subagent (Sonnet)
  └── re-judge
      ├── PASS → Phase 5
      └── FAIL (retry_count=1) → Retry 2: rewrite-subagent (Opus)
          └── re-judge
              ├── PASS → Phase 5
              └── FAIL (retry_count=2) → HITL via AskUserQuestion
```

**Retry 1 — surgical patch (Sonnet):** prompt includes fail_reasons + evidence cites + EDITORIAL.md + current draft. Instruction: fix only failing sections, do not rewrite passing passages, do not add new material. Returns full markdown (for next judge pass).

**Retry 2 — full rewrite (Opus):** reuses Phase 3 draft prompt (with author-bible, brief, related posts, EDITORIAL.md) plus extra context: previous draft, judge verdict on previous draft, patch attempt. Explicit instruction: rewrite from scratch taking prior failures into account.

**HITL after 2 fails** — `AskUserQuestion`:
1. Публиковать как есть (fails logged)
2. Показать детали и остановиться (manual edit, resume at Phase 5)
3. Ещё один rewrite (resets retry_count to 0)
4. Отмена публикации (issue stays open)

Guard: retry_count hardcoded max 2 within one automatic run; only user-choice #3 can reset it.

Each retry is a separate issue comment. Judge JSON preserved at every step.

### 4. Phase 7 — self-improving loop + `update-editorial` subskill

New Phase 7 runs after Phase 6 (deploy) and before closing the issue.

**Phase 7 orchestrator logic (inside `blog-post` SKILL.md):**
1. Read final post-deaify draft from Phase 4 issue comment
2. Read published version from `content/blog/{slug}.md`
3. Compute `git diff --word-diff` between them
4. **Shoist-gate:** skip silently (close issue, done) if any of:
   - total diff < 200 chars
   - only punctuation / whitespace changes
   - only frontmatter changes
5. Otherwise → invoke subskill `update-editorial` with `{slug, diff, judge_scores}` via Skill tool

**New subskill `~/.claude/skills/update-editorial/SKILL.md`:**

```yaml
---
name: update-editorial
description: Use after publishing a blog post to capture author's manual edits and propose updates to EDITORIAL.md. Triggered from blog-post Phase 7.
---
```

Internal workflow:

1. **Append feedback log** (always, even if subsequent steps skip):
   `~/.claude/skills/blog-post/feedback-log.jsonl`
   ```json
   {
     "date": "2026-04-08",
     "slug": "...",
     "issue": 123,
     "judge_scores": { ... },
     "retries": 0,
     "hitl_used": false,
     "hitl_choice": null,
     "diff_size_chars": 542,
     "suggestions_count": null,
     "suggestions_applied": null
   }
   ```

2. **Analyze diff** via Sonnet subagent. Prompt includes: diff, judge nice-to-have scores, current EDITORIAL.md. Task: categorize each change, decide if it represents a pattern that should update EDITORIAL.md (not a one-off taste call), propose rule wording for each pattern. Output JSON with `changes[]` and `suggestions_count`.

3. **If `suggestions_count == 0`** → update feedback-log entry, skip, close issue.

4. **If suggestions exist** → `AskUserQuestion`:
   - Show and apply all
   - Show, pick one by one
   - Skip, keep EDITORIAL as-is

5. Apply chosen suggestions via Edit tool on `EDITORIAL.md`. Commit in sereja.tech? **No** — EDITORIAL.md lives in `~/.claude/skills/blog-post/` which is not a git repo. Apply is write-only; user must manually back up `~/.claude` if they want version history. (Acceptable: dotfiles not versioned is existing state; not this design's problem to fix.)

6. Update feedback-log entry with `suggestions_count` and `suggestions_applied`. Close blog issue.

**Fatigue guard:** if the last 5 entries in feedback-log have `suggestions_applied == 0` (user kept skipping), the 6th run logs + skips `AskUserQuestion` entirely. Resets on next accepted suggestion. Prevents "отстань" loop.

### 5. Date injection

Every Task subagent call gets a `## Временной контекст` block injected:

```
## Временной контекст (КРИТИЧНО)
Сегодня: {$(date +%Y-%m-%d)}
Текущий год: 2026.
При упоминании моделей, инструментов, версий — это твой horizon.
НЕ выдумывай "новинки 2025" или "GPT-5 который скоро выйдет".
Если не знаешь актуальное состояние — пометь [нужна проверка].
```

Injection points: Phase 2 (research), Phase 2.7 (brief), Phase 3 (draft), Phase 4.5 (judge + patch + rewrite retries), Phase 5 (titles), Phase 7 (diff analyze). Rule stated explicitly in SKILL.md orchestration notes so future edits to prompts don't drop it.

### Non-goals

- Do not modify `deaify-text` skill. Judge runs after it.
- Do not add dashboards / metrics UI. feedback-log.jsonl is raw enough for manual inspection.
- Do not background-run update-editorial. Always interactive (`AskUserQuestion`), except fatigue-guard and shoist-gate.
- Do not version `~/.claude/skills/` (out of scope).
- Do not regenerate EDITORIAL.md from corpus. Only per-post incremental updates.

## Implementation sequence — 6 commits

Each stage is atomic and leaves the skill in working order.

| # | Stage | Commit | Test |
|---|-------|--------|------|
| 1 | Rename + add rubric section | `refactor(blog-post): rename writing-guide to EDITORIAL, add judge rubric section` | `grep -r writing-guide ~/.claude/skills/blog-post/` → empty |
| 2 | Judge phase (no retry, HITL on fail) | `feat(blog-post): add Phase 4.5 judge with hybrid rubric` | Run on one live post, inspect JSON in issue |
| 3 | Retry mechanics (patch → rewrite → HITL) | `feat(blog-post): add patch→rewrite→HITL retry mechanics for judge` | Inject "революция" into a test draft, verify Retry 1 fixes it |
| 4a | `update-editorial` subskill | `feat(update-editorial): new subskill for post-publish EDITORIAL updates` | Standalone invocation on a synthetic diff |
| 4b | Phase 7 in blog-post | `feat(blog-post): add Phase 7 self-improving loop via update-editorial` | Publish a post, make manual edit, verify Phase 7 prompts |
| 5 | Date injection across all prompts | `chore(blog-post): inject current date into all subagent prompts` | `grep "Временной контекст" ~/.claude/skills/blog-post/SKILL.md` → 7+ hits |

**Rollback:** each commit is independently revertable except Stage 1 (foundational but safe). No long-lived branch.

**Commit target:** `~/.claude/skills/` is not a git repo, so strictly these are file-level changes without VCS. For the design doc itself (this file), commit to `sereja.tech` repo where blog publishing lives.

## Open items deferred to implementation

- Exact wording of EDITORIAL.md rubric section (will draft during Stage 1)
- Exact patch-subagent prompt (will draft during Stage 3)
- Fatigue-guard threshold = 5 skips (may tune after seeing real usage)
- Shoist-gate threshold = 200 chars (may tune after seeing real usage)

## Source references

- Ametov session intel: `~/Documents/GitHub/ai-native-ops/derived/sessions/s2-w2-ametov/session-intel.md`
- Current blog-post skill: `~/.claude/skills/blog-post/SKILL.md`
- Current writing-guide: `~/.claude/skills/blog-post/writing-guide.md`
- Current author-bible: `~/.claude/skills/blog-post/author-bible.md`
- deaify-text skill (unchanged): `~/.claude/skills/deaify-text/`
