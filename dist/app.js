const articles=[...document.querySelectorAll('.article')];
const tabs=[...document.querySelectorAll('[data-tab]')];
let active=0,observer;
const toast=document.querySelector('.toast');
let toastTimer;
function notify(message){toast.textContent=message;toast.hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>toast.hidden=true,2300);}
function showArticle(index,scroll=true){
  active=index;
  document.querySelectorAll('video').forEach(v=>v.pause());
  articles.forEach((a,i)=>a.hidden=i!==index);
  tabs.forEach((t,i)=>{t.setAttribute('aria-selected',String(i===index));t.tabIndex=i===index?0:-1;});
  document.body.classList.toggle('second',articles[index].id==='article-2');
  document.body.classList.toggle('third',articles[index].id==='article-3');
  document.title=articles[index].querySelector('h1').textContent.replace(/\s+/g,' ').trim()+' · Open-HumanScale';
  const headings=[...articles[index].querySelectorAll('h2')];
  document.querySelector('.toc').replaceChildren(...headings.map(h=>{const a=document.createElement('a');a.href='#'+h.parentElement.id;a.textContent=h.textContent.replace(/^\d{2}/,'');return a;}));
  if(observer)observer.disconnect();
  observer=new IntersectionObserver(entries=>{for(const e of entries)if(e.isIntersecting){document.querySelectorAll('.toc a').forEach(a=>a.classList.toggle('active',a.hash==='#'+e.target.id));}},{rootMargin:'-100px 0px -55% 0px',threshold:0});
  articles[index].querySelectorAll('section').forEach(s=>observer.observe(s));
  const reading=articles[index].querySelector('.prose').cloneNode(true);
  reading.querySelectorAll('details,.benchmark-motion,.pair-actions,video').forEach(e=>e.remove());
  const count=reading.textContent.replace(/\s/g,'').length;
  document.querySelector('#reading-meta').textContent=`约 ${Math.round(count/100)*100} 字 · ${Math.ceil(count/450)} 分钟阅读`;
  document.querySelector('.download').href=articles[index].dataset.download||`article-${String(index+1).padStart(2,'0')}.txt`;
  if(scroll)window.scrollTo({top:0,behavior:'instant'});
  progress();
}
function navigate(index){history.pushState(null,'','#'+articles[index].id);showArticle(index);}
tabs.forEach((t,i)=>{t.addEventListener('click',()=>navigate(i));t.addEventListener('keydown',e=>{if(['ArrowLeft','ArrowRight','Home','End'].includes(e.key)){e.preventDefault();const next=e.key==='Home'?0:e.key==='End'?articles.length-1:(active+(e.key==='ArrowRight'?1:-1)+articles.length)%articles.length;navigate(next);tabs[next].focus();}});});
document.querySelectorAll('[data-next]').forEach(b=>b.addEventListener('click',()=>navigate(Number(b.dataset.next))));
document.querySelector('#phone-toggle').addEventListener('click',e=>{const on=document.body.classList.toggle('phone-mode');e.currentTarget.setAttribute('aria-pressed',String(on));e.currentTarget.textContent=on?'桌面阅读':'手机预览';});
document.querySelector('#copy').addEventListener('click',async()=>{
  const clone=articles[active].cloneNode(true);clone.querySelectorAll('.article-end,video,.zoom,.paired-demo,.demo-section,.benchmark-motion').forEach(e=>e.remove());
  const text=clone.innerText||clone.textContent;
  try{await navigator.clipboard.writeText(text.replace(/\n{3,}/g,'\n\n'));notify('正文已复制');}
  catch{const a=document.createElement('textarea');a.value=text;document.body.append(a);a.select();const ok=document.execCommand('copy');a.remove();notify(ok?'正文已复制':'请点击左侧“下载文稿”获取正文');}
});
const dialog=document.querySelector('#image-dialog');
document.querySelectorAll('[data-image]').forEach(b=>b.addEventListener('click',()=>{const img=dialog.querySelector('img');img.src=b.dataset.image;img.alt=b.querySelector('img').alt;dialog.querySelector('#image-caption').textContent=img.alt;dialog.showModal();document.body.classList.add('modal-open');}));
dialog.querySelector('button').addEventListener('click',()=>dialog.close());
dialog.addEventListener('click',e=>{if(e.target===dialog)dialog.close();});
dialog.addEventListener('close',()=>document.body.classList.remove('modal-open'));
function progress(){const max=document.documentElement.scrollHeight-innerHeight;document.querySelector('.reading-progress').style.width=(max>0?Math.min(100,scrollY/max*100):0)+'%';}
addEventListener('scroll',progress,{passive:true});addEventListener('resize',progress);
function articleFromHash(){const target=document.getElementById(location.hash.slice(1));return target?articles.indexOf(target.closest('.article')):-1;}
addEventListener('hashchange',()=>{const index=articleFromHash();if(index<0)return;if(index!==active)showArticle(index,false);if(location.hash==='#'+articles[index].id)showArticle(index);});
document.querySelectorAll('.paired-demo').forEach(group=>{
  const play=group.querySelector('[data-play-pair],#play-pair');
  const pause=group.querySelector('[data-pause-pair],#pause-pair');
  play?.addEventListener('click',async()=>{
    const videos=[...group.querySelectorAll('video')];
    const results=await Promise.allSettled(videos.map(v=>{v.currentTime=0;return v.play();}));
    play.textContent='重新播放对照';
    if(results.some(r=>r.status==='rejected'))notify('请使用视频下方的播放按钮');
  });
  pause?.addEventListener('click',()=>group.querySelectorAll('video').forEach(v=>v.pause()));
});
document.addEventListener('play',e=>{if(e.target.tagName==='VIDEO'){const pair=e.target.closest('.paired-demo');document.querySelectorAll('video').forEach(v=>{if(v!==e.target&&(!pair||!pair.contains(v)))v.pause();});}},true);
showArticle(Math.max(0,articleFromHash()),false);

// Only the opening montage previews automatically; other demos remain user controlled.
if(!matchMedia('(prefers-reduced-motion: reduce)').matches){
  const montageObserver=new IntersectionObserver(entries=>{
    for(const entry of entries){
      const video=entry.target;
      if(entry.isIntersecting&&!video.closest('[hidden]'))video.play().catch(()=>{});
      else video.pause();
    }
  },{threshold:.2});
  document.querySelectorAll('[data-montage-preview]').forEach(video=>montageObserver.observe(video));
}
