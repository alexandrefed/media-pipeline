// Extract a whole Skool classroom course from a logged-in browser tab.
//
// Run inside any lesson page of the course (e.g. via claude-in-chrome's
// javascript_tool). It walks the course tree in __NEXT_DATA__, fetches each
// lesson page with the same session, and collects:
//   - the lesson body (Skool "[v2]" ProseMirror JSON, converted later by
//     scripts/skool_course_to_md.py)
//   - the caption text of Skool-hosted (Mux) videos
//   - the id of YouTube-embedded videos (captions fetched later with yt-dlp)
//   - the attachments list
// The short-lived Mux playback token is used in memory only and never saved.
// Result: one JSON file downloaded as <course-slug>.json.

(async () => {
  const pageProps = (doc) =>
    JSON.parse(doc.getElementById('__NEXT_DATA__').textContent).props.pageProps;

  const tree = pageProps(document).course;
  const root = tree.course || tree;
  const lessons = [];
  let section = null;
  (function walk(node, depth = 0) {
    const c = node.course || node;
    if (c.unitType === 'set') section = c.metadata?.title || null;
    // A lesson sitting directly under the course belongs to no module.
    if (c.unitType === 'module') lessons.push({ id: c.id, section: depth > 1 ? section : null, title: c.metadata?.title });
    (node.children || []).forEach((ch) => walk(ch, depth + 1));
  })(tree);

  const muxCaptions = async (video) => {
    const base = 'https://stream.mux.com/';
    const manifest = await (await fetch(`${base}${video.playbackId}.m3u8?token=${video.playbackToken}`)).text();
    const m = manifest.match(/TYPE=SUBTITLES[^\n]*URI="([^"]+)"/);
    if (!m) return null;
    const subUrl = new URL(m[1], base);
    const playlist = await (await fetch(subUrl.href)).text();
    const segments = playlist.split('\n').filter((l) => l && !l.startsWith('#'));
    let vtt = '';
    for (const s of segments) vtt += (await (await fetch(new URL(s, subUrl).href)).text()) + '\n';
    return vtt;
  };

  const out = [];
  for (const [i, l] of lessons.entries()) {
    const html = await fetch(`${location.pathname}?md=${l.id}`, { credentials: 'include' }).then((r) => r.text());
    const doc = new DOMParser().parseFromString(html, 'text/html');
    const pp = pageProps(doc);
    const find = (n) => {
      const c = n.course || n;
      if (c.id === l.id) return c;
      for (const ch of n.children || []) { const r = find(ch); if (r) return r; }
    };
    const meta = find(pp.course)?.metadata || {};
    const videoLink = meta.videoLink || '';
    const yt = videoLink.match(/(?:v=|youtu\.be\/|embed\/)([A-Za-z0-9_-]{11})/);
    const rec = {
      order: i + 1,
      id: l.id,
      section: l.section,
      title: meta.title || l.title,
      url: `${location.origin}${location.pathname}?md=${l.id}`,
      body: meta.desc || '',
      resources: meta.resources || '[]',
      video: null,
    };
    if (yt) {
      rec.video = { kind: 'youtube', id: yt[1], durationMs: meta.videoLenMs || null };
    } else if (videoLink) {
      rec.video = { kind: 'other', link: videoLink.split('?')[0], durationMs: meta.videoLenMs || null };
    } else if (meta.videoId && pp.video?.playbackId) {
      let captions = null;
      try { captions = await muxCaptions(pp.video); } catch (e) { captions = null; }
      rec.video = { kind: 'skool', durationMs: pp.video.duration || null, captionsVtt: captions };
    }
    out.push(rec);
  }

  const result = {
    course: root.metadata?.title,
    courseDescription: root.metadata?.desc || '',
    community: location.pathname.split('/')[1],
    extractedAt: new Date().toISOString(),
    lessons: out,
  };
  const slug = (result.course || 'course').toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([JSON.stringify(result, null, 2)], { type: 'application/json' }));
  a.download = `${slug}.json`;
  document.body.appendChild(a);
  a.click();
  a.remove();
  return {
    file: a.download,
    lessons: out.length,
    summary: out.map((r) => `${r.title} | ${r.video?.kind || 'text'} | body ${r.body.length} | captions ${r.video?.captionsVtt ? r.video.captionsVtt.length : '-'}`),
  };
})();
