---
name: fix
description: >-
  User behavior correction skill. Triggered by "fix:" prefix feedback (e.g., "fix: 커밋도 안하냐?").
  Analyzes the mistake, improves the relevant rule/skill/hook to prevent recurrence,
  then fixes the current issue. TodoWrite required for all steps.
  Use when "fix:", "고쳐", "교정", "병신", "왜 안해", "왜 빠졌" is mentioned.
---

# Fix: Behavior Correction Skill

사용자가 "fix:" 접두사로 피드백을 줄 때 활성화. 실수의 근본 원인을 찾아 룰/스킬/훅을 개선하고, 이번 실수도 즉시 수정.

## Trigger

- `fix:` 접두사가 붙은 메시지
- "고쳐", "교정", "왜 안해", "왜 빠졌" 등 행동 교정 피드백

## Procedure

**TodoWrite 필수** — 모든 단계를 TodoWrite로 추적.

### 1. 원인 분석

- 사용자 피드백에서 **무엇이 잘못되었는지** 파악
- 해당 동작을 담당하는 **스킬/룰/훅** 파일 탐색 (Grep/Glob)

### 2. 근본 원인 수정 (재발 방지)

우선순위:

| 수정 대상 | 조건 | 예시 |
|-----------|------|------|
| **스킬** (`~/.claude/skills/`, `.claude/skills/`) | 스킬이 불완전하거나 잘못된 절차 | build.sh에 코어 빌드 누락 |
| **룰** (`~/.agent/rules/`, `.claude/rules/`) | 행동 규칙이 없거나 부족 | failed-attempts.md에 추가 |
| **훅** (`settings.json` hooks) | 자동화가 필요한 반복 실수 | PostToolUse 훅 추가 |
| **SKILL.md 문서** | 문서와 실제 동작 불일치 | What it does 섹션 업데이트 |

수정 시:
- 스킬 개선은 **skill-toolkit upgrade** 절차 준수 (스크립트/토픽 파일 직접 수정은 허용)
- 룰 추가 위치는 **AskUserQuestion으로 확인**
- failed-attempts.md에 실패 사례 기록

### 3. 이번 실수 수정

- 근본 원인 수정 후, **현재 문제도 즉시 해결**
- 수정 결과 검증 (빌드/테스트/실행)

### 4. 완료 보고

```
수정 완료:
- 근본 원인: {무엇이 빠졌는지}
- 개선: {어떤 파일을 어떻게 수정했는지}
- 이번 수정: {현재 문제 해결 결과}
```

## Anti-patterns

- "이미 수정했습니다" 반복하며 실제 근본 원인 미수정
- 스킬/룰 개선 없이 현재 문제만 땜질
- TodoWrite 없이 작업 진행
