/** _s28_t1_update_sar.cjs — Session 28 / Task 1: bring Style_Anchor_Registry.json up to the 552-dir gold corpus.
 *
 *  Source of every value: outputs/_s28_t1_mine_sar.json (ReferenceMiner.Distil over every gold module of the
 *  intake prefixes — the r263 SCCH / r265 CHFUN pattern), aggregated per prefix and per level (prefix + first digit).
 *
 *  What it does, per intake prefix:
 *   A. NO base in the registry  → a NEW base under the subject bucket the label map names (Subject_Prefix_Map.json;
 *      a missing bucket is created with empty subject_rules), COMPLETE base_rules (all 11 fields + template_phase,
 *      the prefix majority — complete so a junk subject tier ('1-10 Science' "—" / "n/a") can never leak through),
 *      one level per first digit with the gold members and a delta holding the level's own template_phase and any
 *      field whose level majority differs from the base majority.
 *   B. Base exists → the new gold codes join their level's members (level created when absent). If the base had NO
 *      gold-built member before this rebuild (its evidence-floor flips OFF now — the r263 trap: ANZHFUN / ENO /
 *      XOTPB / XOTPG / XOTPO), its Stage-1 values are checked against the gold: a base whose members are ALL in the
 *      gold now gets its base_rules REPLACED by the mined majority; a base with un-goldened members (ENO1) keeps
 *      its row and the new level carries a delta for every field the gold disagrees on.
 *   C. Miner normalisation: a chip text equal to the module code (the miner's refCode misses digit-less codes and
 *      7-letter prefixes) reads "full-code"; a null scalar (no <body class>, no level attr) is left unset = default.
 *
 *  Writes data/Style_Anchor_Registry.json with the file's own tab serialisation (byte-faithful re-save proven) and a
 *  change log to outputs/_s28_t1_update_sar.out. --dry-run prints without writing.
 */
"use strict";
const fs = require("fs"), path = require("path");
const ROOT = path.join(__dirname, "..", "..");
const DATA = path.join(ROOT, "pageforge-site", "converter-v2", "data");
const SAR_PATH = path.join(DATA, "Style_Anchor_Registry.json");
const dry = process.argv.includes("--dry-run");
const SAR = JSON.parse(fs.readFileSync(SAR_PATH, "utf8"));
const MINED = JSON.parse(fs.readFileSync(path.join(__dirname, "_s28_t1_mine_sar.json"), "utf8"));
const LABELS = JSON.parse(fs.readFileSync(path.join(DATA, "Subject_Prefix_Map.json"), "utf8")).prefixes;
const MSI_NEW = JSON.parse(fs.readFileSync(path.join(DATA, "Module_Structure_Index.json"), "utf8"));
const MSI_OLD = JSON.parse(fs.readFileSync(path.join(__dirname, "_s28_t1_pre", "Module_Structure_Index.json"), "utf8"));
const goldNew = new Set([...Object.keys(MSI_NEW.modules), ...Object.keys(MSI_NEW.module_meta)]);
const goldOld = new Set([...Object.keys(MSI_OLD.modules), ...Object.keys(MSI_OLD.module_meta)]);
const moveLog = fs.readFileSync(path.join(ROOT, "00-NEW_NEW_NEW", "_MOVE_LOG_2026-09-19.tsv"), "utf8")
  .split(/\r?\n/).filter((l) => l && !l.startsWith("#")).map((l) => l.split("\t")[0]);
const newCodes = new Set(moveLog);
const prefixOf = (c) => (c.match(/^[A-Z]+/) || [""])[0];
const digitsOf = (c) => (c.match(/\d+/) || [""])[0];
const levelName = (c) => prefixOf(c) + (digitsOf(c)[0] ?? "");
const FIELDS = ["template_phase", "body_class", "level_attr", "idoc_host", "footer_class", "acknowledgements",
  "module_code", "h1_count", "menu_type", "menu_button_tooltip", "footer_links", "page_model"];
const PATTERN = new Set(["module_code", "h1_count", "menu_type", "menu_button_tooltip", "footer_links"]);
const log = [];
const L = (s) => { log.push(s); console.log(s); };

