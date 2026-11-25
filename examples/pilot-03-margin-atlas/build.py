from pathlib import Path
from html import escape
root=Path(__file__).parent
site=root/'site'
assets=site/'assets'; assets.mkdir(parents=True,exist_ok=True)
navs=[('index.html','Home'),('journal.html','Journal'),('about.html','About')]

def header(active):
    links=''.join(f'<a href="{href}"'+(' aria-current="page"' if href==active else '')+f'>{name}</a>' for href,name in navs)
    return f'''<a class="skip" href="#main">Skip to content</a>
<header class="site-header"><div class="header-inner">
  <a href="index.html" class="brand" aria-label="Margin Atlas — home"><span class="brand-mark" aria-hidden="true">M<span>·</span>A</span><span class="brand-name">Margin Atlas<small>A journal of ordinary places</small></span></a>
  <button class="menu-toggle" type="button" aria-controls="primary-menu" aria-expanded="false" aria-label="Open navigation"><span aria-hidden="true">☰</span></button>
  <nav id="primary-menu" aria-label="Primary navigation" class="nav-list">{links}</nav>
</div></header>'''

def footer():
    return '''<footer class="site-footer"><div class="footer-grid"><div><div class="foot-brand">Margin Atlas<span class="gold-dot">.</span></div><p>An independent fictional editorial demo about looking closely at everyday public spaces.</p></div><div class="footer-links"><p class="eyebrow">Explore</p><a href="journal.html">Read the journal</a><a href="about.html">About this project</a><a href="index.html">Return home</a></div></div><div class="footer-bottom"><span>Fictional demonstration • no advertising, tracking or submissions</span><span>Made for the SearchReady Skill quality pilot</span></div></footer>'''

def html_page(slug,title,description,content,active=None):
    return f'''<!doctype html><html lang="en" class="no-js"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)}</title><meta name="description" content="{escape(description,quote=True)}">
<meta name="robots" content="noindex, nofollow"><meta name="color-scheme" content="light">
<link rel="icon" type="image/svg+xml" href="assets/mark.svg"><link rel="stylesheet" href="assets/site.css"><script src="assets/site.js" defer></script>
</head><body>{header(active)}<main id="main" tabindex="-1">{content}</main>{footer()}</body></html>'''

def story_card(href,num,category,time,title,abstract):
    return f'''<article class="story-card" data-search="{escape((title+' '+category+' '+abstract).lower(),quote=True)}"><div class="story-topline"><span>{num} / {category}</span><span>{time}</span></div><h3><a href="{href}">{title}<span class="card-arrow" aria-hidden="true">↗</span></a></h3><p>{abstract}</p><span class="read-cue" aria-hidden="true">READ FIELD NOTE →</span></article>'''

card1=story_card('the-art-of-noticing.html','01','OBSERVATION','2 MIN READ','The art of noticing a street','A practical invitation to see the details that make a familiar route feel different.')
card2=story_card('a-bench-is-a-small-promise.html','02','PUBLIC LIFE','2 MIN READ','A bench is a small public promise','What a place to sit says about rest, belonging, and the pace of a city.')

home='''<section class="hero"><div class="hero-copy"><span class="edition">ISSUE NO. 001 <span aria-hidden="true">/</span> THE EVERYDAY CITY</span><h1>Look closer.<br><em>There is more</em><br>to the ordinary.</h1><p class="hero-intro">Short, curious field notes about the spaces we move through without thinking—from a quiet corner to a bench at the edge of a busy street.</p><a class="primary-link" href="journal.html">Explore the journal <span aria-hidden="true">↗</span></a><div class="hero-stamp">INDEPENDENT<br>EDITORIAL<br>DEMO <span aria-hidden="true">✳</span></div></div><div class="hero-art"><div class="art-label"><span>FIG. 01</span><span>THE SHAPE OF ATTENTION</span></div><img src="assets/field-map.svg" width="780" height="850" alt="Abstract illustrated neighborhood plan with buildings, pathways and small trees"><div class="art-bottom"><span>MAP IS ILLUSTRATIVE, NOT GEOGRAPHIC</span><span>40° / ∞</span></div></div></section>
<section class="lede-band" aria-label="Editorial premise"><span class="section-number">THE PREMISE / 01</span><p>A city is not just what gets built. It is what gets <em>noticed.</em></p></section>
<section class="content-wrap feature-section"><div class="section-bar"><div><span class="eyebrow">FROM THE JOURNAL</span><h2>Two ways of seeing</h2></div><a class="text-link" href="journal.html">All field notes <span aria-hidden="true">↗</span></a></div><div class="story-grid">'''+card1+card2+'''</div></section>
<section class="editorial-quote"><div class="quote-inner"><span class="eyebrow">A NOTE ON THIS PROJECT</span><p>Not a guide to the best places. A reason to pay more attention to the places already around us.</p><a class="outline-link" href="about.html">How Margin Atlas works <span aria-hidden="true">↗</span></a></div></section>'''

