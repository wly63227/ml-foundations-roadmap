import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {execFileSync} from 'node:child_process';
import {createHash} from 'node:crypto';
import {marked} from 'marked';
import katex from 'katex';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'../..');
const docs=path.join(root,'教材/docs'),out=path.join(root,'教材/site'),reports=path.join(root,'教材/reports');
fs.mkdirSync(out,{recursive:true});fs.mkdirSync(reports,{recursive:true});
const walk=dir=>fs.readdirSync(dir,{withFileTypes:true}).flatMap(e=>e.isDirectory()?walk(path.join(dir,e.name)):[path.join(dir,e.name)]);
const esc=s=>s.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
const slug=s=>s.toLowerCase().replace(/<[^>]*>/g,'').replace(/[^\p{L}\p{N} -]/gu,'').trim().replace(/\s+/g,'-');
const order=['index.md','roadmap.md','checklist.md','diagnostic.md','math-refresh.md','setup.md',...Array.from({length:16},(_,i)=>`weeks/${String(i+1).padStart(2,'0')}.md`),'bridge.md','resources.md','project.md','tracker.md','answers.md','audit.md'];
const entries=walk(docs).filter(f=>f.endsWith('.md')).map(file=>{const rel=path.relative(docs,file).replaceAll('\\','/'),text=fs.readFileSync(file,'utf8');return {file,rel,text,title:text.match(/^# (.+)$/m)?.[1]??rel,url:rel.replace(/\.md$/,'.html')};});
entries.sort((a,b)=>(order.indexOf(a.rel)<0?999:order.indexOf(a.rel))-(order.indexOf(b.rel)<0?999:order.indexOf(b.rel)));
// Refuse stale output rather than silently serving removed Markdown as a live page.
for(const file of walk(out).filter(f=>f.endsWith('.html'))){const rel=path.relative(out,file).replaceAll('\\','/');if(!entries.some(e=>e.url===rel))throw new Error(`Stale generated page ${rel}; review source change before cleanup.`);}
let formulaCount=0;
for(const [i,e] of entries.entries()){
 const prefix='../'.repeat(e.rel.split('/').length-1),math=[],code=[];
 // Shield fenced and inline code from the math parser.
 let source=e.text.replace(/```[^\n]*\n[\s\S]*?```|`[^`\n]+`/g,m=>{code.push(m);return `CODETOKEN${code.length-1}END`;});
 source=source.replace(/\$\$([\s\S]*?)\$\$|\$([^$\n]+)\$/g,(_,block,inline)=>{math.push(katex.renderToString((block??inline).trim(),{displayMode:block!==undefined,throwOnError:true,strict:'error',output:'htmlAndMathml'}));formulaCount++;return `MATHTOKEN${math.length-1}END`;});
 source=source.replace(/CODETOKEN(\d+)END/g,(_,n)=>code[Number(n)]);
 const headings=[],ids=new Set();
 const renderer=new marked.Renderer();
 renderer.heading=function({tokens,depth}){let label=this.parser.parseInline(tokens),id=label.match(/\s*\{#([^}]+)\}$/)?.[1];label=label.replace(/\s*\{#[^}]+\}$/,'');id??=slug(label);if(ids.has(id))throw new Error(`Duplicate heading ${e.rel}#${id}`);ids.add(id);headings.push({depth,label,id});return `<h${depth} id="${esc(id)}">${label}<a class="anchor" href="#${esc(id)}" aria-label="本节链接">#</a></h${depth}>`;};
 let body=marked.parse(source,{renderer,gfm:true}).replace(/MATHTOKEN(\d+)END/g,(_,n)=>math[Number(n)]).replace(/href="([^"#?]*?)\.md(#[^"]*)?"/g,(_,name,anchor)=>`href="${name}.html${anchor??''}"`).replaceAll('<table>','<div class="table-scroll" tabindex="0" role="region" aria-label="可横向滚动的表格"><table>').replaceAll('</table>','</table></div>');
 body=body.replace(/<p>(<img\b[^>]*>)<\/p>/g,'<div class="figure-scroll" tabindex="0" role="region" aria-label="可横向滚动的图形">$1</div>');
 const nav=entries.map(x=>`<a ${x===e?'aria-current="page"':''} class="${x.rel.startsWith('weeks/')?'week-link':''}" href="${prefix+x.url}">${esc(x.title)}</a>`).join('');
 const toc=headings.filter(h=>h.depth===2).map(h=>`<a href="#${esc(h.id)}">${h.label}</a>`).join('');
 const prev=entries[i-1],next=entries[i+1];
 const html=`<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="数学三周复习，Python 从零起步。面向土木工程转机器学习的 16 周学习路线，每周 8–10 小时。"><title>${esc(e.title)} · 机器学习起步</title><link rel="icon" href="data:,"><link rel="stylesheet" href="${prefix}assets/katex/katex.min.css"><link rel="stylesheet" href="${prefix}assets/style.css"></head><body><a class="skip" href="#content">跳到正文</a><header><a class="brand" href="${prefix}index.html"><span class="brand-icon">↗</span><span>机器学习起步<small>FOUNDATIONS / 16 WEEKS</small></span></a><a class="repo" href="https://github.com/wly63227/ml-foundations-roadmap">GitHub ↗</a></header><div class="layout"><aside class="sidebar"><details class="menu" open><summary>学习目录</summary><nav aria-label="学习目录">${nav}</nav></details><p class="sidebar-note">每周 8–10 小时<br>先自测，再补缺<br>编者自编 · 2026-10-24</p></aside><main id="content"><div class="eyebrow">CIVIL ENGINEERING → MACHINE LEARNING</div><article>${body}</article><footer>${prev?`<a href="${prefix+prev.url}">← ${esc(prev.title)}</a>`:'<span></span>'}${next?`<a href="${prefix+next.url}">${esc(next.title)} →</a>`:''}</footer></main><aside class="toc"><p>本页内容</p>${toc}<a href="#content">返回顶部 ↑</a></aside></div><script src="${prefix}assets/app.js" defer></script><noscript><p class="noscript">正文、公式与目录不依赖 JavaScript。目录默认展开；学习记录请在 Markdown 中保存。</p></noscript></body></html>`;
 const target=path.join(out,e.url);fs.mkdirSync(path.dirname(target),{recursive:true});fs.writeFileSync(target,html);
}
fs.cpSync(path.join(docs,'assets'),path.join(out,'assets'),{recursive:true});
for(const file of ['style.css','app.js'])fs.copyFileSync(path.join(root,'教材/scripts',file),path.join(out,'assets',file));
fs.cpSync(path.join(root,'node_modules/katex/dist'),path.join(out,'assets/katex'),{recursive:true});
let commit=process.env.GITHUB_SHA??null,dirty=null;
try{if(!commit)commit=execFileSync('git',['rev-parse','HEAD'],{cwd:root,encoding:'utf8',stdio:['ignore','pipe','ignore']}).trim();dirty=Boolean(execFileSync('git',['status','--porcelain'],{cwd:root,encoding:'utf8',stdio:['ignore','pipe','ignore']}).trim());}catch{}
fs.writeFileSync(path.join(out,'version.json'),JSON.stringify({commit,dirty,builtAt:new Date().toISOString(),contentVersion:'16-week-v1'},null,2));
fs.writeFileSync(path.join(out,'.nojekyll'),'');
const report={pages:entries.length,formulas:formulaCount,math:'local KaTeX HTML + MathML',builtAt:new Date().toISOString()};
fs.writeFileSync(path.join(reports,'build.json'),JSON.stringify(report,null,2));
fs.writeFileSync(path.join(reports,'content-sha256.json'),JSON.stringify(entries.map(e=>({path:e.rel,sha256:createHash('sha256').update(e.text).digest('hex')})),null,2));
console.log(JSON.stringify(report));