// ---- normalise one module's mined rules (C) --------------------------------------------------------------------
function normalised(code, r) {
  const out = {};
  for (const f of FIELDS) {
    let v = r[f];
    if (v == null) continue;
    if (PATTERN.has(f)) {
      const o = {};
      for (const [k, x] of Object.entries(v)) {
        if (x == null) continue;
        let y = x;
        if (f === "module_code" && typeof y === "string") {
          // the miner returns the RAW chip text when it matches no form; map it onto the registry vocabulary
          // (Emit_Templates header.module_code_value_map: full-code / decimal / padded-number / free-text:"…")
          const up = y.toUpperCase();
          if (up === code.toUpperCase()) y = "full-code";                               // digit-less / 7-letter codes the miner's refCode missed
          else if (/^[A-Z]+\d+[._\- ]0\d$/.test(up)) y = "padded-number";                // "ENO2060.01" — the code + a zero-padded lesson (closest form)
          else if (/^[A-Z]+\d+[._\- ]\d+(\.\d+)?$/.test(up)) y = "decimal";              // "CODE 1.0"
          else if (/^LESSON \d+$/.test(up)) y = 'free-text:"Lesson"';                    // renders "Lesson N" (the literal + the lesson number)
        }
        o[k] = y;
      }
      if (!Object.keys(o).length) continue;
      v = o;
    }
    out[f] = v;
  }
  return out;
}
const key = (v) => JSON.stringify(v);
function majority(codes, f) {
  const cnt = new Map();
  for (const c of codes) {
    const r = normalised(c, MINED.per_module[c] || {});
    if (r[f] === undefined) continue;
    const k = key(r[f]);
    const e = cnt.get(k) || { v: r[f], n: 0, codes: [] }; e.n++; e.codes.push(c); cnt.set(k, e);
  }
  const ranked = [...cnt.values()].sort((a, b) => b.n - a.n || key(a.v).localeCompare(key(b.v)));
  return ranked.length ? { ...ranked[0], of: codes.length, ranked } : null;
}
function profile(codes) {   // complete majority profile over a code set
  const p = {}, notes = [];
  for (const f of FIELDS) {
    const m = majority(codes, f);
    if (!m) continue;
    p[f] = m.v;
    if (m.ranked.length > 1) notes.push(`${f}: ${key(m.v)} ${m.n}/${m.of}` + m.ranked.slice(1).map((x) => ` | ${key(x.v)} ×${x.n} (${x.codes.join(",")})`).join(""));
  }
  return { rules: p, notes };
}
// ---- registry helpers ----------------------------------------------------------------------------------------------
function findBase(prefix) {
  for (const [s, subj] of Object.entries(SAR)) {
    if (s.startsWith("_") || s === "defaults") continue;
    if (subj.bases?.[prefix]) return { subject: s, base: subj.bases[prefix] };
  }
  return null;
}
function evidence(base, gold) {
  let n = 0;
  for (const lvl of Object.values(base.levels ?? {})) for (const m of lvl.members ?? []) if (gold.has(String(m).replace(/\.html$/i, ""))) n++;
  return n;
}
function resolvedFor(subjectName, base, lvlName) {   // the plain walk: defaults -> subject -> base -> level
  const rules = structuredClone(SAR.defaults);
  Object.assign(rules, structuredClone(SAR[subjectName].subject_rules ?? {}));
  Object.assign(rules, structuredClone(base.base_rules ?? {}));
  if (lvlName && base.levels?.[lvlName]) Object.assign(rules, structuredClone(base.levels[lvlName].delta ?? {}));
  return rules;
}
const goldCodesOf = (prefix) => (MINED.by_prefix[prefix]?.codes ?? []).filter((c) => (MINED.per_module[c] || {})._pages > 0);

