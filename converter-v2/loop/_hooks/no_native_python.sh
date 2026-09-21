#!/usr/bin/env bash
# PreToolUse hook (Bash / PowerShell): refuse a shell command that runs python NATIVELY on this
# Windows machine. The native `python3` resolves to the Windows Store stub and hangs for the full
# 30-minute shell timeout (five recorded hits, sessions 28-31). Every Python runs under WSL —
# LOOP__Autonomous_Rounds.md §6. Installed by /loop-review 2026-09-22.
#
# Reads the hook JSON on stdin; exit 2 = block (stderr is shown to Claude), exit 0 = allow.
# Allowed: any command that mentions `wsl` (the python is assumed to be inside the WSL call).
node -e '
let s = "";
process.stdin.on("data", d => s += d).on("end", () => {
  let cmd = "";
  try { const j = JSON.parse(s); cmd = (j.tool_input && j.tool_input.command) || ""; } catch (e) {}
  const mentionsPython = /(^|[^A-Za-z0-9_\-.\/])python[0-9.]*(\s|$|["'"'"')])/m.test(cmd);
  const viaWsl = /(^|[^A-Za-z0-9_])wsl(\.exe)?(\s|$)/m.test(cmd);
  if (mentionsPython && !viaWsl) {
    process.stderr.write(
      "BLOCKED by .claude/hooks/no_native_python.sh: python runs ONLY under WSL on this machine " +
      "(LOOP__Autonomous_Rounds.md §6) — the native python3 is the Windows Store stub and hangs for the " +
      "full 30-minute timeout. Re-run it as: wsl -e bash -lc \"cd <linux path> && python3 <script>\" " +
      "(write the script with the Write tool first; never `python3 - <<EOF`).\n");
    process.exit(2);
  }
  process.exit(0);
});
'