journal='''<section class="page-head content-wrap"><span class="eyebrow">THE INDEX / VOL. 01</span><h1>Field notes, <em>in public.</em></h1><p class="page-intro">Writing about streets, small spaces, and the decisions that shape daily life. Start anywhere; every article stands on its own.</p></section>
<section class="content-wrap journal-section"><div class="journal-tools"><label for="filter-notes">Find a note</label><div class="search-wrap"><input id="filter-notes" type="search" placeholder="Search titles and themes" autocomplete="off" aria-describedby="filter-help"><span class="search-icon" aria-hidden="true">⌕</span></div><p id="filter-help" class="helper">Search filters the two notes below in your browser. It does not send your query anywhere.</p></div><h2 class="sr-only">Journal articles</h2><div id="journal-results" class="story-grid journal-results">'''+card1+card2+'''</div><p id="no-results" class="no-results" hidden>No matching notes. Try “street” or “bench”.</p><p id="result-status" class="sr-only" aria-live="polite" aria-atomic="true">2 notes shown</p></section>'''


def article_shell(kicker,title,intro,readtime,sections,next_href,next_label):
    parts=[]
    links=[]
    for anchor,heading,paragraphs in sections:
        links.append(f'<li><a href="#{anchor}">{heading}</a></li>')
        parts.append('<section class="article-section" id="'+anchor+'"><h2>'+heading+'</h2>'+''.join('<p>'+p+'</p>' for p in paragraphs)+'</section>')
    return f'''<div class="article-head"><div class="content-wrap"><a class="back-link" href="journal.html">← BACK TO JOURNAL</a><div class="article-type"><span>FIELD NOTE / {kicker}</span><span>{readtime}</span></div><h1>{title}</h1><p class="article-deck">{intro}</p></div></div><div class="article-layout content-wrap"><aside class="article-aside"><span class="eyebrow">IN THIS NOTE</span><nav aria-label="On this page"><ol>{''.join(links)}</ol></nav><span class="aside-note">An editorial demonstration. No external sources or fabricated expert credentials.</span></aside><article class="article-body">{''.join(parts)}<div class="article-end"><span>END OF FIELD NOTE</span><a href="{next_href}">NEXT: {next_label} ↗</a></div></article></div>'''

street=article_shell('OBSERVATION','The art of <em>noticing a street.</em>','A familiar route can become an unfamiliar story when you change what you pay attention to.','2 MIN READ',[
('look-up','Look above eye level',[
'The quickest way to change a walk is to stop looking only where your feet are going. Above the familiar signs and traffic lights sit smaller decisions: the rhythm of windows, the depth of a doorway, a tree leaning toward the light.',
'You do not need to name an architectural style to notice repetition. Try counting how many different materials meet along one block. Then ask which details have been repaired and which have been left alone.']),
('slow-down','Choose one ordinary corner',[
'A corner is a useful place to watch how people share space. The shop doorway, crossing, parked bicycle and bus stop may each claim a different kind of attention.',
'Instead of judging the place as beautiful or ugly, notice what it makes easy. Is there somewhere to wait without blocking a path? Can someone find their way without guessing? Is shade available when the pavement is hot?']),
('take-notes','Make a tiny field note',[
'Keep a record with three sentences: what you saw, what you wondered, and what you would look for next time. A good note is specific enough that another person could recognise the moment.',
'The aim is not to become an expert in one afternoon. It is to discover that the city you know contains details you have not yet met.'])],
'a-bench-is-a-small-promise.html','A bench is a small promise')

