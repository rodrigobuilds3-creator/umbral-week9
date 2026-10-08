import {rm,mkdir,cp,copyFile} from 'node:fs/promises';
await rm('dist',{recursive:true,force:true});
await mkdir('dist/server',{recursive:true});
await cp('src/public','dist/client',{recursive:true});
await copyFile('src/worker.mjs','dist/server/index.js');
console.log('Built Worker and browser assets in dist/');
