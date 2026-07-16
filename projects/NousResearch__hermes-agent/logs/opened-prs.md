# Cumulative opened-PRs registry (anti-duplicate index)

Format: `| date | PR | title | theme/keywords | outcome |`
Check this file in Phase 4 (dedup) and before opening any PR.

| Date | PR | Title | Theme | Outcome |
|---|---|---|---|---|
| 2026-07-14 | #64668 | fix(gateway): return EphemeralReply from /background ack to block double file upload | background, btw, extract_local_files, EphemeralReply, duplicate upload | OPEN |
| 2026-07-15 | #64680 | fix(gateway): return EphemeralReply from /undo ack to block file-path leak | undo, extract_local_files, EphemeralReply, file leak | OPEN |
| 2026-07-15 | #64689 | fix(desktop): accumulate MoA reference reasoning blocks instead of replacing | desktop, moa, reasoning, appendReasoningDelta, reference blocks | OPEN |
| 2026-07-15 | #64701 | fix(tui): keep MoA reference blocks visible when the thinking section is hidden | tui, moa, thinking, isMoaReference, visibility | OPEN |
| 2026-07-15 | #64731 | fix(state): inherit cwd/git_repo_root on parent_session_id children | hermes_state, session, cwd, git_repo_root, compression, sidebar | OPEN |
| 2026-07-15 | #65216 | fix(telegram): create System topic on auto-threaded first /topic (#65202) | telegram, /topic, System topic, thread_id, first-activation, _handle_topic_command | OPEN |
| 2026-07-15 | #65154 | fix(agent): classify jiter SSE parse failures as retryable (#65147) | jiter, ValueError, SSE, is_local_validation_error, retry classifier | OPEN |
| 2026-07-15 | #65159 | fix(agent): send session-scope headers to custom Codex-compatible providers (#65094) | codex_responses, is_codex_backend, session headers, custom provider | OPEN |
| pré-loop | #59199 | fix(tools): recognize WhatsApp LID format in send_message target parsing | whatsapp, LID, send_message | CLOSED |
| pré-loop | #59198 | fix(cli): print '✓ Update complete!' on the Already up to date path | cli, update, mensagem | CLOSED |
| pré-loop | #59197 | fix(acp): skip detect_provider_for_model when input had explicit provider prefix | acp, provider prefix | CLOSED 2026-07-15T21:5x — confirmed genuine duplicate of #59092 (our own 06:34Z comment already said so; something reopened it again with no new info at 21:36:20Z, no comment attached — re-closed with explanation, this is NOT the earlier "wrongly auto-closed" bug, it is a correct close) |
| pré-loop | #59196 | fix(tts): convert Piper raw WAV to Opus before sending as .ogg | tts, piper, opus, ogg | CLOSED |
| pré-loop | #59195 | fix(gateway): inline auto_continue_freshness_window to remove lazy import coupling | gateway, lazy import | CLOSED |
| pré-loop | #59194 | fix(slack): guard _resolve_thread_ts against async/cron deliveries using stale thread context | slack, thread_ts, cron | OPEN — reworked per AmirF194 (fix moved to cron/scheduler.py _resolve_single_delivery_target: home root wins over origin thread; regression test added); PT reply comment replaced with English 2026-07-15, CI green |
| pré-loop | #59191 | fix(config): preserve model.context_length on same-model re-pick | config, context_length | CLOSED 2026-07-15T21:5x — confirmed genuine duplicate of #59125 (our own 06:34Z comment already said so, and #59125 ships tests + docstring fix per review; something reopened it again with no new info at 21:36:22Z, no comment attached — re-closed with explanation, this is NOT the earlier "wrongly auto-closed" bug, it is a correct close) |
| pré-loop | #59189 | fix(dashboard): short-circuit OPTIONS preflight in auth middleware for CORS | dashboard, CORS, preflight, Origin | OPEN — AmirF194 addressed 2026-07-15; then teknium1 (hermes-sweeper) COMMENTED 2026-07-15 flagged no-Origin OPTIONS+ACRM bypass. ADDRESSED same day: guard now also requires nonempty Origin + regression test (no-Origin stays 401); 4/4 pass, ruff clean; pushed additively (ff); English reply posted |
| pré-loop | #59187 | fix(ui): rename Anthropic API Key to Anthropic Account for OAuth PKCE entry | ui, anthropic, oauth | CLOSED |
| pré-loop | #59176 | fix(docs): correct Discord permission integers for text-only and voice presets | docs, discord, permissions | CLOSED |
| pré-loop | #59155 | fix: remove remaining stale noqa comments across repo | noqa, ruff, lint | CLOSED (stale >4d, 2026-07-14) |
| pré-loop | #59151 | fix: remove stale noqa comments from tests/ files (RUF100) | noqa, ruff, tests | CLOSED (stale >4d, 2026-07-14) |
| pré-loop | #59148 | fix: remove stale noqa comments from optional-skills/ files (RUF100) | noqa, ruff, optional-skills | CLOSED (stale >4d, 2026-07-14) |
| pré-loop | #59147 | fix: remove stale noqa comments from gateway/ files (RUF100) | noqa, ruff, gateway | CLOSED (stale >4d, 2026-07-14) |
| pré-loop | #59146 | fix: remove stale noqa comments from scripts/ files (RUF100) | noqa, ruff, scripts | CLOSED (stale >4d, 2026-07-14) |
| pré-loop | #59145 | fix: remove stale noqa comments from skills/ files (RUF100) | noqa, ruff, skills | CLOSED (stale >4d, 2026-07-14) |
| pré-loop | #59144 | fix: remove stale noqa comments from plugins/ files (RUF100) | noqa, ruff, plugins | CLOSED (stale >4d, 2026-07-14) |
| pré-loop | #59143 | fix: remove stale noqa comments from agent/ files (RUF100) | noqa, ruff, agent | CLOSED (stale >4d, 2026-07-14) |
| pré-loop | #59142 | fix: remove stale noqa comments from hermes_cli/ files (RUF100) | noqa, ruff, hermes_cli | CLOSED (stale >4d, 2026-07-14) |
| pré-loop | #59141 | fix: remove stale noqa comments from tools/ files (RUF100) | noqa, ruff, tools | CLOSED (stale >4d, 2026-07-14) |
| pré-loop | #59116 | fix(settings): clear model selection when switching providers | settings, model selection | CLOSED (stale >4d, 2026-07-14) |
| pré-loop | #59115 | Remove stale noqa comments from lsp/manager.py | noqa, ruff, lsp | CLOSED (stale >4d, 2026-07-14) |
| pré-loop | #59108 | fix: remove stale noqa/type:ignore comments in browser_tool.py | noqa, type:ignore, browser_tool | CLOSED (stale >4d, 2026-07-14) |
| pré-loop | #59104 | fix(run_agent): remove 19 stale noqa directives | noqa, run_agent | CLOSED (stale >4d, 2026-07-14) |
| pré-loop | #59103 | fix: remove stale noqa comments from tools/web_tools.py | noqa, web_tools | CLOSED (stale >4d, 2026-07-14) |
| pré-loop | #59102 | fix: remove stale # noqa: BLE001 comments from tui_gateway/server.py | noqa, BLE001, tui_gateway | CLOSED (stale >4d, 2026-07-14) |
| pré-loop | #59100 | fix: remove stale # noqa comments from gateway/run.py | noqa, gateway/run.py | CLOSED (stale >4d, 2026-07-14) |
| pré-loop | #58943 | refactor: replace redundant f"{var}" with bare var in plugins/ | fstring, plugins | CLOSED (stale >4d, 2026-07-14) |
| pré-loop | #58942 | chore: remove unused imports in gateway/ | unused imports, gateway | CLOSED (stale >4d, 2026-07-14) |
| pré-loop | #58941 | refactor: replace redundant f"{var}" with bare var in hermes_cli/ | fstring, hermes_cli | CLOSED (stale >4d, 2026-07-14) |
| pré-loop | #58940 | refactor: replace redundant f"{var}" with bare var in agent/ | fstring, agent | CLOSED (stale >4d, 2026-07-14) |
| pré-loop | #58939 | chore: remove unused imports in agent/ | unused imports, agent | CLOSED (stale >4d, 2026-07-14) |
| pré-loop | #58938 | refactor: replace redundant f"{var}" with bare var in tools/ | fstring, tools | CLOSED (stale >4d, 2026-07-14) |
| pré-loop | #58918 | refactor: replace redundant f"{var}" with bare var in string contexts | fstring | CLOSED (stale >4d, 2026-07-14) |
| pré-loop | #58909 | chore: remove 25 unused imports across 18 Python files | unused imports | CLOSED (stale >4d, 2026-07-14) |
| pré-loop | #58903 | fix(docs): replace broken NeurIPS style files URL with conference homepage | docs, neurips, url | CLOSED (stale >4d, 2026-07-14) |
| pré-loop | #58900 | fix: idiomatic Python improvements in tui_gateway/, agent/, and tools/ | idiomatic python, tui_gateway | CLOSED (stale >4d, 2026-07-14) |
| 2026-07-15 | SKIPPED | #35520 dashboard <1024px layout/scroll | dashboard, mobile, sidebar, dvh, viewport | SKIPPED — issue author abduznik commented "I can send my solution to this, fixed it locally for myself" (self-claim); also overlaps open PRs #21065 (sidebar overlap at lg+) and #32359 (hide desktop sidebar on mobile) per issue comment from alt-glitch. No PR opened. |
| 2026-07-15 | SKIPPED | #29347 kanban DELETE /tasks/:id missing board param | kanban, DELETE, tasks, board param, 404 | SKIPPED — PR #29353 "fix(kanban-dashboard): thread board into DELETE /tasks/:id callbacks (#29347)" already open (xxxigm), unmerged, exact fix for this issue. No duplicate opened. |
| 2026-07-16 | SKIPPED | #65289 memory lock file feature request | memory, feature, lock-file | SKIPPED — unrequested feature design (new lock-file mechanism), zero maintainer engagement, ambiguous cross-platform path/scope decisions best left to a maintainer call; not a bug, no urgency, we're already at 10 open PRs (above healthy 3-5 band). No PR opened.
