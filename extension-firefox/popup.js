const api = globalThis.browser ?? globalThis.chrome;
const $=id=>document.getElementById(id);
let info=null,mode='video',url=null,busy=false,lastPhase=null;
const selected={video:null,audio:'320'};
const reduced=matchMedia('(prefers-reduced-motion: reduce)');
let motionEnabled=true;
function updateMotion(){document.body.classList.toggle('motion-off',!motionEnabled||reduced.matches);$('motionToggle').textContent=reduced.matches?'Motion off · system preference':motionEnabled?'Motion on':'Motion off';$('motionToggle').setAttribute('aria-pressed',String(motionEnabled&&!reduced.matches));}
reduced.addEventListener('change',updateMotion);
$('motionToggle').onclick=()=>{motionEnabled=!motionEnabled;updateMotion();api.storage.local.set({motionEnabled});};
api.storage.local.get('motionEnabled').then(x=>{motionEnabled=x.motionEnabled!==false;updateMotion();});
updateMotion();
$('extensionId').textContent=api.runtime.id;
function options(){
 const select=$('quality');select.replaceChildren();
 const choices=mode==='audio'?[{id:'320',label:'320 kbps · MP3'},{id:'192',label:'192 kbps · MP3'},{id:'128',label:'128 kbps · MP3'}]:(info?.formats||[]);
 if(!choices.length){const o=document.createElement('option');o.textContent=busy?'Finding formats…':info?'No video formats exposed':'Connect helper to load qualities';select.append(o);}
 for(const f of choices){const o=document.createElement('option');o.value=f.id;o.textContent=f.label;select.append(o);}
 if(choices.some(f=>f.id===selected[mode]))select.value=selected[mode];
 select.disabled=busy||!info||!choices.length;
 $('download').disabled=busy||!info||!choices.length;
 $('download').textContent=mode==='audio'?'✦   Download MP3   ↓':'✦   Download video   ↓';
 $('hint').textContent=mode==='audio'?'Converted locally. A higher bitrate cannot improve the source.':'Video includes audio. Original codecs are preserved.';
}
function render(s){
 document.body.dataset.phase=s.phase;
 if(s.setupRequired)$('setup').open=true;
 $('heroArrow').textContent=s.phase==='complete'?'✓':s.phase==='processing'?'↻':'↓';
 if(s.phase==='complete'&&['downloading','processing'].includes(lastPhase)){const hero=document.querySelector('.hero');hero.classList.add('celebrate');setTimeout(()=>hero.classList.remove('celebrate'),900);}
 lastPhase=s.phase;
 busy=['inspecting','downloading','processing'].includes(s.phase);$('status').textContent=s.message||s.phase;
 $('cancel').hidden=!busy;$('refresh').disabled=busy;
 $('progress').hidden=!busy;if(typeof s.percent==='number')$('progress').value=s.percent;else $('progress').removeAttribute('value');
 if(s.info?.url===url){info=s.info;$('title').textContent=info.title;}
 options();}
async function send(msg){try{const r=await api.runtime.sendMessage(msg);if(r?.error)$('status').textContent=r.error;}catch(e){$('status').textContent=e.message;}}
async function inspect(){if(!url){$('status').textContent='Open a YouTube watch page or Short, then reopen FrameDrop.';return;}info=null;options();await send({type:'inspect',url});}
for(const m of ['video','audio'])$(m).onclick=()=>{mode=m;document.body.dataset.mode=m;for(const n of ['video','audio'])$(n).setAttribute('aria-pressed',String(n===m));options();};
$('quality').onchange=()=>{selected[mode]=$('quality').value;const q=$('quality');q.classList.remove('quality-picked');void q.offsetWidth;q.classList.add('quality-picked');};
$('refresh').onclick=inspect;$('cancel').onclick=()=>send({type:'cancel'});
$('download').onclick=()=>send({type:'download',url,mode,format:$('quality').value});
api.storage.onChanged.addListener(c=>{if(c.state)render(c.state.newValue);});
(async()=>{const [tab]=await api.tabs.query({active:true,currentWindow:true});try{const u=new URL(tab.url);if(u.hostname==='www.youtube.com'&&(u.pathname==='/watch'||u.pathname.startsWith('/shorts/'))){url=u.href;$('title').textContent=tab.title?.replace(/ - YouTube$/, '')||'YouTube video detected';}}catch{}
const state=await api.runtime.sendMessage({type:'state'});if(state)render(state);if(!state?.active&&!(info&&info.url===url))await inspect();})();
