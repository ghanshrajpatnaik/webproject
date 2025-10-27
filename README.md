<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Novel Reader</title>
  <style>
    :root{
      --bg: #f4f6f8;
      --card: #fff;
      --text: #111;
      --muted: #555;
      --accent: #2b7cff;
    }
    [data-theme="dark"]{
      --bg: #0f1720;
      --card: #0b1220;
      --text: #e6eef7;
      --muted: #9fb0cc;
      --accent: #66a9ff;
    }
    *{box-sizing:border-box}
    body{margin:0;font-family:Inter,system-ui,Segoe UI,Roboto,Arial;background:var(--bg);color:var(--text);line-height:1.5}
    .app{max-width:1100px;margin:28px auto;padding:20px}
    header{display:flex;align-items:center;justify-content:space-between;margin-bottom:18px}
    header h1{margin:0;font-size:20px}
    header .controls{display:flex;gap:8px;align-items:center}
    button{cursor:pointer;border:0;background:var(--accent);color:#fff;padding:8px 12px;border-radius:8px}
    .muted{color:var(--muted);font-size:13px}
    .layout{display:grid;grid-template-columns:320px 1fr;gap:18px}
    .panel{background:var(--card);padding:14px;border-radius:12px;box-shadow:0 6px 18px rgba(2,6,23,0.06)}
    .library-list{list-style:none;padding:0;margin:0;display:flex;flex-direction:column;gap:10px}
    .lib-item{display:flex;gap:10px;align-items:flex-start;padding:10px;border-radius:8px;cursor:pointer}
    .lib-item:hover{background:rgba(0,0,0,0.03)}
    .lib-thumb{width:60px;height:80px;flex-shrink:0;background:#ddd;border-radius:6px;display:flex;align-items:center;justify-content:center;color:#666;font-size:12px}
    .lib-meta{flex:1}
    .lib-title{font-weight:600;margin:0}
    .lib-sub{margin:6px 0 0;font-size:13px;color:var(--muted)}
    .reader-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}
    .reader-title{margin:0}
    .reader-body{background:var(--card);padding:20px;border-radius:12px;min-height:320px;box-shadow:0 6px 18px rgba(2,6,23,0.06)}
    .reader-controls{display:flex;gap:10px;align-items:center;margin-top:12px}
    .small{font-size:13px;padding:6px 8px;background:transparent;color:var(--text);border:1px solid rgba(0,0,0,0.06);border-radius:8px}
    .progress-bar{height:8px;background:rgba(0,0,0,0.06);border-radius:8px;overflow:hidden;margin-top:8px}
    .progress-fill{height:100%;background:var(--accent);width:0%}
    pre.chapter{white-space:pre-wrap;font-family:inherit;margin:0}
    .meta-row{display:flex;gap:10px;align-items:center}
    .spacer{flex:1}
    footer{margin-top:22px;text-align:center;color:var(--muted);font-size:13px}
    @media (max-width:900px){ .layout{grid-template-columns:1fr} .panel{padding:12px} .lib-thumb{display:none} }
  </style>
</head>
<body>
  <div class="app" id="app" data-theme="light">
    <header>
      <h1>Novel Reader</h1>
      <div class="controls">
        <label class="muted">User:</label>
        <input id="username" placeholder="Your name" style="padding:8px;border-radius:8px;border:1px solid #ddd"/>
        <button id="btnSetUser" class="">Set</button>
        <button id="btnTheme" title="Toggle dark mode">Dark</button>
      </div>
    </header>

    <div class="layout">
      <aside class="panel">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px">
          <strong>Library</strong>
          <span class="muted" id="libCount">0</span>
        </div>
        <ul class="library-list" id="library"></ul>

        <div style="margin-top:12px" class="muted small">
          <div>Total reading time (this session): <span id="sessionTime">0s</span></div>
          <div style="margin-top:6px">Saved progress: <span id="savedProgress">—</span></div>
        </div>
      </aside>

      <main>
        <div class="panel">
          <div class="reader-header">
            <div>
              <h2 class="reader-title" id="readerTitle">Select a novel to start reading</h2>
              <div class="muted" id="chapterLabel"></div>
            </div>
            <div class="meta-row">
              <div class="muted">Progress</div>
              <div style="width:160px;margin-left:10px">
                <div class="progress-bar"><div id="progressFill" class="progress-fill"></div></div>
              </div>
            </div>
          </div>

          <div id="readerBody" class="reader-body">
            <div class="muted">No content loaded.</div>
          </div>

          <div class="reader-controls">
            <button id="btnPrev" class="small">Previous</button>
            <button id="btnNext" class="small">Next</button>
            <button id="btnBookmark" class="small">Bookmark</button>
            <div class="spacer"></div>
            <button id="btnIncreaseFont" class="small">A+</button>
            <button id="btnDecreaseFont" class="small">A-</button>
            <button id="btnReset" class="small">Reset Progress</button>
          </div>
        </div>
      </main>
    </div>

    <footer>
      Built for reading. Progress & time save locally. Open-source and extendable.
    </footer>
  </div>

  <script>
    /***************
     * Sample content
     * Replace with server-loaded content in production
     ***************/
    const SAMPLE = [
      {
        id: 'novel-1',
        title: 'The Silent Lake',
        author: 'A. Writer',
        chapters: [
          { title: 'Chapter 1', body: 'It was a bright cold day in April. The lake lay still...' },
          { title: 'Chapter 2', body: 'The cabin smelled of pine and old paper. He remembered the promise...' },
          { title: 'Chapter 3', body: 'Night came hard and early. Stars were sharp as glass...' }
        ]
      },
      {
        id: 'novel-2',
        title: 'City of Lanterns',
        author: 'B. Novelist',
        chapters: [
          { title: 'Prologue', body: 'Lanterns burned in lines down the river. That night changed everything.' },
          { title: 'Chapter 1', body: 'She walked through markets, buying nothing but time.' }
        ]
      }
    ];

    /***************
     * App state and helpers
     ***************/
    const el = id => document.getElementById(id);
    let user = null;
    let current = { novelId: null, chapterIndex: 0 };
    let fontSize = 16;
    let sessionSeconds = 0;
    let sessionTimer = null;

    // storage keys per user
    function userKey(k){ return `nr:${user || 'anon'}:${k}` }

    // load library into UI
    function renderLibrary(list){
      const ul = el('library');
      ul.innerHTML = '';
      list.forEach(n => {
        const li = document.createElement('li');
        li.className = 'lib-item';
        li.innerHTML = `
          <div class="lib-thumb">IMG</div>
          <div class="lib-meta">
            <div class="lib-title">${escapeHtml(n.title)}</div>
            <div class="lib-sub">${escapeHtml(n.author || '')}</div>
          </div>
        `;
        li.addEventListener('click', ()=> openNovel(n.id));
        ul.appendChild(li);
      });
      el('libCount').innerText = list.length;
    }

    // simple html escape
    function escapeHtml(s){ return String(s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;') }

    // find novel by id
    function findNovel(id){ return SAMPLE.find(n => n.id === id) }

    // show a chapter
    function showChapter(novel, idx){
      el('readerTitle').innerText = novel ? `${novel.title} — ${novel.author || ''}` : 'Select a novel';
      const chapter = novel && novel.chapters[idx];
      if (!chapter){
        el('readerBody').innerHTML = '<div class="muted">No chapter found.</div>';
        el('chapterLabel').innerText = '';
        return;
      }
      el('chapterLabel').innerText = chapter.title;
      el('readerBody').innerHTML = `<pre class="chapter" style="font-size:${fontSize}px">${escapeHtml(chapter.body)}</pre>`;
      updateProgress(novel.id, idx);
      savePosition(novel.id, idx);
    }

    // update progress bar & saved info
    function updateProgress(novelId, chapterIndex){
      const novel = findNovel(novelId);
      if (!novel) {
        el('progressFill').style.width = '0%';
        el('savedProgress').innerText = '—';
        return;
      }
      const total = novel.chapters.length;
      const percent = Math.round(((chapterIndex+1)/total) * 100);
      el('progressFill').style.width = percent + '%';
      const saved = JSON.parse(localStorage.getItem(userKey('progress') ) || '{}');
      const val = saved[novelId];
      el('savedProgress').innerText = val ? `ch ${val.chapter+1} (${Math.round(((val.chapter+1)/total)*100)}%)` : 'none';
    }

    // save current position
    function savePosition(novelId, chapterIndex){
      const key = userKey('progress');
      const all = JSON.parse(localStorage.getItem(key) || '{}');
      all[novelId] = { chapter: chapterIndex, at: Date.now() };
      localStorage.setItem(key, JSON.stringify(all));
    }

    // load last saved position
    function loadLastPosition(novelId){
      const all = JSON.parse(localStorage.getItem(userKey('progress')) || '{}');
      return all[novelId] ? all[novelId].chapter : 0;
    }

    // open a novel by id
    function openNovel(id){
      const novel = findNovel(id);
      if (!novel) return alert('Novel not found');
      current.novelId = id;
      current.chapterIndex = loadLastPosition(id);
      showChapter(novel, current.chapterIndex);
      startSessionTimer();
    }

    // navigation
    el('btnNext').addEventListener('click', ()=>{
      const novel = findNovel(current.novelId); if(!novel) return;
      if (current.chapterIndex < novel.chapters.length - 1) current.chapterIndex++;
      showChapter(novel, current.chapterIndex);
    });
    el('btnPrev').addEventListener('click', ()=>{
      const novel = findNovel(current.novelId); if(!novel) return;
      if (current.chapterIndex > 0) current.chapterIndex--;
      showChapter(novel, current.chapterIndex);
    });

    // bookmark (simple — saves current to a named bookmarks object)
    el('btnBookmark').addEventListener('click', ()=>{
      if (!current.novelId) return;
      const all = JSON.parse(localStorage.getItem(userKey('bookmarks')) || '[]');
      all.push({ novelId: current.novelId, chapter: current.chapterIndex, time: Date.now() });
      localStorage.setItem(userKey('bookmarks'), JSON.stringify(all));
      alert('Bookmark saved');
    });

    // font controls
    el('btnIncreaseFont').addEventListener('click', ()=>{ fontSize = Math.min(28, fontSize + 2); showChapter(findNovel(current.novelId), current.chapterIndex) });
    el('btnDecreaseFont').addEventListener('click', ()=>{ fontSize = Math.max(12, fontSize - 2); showChapter(findNovel(current.novelId), current.chapterIndex) });

    // reset progress
    el('btnReset').addEventListener('click', ()=>{
      if (!current.novelId) return;
      const all = JSON.parse(localStorage.getItem(userKey('progress')) || '{}');
      delete all[current.novelId];
      localStorage.setItem(userKey('progress'), JSON.stringify(all));
      updateProgress(current.novelId, 0);
      alert('Progress reset for this novel');
    });

    // user management (very light)
    el('btnSetUser').addEventListener('click', ()=> {
      const v = el('username').value.trim();
      if (!v) return alert('Enter a name');
      user = v;
      // restore session time from saved store if exists
      const s = parseInt(localStorage.getItem(userKey('sessionSeconds') ) || '0', 10);
      sessionSeconds = s || 0;
      el('sessionTime').innerText = `${sessionSeconds}s`;
      // load library and last opened if any
      const last = localStorage.getItem(userKey('lastOpened'));
      if (last) {
        try { const obj = JSON.parse(last); openNovel(obj.novelId); }
        catch {}
      }
      alert('User set: ' + user);
    });

    // session time tracking (counts while the reader view is open)
    function startSessionTimer(){
      if (sessionTimer) clearInterval(sessionTimer);
      sessionTimer = setInterval(()=> {
        sessionSeconds += 1;
        el('sessionTime').innerText = `${sessionSeconds}s`;
        localStorage.setItem(userKey('sessionSeconds'), String(sessionSeconds));
      }, 1000);
      // store last opened
      localStorage.setItem(userKey('lastOpened'), JSON.stringify({ novelId: current.novelId, at: Date.now() }));
    }

    // theme toggle
    el('btnTheme').addEventListener('click', ()=>{
      const root = document.getElementById('app');
      const t = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      root.setAttribute('data-theme', t);
      localStorage.setItem('nr:theme', t);
    });

    // load saved theme
    (function loadTheme(){
      const t = localStorage.getItem('nr:theme') || 'light';
      document.getElementById('app').setAttribute('data-theme', t);
    })();

    // persist last opened when leaving
    window.addEventListener('beforeunload', ()=>{
      if (user) localStorage.setItem(userKey('sessionSeconds'), String(sessionSeconds));
    });

    // demo init
    renderLibrary(SAMPLE);

    // optional: auto-open the first novel if demo user not set
    // openNovel(SAMPLE[0].id);
  </script>
</body>
</html>