// ---- the intake prefixes ---------------------------------------------------------------------------------------------
const prefixes = [...new Set(moveLog.map(prefixOf))].sort();
// HELD BACK (session 28, measured): FRFUN — the MULTI-FILE level-page fundamentals dialect ('[Title] [H1] [Novice Page N]'
// + '[End page]' per file, side-tab '[Tab N]' markers inside the lessons; gold lesson pages keep the Standard chip + rows
// under a 'fundamentals container-fluid' body). The faithful row (body_class fundamentals …) switches the engine's
// fundamentals panel mode on, whose HPFUN '[New tab]' sentinel then wraps every FRFUN lesson page in a phase panel:
// the in-memory probe scored FRFUN06/07/08 28 pages 2 up / 26 down, pp-sum −763.7 (FRFUN08_9_0 78.5 → 21.9). The row
// stays MEASURED (outputs/_s28_t1_mine_sar.json, prefix FRFUN) and waits for the dialect round; FRFUN keeps resolving
// from the global defaults exactly as before.
const HELD_BACK = new Set(["FRFUN"]);
const summary = { new_bases: [], members_added: [], rows_replaced: [], level_deltas: [], buckets_created: [], held_back: [] };
for (const prefix of prefixes) {
  const codes = goldCodesOf(prefix);
  if (!codes.length) { L(`${prefix}: no gold pages mined — skipped`); continue; }
  if (HELD_BACK.has(prefix)) { summary.held_back.push(`${prefix} (${codes.length} gold modules — measured, not registered; see the HELD_BACK note)`); L(`! ${prefix}: HELD BACK — measured, not registered (the multi-file level-page fundamentals dialect has no renderer yet)`); continue; }
  const found = findBase(prefix);
  const byLevel = {};
  for (const c of codes) (byLevel[levelName(c)] ??= []).push(c);

  if (!found) {   // (A) a new base
    const label = LABELS[prefix];
    if (!label) { L(`${prefix}: NO LABEL in Subject_Prefix_Map — base not created`); continue; }
    if (!SAR[label]) { SAR[label] = { subject_rules: {}, bases: {} }; summary.buckets_created.push(label); L(`  + subject bucket "${label}" created (empty subject_rules)`); }
    const bp = profile(codes);
    const base = { base_code: prefix, base_rules: bp.rules, levels: {} };
    for (const [lv, lcodes] of Object.entries(byLevel).sort()) {
      const lp = profile(lcodes);
      const delta = {};
      for (const f of FIELDS) {
        if (lp.rules[f] === undefined) continue;
        if (f === "template_phase" || key(lp.rules[f]) !== key(bp.rules[f])) delta[f] = lp.rules[f];
      }
      base.levels[lv] = { members: lcodes.slice().sort(), delta };
    }
    base._mined_2026_09_20 = `Session 28 / Task 1: base row mined from the ${codes.length} gold module(s) ${codes.join(" ")} with ReferenceMiner.Distil (outputs/_s28_t1_mine_sar.json); majority per field` + (bp.notes.length ? `; splits — ${bp.notes.join("; ")}` : "; every field unanimous");
    SAR[label].bases[prefix] = base;
    summary.new_bases.push(`${label}/${prefix} (${codes.length})`);
    L(`+ NEW base ${label}/${prefix}: ${codes.length} gold modules, levels ${Object.keys(base.levels).join(",")}`);
    for (const n of bp.notes) L(`    split ${n}`);
    continue;
  }

  // (B) an existing base
  const { subject, base } = found;
  const evOld = evidence(base, goldOld);   // BEFORE the new members join (the pre-rebuild floor state)
  const added = [];
  for (const [lv, lcodes] of Object.entries(byLevel).sort()) {
    base.levels ??= {};
    if (!base.levels[lv]) {
      const lp = profile(lcodes);
      base.levels[lv] = { members: [], delta: { template_phase: lp.rules.template_phase ?? resolvedFor(subject, base, null).template_phase } };
      L(`  + level ${prefix}.${lv} created`);
    }
    for (const c of lcodes) {
      const mem = base.levels[lv].members ??= [];
      if (!mem.some((m) => String(m).replace(/\.html$/i, "").toUpperCase() === c)) { mem.push(c); added.push(c); }
    }
    base.levels[lv].members.sort();
  }
  const evNew = evidence(base, goldNew);   // AFTER: the floor state the engine will see (a module's own code counts once indexed)
  if (added.length) { summary.members_added.push(`${subject}/${prefix}: ${added.join(" ")}`); L(`~ ${subject}/${prefix}: members +${added.length} (${added.join(" ")}); evidence ${evOld} → ${evNew}`); }
  else L(`= ${subject}/${prefix}: members already complete; evidence ${evOld} → ${evNew}`);

  if (evOld === 0 && evNew > 0) {   // the evidence floor flips OFF for this base: its Stage-1 row must match the gold
    const allMembers = [...new Set(Object.values(base.levels).flatMap((l) => (l.members ?? []).map((m) => String(m).replace(/\.html$/i, ""))))];
    const unGold = allMembers.filter((m) => !goldNew.has(m));
    const bp = profile(codes);
    if (!unGold.length) {   // every member is gold now → replace the row wholesale
      const before = JSON.stringify(base.base_rules);
      base.base_rules = bp.rules;
      for (const [lv, lcodes] of Object.entries(byLevel)) {
        const lp = profile(lcodes); const delta = {};
        for (const f of FIELDS) { if (lp.rules[f] === undefined) continue; if (f === "template_phase" || key(lp.rules[f]) !== key(bp.rules[f])) delta[f] = lp.rules[f]; }
        base.levels[lv].delta = delta;
      }
      for (const lv of Object.keys(base.levels)) if (!byLevel[lv]) { const d = base.levels[lv].delta ?? {}; base.levels[lv].delta = { template_phase: d.template_phase ?? bp.rules.template_phase }; }
      base._mined_2026_09_20 = `Session 28 / Task 1: the Stage-1 row (no gold-built member until the September intake — the r263 stale-registry class) REPLACED by the ReferenceMiner.Distil majority over ${codes.join(" ")}; previous base_rules: ${before}` + (bp.notes.length ? `; splits — ${bp.notes.join("; ")}` : "; every field unanimous");
      summary.rows_replaced.push(`${subject}/${prefix}`);
      L(`  ! base_rules REPLACED from gold (floor 0 → ${evNew}, every member gold): was ${before}`);
    } else {   // un-goldened members remain: scope the correction to the new members' level(s)
      for (const [lv, lcodes] of Object.entries(byLevel)) {
        const res = resolvedFor(subject, base, lv);
        const lp = profile(lcodes); const delta = base.levels[lv].delta ??= {}; const fixed = [];
        for (const f of FIELDS) { if (lp.rules[f] === undefined) continue; if (key(res[f]) !== key(lp.rules[f])) { delta[f] = lp.rules[f]; fixed.push(`${f} ${key(res[f])} → ${key(lp.rules[f])}`); } }
        if (fixed.length) { summary.level_deltas.push(`${subject}/${prefix}.${lv}: ${fixed.join(", ")}`); L(`  ! level ${lv} delta corrected to gold (floor 0 → ${evNew}; ${unGold.length} un-goldened member(s) ${unGold.slice(0, 5).join(",")} keep the row): ${fixed.join(", ")}`); }
      }
    }
  }
}

