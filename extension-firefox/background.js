const api = globalThis.browser ?? globalThis.chrome;
let port;
let state = {phase:'idle'};
const save = () => api.storage.local.set({state});
function connectionFailure(message) {
 state={phase:'error',setupRequired:true,message:'Download helper unavailable: '+message};save();
}
api.runtime.onMessage.addListener((msg, sender, reply) => {
 if(msg.type==='open'){api.action.openPopup().catch(()=>{});return;}
 if(sender.tab)return;
 if(msg.type==='state'){reply({...state,active:!!port});return;}
 if(!['inspect','download','cancel'].includes(msg.type))return;
 if(msg.type==='cancel'){
  const previous=port;port=null;previous?.disconnect();
  state={phase:'cancelled',message:'Cancelled. Partial files may remain.'};save();reply({ok:true});return;
 }
 if(port){reply({error:'A task is already running.'});return;}
 state={phase:msg.type==='inspect'?'inspecting':'downloading',message:msg.type==='inspect'?'Finding available formats…':'Starting download…',setupRequired:false};save();
 try{
  const current=api.runtime.connectNative('com.framedrop.helper');port=current;
  current.onMessage.addListener(data=>{if(port!==current)return;state={...state,...data};save();});
  current.onDisconnect.addListener(()=>{
   const error=current.error?.message || api.runtime.lastError?.message;
   if(port!==current)return;
   port=null;
   if(!['ready','complete','error'].includes(state.phase))connectionFailure(error||'The helper exited before replying. Run the setup check in the package.');
  });
  current.postMessage(msg);reply({ok:true});
 }catch(error){const previous=port;port=null;previous?.disconnect();connectionFailure(error.message);reply({error:state.message});}
});
