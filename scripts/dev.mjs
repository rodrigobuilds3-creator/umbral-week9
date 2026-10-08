import http from 'node:http';
import {readFile} from 'node:fs/promises';
import path from 'node:path';
import worker from '../src/worker.mjs';
const root=path.resolve('src/public');
const types={'.html':'text/html; charset=utf-8','.js':'text/javascript; charset=utf-8','.css':'text/css; charset=utf-8','.svg':'image/svg+xml'};
const asset=async request=>{try{let name=decodeURIComponent(new URL(request.url).pathname);if(name==='/')name='/index.html';const file=path.resolve(root,'.'+name);if(!file.startsWith(root+path.sep))return new Response('Not found',{status:404});return new Response(await readFile(file),{headers:{'Content-Type':types[path.extname(file)]||'application/octet-stream'}});}catch{return new Response('Not found',{status:404});}};
const server=http.createServer(async(req,res)=>{try{const chunks=[];for await(const chunk of req)chunks.push(chunk);const request=new Request(`http://127.0.0.1:4179${req.url}`,{method:req.method,headers:req.headers,...(!['GET','HEAD'].includes(req.method)?{body:Buffer.concat(chunks)}:{})});const response=await worker.fetch(request,{...process.env,ASSETS:{fetch:asset}});res.writeHead(response.status,Object.fromEntries(response.headers));res.end(Buffer.from(await response.arrayBuffer()));}catch{res.writeHead(500);res.end('Server error');}});
server.listen(4179,'127.0.0.1',()=>console.log('Umbral preview: http://127.0.0.1:4179'));
