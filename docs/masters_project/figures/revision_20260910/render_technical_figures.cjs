const fs = require('fs');
const path = require('path');
const {chromium} = require('C:/Users/adebo/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const root = __dirname;
(async()=>{
  const browser = await chromium.launch({channel:'msedge',headless:true});
  const page = await browser.newPage({viewport:{width:1600,height:1800},deviceScaleFactor:2});
  await page.setContent('<!DOCTYPE html><html><head><meta charset="utf-8"></head><body style="margin:0;background:white"></body></html>');
  await page.evaluate(async()=>{
    const {default: mermaid}=await import('https://cdn.jsdelivr.net/npm/mermaid@11.12.0/dist/mermaid.esm.min.mjs');
    window.mermaid=mermaid;
  });
  const manifest=[];
  for(const name of ['figure_3_3_heartbeat_panel','figure_3_3_threat_panel','figure_3_5_corrected']){
    const source=fs.readFileSync(path.join(root,name+'.mmd'),'utf8');
    const svg=await page.evaluate(async({source,name})=>{
      window.mermaid.initialize({startOnLoad:false,securityLevel:'loose',theme:'base',fontFamily:'Arial',
        themeVariables:{fontFamily:'Arial',fontSize:'20px',primaryColor:'#f3f6fa',primaryTextColor:'#14273b',primaryBorderColor:'#41566d',lineColor:'#41566d',secondaryColor:'#eef4ef',tertiaryColor:'#ffffff',actorBkg:'#edf3f8',actorBorder:'#41566d',actorTextColor:'#14273b',signalColor:'#41566d',signalTextColor:'#14273b',noteBkgColor:'#fff8ea',noteBorderColor:'#a17a35',noteTextColor:'#392b16'},
        flowchart:{htmlLabels:true,curve:'linear',nodeSpacing:18,rankSpacing:18,padding:9,useMaxWidth:false,wrappingWidth:330},
        sequence:{useMaxWidth:false,actorMargin:25,width:145,height:55,boxMargin:8,boxTextMargin:7,noteMargin:12,messageMargin:30,mirrorActors:false,wrap:true,wrapPadding:10}
      });
      const {svg}=await window.mermaid.render(name,source);
      document.body.innerHTML=svg;
      const el=document.querySelector('svg');
      el.style.maxWidth='none';
      el.style.background='white';
      return el.outerHTML;
    },{source,name});
    fs.writeFileSync(path.join(root,name+'.svg'),svg);
    const locator=page.locator('svg');
    const box=await locator.boundingBox();
    await locator.screenshot({path:path.join(root,name+'.png'),scale:'device'});
    manifest.push({name,...box,source:name+'.mmd',svg:name+'.svg',png:name+'.png'});
  }
  const heartbeat=manifest.find(x=>x.name==='figure_3_3_heartbeat_panel');
  const threat=manifest.find(x=>x.name==='figure_3_3_threat_panel');
  const hbSvg=fs.readFileSync(path.join(root,heartbeat.svg),'utf8');
  const thSvg=fs.readFileSync(path.join(root,threat.svg),'utf8');
  const pad=16, gap=28, heading=54;
  const width=Math.ceil(heartbeat.width+threat.width+pad*2+gap);
  const height=Math.ceil(Math.max(heartbeat.height,threat.height+340)+heading+pad);
  const rightX=pad+heartbeat.width+gap;
  const noteY=heading+threat.height+28;
  const nested=(svg,x,y)=>svg.replace('<svg ',`<svg x="${x}" y="${y}" `);
  const composite=`<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${height}" viewBox="0 0 ${width} ${height}">
    <rect width="100%" height="100%" fill="white"/>
    <text x="${pad+heartbeat.width/2}" y="28" text-anchor="middle" font-family="Arial" font-size="22" font-weight="bold" fill="#15283b">Scheduled heartbeat</text>
    <text x="${rightX+threat.width/2}" y="28" text-anchor="middle" font-family="Arial" font-size="22" font-weight="bold" fill="#15283b">Operator-approved threat response</text>
    ${nested(hbSvg,pad,heading)}
    ${nested(thSvg,rightX,heading)}
    <rect x="${rightX+8}" y="${noteY}" width="${threat.width-16}" height="340" rx="8" fill="#fff8ea" stroke="#a17a35"/>
    <text x="${rightX+26}" y="${noteY+32}" font-family="Arial" font-size="18" fill="#392b16">
      <tspan font-weight="bold">Control and failure boundaries</tspan>
      <tspan x="${rightX+26}" dy="32">Stored verdicts support operator review.</tspan>
      <tspan x="${rightX+26}" dy="27">Acknowledgements change presentation.</tspan>
      <tspan x="${rightX+26}" dy="27">Service remediation remains manual.</tspan>
      <tspan x="${rightX+26}" dy="38">Notification errors are retained results;</tspan>
      <tspan x="${rightX+26}" dy="27">the graph can still return for storage.</tspan>
      <tspan x="${rightX+26}" dy="38">Unhandled cycle exception:</tspan>
      <tspan x="${rightX+26}" dy="27">log failure and wait.</tspan>
      <tspan x="${rightX+26}" dy="27">Persistence is not guaranteed.</tspan>
    </text>
  </svg>`;
  fs.writeFileSync(path.join(root,'figure_3_3_corrected.svg'),composite);
  await page.setContent('<html><body style="margin:0;background:white">'+composite+'</body></html>');
  await page.locator('svg').first().screenshot({path:path.join(root,'figure_3_3_corrected.png'),scale:'device'});
  manifest.push({name:'figure_3_3_corrected',width,height,sources:['figure_3_3_heartbeat_panel.mmd','figure_3_3_threat_panel.mmd'],svg:'figure_3_3_corrected.svg',png:'figure_3_3_corrected.png'});
  fs.writeFileSync(path.join(root,'technical_figures_manifest.json'),JSON.stringify(manifest,null,2));
  console.log(JSON.stringify(manifest));
  await browser.close();
})().catch(e=>{console.error(e);process.exit(1);});
