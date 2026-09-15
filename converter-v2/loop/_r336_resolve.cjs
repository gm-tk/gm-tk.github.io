// ROUND 336 probe — what the registry resolves for module_code / h1_count on the Fundamentals families
const eng = require("../reference/tests/_engine_load.cjs");
const Data = eng.loadData();
globalThis.DataService = { Data, async FetchOembed() { return { ok: false }; } };
eng.loadEngine();
for (const code of process.argv.slice(2)) {
  const run = { moduleCode: code, notes: [], AddNote() {} };
  const r = ModuleResolver.Resolve(code, run);
  console.log(code, JSON.stringify(r.module_code), "h1", JSON.stringify(r.h1_count), "body", r.body_class, "| path", JSON.stringify(r._path ?? run.registryPath ?? ""));
}
