const fs=require("fs"),path=require("path");
const ROOT=path.join(__dirname,"..");
const APP=path.join(ROOT,"app","js"),DATA=path.join(ROOT,"data");
const j=p=>JSON.parse(fs.readFileSync(p,"utf8"));
const {Utils}=require(path.join(APP,"Utils.js"));globalThis.Utils=Utils;
const Data=Object.fromEntries(Object.entries({TagLexicon:"Tag_Lexicon.json",TagExceptions:"Tag_Exceptions.json",InstructionCues:"Instruction_Cues.json",InputDocRules:"Input_Doc_Rules.json"}).map(([k,f])=>[k,j(path.join(DATA,f))]));
globalThis.DataService={Data};
Object.assign(globalThis,require(path.join(APP,"TagNormaliser.js")));
const norm=new TagNormaliser(Data.TagLexicon,Data.TagExceptions,Data.InstructionCues,Data.InputDocRules);
for (const t of process.argv.slice(2)) { const r=norm.Parse(t); const p=r&&r.primary; console.log(JSON.stringify(t), "->", p?p.tag:"null", p?p.directive:"-", "class="+r.class, "how="+(p?p.how:"-"), "tags="+JSON.stringify((r.tags||[]).map(x=>x.tag))); }
