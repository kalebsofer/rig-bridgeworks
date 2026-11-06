# Mac setup prompt

## Before starting Claude Code

The guard hook blocks every tool call if no Python runs, so install these first.

```bash
xcode-select --install                            # git and python3
curl -LsSf https://astral.sh/uv/install.sh | sh   # uv
cd ~/Code && git clone https://github.com/kalebsofer/rig-bridgeworks.git
cd rig-bridgeworks && claude
```

Keep the folder name, because `autoMemoryDirectory` in `.claude/settings.json` expects `~/Code/rig-bridgeworks`.
Clone `agent-config` to `~/Code/agent-config` as well, because `.claude/settings.json` and the client writing rules depend on it.

## Prompt

Paste this into Claude Code.

```text
I've just cloned this workspace onto my Mac, having set it up on Windows. Get it working and report back.
This is setup only, so do not start any key task.
Do not commit, push, or change anything outside this repo without asking me.

1. Read CLAUDE.md and docs/rig-scenario.txt, and confirm the folder is ~/Code/rig-bridgeworks.
2. Run ./bootstrap.sh, then uv run pytest tools -q, and confirm git status is still clean.
3. Check .claude/settings.json no longer has a bare `python` hook command or a C:/ additionalDirectories entry.
   If it does, stop and tell me, because the Windows settings patch was never applied.
4. Test .claude/hooks/guard.py by feeding it JSON payload files with a tool_input.file_path value.
   An ordinary path must exit 0, and a path containing a blocked folder name must exit 2.
   Write the payloads with the Write tool, because the guard also checks command text, and do not disguise the name to get past it.
   Test only the guard, and never touch the walled-off folders themselves.
5. Confirm ~/Code/agent-config/context/VOICE.md and OPINIONS.md are readable, and that ~/.claude/CLAUDE.md imports ~/Code/agent-config/AGENTS.md.
   If they are missing, tell me rather than creating them.
6. Tell me to run /memory, and to confirm it shows ~/Code/rig-bridgeworks/.claude/memory.
7. Check whether docs/pack/ has arrived, and run uv run python tools/q.py --tables.

Finish with one line per step, pass or fail, then anything I need to do, then the next step on the exercise.
```
