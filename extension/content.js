const api = globalThis.browser ?? globalThis.chrome;
(() => {
 const update=()=>{
  let button=document.getElementById('framedrop-launch');
  const valid=location.pathname==='/watch'||location.pathname.startsWith('/shorts/');
  if(!valid){button?.remove();return;}
  if(button)return;
  button=document.createElement('button');button.id='framedrop-launch';button.textContent='✦ FrameDrop';button.title='Open video and MP3 downloader';
  button.style.cssText='position:fixed;right:24px;bottom:24px;z-index:2147483647;background:#fffaf5;color:#171514;border:1.5px solid #171514;border-radius:30px;padding:13px 20px;font:bold 14px system-ui;cursor:pointer;box-shadow:3px 3px 0 #171514';
  button.onclick=()=>api.runtime.sendMessage({type:'open'});document.documentElement.append(button);
 }; document.addEventListener('yt-navigate-finish',update);update();
})();