bench=article_shell('PUBLIC LIFE','A bench is a <em>small public promise.</em>','A place to sit can change the way a street welcomes people.','2 MIN READ',[
('beyond-seat','More than a seat',[
'A bench tells people that staying is allowed. It can turn a trip into a pause, offer a moment to someone carrying a heavy bag, or make room for a conversation that was not planned.',
'Of course, one bench cannot solve the problems of a public place. Its position, shade, visibility and approach all shape whether it feels useful.']),
('pause','Who gets to pause?',[
'Imagine arriving at the same square at different speeds: walking with a child, rolling a suitcase, using a mobility aid, or finding your way for the first time. A seat may be essential for one visitor and barely noticed by another.',
'That difference is a reminder that good public spaces should not assume everyone uses them in the same way.']),
('observation','One exercise for the next walk',[
'Look for a place to rest on your next familiar route. Where is it? What can you see from it? Could you reach it without climbing a step? What would make a short stay more comfortable?',
'Questions like these will not produce a complete design assessment. But they are a simple beginning: paying attention to how a public place treats the people moving through it.'])],
 'the-art-of-noticing.html','The art of noticing a street')

about='''<section class="page-head content-wrap about-head"><span class="eyebrow">ABOUT / THE PROJECT</span><h1>Curiosity is a <em>public practice.</em></h1><p class="page-intro">Margin Atlas is a fictional editorial publication created to demonstrate a content-first, search-aware website—not to present a real magazine or a credentialed urban-design authority.</p></section><section class="content-wrap about-grid"><div class="about-mark" aria-hidden="true">M<span>·</span>A</div><div class="about-copy"><h2>What belongs here?</h2><p>Short, original notes that begin with ordinary observations: a street corner, a bench, a threshold. Each piece is designed to be readable without registration, a mailing list, or external scripts.</p><p>The demo explores a different website model from a service-business homepage. Article headings, useful internal links, a journal index and lightweight reading interactions all matter here.</p><h2>What we will not claim</h2><p>We do not invent people, qualifications, reviews or location facts. The publication is fictional. This staging build is intentionally excluded from search indexing and has no production canonical URL.</p><a href="journal.html" class="primary-link">Start reading <span aria-hidden="true">↗</span></a></div></section>'''

pages={
'index.html':('Margin Atlas | An Editorial Journal About Everyday Places','An original fictional editorial journal exploring how to notice everyday streets, small public spaces, and the places we share.',home,'index.html'),
'journal.html':('The Journal | Margin Atlas Field Notes','Browse original field notes about everyday public spaces, streets and design observations in a simple, readable journal.',journal,'journal.html'),
'the-art-of-noticing.html':('The Art of Noticing a Street | Margin Atlas','A field note on discovering overlooked details along familiar streets, with a short observation exercise for your next walk.',street,'journal.html'),
'a-bench-is-a-small-promise.html':('A Bench Is a Small Public Promise | Margin Atlas','An editorial reflection on benches, rest and public belonging, with questions to notice on your next walk.',bench,'journal.html'),
'about.html':('About This Editorial Demo | Margin Atlas','Learn how Margin Atlas is designed as a fictional, content-first, SEO-aware publication without tracking or made-up credentials.',about,'about.html')}
# Force LF on every generated asset, including on Windows.
for slug,(t,d,body,active) in pages.items():
    (site/slug).write_text(html_page(slug,t,d,body,active),encoding='utf-8', newline='\n')

