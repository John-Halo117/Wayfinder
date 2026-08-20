#!/usr/bin/env python3
from __future__ import annotations
import ast, json, re, subprocess
from pathlib import Path
from dataclasses import dataclass, asdict
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/".wayfinder"/"generated"
BIN={".png",".jpg",".jpeg",".gif",".webp",".ico",".pdf",".zip",".gz",".zst",".jar",".apk",".so",".dll",".dylib",".class",".pyc",".woff",".woff2",".ttf",".otf",".mp3",".mp4",".wav",".sqlite",".db"}
SKIP_PREFIX=(".wayfinder/generated/","build/","dist/","node_modules/","vendor/",".venv/","venv/")
@dataclass(frozen=True)
class Finding: path:str; line:int; severity:str; rule:str; message:str
@dataclass(frozen=True)
class Skip: path:str; reason:str

def files():
 c=subprocess.run(["git","ls-files","-z"],cwd=ROOT,check=True,stdout=subprocess.PIPE).stdout
 return [x.decode("utf-8","surrogateescape") for x in c.split(b"\0") if x]
def py(path,text):
 out=[]
 try: tree=ast.parse(text,filename=path)
 except SyntaxError as e: return [Finding(path,e.lineno or 0,"BLOCKER","PY_SYNTAX",e.msg)]
 for n in ast.walk(tree):
  if isinstance(n,ast.ExceptHandler) and n.type is None: out.append(Finding(path,n.lineno,"WARN","BARE_EXCEPT","bare except hides failure semantics"))
  if isinstance(n,ast.ExceptHandler) and isinstance(n.type,ast.Name) and n.type.id=="Exception": out.append(Finding(path,n.lineno,"INFO","BROAD_EXCEPTION","broad exception needs recovery justification"))
  if isinstance(n,ast.Call):
   f=n.func
   if isinstance(f,ast.Name) and f.id in {"eval","exec"}: out.append(Finding(path,n.lineno,"BLOCKER","DYNAMIC_EXEC",f"{f.id}() expands code surface"))
   if isinstance(f,ast.Attribute) and isinstance(f.value,ast.Name) and f.value.id=="os" and f.attr=="system": out.append(Finding(path,n.lineno,"BLOCKER","OS_SYSTEM","os.system bypasses structured execution"))
   if isinstance(f,ast.Attribute) and f.attr in {"Popen","run","call","check_call","check_output"}:
    if any(k.arg=="shell" and isinstance(k.value,ast.Constant) and k.value.value is True for k in n.keywords): out.append(Finding(path,n.lineno,"BLOCKER","SUBPROCESS_SHELL_TRUE","shell=True expands injection surface"))
  if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)):
   for d in list(n.args.defaults)+[x for x in n.args.kw_defaults if x is not None]:
    if isinstance(d,(ast.List,ast.Dict,ast.Set)): out.append(Finding(path,n.lineno,"WARN","MUTABLE_DEFAULT",f"mutable default in {n.name}()"))
 return out

def main():
 fs=files(); findings=[]; skips=[]; nfiles=nlines=nbytes=0; conflicts=re.compile(r"^(<{7}|={7}|>{7})(?:\s|$)"); todo=re.compile(r"\b(TODO|FIXME|HACK|XXX)\b",re.I)
 for rel in fs:
  p=ROOT/rel
  if not p.exists() or p.is_dir(): skips.append(Skip(rel,"absent/gitlink/directory")); continue
  if rel.startswith(SKIP_PREFIX): skips.append(Skip(rel,"generated/vendor")); continue
  if p.suffix.lower() in BIN: skips.append(Skip(rel,"binary extension")); continue
  data=p.read_bytes(); nbytes+=len(data)
  if b"\0" in data[:8192]: skips.append(Skip(rel,"binary content")); continue
  try: text=data.decode("utf-8")
  except UnicodeDecodeError: skips.append(Skip(rel,"non-UTF8")); continue
  lines=text.splitlines(keepends=True); nfiles+=1; nlines+=max(1,len(lines))
  for i,line in enumerate(lines,1):
   raw=line.rstrip("\r\n")
   if conflicts.match(raw): findings.append(Finding(rel,i,"BLOCKER","MERGE_MARKER","unresolved merge marker"))
   if raw.endswith(" ") or raw.endswith("\t"): findings.append(Finding(rel,i,"INFO","TRAILING_WHITESPACE","trailing whitespace"))
   if todo.search(raw): findings.append(Finding(rel,i,"INFO","UNRESOLVED_MARKER","TODO/FIXME/HACK remains"))
   if len(raw)>240 and p.suffix.lower() in {".py",".js",".ts",".kt",".java"}: findings.append(Finding(rel,i,"INFO","VERY_LONG_LINE","line >240 chars"))
  if p.suffix.lower()==".py": findings.extend(py(rel,text))
 sev=Counter(f.severity for f in findings); rules=Counter(f.rule for f in findings); report={"tracked_files":len(fs),"audited_text_files":nfiles,"audited_lines":nlines,"bytes_read":nbytes,"skip_count":len(skips),"skipped":[asdict(s) for s in skips],"severity_counts":dict(sev),"rule_counts":dict(rules),"findings":[asdict(f) for f in findings]}
 OUT.mkdir(parents=True,exist_ok=True); (OUT/"full-code-audit.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
 md=["# Wayfinder Full Code Audit","",f"- Tracked files: {len(fs)}",f"- Audited text files: {nfiles}",f"- Audited lines: {nlines}",f"- Skipped: {len(skips)}",f"- BLOCKER: {sev.get('BLOCKER',0)} | WARN: {sev.get('WARN',0)} | INFO: {sev.get('INFO',0)}","","## Rules"]+[f"- {k}: {v}" for k,v in rules.most_common()]+["","## Findings"]+[f"- **{f.severity}** `{f.path}:{f.line}` `{f.rule}` — {f.message}" for f in findings]
 (OUT/"full-code-audit.md").write_text("\n".join(md)+"\n"); print(json.dumps({"tracked_files":len(fs),"audited_text_files":nfiles,"audited_lines":nlines,"skip_count":len(skips),"severity_counts":dict(sev)},sort_keys=True)); return 1 if sev.get("BLOCKER") else 0
if __name__=="__main__": raise SystemExit(main())
