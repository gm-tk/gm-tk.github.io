#!/usr/bin/env node
// Session 28 / Task 1 — census of the 98 September-intake modules against the mined registries.
// For each new code: template (from the move log), prefix, in module_meta?, in StyleRegistry (base)?,
// in subject_map?, current ModuleResolver note (from the Claude dir's _run.json), Claude dir present?
"use strict";
const fs = require("fs");
const path = require("path");
const ROOT = path.resolve(__dirname, "..", "..");
const DATA = path.join(ROOT, "pageforge-site", "converter-v2", "data");
const MSI = JSON.parse(fs.readFileSync(path.join(DATA, "Module_Structure_Index.json"), "utf8"));
const SAR = JSON.parse(fs.readFileSync(path.join(DATA, "Style_Anchor_Registry.json"), "utf8"));
const MAJ = JSON.parse(fs.readFileSync(path.join(DATA, "Style_Anchor_Registry_Majority_And_Deviations.json"), "utf8"));
const MSR = JSON.parse(fs.readFileSync(path.join(DATA, "Menu_Scaffold_Registry.json"), "utf8"));
const GSR = JSON.parse(fs.readFileSync(path.join(DATA, "Granular_Scaffold_Registry.json"), "utf8"));
const MFI = JSON.parse(fs.readFileSync(path.join(DATA, "Module_Feature_Index.json"), "utf8"));

const moveLog = fs.readFileSync(path.join(ROOT, "00-NEW_NEW_NEW", "_MOVE_LOG_2026-09-19.tsv"), "utf8")
  .split(/\r?\n/).filter((l) => l && !l.startsWith("#")).map((l) => l.split("\t"));
const newCodes = moveLog.map(([code, tpl]) => ({ code, tpl }));

// StyleRegistry bases
const bases = [];
for (const [subj, s] of Object.entries(SAR)) {
  if (subj.startsWith("_") || subj === "defaults") continue;
  for (const [b, base] of Object.entries(s.bases ?? {})) {
    const members = [];
    for (const lvl of Object.values(base.levels ?? {})) for (const m of lvl.members ?? []) members.push(String(m).replace(/\.html$/i, ""));
    bases.push({ subj, base: b, members });
  }
}
function findBase(code) {
  const u = code.toUpperCase();
  for (const b of bases) if (b.members.includes(u)) return { ...b, exact: true };
  let best = null;
  for (const b of bases) if (u.startsWith(b.base.toUpperCase()) && (!best || b.base.length > best.base.length)) best = b;
  return best ? { ...best, exact: false } : null;
}
// Majority registry series knowledge
function majHit(code) {
  const prefix = code.match(/^[A-Z]+/)?.[0] ?? "";
  for (const [subjectName, subject] of Object.entries(MAJ)) {
    if (subjectName.startsWith("_")) continue;
    for (const phase of Object.values(subject)) {
      if (!phase?.series_deviations) continue;
      if (Object.keys(phase.series_deviations).some((s) => prefix.startsWith(s) || s.startsWith(prefix))) return subjectName;
    }
  }
  return null;
}
const subjectMap = MSI._meta.subject_map ?? {};
const gsrSubjectMap = GSR._meta._subject_map ?? {};
const msrGroups = Object.keys(MSR.groups ?? {});
const msrSeries = Object.keys(MSR.series ?? {});

const rows = [];
const prefixes = new Map();
for (const { code, tpl } of newCodes) {
  const prefix = code.match(/^[A-Z]+/)?.[0] ?? "";
  const inMeta = !!MSI.module_meta?.[code];
  const inMods = !!MSI.modules?.[code];
  const inMFI = !!MFI.modules?.[code];
  const b = findBase(code);
  const maj = majHit(code);
  let note = "(no Claude dir)";
  const cdir = path.join(ROOT, "01-Claude_Modules_", tpl, code);
  const hasClaude = fs.existsSync(cdir);
  if (hasClaude) {
    const rj = path.join(cdir, "_run.json");
    if (fs.existsSync(rj)) {
      const run = JSON.parse(fs.readFileSync(rj, "utf8"));
      const n = (run.notes ?? []).filter((x) => x.stage === "ModuleResolver" || x.stage === "ConventionResolver").map((x) => x.text.replace(code + ": ", "").slice(0, 90));
      note = n.join(" | ");
    } else note = "(no _run.json)";
  }
  rows.push({ code, tpl, prefix, inMeta, inMods, inMFI, base: b ? `${b.subj}/${b.base}${b.exact ? "*" : ""}` : "-", maj: maj ?? "-", subjMap: subjectMap[prefix] ?? "-", gsrMap: gsrSubjectMap[prefix] ?? "-", hasClaude, note });
  const p = prefixes.get(prefix) ?? { n: 0, tpls: new Set(), codes: [] };
  p.n++; p.tpls.add(tpl); p.codes.push(code);
  prefixes.set(prefix, p);
}
console.log("code\ttpl\tprefix\tmeta\tmods\tMFI\tclaude\tSAR base\tMAJ subj\tsubject_map\tGSR map\tresolver note");
for (const r of rows) console.log([r.code, r.tpl, r.prefix, r.inMeta ? "Y" : "-", r.inMods ? "Y" : "-", r.inMFI ? "Y" : "-", r.hasClaude ? "Y" : "-", r.base, r.maj, r.subjMap, r.gsrMap, r.note].join("\t"));
console.log("\n== PREFIX SUMMARY ==");
for (const [p, v] of [...prefixes.entries()].sort()) {
  const knownSubj = subjectMap[p] ?? "-";
  const sarBase = bases.find((b) => p.startsWith(b.base.toUpperCase()) || b.base.toUpperCase().startsWith(p));
  console.log(`${p}\tn=${v.n}\t${[...v.tpls].join("/")}\tsubject_map=${knownSubj}\tSARbase=${sarBase ? sarBase.subj + "/" + sarBase.base : "-"}\tMSR=${msrGroups.filter((g) => g.startsWith(p + "|")).join(",") || "-"}\t${v.codes.join(" ")}`);
}
console.log("\nmodule_meta n=", Object.keys(MSI.module_meta).length, " modules n=", Object.keys(MSI.modules).length, " MFI n=", Object.keys(MFI.modules).length);
console.log("subject_map keys:", Object.keys(subjectMap).length, " distinct subjects:", [...new Set(Object.values(subjectMap))].sort().join(" | "));
