import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..'),site=path.join(root,'教材/site'),docs=path.join(root,'教材/docs'),errors=[];
const walk=dir=>fs.readdirSync(dir,{withFileTypes:true}).flatMap(e=>e.isDirectory()?walk(path.join(dir,e.name)):[path.join(dir,e.name)]);
const pages=walk(site).filter(f=>f.endsWith('.html'));let links=0,formulas=0;
for(const file of pages){const html=fs.readFileSync(file,'utf8'),ids=[...html.matchAll(/\bid="([^"]+)"/g)].map(x=>x[1]);
 if(new Set(ids).size!==ids.length)errors.push(`Duplicate ID ${file}`);
 if(/MATHTOKEN|CODETOKEN|katex-error|\{#[a-z-]+\}/.test(html))errors.push(`Unrendered token ${file}`);
 formulas+=(html.match(/class="katex"/g)||[]).length;
 if(!html.includes('lang="zh-CN"')||!html.includes('name="viewport"'))errors.push(`Missing accessibility metadata ${file}`);
 for(const [,url] of html.matchAll(/\b(?:href|src)="([^"]+)"/g)){
  if(/^(https?:|mailto:|data:)/.test(url))continue;
  const [name,anchor]=url.split('#'),target=path.resolve(path.dirname(file),decodeURIComponent(name||path.basename(file)));
  if(!target.startsWith(site+path.sep)){errors.push(`Outside site ${url}`);continue;}
  if(!fs.existsSync(target)){errors.push(`Missing ${path.relative(site,file)} -> ${url}`);continue;}
  if(anchor&&target.endsWith('.html')&&!fs.readFileSync(target,'utf8').includes(`id="${decodeURIComponent(anchor)}"`))errors.push(`Missing anchor ${url}`);
  links++;
 }
}
const required=['问题与直觉','本周知识与阅读','分次安排','手算任务','代码任务','完成标准','限制与补救'];
for(let n=1;n<=16;n++){const p=path.join(docs,`weeks/${String(n).padStart(2,'0')}.md`);if(!fs.existsSync(p)){errors.push(`Missing week ${n}`);continue;}const text=fs.readFileSync(p,'utf8');for(const heading of required)if(!text.includes(`## ${heading}`))errors.push(`Week ${n} missing ${heading}`);if(!text.includes('- [ ]')||text.includes('- [x]'))errors.push(`Week ${n} initial status wrong`);}
const tracker=fs.readFileSync(path.join(docs,'tracker.md'),'utf8');if((tracker.match(/- \[ \] 第/g)||[]).length!==16||tracker.includes('- [x]'))errors.push('Tracker must contain 16 unfinished weeks');
// Serve the same output under a project prefix: any root-absolute local URL would fail Pages.
for(const file of pages)if(/(?:href|src)="\/(?!\/)/.test(fs.readFileSync(file,'utf8')))errors.push(`Root-absolute path in ${file}`);
const result={checkedAt:new Date().toISOString(),pages:pages.length,internalLinksAndResources:links,formulas,weeklyPlans:16,errors};
fs.mkdirSync(path.join(root,'教材/reports'),{recursive:true});fs.writeFileSync(path.join(root,'教材/reports/check.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result,null,2));if(errors.length)process.exitCode=1;
