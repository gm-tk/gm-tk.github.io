// _s29_r7_titlerule.cjs — apply the candidate EMBEDDED-TITLE rule to every site of _s29_r7_redtitle.json and report the gold share.
const fs=require("fs"),path=require("path");
const ROOT=path.join(__dirname,"..");const APP=path.join(ROOT,"app","js"),DATA=path.join(ROOT,"data");
const j=p=>JSON.parse(fs.readFileSync(p,"utf8"));
const {Utils}=require(path.join(APP,"Utils.js"));globalThis.Utils=Utils;
const Data=Object.fromEntries(Object.entries({TagLexicon:"Tag_Lexicon.json",TagExceptions:"Tag_Exceptions.json",InstructionCues:"Instruction_Cues.json",InputDocRules:"Input_Doc_Rules.json",EmitTemplates:"Emit_Templates.json",BoundaryBank:"Interactive_Boundary_ChildTag_Bank.json"}).map(([k,f])=>[k,j(path.join(DATA,f))]));
globalThis.DataService={Data};
Object.assign(globalThis,require(path.join(APP,"TagNormaliser.js")));
const norm=new TagNormaliser(Data.TagLexicon,Data.TagExceptions,Data.InstructionCues,Data.InputDocRules);
const cues=(Data.InstructionCues.cue_patterns||[]).map(p=>new RegExp(p,"i"));
const rows=j(path.join(__dirname,"_s29_r7_redtitle.json")).filter(r=>r.kind==="title");
function verdict(r){
  const free=r.free.trim();
  const b=r.bracket.toLowerCase();
  let span=r.bracket+" "+free; let p=null; try{p=norm.Parse(span);}catch(e){return "parse-err";}
  if(!p||!p.primary||p.primary.tag!=="activity") return "not an activity opener";
  if((p.primary.remainder||"").trim()) return "opener with remainder ("+p.primary.remainder.trim()+")";
  if(p.instructionFragment) return "instruction fragment";
  if(/^\(|\)$/.test(free)) return "parenthesised";
  if(/^\d/.test(free)) return "digit-led";
  if(/[:]$/.test(free)) return "colon-ended";
  if(free.split(/\s+/).length>8) return ">8 words";
  if(cues.some(c=>c.test(free))) return "instruction cue";
  let q=null; try{q=norm.Parse("["+free+"]");}catch(e){}
  if(q&&q.primary) return "widget/tag name ("+q.primary.tag+")";
  return "TITLE";
}
const C={};const ex={};
for(const r of rows){const v=verdict(r);const k=v.replace(/\(.*\)/,"").trim()+" | gold "+r.gold;C[k]=(C[k]||0)+1;(ex[k]=ex[k]||[]).length<3&&ex[k].push(r.code+" "+r.bracket.slice(0,28)+" «"+r.free.slice(0,34)+"» "+v);}
for(const k of Object.keys(C).sort())console.log(String(C[k]).padStart(4),k,"   e.g.",ex[k].join(" ; "));
const T=rows.filter(r=>verdict(r)==="TITLE");const g={};for(const r of T)g[r.tmpl+"|"+r.subj+"|"+r.gold]=(g[r.tmpl+"|"+r.subj+"|"+r.gold]||0)+1;
console.log("\nTITLE by group:");for(const k of Object.keys(g).sort())console.log("  ",k,g[k]);
console.log("TITLE sites",T.length,"gold h3",T.filter(r=>r.gold==="h3").length,"pages",new Set(T.map(r=>r.code)).size+" modules");
