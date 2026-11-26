import puppeteer from 'puppeteer-core'; import http from 'http'; import fs from 'fs'; import path from 'path';
const [,, w, h, fps, start, end, outdir, ...rest] = process.argv;
const timing = fs.existsSync('timing.json') ? JSON.parse(fs.readFileSync('timing.json')) : {};
const root=path.resolve('.'); const port = 8800 + Math.floor(Math.random()*100);
const server=http.createServer((q,s)=>{const p=path.join(root,decodeURIComponent(q.url.split('?')[0])); if(!fs.existsSync(p)){s.writeHead(404);return s.end();} const e=path.extname(p); s.writeHead(200,{'Content-Type':e==='.html'?'text/html':e==='.js'?'text/javascript':'application/octet-stream'}); fs.createReadStream(p).pipe(s);}).listen(port);
const b=await puppeteer.launch({executablePath:'/usr/bin/google-chrome',headless:'new',protocolTimeout:900000,args:['--no-sandbox','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const p=await b.newPage(); p.on('pageerror',e=>console.log('ERR',e.message));
await p.setViewport({width:+w,height:+h});
await p.goto(`http://localhost:${port}/real.html?w=${w}&h=${h}`); await p.waitForFunction('window.ready===true',{timeout:300000});
await p.evaluate(o=>window.setTiming(o), timing);
fs.mkdirSync(outdir,{recursive:true});
const times = rest.length ? rest.map(Number) : null;
const list = times || Array.from({length: Math.round((+end - +start) * +fps)}, (_, i) => +start + i / +fps);
let t0 = Date.now();
for (const t of list) {
  const name = times ? `t_${t}.jpg` : `f${String(Math.round(t * +fps)).padStart(5,'0')}.jpg`;
  if (fs.existsSync(path.join(outdir, name))) continue;
  await p.evaluate(t=>window.renderFrame(t), t);
  const d = await p.evaluate(()=>window.grab());
  fs.writeFileSync(path.join(outdir, name), Buffer.from(d.split(',')[1], 'base64'));
}
console.log('done', list.length, 'frames', ((Date.now()-t0)/1000).toFixed(1)+'s');
await b.close(); server.close();