// ---- BLLR: doc-14 §14.9 says BLLR is a DISTINCT series from BLL; its 3 gold modules agree on every field but one ----
if (!findBase("BLLR")) {
  const codes = goldCodesOf("BLLR");
  if (codes.length) {
    const label = LABELS.BLLR; const bp = profile(codes);
    const base = { base_code: "BLLR", base_rules: bp.rules, levels: { BLLR2: { members: codes.slice().sort(), delta: { template_phase: bp.rules.template_phase } } } };
    base._mined_2026_09_20 = `Session 28 / Task 1: BLLR had no row and inherited the BLL base's BLL2 level by prefix match (doc-14 §14.9: a DISTINCT series); mined from ${codes.join(" ")}` + (bp.notes.length ? `; splits — ${bp.notes.join("; ")}` : "; every field unanimous");
    SAR[label].bases.BLLR = base; summary.new_bases.push(`${label}/BLLR (${codes.length})`);
    L(`+ NEW base ${label}/BLLR: ${codes.length} gold modules`); for (const n of bp.notes) L(`    split ${n}`);
  }
}

L("\n== SUMMARY ==");
L(`new bases (${summary.new_bases.length}): ${summary.new_bases.join(", ")}`);
L(`subject buckets created: ${summary.buckets_created.join(", ") || "none"}`);
L(`rows replaced from gold (floor flipped, all members gold): ${summary.rows_replaced.join(", ") || "none"}`);
L(`level deltas corrected (floor flipped, un-goldened members kept): ${summary.level_deltas.join(" ; ") || "none"}`);
L(`held back (measured, not registered): ${summary.held_back.join(", ") || "none"}`);
L(`members added: ${summary.members_added.length} bases`);
for (const m of summary.members_added) L(`   ${m}`);
fs.writeFileSync(path.join(__dirname, "_s28_t1_update_sar.out"), log.join("\n") + "\n");
if (dry) { console.log("(dry run — nothing written)"); process.exit(0); }
fs.writeFileSync(SAR_PATH, JSON.stringify(SAR, null, "\t") + "\n");
console.log("wrote", SAR_PATH);
