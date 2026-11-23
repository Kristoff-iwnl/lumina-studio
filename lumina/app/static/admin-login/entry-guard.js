document.documentElement.classList.add('entry-pending');
window.__entryFallback=setTimeout(function(){
  document.documentElement.classList.remove('entry-pending');
},3500);
