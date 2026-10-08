const json=(body,status=200)=>new Response(JSON.stringify(body),{status,headers:{'Content-Type':'application/json; charset=utf-8','Cache-Control':'no-store','X-Content-Type-Options':'nosniff'}});
const quotas=new Map();
const configured=env=>!!env.GEMINI_API_KEY;
const prompt='Redacta en español una instrucción breve (máximo 160 palabras) para una tarea FICTICIA de conciliación de caja. Apertura 500, ventas en efectivo 1890, devolución en efectivo 120, gastos 250 y depósito 1000. El candidato explica su procedimiento y después revisa una condición: la devolución fue a tarjeta. NO des el resultado aritmético. Un humano revisa cuatro criterios: trazar movimientos, identificar evidencia contradictoria, explicar el cambio y declarar supuestos/asistencia IA. Permite explicación escrita con preguntas posteriores como alternativa accesible. Es una evaluación acotada, gratis para el candidato, sin producción para clientes. No evalúes candidatos ni prometas identidad, capacidad general, empleo o certificación. Devuelve solo la instrucción, sin Markdown.';
export async function handleDraft(request,env,fetcher=fetch){
 if(request.method!=='POST')return json({error:'METHOD',message:'Usa la acción de redacción de la app.'},405);
 const origin=request.headers.get('origin');if(origin&&origin!==new URL(request.url).origin)return json({error:'ORIGIN',message:'Solicitud no permitida.'},403);
 let v;try{const body=await request.text();if(body.length>2000)return json({error:'SIZE',message:'La solicitud excede el alcance permitido.'},413);v=JSON.parse(body);}catch{return json({error:'INPUT',message:'Solicitud inválida.'},400);}
 if(!v||v.taskId!=='cash-v1'||!['written','standard'].includes(v.accommodation)||Object.keys(v).some(k=>!['taskId','accommodation'].includes(k)))return json({error:'SCOPE',message:'La IA solo puede redactar la plantilla ficticia. No envíes respuestas ni datos personales.'},400);
 if(!configured(env))return json({error:'AI_UNAVAILABLE',message:'La asistencia con IA todavía no está configurada. Puedes usar la plantilla revisada.'},503);
 const ip=request.headers.get('CF-Connecting-IP')||'local',now=Date.now(),q=quotas.get(ip);if(q&&q.until>now&&q.count>=8)return json({error:'RATE',message:'Límite temporal alcanzado. Usa la plantilla revisada.'},429);quotas.set(ip,{count:q&&q.until>now?q.count+1:1,until:q&&q.until>now?q.until:now+3600000});if(quotas.size>1000)for(const [key,val]of quotas)if(val.until<now)quotas.delete(key);
 const model=/^[a-zA-Z0-9.-]{1,80}$/.test(env.GEMINI_MODEL||'')?env.GEMINI_MODEL:'gemini-3.5-flash-lite';
 const generationConfig={temperature:model.startsWith('gemini-3')?1:0.2,maxOutputTokens:1024};
 if(/^gemini-2\.5-flash(?:-lite)?$/.test(model))generationConfig.thinkingConfig={thinkingBudget:0};
 else if(/^gemini-3\.(?:1|5)-flash-lite$/.test(model))generationConfig.thinkingConfig={thinkingLevel:'minimal'};
 else if(model.startsWith('gemini-3'))generationConfig.thinkingConfig={thinkingLevel:'low'};
 try{
  const upstream=await fetcher(`https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent`,{method:'POST',headers:{'Content-Type':'application/json','x-goog-api-key':env.GEMINI_API_KEY},body:JSON.stringify({system_instruction:{parts:[{text:prompt}]},contents:[{role:'user',parts:[{text:v.accommodation==='written'?'Ofrece explícitamente una alternativa escrita.':'Usa la instrucción estándar.'}]}],generationConfig}),signal:AbortSignal.timeout(15000)});
  if(!upstream.ok){console.warn('Gemini scope request failed',{status:upstream.status});if(upstream.status===429)return json({error:'AI_QUOTA',message:'Gemini alcanzó su cuota temporal. Puedes seguir con la plantilla revisada.'},429);throw new Error('provider');}
  const data=await upstream.json(),candidate=data.candidates?.[0];
  const scope=(candidate?.content?.parts||[]).filter(p=>!p.thought&&typeof p.text==='string').map(p=>p.text).join('').trim();
  if(candidate?.finishReason!=='STOP'||!scope||scope.length>1200)throw new Error('format');
  return json({scope,provider:'Gemini',model,grounding:'cash-v1 / 1.0',purpose:'Routine scope wording only; not assessment.'});
 }catch{return json({error:'PROVIDER',message:'La IA no pudo responder. Puedes seguir con la plantilla revisada.'},502);}
}
export default {async fetch(request,env){const url=new URL(request.url);if(url.pathname==='/api/status')return json({llmConfigured:configured(env),provider:configured(env)?'Gemini':null,mode:'fictional-demo'});if(url.pathname==='/api/draft')return handleDraft(request,env);const response=await env.ASSETS.fetch(request);const headers=new Headers(response.headers);headers.set('X-Content-Type-Options','nosniff');headers.set('Referrer-Policy','no-referrer');return new Response(response.body,{status:response.status,headers});}};
