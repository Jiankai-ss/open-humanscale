'use strict';
const $=(s,root=document)=>root.querySelector(s);
const $$=(s,root=document)=>[...root.querySelectorAll(s)];
const toast=$('.toast');let timer;
function announce(message){toast.textContent=message;toast.hidden=false;clearTimeout(timer);timer=setTimeout(()=>toast.hidden=true,3500);}
const dialog=$('#figure-dialog');
$$('[data-image]').forEach(button=>button.addEventListener('click',()=>{
 const image=$('img',button);$('img',dialog).src=button.dataset.image;$('img',dialog).alt=image?.alt||'研究配图';
 $('#figure-caption').textContent=image?.alt||'研究配图';dialog.showModal();document.body.classList.add('modal-open');
}));
$('[data-close]').addEventListener('click',()=>dialog.close());
dialog.addEventListener('click',e=>{if(e.target===dialog)dialog.close();});
dialog.addEventListener('close',()=>document.body.classList.remove('modal-open'));
$$('.goal-pair').forEach(group=>{
 const films=$$('video',group),button=$('[data-play-pair]',group),status=$('.pair-status',group);
 button.addEventListener('click',async()=>{
  $$('video').forEach(v=>{if(!films.includes(v))v.pause();});
  films.forEach(v=>{v.muted=true;v.currentTime=0;});
  button.disabled=true;
  const outcomes=await Promise.allSettled(films.map(v=>v.play()));
  button.disabled=false;status.textContent=outcomes.every(x=>x.status==='fulfilled')?'两段视频正在同时播放':'请点视频中的播放按钮继续';
 });
 $('[data-pause-pair]',group).addEventListener('click',()=>{films.forEach(v=>v.pause());status.textContent='已暂停';});
});
document.addEventListener('play',event=>{
 const current=event.target;if(current.tagName!=='VIDEO')return;
 const pair=current.closest('.goal-pair');
 $$('video').forEach(v=>{if(v!==current&&(!pair||!pair.contains(v)))v.pause();});
},true);
const hero=$('[data-hero]');let previewAttempted=false;
const visibility=new IntersectionObserver(entries=>entries.forEach(entry=>{
 const v=entry.target;
 if(!entry.isIntersecting){v.pause();return;}
 if(v===hero&&!previewAttempted&&!matchMedia('(prefers-reduced-motion: reduce)').matches&&!navigator.connection?.saveData&&!$$('video').some(other=>other!==v&&!other.paused)){
  previewAttempted=true;v.play().catch(()=>{});
 }
}),{threshold:.12});
$$('video').forEach(v=>visibility.observe(v));
document.addEventListener('visibilitychange',()=>{if(document.hidden)$$('video').forEach(v=>v.pause());});
const progress=$('.progress');let frame;
function updateProgress(){const extent=document.documentElement.scrollHeight-innerHeight;progress.style.width=(extent>0?100*scrollY/extent:0)+'%';}
addEventListener('scroll',()=>{if(frame)return;frame=requestAnimationFrame(()=>{updateProgress();frame=null;});},{passive:true});
addEventListener('resize',updateProgress);updateProgress();
const sectionObserver=new IntersectionObserver(entries=>entries.forEach(entry=>{if(entry.isIntersecting){$$('.nav-links a').forEach(a=>a.classList.toggle('active',a.hash==='#'+entry.target.id));}}),{rootMargin:'-20% 0px -60% 0px'});
$$('.chapter').forEach(section=>sectionObserver.observe(section));
$('[data-copy]').addEventListener('click',async()=>{
 const copy=$('#story').cloneNode(true);$$('button,video,.pair-controls,.bm-original-footer,.bm-reveal-layer,.bm-final-overlay',copy).forEach(e=>e.remove());
 const box=document.createElement('div');box.style.cssText='position:fixed;left:-100000px;width:700px;';box.append(copy);document.body.append(box);
 const text=copy.innerText;box.remove();
 try{await navigator.clipboard.writeText(text);announce('文稿已复制');}catch{announce('当前浏览器未允许复制，可点击右上角下载文稿。');}
});