(assets/'mark.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="#233fba"/><path d="M12 46V18h7l13 16 13-16h7v28h-8V30L32 44 20 30v16z" fill="#fbfaf5"/></svg>''',encoding='utf-8', newline='\n')
(assets/'field-map.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 780 850" role="img"><title>Abstract city sketch</title><rect width="780" height="850" fill="#e6e3d6"/><g stroke="#b4b7ac" stroke-width="2"><path d="M0 210h780M0 555h780M215 0v850M510 0v850"/></g><g fill="#d1d5c4" stroke="#36504a" stroke-width="3"><rect x="33" y="34" width="148" height="136"/><rect x="266" y="46" width="192" height="121"/><rect x="554" y="35" width="197" height="135"/><rect x="27" y="263" width="155" height="237"/><rect x="256" y="262" width="209" height="239"/><rect x="550" y="258" width="194" height="256"/><rect x="30" y="603" width="146" height="206"/><rect x="258" y="601" width="210" height="208"/><rect x="547" y="593" width="199" height="219"/></g><g stroke="#36504a" stroke-width="2" fill="none"><path d="M63 59h85M63 89h85M63 118h85M292 78h139M292 108h139M292 138h139M585 72h126M585 102h126"/></g><path d="M0 574h200l38-46 272 0 24-24 246 0" fill="none" stroke="#304fc1" stroke-width="20" stroke-linecap="square"/><path d="M224 0v210l-10 30v257l-8 51v302" fill="none" stroke="#f4aa44" stroke-width="14"/><g fill="#315949" stroke="#315949"><circle cx="189" cy="188" r="25"/><circle cx="205" cy="205" r="17"/><circle cx="513" cy="235" r="21"/><circle cx="533" cy="246" r="17"/><circle cx="749" cy="544" r="24"/><circle cx="40" cy="564" r="18"/><circle cx="240" cy="836" r="18"/><circle cx="486" cy="587" r="21"/><circle cx="755" cy="212" r="15"/></g><g fill="#fdf9e8" font-family="Arial,sans-serif" font-size="24" font-weight="bold"><text x="68" y="435">BLOCK A</text><text x="295" y="426">BLOCK B</text><text x="594" y="434">BLOCK C</text></g><circle cx="370" cy="576" r="19" fill="#ec7d52" stroke="#15272d" stroke-width="5"/><path d="M370 575l-4-7m4 7 8-6" stroke="#15272d" stroke-width="4"/><g fill="#24323e" font-family="monospace" font-size="15"><text x="45" y="833">FIELD MAP / NOT TO SCALE</text><text x="592" y="833">01 — 05</text></g></svg>''',encoding='utf-8', newline='\n')

(assets/'site.js').write_text('''document.documentElement.classList.replace('no-js','js');
(() => {
  const button = document.querySelector('.menu-toggle');
  const menu = document.getElementById('primary-menu');
  if (button && menu) {
    const close = (returnFocus = false) => {
      if (button.getAttribute('aria-expanded') !== 'true') return;
      button.setAttribute('aria-expanded','false');
      button.setAttribute('aria-label','Open navigation');
      if (returnFocus) button.focus();
    };
    button.addEventListener('click', () => {
      const open = button.getAttribute('aria-expanded') === 'true';
      if (open) close();
      else {button.setAttribute('aria-expanded','true');button.setAttribute('aria-label','Close navigation');}
    });
    document.addEventListener('keydown', e => {if (e.key === 'Escape') close(true);});
    menu.addEventListener('click', e => {if(e.target.closest('a')) close();});
    window.addEventListener('resize', () => { if(window.innerWidth > 720) close(); });
  }
  const input=document.getElementById('filter-notes');
  if (input) {
    const cards=[...document.querySelectorAll('.story-card')];
    const empty=document.getElementById('no-results');
    const status=document.getElementById('result-status');
    input.addEventListener('input',()=>{
      const query=input.value.toLocaleLowerCase().trim();
      let count=0;
      cards.forEach(card=>{
        const match=card.dataset.search.includes(query);
        card.hidden=!match;
        if(match) count++;
      });
      empty.hidden=count>0;
      status.textContent=`${count} ${count===1?'note':'notes'} shown`;
    });
  }
})();
''',encoding='utf-8', newline='\n')

