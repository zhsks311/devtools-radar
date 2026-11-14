import assert from 'node:assert/strict';
import { attemptEmail } from '../content/examples/resend-attempt.mjs';
const now=1000000000, row={key:'receipt/event-1/v1',firstAttemptAt:now,payload:{html:'immutable'}};
let calls=0, args;
const mock=response=>({emails:{send:async(...a)=>{calls++;args=a;return response}}});
assert.deepEqual(await attemptEmail(mock({data:{id:'accepted'}}),row,now),{acceptedId:'accepted'});
assert.deepEqual(args,[row.payload,{idempotencyKey:row.key}]);
calls=0;
await attemptEmail(mock({}),{...row,acceptedId:'known'},now+100000000);assert.equal(calls,0);
for(const firstAttemptAt of [now-86400000,now-86100000,NaN,now+1]){
 calls=0;await assert.rejects(attemptEmail(mock({}),{...row,firstAttemptAt},now),/reconcile_required/);assert.equal(calls,0);
}
for(const [name,message] of [['invalid_idempotent_request','payload_conflict'],['concurrent_idempotent_requests','in_progress'],['validation_error','send_failed']]){
 calls=0;await assert.rejects(attemptEmail(mock({error:{name,statusCode:409}}),row,now),new RegExp(message));assert.equal(calls,1);
}
await assert.rejects(attemptEmail({emails:{send:async()=>{throw Error('timeout')}}},row,now),/unknown_outcome/);
await assert.rejects(attemptEmail(mock({data:{}}),row,now),/unknown_outcome/);
console.log('Resend single-attempt safety tests passed');
