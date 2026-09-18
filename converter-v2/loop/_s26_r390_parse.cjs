const fs=require("fs"),path=require("path");
const ROOT=path.join(__dirname,"..");
const APP=path.join(ROOT,"app","js"),DATA=path.join(ROOT,"data");
const j=p=>JSON.parse(fs.readFileSync(p,"utf8"));
const {Utils}=require(path.join(APP,"Utils.js"));globalThis.Utils=Utils;
const Data=Object.fromEntries(Object.entries({TagLexicon:"Tag_Lexicon.json",TagExceptions:"Tag_Exceptions.json",InstructionCues:"Instruction_Cues.json",InputDocRules:"Input_Doc_Rules.json",StyleRegistry:"Style_Anchor_Registry.json",MajorityRegistry:"Style_Anchor_Registry_Majority_And_Deviations.json",BoundaryBank:"Interactive_Boundary_ChildTag_Bank.json",WrapperCatalogue:"Interactive_Wrapper_Catalogue.json",EmitTemplates:"Emit_Templates.json",AcksFormats:"Acks_Formats.json",ManifestPatterns:"Manifest_Patterns.json",ConventionRegistry:"Html_Convention_Registry.json",MenuScaffold:"Menu_Scaffold_Registry.json"}).map(([k,f])=>[k,j(path.join(DATA,f))]));
globalThis.DataService={Data};
Object.assign(globalThis,require(path.join(APP,"TagNormaliser.js")));
const norm=new TagNormaliser(Data.TagLexicon,Data.TagExceptions,Data.InstructionCues,Data.InputDocRules);
for(const t of process.argv.slice(2)){
  let r=null;try{r=norm.Parse(t);}catch(e){console.log(t,"ERR",e.message);continue;}
  const p=r&&r.primary;
  const wt = p? (norm.GetWidgetTypes(p.tag)||[]):[];
  console.log(t.padEnd(14), "primary.tag="+(p?p.tag:"null"), "| dir="+(p?p.directive:"-"), "| widgetTypes=["+wt+"]", "| folded="+JSON.stringify(r.folded), "| tags="+JSON.stringify(r.tags.map(x=>x.tag)));
}