(assets/'site.css').write_text('''
:root{--paper:#fbfaf5;--ink:#22282c;--muted:#4e5b62;--blue:#233fba;--deep:#192b35;--gold:#ebaa49;--rule:#c7ccc7;--mist:#e3e8e5;--font-serif:Georgia,'Times New Roman',serif;--font-sans:system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--font-sans);line-height:1.62}img{display:block;max-width:100%;height:auto}a{color:inherit;text-decoration-thickness:1px;text-underline-offset:4px}button,input{font:inherit}button{cursor:pointer}p{margin:0 0 1.15em}h1,h2,h3{line-height:1.13}h1,h2,h3,blockquote{font-family:var(--font-serif);font-weight:normal}h1{letter-spacing:-.055em}em{font-weight:normal}a:focus-visible,button:focus-visible,input:focus-visible{outline:3px solid #233fba;outline-offset:4px}.site-footer a:focus-visible,.editorial-quote a:focus-visible{outline-color:#fff7e6}a:hover{text-decoration-thickness:2px}.skip{position:absolute;left:16px;top:-130px;background:#fff;padding:12px;z-index:99;color:#111}.skip:focus{top:10px} .sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}
.site-header{border-bottom:1px solid var(--rule)}.header-inner{max-width:1440px;margin:auto;padding:20px clamp(22px,5vw,76px);display:flex;align-items:center;justify-content:space-between;gap:24px}.brand{display:flex;gap:14px;align-items:center;text-decoration:none}.brand-mark,.about-mark{font-family:var(--font-serif);font-size:32px;letter-spacing:-.1em;font-weight:bold}.brand-mark span,.about-mark span{color:var(--blue)}.brand-name{font-family:var(--font-serif);font-size:22px;line-height:1.02;font-weight:bold;letter-spacing:-.035em}.brand-name small{display:block;font:normal 10px/1.5 var(--font-sans);text-transform:uppercase;letter-spacing:.12em;color:var(--muted);margin-top:5px}.nav-list{display:flex;gap:34px;align-items:center}.nav-list a{font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.11em;text-decoration:none;border-bottom:2px solid transparent;padding:10px 0}.nav-list a[aria-current]{border-bottom-color:var(--blue)}.nav-list a:hover{color:var(--blue)}.menu-toggle{display:none;background:transparent;border:2px solid var(--ink);padding:5px 13px;border-radius:0;font-size:26px}
.content-wrap{max-width:1260px;padding-left:clamp(22px,5vw,76px);padding-right:clamp(22px,5vw,76px);margin:0 auto}.eyebrow,.edition,.section-number,.story-topline,.read-cue,.art-label,.art-bottom,.foot-brand,.back-link,.article-type,.aside-note,.article-end,.footer-bottom{font-size:11px;font-weight:750;letter-spacing:.14em;text-transform:uppercase}
.hero{max-width:1440px;margin:0 auto;display:grid;grid-template-columns:1.04fr .96fr;min-height:695px}.hero-copy{position:relative;padding:clamp(58px,9vw,115px) clamp(22px,5vw,76px) 60px;display:flex;flex-direction:column;align-items:flex-start}.edition{color:var(--blue);border-top:3px solid var(--blue);padding-top:14px}.edition span{padding:0 8px;color:var(--muted)}.hero h1{font-size:clamp(54px,5.8vw,96px);line-height:.99;margin:45px 0 28px;max-width:750px}.hero h1 em,.page-head h1 em,.article-head h1 em{font-style:italic;color:var(--blue)}.hero-intro{font-size:clamp(16px,1.3vw,20px);max-width:530px;line-height:1.6}.primary-link{display:inline-flex;gap:28px;align-items:center;text-decoration:none;font-weight:750;font-size:13px;text-transform:uppercase;letter-spacing:.09em;border-bottom:2px solid var(--blue);color:var(--blue);padding:12px 0;margin-top:25px}.primary-link:hover{background:#edf0ff}.hero-stamp{border:1px solid var(--rule);font-size:10px;line-height:1.45;letter-spacing:.15em;font-weight:750;padding:14px;margin-top:auto;align-self:flex-end;transform:rotate(7deg)}.hero-stamp span{color:var(--blue);font-size:22px}.hero-art{background:#e6e3d6;display:flex;flex-direction:column;min-width:0}.art-label,.art-bottom{padding:18px 24px;display:flex;justify-content:space-between;gap:12px}.hero-art img{width:100%;height:100%;flex:1;min-height:0;object-fit:cover}.art-bottom{font-size:11px}
.lede-band{border-block:1px solid var(--rule);display:grid;grid-template-columns:1fr 2fr;align-items:start;gap:30px;padding:48px max(22px,calc((100vw - 1110px)/2))}.lede-band p{font-family:var(--font-serif);font-size:clamp(28px,3vw,47px);line-height:1.21;letter-spacing:-.03em;margin:0;max-width:760px}.lede-band em{color:var(--blue)}.feature-section{padding-top:105px;padding-bottom:110px}.section-bar{display:flex;align-items:end;justify-content:space-between;gap:24px;border-top:1px solid var(--ink);padding-top:26px;margin-bottom:38px}.section-bar h2{font-size:clamp(38px,4vw,58px);letter-spacing:-.045em;margin:12px 0 0}.text-link{font-size:13px;font-weight:750;text-transform:uppercase;letter-spacing:.08em;text-decoration:none;border-bottom:2px solid var(--blue);padding:7px 0;white-space:nowrap}.story-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:32px}.story-card{border:1px solid var(--rule);padding:30px;min-width:0;display:flex;flex-direction:column;min-height:360px;background:#fffefa}.story-card[hidden]{display:none}.story-topline{display:flex;justify-content:space-between;gap:12px;color:#455257}.story-card h3{font-size:clamp(28px,3vw,44px);letter-spacing:-.045em;margin:48px 0 15px}.story-card h3 a{text-decoration:none}.story-card h3 a:hover{text-decoration:underline}.card-arrow{color:var(--blue);font-family:var(--font-sans);font-size:.6em;margin-left:8px}.story-card p{font-size:15px;max-width:440px}.read-cue{margin-top:auto;color:var(--blue);padding-top:26px}.editorial-quote{background:var(--deep);color:#fdfbf3;padding:110px 24px}.quote-inner{max-width:820px;margin:auto;text-align:center}.quote-inner .eyebrow{color:#d7e3ef}.quote-inner p{font:normal clamp(28px,4.5vw,64px)/1.2 var(--font-serif);letter-spacing:-.04em;margin:25px 0}.outline-link{display:inline-block;color:#fff7e6;border:1px solid #fff7e6;padding:14px 19px;font-size:12px;letter-spacing:.09em;text-transform:uppercase;text-decoration:none;font-weight:750}
.site-footer{background:#101c23;color:#f9f7ef;padding:75px clamp(22px,5vw,76px) 22px}.footer-grid{max-width:1140px;margin:0 auto;display:grid;grid-template-columns:2fr 1fr;gap:50px}.foot-brand{text-transform:none;letter-spacing:-.045em;font-family:var(--font-serif);font-size:40px}.gold-dot{color:#f5bf5f}.footer-grid p{font-size:14px;color:#cbd5d6;max-width:490px}.footer-links{display:flex;flex-direction:column;align-items:flex-start;gap:10px}.footer-links .eyebrow{color:#cbd5d6}.footer-links a{font-size:14px}.footer-bottom{max-width:1140px;margin:55px auto 0;border-top:1px solid #56646b;padding-top:20px;display:flex;justify-content:space-between;gap:20px;flex-wrap:wrap;font-size:11px;color:#cbd5d6}
.page-head{padding-top:100px;padding-bottom:75px}.page-head h1{font-size:clamp(54px,7vw,100px);max-width:980px;margin:24px 0 28px}.page-intro{font-size:clamp(18px,1.8vw,24px);max-width:690px;line-height:1.55}.journal-section{padding-bottom:130px}.journal-tools{border-top:1px solid var(--rule);padding-top:28px;max-width:580px;margin-bottom:52px}.journal-tools label{display:block;font-weight:750;margin-bottom:12px}.search-wrap{position:relative}.search-wrap input{width:100%;min-height:54px;border:2px solid #52636c;background:#fffefa;padding:10px 45px 10px 15px;border-radius:0}.search-icon{font-size:28px;position:absolute;right:15px;top:2px;pointer-events:none;color:var(--muted)}.helper{color:var(--muted);font-size:13px;margin-top:9px}.no-results{padding:28px;background:#eceff0;font-size:16px}
.article-head{border-bottom:1px solid var(--rule);padding:90px 0 80px}.back-link{display:inline-block;text-decoration:none;color:var(--blue);margin-bottom:75px}.article-type{display:flex;justify-content:space-between;gap:15px;max-width:800px;color:var(--muted)}.article-head h1{max-width:920px;font-size:clamp(58px,8vw,112px);margin:25px 0}.article-deck{max-width:750px;font:normal clamp(22px,2.5vw,32px)/1.4 var(--font-serif)}.article-layout{display:grid;grid-template-columns:240px minmax(0,730px);gap:clamp(36px,7vw,130px);padding-top:85px;padding-bottom:135px}.article-aside{border-top:2px solid var(--blue);padding-top:18px;align-self:start;position:sticky;top:24px}.article-aside ol{padding-left:19px}.article-aside li{margin:12px 0}.article-aside a{font-size:13px}.aside-note{display:block;margin-top:38px;color:var(--muted);line-height:1.6;font-size:10px}.article-body{font-family:var(--font-serif);font-size:clamp(18px,1.7vw,22px);line-height:1.77}.article-body p{margin-bottom:1.3em}.article-body h2{font-size:clamp(30px,3.2vw,43px);letter-spacing:-.035em;margin:0 0 21px}.article-section{scroll-margin-top:35px;padding-bottom:44px}.article-section+.article-section{border-top:1px solid var(--rule);padding-top:55px}.article-end{font-family:var(--font-sans);display:flex;justify-content:space-between;gap:22px;border-top:2px solid var(--ink);padding-top:30px;font-size:10px}.article-end a{color:var(--blue)}
.about-grid{display:grid;grid-template-columns:1fr 2fr;gap:70px;padding:15px 0 140px}.about-mark{font-size:clamp(85px,16vw,260px);line-height:1;white-space:nowrap;align-self:start}.about-copy{max-width:700px}.about-copy h2{font-size:38px;margin:6px 0 20px}.about-copy p{font-size:17px;line-height:1.8;margin-bottom:25px}
@media(max-width:1040px){.hero{min-height:620px}.hero-copy{padding-top:65px}.hero h1{font-size:clamp(50px,5vw,70px)}.lede-band{padding:40px 32px}}
@media(max-width:720px){.header-inner{padding:15px 22px;flex-wrap:wrap}.brand-name{font-size:19px}.menu-toggle{display:block}.nav-list{width:100%;display:flex;gap:0;justify-content:space-between;border-top:1px solid var(--rule);padding-top:10px}.js .nav-list{display:none}.js .menu-toggle[aria-expanded=true]+.nav-list{display:flex}.nav-list a{padding:10px 6px}.hero{grid-template-columns:1fr}.hero-copy{padding:70px 22px 30px}.hero h1{font-size:clamp(53px,11vw,78px);margin:35px 0 25px}.hero-stamp{display:none}.hero-art{min-height:380px}.hero-art img{height:300px;object-fit:cover}.lede-band{grid-template-columns:1fr;padding:32px 22px}.feature-section{padding:65px 22px}.story-grid{grid-template-columns:1fr;gap:18px}.story-card{min-height:300px;padding:25px}.story-card h3{margin:38px 0 15px}.section-bar{align-items:start}.section-bar h2{font-size:40px}.text-link{white-space:normal}.editorial-quote{padding:75px 22px}.page-head{padding-top:65px;padding-bottom:45px}.page-head h1{font-size:clamp(50px,10vw,76px)}.journal-section{padding-bottom:80px}.article-head{padding:65px 0 50px}.back-link{margin-bottom:50px}.article-head h1{font-size:clamp(54px,10vw,85px)}.article-layout{grid-template-columns:1fr;padding-top:45px;padding-bottom:75px}.article-aside{position:static}.article-aside nav ol{display:flex;gap:25px;flex-wrap:wrap;list-style:none;padding:0}.article-aside li{margin:4px 0}.aside-note{margin-top:15px}.article-body{font-size:19px}.about-grid{grid-template-columns:1fr;gap:25px;padding-bottom:80px}.about-mark{font-size:100px}.footer-grid{grid-template-columns:1fr;gap:25px}}
@media(max-width:380px){.brand-mark{font-size:27px}.brand-name{font-size:17px}.brand-name small{font-size:9px}.section-bar{display:block}.text-link{display:inline-block;margin-top:17px}.story-topline{font-size:10px}.hero h1{font-size:50px}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*,*::before,*::after{animation-duration:.01ms!important;transition-duration:.01ms!important}}
''',encoding='utf-8', newline='\n')
print('built',len(pages),'pages')
