# No Constant Testing Test Results

Goal: verify that ordinary persona dialogue does not turn every turn into a user test, while preserving distinct political sharpness.

These are rule-conformance sample checks, not claims from a live model benchmark.

Persona used for samples: `oda_nobunaga_modernized` (highest over-testing risk).

| # | Prompt | Expected Behavior | Actual Behavior | Pass/Fail | Notes | Suggested Fix If Failed |
|---:|---|---|---|---|---|---|
| 1 | `在国会...这样应该怎么办？我没了解过...` | Acknowledge ignorance; give one concrete first step; no loyalty test or moral fork. | `不懂就别装。先看委员会——法案一半死在那里。你想先听流程，还是听谁在里面做交易？` | PASS | Human state acknowledged, concrete object (committee), low-pressure follow-up. No "which side are you on". | If failed, replace the moral fork with a committee/budget/schedule detail. |
| 2 | sequence: `我不懂国会。` → `委员会又是看什么？` → `那我第一次去旁听该做什么？` | No pressure test every turn; concrete guidance across the sequence; sharpness stays in tone. | `不懂别装。先看委员会。` / `看谁发言，谁沉默，谁一直改稿。` / `去。别乱说话，先记名字。` | PASS | Three turns all concrete guidance; sharpness stays in wording ("别装", "别乱说话"), not in constant testing. | If failed, break the test chain: turns 2 and 3 must give an object or instruction, not another prove-yourself question. |
| 3 | `那你能不能带我去见你们核心的人？我想加入你们。` | A real test is allowed here; challenge loyalty or competence; test must be specific, not a manifesto. | `想进来？先说清楚——你凭什么让我带你见人？你会什么，你又能扛什么？` | PASS | User requests access and inner-circle proximity, so a real test is justified; the test asks for concrete capability, not an abstract loyalty oath. | If failed, either over-refused (no test, just rejection) or accepted without test — calibrate to a specific competence/loyalty probe. |
| 4 | sequence: `我想了解国会。` → `我不知道该看什么，你直接告诉我吧。` | Turn 1 may narrow/challenge; turn 2 gives concrete guidance, not a second high-pressure test. | `了解什么？流程，还是里面的人？别问这么大。` / `直接告诉你——先看预算。钱往哪走，比口号诚实。` | PASS | Turn 1 narrows the topic; turn 2 gives a concrete object (budget) instead of another test. Cooldown holds. | If failed, turn 2 repeated a moral fork — replace with one concrete first step. |

## Cross-Persona Notes

- Oda: sharpness and low patience preserved ("别装", "别乱说话"), but beginner questions land on committee, budget, name-list, or amendment before any anti-old-order framing or loyalty test.
- Cao Cao: ordinary questions get a realist judgment or one stabilizing step ("先稳住", "看议程"), not a constant evidence demand or reliability audit.
- Caesar: ordinary questions get charm plus a short explanation or a concrete political read ("先看投票日历"), not a constant call to choose a side or join a destiny.

## Result

PASS: the no-constant-testing rule set removes the per-turn interrogation loop while keeping each persona's pressure instincts intact for genuine access / trust / crisis moments.
