import assert from 'node:assert/strict';
import { queryAll } from '../content/examples/notion-query.mjs';
const ok = (results, next = null) => ({status:200, body:{results,has_more:next!==null,next_cursor:next}});
function mock(sequence) {
  const calls=[], waits=[];
  return {calls, waits, options:{random:()=>0,sleep:async ms=>waits.push(ms),
    fetchImpl:async (url,opts)=>{
      calls.push({url,...opts,body:JSON.parse(opts.body)});
      assert.ok(sequence.length,'unexpected extra request');
      const s=sequence.shift();
      return {ok:s.status===200,status:s.status,headers:new Headers(s.headers??{}),json:async()=>s.body};
    }}};
}
let m=mock([{status:429,headers:{'Retry-After':'90'},body:{code:'rate_limited'}},
 ok(Array.from({length:100},(_,i)=>i),'cursor2'),ok([100])]);
assert.equal((await queryAll('source-id','test',m.options)).length,101);
assert.equal(m.waits[0],90000);
assert.deepEqual(m.calls[0].body,m.calls[1].body);
assert.equal(m.calls[2].body.start_cursor,'cursor2');
assert.match(m.calls[0].url,/\/data_sources\/source-id\/query$/);
assert.equal(m.calls[0].headers['Notion-Version'],'2026-03-11');
m=mock([{status:529,body:{code:'service_overload'}},ok([])]);
await queryAll('id','test',m.options);assert.equal(m.waits[0],1000);
for(const status of [400,401,403,404,500]){
 m=mock([{status,body:{code:'permanent'}}]);
 await assert.rejects(queryAll('id','test',m.options),new RegExp('HTTP '+status));
 assert.equal(m.calls.length,1);assert.equal(m.waits.length,0);
}
m=mock([{status:429,body:{additional_data:{rate_limit_reason:'public_api_request_blocked'}}}]);
await assert.rejects(queryAll('id','test',m.options));assert.equal(m.calls.length,1);
m=mock(Array.from({length:5},()=>({status:429,body:{code:'rate_limited'}})));
await assert.rejects(queryAll('id','test',m.options));assert.equal(m.calls.length,5);
m=mock([{status:529,headers:{'Retry-After':'600'},body:{}}]);
await assert.rejects(queryAll('id','test',m.options),/reschedule/);assert.equal(m.waits.length,0);
m=mock([ok([1],'x'),ok([2],'x')]);
await assert.rejects(queryAll('id','test',m.options),/cursor/);
m=mock([ok([1],'x')]);
await assert.rejects(queryAll('id','test',{...m.options,maxPages:1}),/Page limit/);
console.log('Notion mock retry/pagination tests passed');

m=mock([{status:200,body:{results:[],has_more:false,request_status:{type:'incomplete'}}}]);
await assert.rejects(queryAll('id','test',m.options),/10,000/);
