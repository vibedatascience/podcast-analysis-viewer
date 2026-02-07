#!/usr/bin/env python3
"""
Podcast Analysis Viewer v2
Generates a modern web interface for viewing podcast analysis.
Reads the same .txt metadata + _claude_artifact.md content files.
"""
import os
import re
import markdown
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import html


class PodcastAnalyzer:
    def __init__(self, directory: str = "/Users/rahulchaudhary/youtube_subs_extractor/output"):
        self.directory = Path(directory)
        self.episodes = []
        self.channels = {}
        self.recent_channels = set()

    def extract_metadata_from_txt(self, txt_file: Path) -> Dict:
        try:
            with open(txt_file, 'r', encoding='utf-8') as f:
                content = f.read()

            metadata = {}
            for key in ['title', 'channel', 'published', 'duration', 'views', 'url']:
                match = re.search(rf'{key.upper()}:\s*(.+)', content)
                if match:
                    metadata[key] = match.group(1).strip()
            return metadata
        except Exception as e:
            print(f"Error reading {txt_file}: {e}")
            return {}

    def load_markdown_content(self, md_file: Path) -> str:
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading {md_file}: {e}")
            return ""

    def scan_episodes(self):
        self.episodes = []
        self.channels = {}
        self.recent_channels = set()

        today = datetime.now()
        one_week_ago = today - timedelta(days=7)

        txt_files = list(self.directory.glob("*.txt"))

        for txt_file in txt_files:
            if not re.match(r'\d{4}-\d{2}-\d{2}_', txt_file.name):
                continue

            metadata = self.extract_metadata_from_txt(txt_file)
            if not metadata:
                continue

            md_filename = txt_file.stem + "_claude_artifact.md"
            md_file = self.directory / md_filename

            if not md_file.exists():
                print(f"Warning: No corresponding MD file found for {txt_file.name}")
                continue

            md_content = self.load_markdown_content(md_file)

            episode = {
                'txt_file': txt_file,
                'md_file': md_file,
                'metadata': metadata,
                'md_content': md_content,
            }

            self.episodes.append(episode)

            channel = metadata.get('channel', 'Unknown')
            if channel not in self.channels:
                self.channels[channel] = []
            self.channels[channel].append(episode)

            published_str = metadata.get('published', '')
            if published_str:
                for date_format in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%B %d, %Y']:
                    try:
                        episode_date = datetime.strptime(published_str, date_format)
                        if episode_date >= one_week_ago:
                            self.recent_channels.add(channel)
                        break
                    except ValueError:
                        continue

        self.episodes.sort(key=lambda x: x['metadata'].get('published', ''), reverse=True)

        for channel in self.channels:
            self.channels[channel].sort(
                key=lambda x: x['metadata'].get('published', ''), reverse=True
            )

        sorted_channels = sorted(
            self.channels.items(),
            key=lambda x: x[1][0]['metadata'].get('published', '') if x[1] else '',
            reverse=True,
        )
        self.channels = dict(sorted_channels)

    def _get_channel_color(self, index: int) -> str:
        colors = [
            '#E3120B', '#006BA2', '#379A8B', '#9A607F',
            '#EBB434', '#3EBCD2', '#B4BA39', '#D1B07C', '#758D99',
        ]
        return colors[index % len(colors)]

    def _get_youtube_id(self, url: str) -> str:
        if 'youtube.com/watch?v=' in url:
            return url.split('v=')[1].split('&')[0]
        elif 'youtu.be/' in url:
            return url.split('youtu.be/')[1].split('?')[0]
        return ''

    def _slugify(self, text: str) -> str:
        return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')

    def _build_episodes_json(self) -> str:
        channel_colors = {}
        for i, ch in enumerate(self.channels.keys()):
            channel_colors[ch] = self._get_channel_color(i)

        episodes_json = []
        for i, episode in enumerate(self.episodes):
            meta = episode['metadata']
            channel = meta.get('channel', 'Unknown')
            url = meta.get('url', '')
            yt_id = self._get_youtube_id(url)
            channel_slug = self._slugify(channel)
            identifier = yt_id if yt_id else f'episode-{i}'
            permalink = f'#{channel_slug}/{identifier}'

            html_content = markdown.markdown(
                episode['md_content'],
                extensions=['tables', 'fenced_code', 'md_in_html'],
            )

            episodes_json.append({
                'index': i,
                'title': meta.get('title', 'Unknown Title'),
                'channel': channel,
                'channelColor': channel_colors.get(channel, '#758D99'),
                'published': meta.get('published', ''),
                'duration': meta.get('duration', ''),
                'views': meta.get('views', ''),
                'url': url,
                'youtube_id': yt_id,
                'permalink': permalink,
                'content': html_content,
            })

        return json.dumps(episodes_json, ensure_ascii=False)

    def _build_sidebar_html(self) -> str:
        channel_colors = {}
        for i, ch in enumerate(self.channels.keys()):
            channel_colors[ch] = self._get_channel_color(i)

        parts = []
        for channel_name, channel_episodes in self.channels.items():
            ch_id = re.sub(r'[^a-z0-9]+', '_', channel_name.lower()).strip('_')
            color = channel_colors[channel_name]
            is_recent = channel_name in self.recent_channels

            new_badge = ''
            if is_recent:
                new_badge = (
                    '<span style="font-size:7.5px;font-weight:700;padding:1.5px 5px;'
                    'background:#10b981;color:#fff;border-radius:3.5px;letter-spacing:0.04em;">NEW</span>'
                )

            parts.append(f'''
            <div class="channel-group">
              <button class="channel-toggle" onclick="toggleChannel('{ch_id}')"
                      aria-expanded="false" aria-controls="eps_{ch_id}">
                <span class="channel-arrow" id="arrow_{ch_id}" style="color:{color}">▶</span>
                <span class="channel-label">{html.escape(channel_name)}</span>
                {new_badge}
              </button>
              <div class="channel-episodes" id="eps_{ch_id}">
            ''')

            for episode in channel_episodes:
                title = episode['metadata'].get('title', 'Unknown Title')
                published = episode['metadata'].get('published', '')
                display_title = title if len(title) <= 50 else title[:47] + '...'

                correct_index = -1
                for idx, ep in enumerate(self.episodes):
                    if (ep['metadata'].get('title') == title and
                        ep['metadata'].get('channel') == channel_name and
                        ep['metadata'].get('published') == published):
                        correct_index = idx
                        break

                parts.append(f'''
                <button class="episode-btn" data-episode="{correct_index}"
                        onclick="selectEpisode({correct_index})">
                  <span class="ep-dot">●</span>
                  <div class="ep-info">
                    <div class="ep-title">{html.escape(display_title)}</div>
                    <div class="ep-date">{html.escape(published)}</div>
                  </div>
                </button>
                ''')

            parts.append('</div></div>')

        return '\n'.join(parts)

    def generate_html(self) -> str:
        episodes_json = self._build_episodes_json()
        sidebar_html = self._build_sidebar_html()

        first_channel_id = ''
        if self.channels:
            first_name = list(self.channels.keys())[0]
            first_channel_id = re.sub(r'[^a-z0-9]+', '_', first_name.lower()).strip('_')

        return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Podcast Analysis Viewer</title>
<link href="https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,300;0,8..60,400;0,8..60,500;0,8..60,600;0,8..60,700;1,8..60,400;1,8..60,500&family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:ital,wght@0,400;0,500;1,400&display=swap" rel="stylesheet">
<style>
{self._generate_css()}
</style>
</head>
<body>

<div class="progress-bar" id="progressBar"></div>

<button class="mobile-toggle" id="mobileToggle" onclick="openMobileMenu()" aria-label="Open menu">
  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round">
    <line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/>
  </svg>
</button>

<div class="overlay" id="overlay" onclick="closeMobileMenu()"></div>

<div class="shell">
  <!-- Sidebar -->
  <aside class="sidebar" id="sidebar">
    <div class="sidebar-header">
      <div class="sidebar-brand">
        <div class="brand-icon">▶</div>
        <div>
          <div class="brand-title">Podcast Viewer</div>
          <div class="brand-sub">Analysis &amp; Notes</div>
        </div>
        <button class="close-sidebar" onclick="closeSidebar()" aria-label="Close sidebar">&times;</button>
      </div>
      <div class="search-wrap">
        <span class="search-icon">⌕</span>
        <input type="text" id="searchInput" class="search-input" placeholder="Search episodes..."
               oninput="filterEpisodes(this.value)">
      </div>
      <a href="https://buymeacoffee.com/rahulxc" target="_blank" rel="noopener" class="coffee-link">☕ Buy me a coffee</a>
    </div>
    <div class="sidebar-scroll" id="sidebarScroll">
      {sidebar_html}
    </div>
  </aside>

  <!-- Main Content -->
  <main class="main" id="mainContent">
    <div class="welcome" id="welcome">
      <div class="welcome-icon">📻</div>
      <div class="welcome-title">Podcast Analysis Viewer</div>
      <div class="welcome-sub">Select an episode from the sidebar to view detailed analysis.</div>
    </div>
    <div class="spinner" id="spinner" style="display:none">
      <div class="spinner-ring"></div>
    </div>
    <div class="article-wrap" id="articleWrap" style="display:none">
      <div class="ep-header" id="epHeader"></div>
      <div class="ep-content" id="epContent"></div>
      <div class="ep-footer">Analysis generated with AI · Content may be summarized or paraphrased</div>
    </div>
  </main>
</div>

<script>
const episodes = {episodes_json};
const firstChannelId = "{first_channel_id}";

let currentIndex = -1;
let sidebarVisible = true;

// --- Episode Selection ---
function selectEpisode(idx, pushState) {{
  if (pushState === undefined) pushState = true;
  const ep = episodes[idx];
  if (!ep) return;

  currentIndex = idx;

  // Active state in sidebar
  document.querySelectorAll('.episode-btn').forEach(b => b.classList.remove('active'));
  const btn = document.querySelector('.episode-btn[data-episode="' + idx + '"]');
  if (btn) {{
    btn.classList.add('active');
    btn.style.setProperty('--active-color', ep.channelColor);
  }}

  // Update URL
  if (pushState) window.history.pushState(null, '', ep.permalink);

  // Show loading
  document.getElementById('welcome').style.display = 'none';
  document.getElementById('articleWrap').style.display = 'none';
  document.getElementById('spinner').style.display = 'flex';
  document.getElementById('spinner').querySelector('.spinner-ring').style.borderTopColor = ep.channelColor;
  document.getElementById('progressBar').style.width = '0%';
  document.getElementById('progressBar').style.background = ep.channelColor;

  // Apply channel color to h2 borders
  const style = document.getElementById('dynamicChannelStyle');
  if (style) style.textContent = '.ep-content h2 {{ border-bottom-color: ' + ep.channelColor + ' !important; }}';

  setTimeout(function() {{
    // Build header
    let viewsHtml = '';
    if (ep.views) {{
      const n = parseInt(ep.views.replace(/,/g, ''));
      let formatted = ep.views;
      if (n >= 1e6) formatted = (n / 1e6).toFixed(1) + 'M';
      else if (n >= 1e3) formatted = (n / 1e3).toFixed(0) + 'K';
      viewsHtml = '<span class="meta-dot">·</span><span>' + formatted + ' views</span>';
    }}
    let linkHtml = '';
    if (ep.url) {{
      linkHtml = '<span class="meta-dot">·</span><a href="' + ep.url + '" target="_blank" rel="noopener" class="meta-link" style="color:' + ep.channelColor + '">Watch ↗</a>';
    }}

    document.getElementById('epHeader').innerHTML =
      '<div class="header-accent" style="background:' + ep.channelColor + '"></div>' +
      '<div class="header-channel" style="color:' + ep.channelColor + '">' + escapeHtml(ep.channel) + '</div>' +
      '<h1 class="header-title">' + escapeHtml(ep.title) + '</h1>' +
      '<div class="header-meta">' +
        '<span>' + escapeHtml(ep.published) + '</span>' +
        '<span class="meta-dot">·</span>' +
        '<span>' + escapeHtml(ep.duration) + '</span>' +
        viewsHtml + linkHtml +
      '</div>';

    // Process content
    let content = ep.content;

    // Format "Contents Covered:" sections with list
    content = content.replace(
      new RegExp('<p><strong>Contents Covered:<\\/strong><\\/p>\\\\s*<ol>([\\\\s\\\\S]*?)<\\/ol>', 'gi'),
      function(match, listContent) {{
        return '<div class="contents-card"><div class="contents-label">Contents Covered<\\/div><ol>' + listContent + '<\\/ol><\\/div>';
      }}
    );
    // Inline version
    content = content.replace(
      new RegExp('<p><strong>Contents Covered:<\\/strong>([\\\\s\\\\S]*?)(?=<\\/p>)', 'gi'),
      function(match, inner) {{
        var items = [];
        inner.split(new RegExp('\\\\n|<br\\\\s*\\/?>'))
          .forEach(function(line) {{
            line = line.replace(/<[^>]*>/g, '').trim();
            if (line.match(new RegExp('^\\\\d+\\\\.'))) {{
              items.push(line.replace(new RegExp('^\\\\d+\\\\.\\\\s*'), '').trim());
            }}
          }});
        if (items.length === 0) return match;
        var lis = items.map(function(item) {{ return '<li>' + item + '<\\/li>'; }}).join('');
        return '<div class="contents-card"><div class="contents-label">Contents Covered<\\/div><ol>' + lis + '<\\/ol>';
      }}
    );

    // Format "Guest:" sections
    content = content.replace(
      new RegExp('<p><strong>Guest:<\\/strong>([^<]*)<\\/p>', 'gi'),
      function(match, info) {{
        return '<div class="guest-card" style="background:' + ep.channelColor + '0a;border-color:' + ep.channelColor + '30">' +
          '<div class="guest-label" style="color:' + ep.channelColor + '">Guest<\\/div>' +
          info.trim() + '<\\/div>';
      }}
    );

    // Format "Key Quote:" — standalone paragraph version
    content = content.replace(
      new RegExp('<p><strong>Key Quote:<\\/strong>([\\\\s\\\\S]*?)<\\/p>', 'gi'),
      function(match, quote) {{
        var clean = quote.replace(new RegExp('<\\\\/?strong>', 'g'), '').replace(new RegExp('<\\\\/?em>', 'g'), '')
          .replace(new RegExp('<br\\\\s*\\\\/?>','g'), ' ').replace(new RegExp('\\\\*\\\\*\\\\*','g'), '').trim();
        return '<div class="key-quote-card"><span class="kq-mark" style="color:' + ep.channelColor + '">\\"<\\/span><div class="kq-text">' + clean + '<\\/div><\\/div>';
      }}
    );

    // Remove redundant "Detailed Analysis:" heading
    content = content.replace(new RegExp('<p><strong>Detailed Analysis:<\\/strong><\\/p>', 'gi'), '');

    document.getElementById('epContent').innerHTML = content;
    document.getElementById('spinner').style.display = 'none';
    document.getElementById('articleWrap').style.display = 'block';

    // Scroll to top
    document.getElementById('mainContent').scrollTop = 0;

    // Close mobile menu
    if (window.innerWidth <= 1024) closeMobileMenu();
  }}, 250);
}}

function escapeHtml(str) {{
  const div = document.createElement('div');
  div.appendChild(document.createTextNode(str));
  return div.innerHTML;
}}

// --- Channel Toggle ---
function toggleChannel(chId) {{
  const el = document.getElementById('eps_' + chId);
  const arrow = document.getElementById('arrow_' + chId);
  if (!el) return;
  const isOpen = el.classList.contains('open');
  if (isOpen) {{
    el.classList.remove('open');
    arrow.classList.remove('open');
  }} else {{
    el.classList.add('open');
    arrow.classList.add('open');
  }}
}}

// --- Search ---
function filterEpisodes(query) {{
  const q = query.toLowerCase();
  document.querySelectorAll('.channel-group').forEach(function(group) {{
    let anyVisible = false;
    group.querySelectorAll('.episode-btn').forEach(function(btn) {{
      const idx = parseInt(btn.getAttribute('data-episode'));
      const ep = episodes[idx];
      const match = !q || ep.title.toLowerCase().includes(q) || ep.channel.toLowerCase().includes(q);
      btn.style.display = match ? '' : 'none';
      if (match) anyVisible = true;
    }});
    group.style.display = anyVisible ? '' : 'none';
    if (q && anyVisible) {{
      const epDiv = group.querySelector('.channel-episodes');
      const arrow = group.querySelector('.channel-arrow');
      if (epDiv) epDiv.classList.add('open');
      if (arrow) arrow.classList.add('open');
    }}
  }});
}}

// --- Sidebar ---
function closeSidebar() {{
  document.getElementById('sidebar').classList.add('hidden');
  document.getElementById('mobileToggle').classList.add('show');
  sidebarVisible = false;
}}
function openSidebar() {{
  document.getElementById('sidebar').classList.remove('hidden');
  document.getElementById('mobileToggle').classList.remove('show');
  sidebarVisible = true;
}}

// --- Mobile ---
function openMobileMenu() {{
  document.getElementById('sidebar').classList.add('mobile-open');
  document.getElementById('overlay').classList.add('show');
  document.getElementById('mobileToggle').style.display = 'none';
  document.body.style.overflow = 'hidden';
}}
function closeMobileMenu() {{
  document.getElementById('sidebar').classList.remove('mobile-open');
  document.getElementById('overlay').classList.remove('show');
  document.getElementById('mobileToggle').style.display = '';
  document.body.style.overflow = '';
}}

// --- Reading Progress ---
document.getElementById('mainContent').addEventListener('scroll', function() {{
  const el = this;
  const h = el.scrollHeight - el.clientHeight;
  if (h > 0) {{
    document.getElementById('progressBar').style.width = Math.min((el.scrollTop / h) * 100, 100) + '%';
  }}
}}, {{ passive: true }});

// --- Deep Linking ---
function handleHash() {{
  const hash = window.location.hash.slice(1);
  if (!hash) return false;
  const parts = hash.split('/');
  if (parts.length < 1) return false;

  const channelSlug = parts[0];
  const identifier = parts[1] || '';

  let matchIdx = -1;
  if (identifier) {{
    matchIdx = episodes.findIndex(function(ep) {{ return ep.youtube_id === identifier; }});
    if (matchIdx === -1 && identifier.startsWith('episode-')) {{
      const parsed = parseInt(identifier.replace('episode-', ''));
      if (parsed >= 0 && parsed < episodes.length) matchIdx = parsed;
    }}
  }}
  if (matchIdx === -1) {{
    matchIdx = episodes.findIndex(function(ep) {{
      return ep.channel.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') === channelSlug;
    }});
  }}

  if (matchIdx >= 0) {{
    // Expand parent channel
    const ep = episodes[matchIdx];
    const chId = ep.channel.toLowerCase().replace(/[^a-z0-9]+/g, '_').replace(/^_|_$/g, '');
    toggleChannel(chId);
    selectEpisode(matchIdx, false);
    return true;
  }}
  return false;
}}

// --- Resize ---
window.addEventListener('resize', function() {{
  if (window.innerWidth > 1024) closeMobileMenu();
}});
window.addEventListener('hashchange', handleHash);
document.addEventListener('keydown', function(e) {{
  if (e.key === 'Escape' && window.innerWidth <= 1024) closeMobileMenu();
}});

// --- Init ---
document.addEventListener('DOMContentLoaded', function() {{
  // Inject dynamic style tag for channel-colored h2 borders
  const s = document.createElement('style');
  s.id = 'dynamicChannelStyle';
  document.head.appendChild(s);

  const hashHandled = handleHash();
  if (!hashHandled && episodes.length > 0) {{
    if (firstChannelId) toggleChannel(firstChannelId);
    selectEpisode(0, false);
  }}
}});
</script>
</body>
</html>'''

    def _generate_css(self) -> str:
        return '''
*,*::before,*::after { margin:0; padding:0; box-sizing:border-box; }

body {
  font-family: 'Source Serif 4', Georgia, serif;
  color: #1a1a1a;
  background: #F4F3EF;
  line-height: 1.6;
}

/* --- Progress Bar --- */
.progress-bar {
  position: fixed; top:0; left:0; height:3px; width:0;
  background: #E3120B; z-index:200;
  transition: width 0.08s linear;
}

/* --- Mobile Toggle --- */
.mobile-toggle {
  display:none; position:fixed; top:14px; left:14px; z-index:100;
  background:#FDFCF9; border:1px solid #E5E2D9; border-radius:7px;
  padding:7px 11px; cursor:pointer; color:#888;
  box-shadow: 0 1px 6px rgba(0,0,0,0.05);
  align-items:center; justify-content:center;
}
.mobile-toggle.show { display:flex; }

/* --- Overlay --- */
.overlay {
  display:none; position:fixed; inset:0;
  background:rgba(0,0,0,0.35); z-index:80;
  backdrop-filter:blur(2px);
}
.overlay.show { display:block; }

/* --- Shell --- */
.shell { display:flex; height:100vh; width:100vw; overflow:hidden; }

/* --- Sidebar --- */
.sidebar {
  width:272px; min-width:272px;
  background:#FDFCF9; border-right:1px solid #E5E2D9;
  display:flex; flex-direction:column;
  transition: all 0.25s cubic-bezier(0.4,0,0.2,1);
  overflow:hidden; z-index:10;
}
.sidebar.hidden { width:0; min-width:0; border-right:none; }

.sidebar-header {
  padding:18px 18px 12px; border-bottom:1px solid #E5E2D9; flex-shrink:0;
}
.sidebar-brand {
  display:flex; align-items:center; gap:9px;
}
.brand-icon {
  width:28px; height:28px; border-radius:7px; background:#E3120B;
  display:flex; align-items:center; justify-content:center;
  color:#fff; font-size:13px; font-family:'Outfit',sans-serif; font-weight:700;
  flex-shrink:0;
}
.brand-title {
  font-family:'Outfit',sans-serif; font-weight:700; font-size:14px;
  letter-spacing:-0.02em; color:#1a1a1a;
}
.brand-sub {
  font-family:'Outfit',sans-serif; font-size:9.5px; color:#aaa;
  letter-spacing:0.05em; text-transform:uppercase;
}
.close-sidebar {
  margin-left:auto; background:none; border:none; cursor:pointer;
  color:#aaa; font-size:18px; padding:4px; line-height:1;
}

.search-wrap { margin-top:10px; position:relative; }
.search-icon {
  position:absolute; left:9px; top:50%; transform:translateY(-50%);
  font-size:11.5px; color:#bbb;
}
.search-input {
  width:100%; padding:6px 10px 6px 28px;
  border:1px solid #E5E2D9; border-radius:7px;
  font-size:11.5px; font-family:'Outfit',sans-serif;
  background:#F4F3EF; outline:none; color:#1a1a1a;
}
.search-input:focus { border-color:#ccc; }

.coffee-link {
  display:inline-flex; align-items:center; gap:3px;
  font-size:9.5px; color:#ccc; text-decoration:none;
  margin-top:6px; font-family:'Outfit',sans-serif;
}
.coffee-link:hover { color:#999; }

.sidebar-scroll { flex:1; overflow-y:auto; padding:6px 0; }

/* --- Channels --- */
.channel-group {}
.channel-toggle {
  display:flex; align-items:center; gap:7px;
  width:100%; padding:7px 18px;
  background:none; border:none; cursor:pointer;
  font-family:'Outfit',sans-serif; font-size:10.5px; font-weight:600;
  color:#999; text-transform:uppercase; letter-spacing:0.05em; text-align:left;
}
.channel-toggle:hover { background:#F4F3EF; }
.channel-arrow {
  font-size:8px; transition:transform 0.15s; display:inline-block;
}
.channel-arrow.open { transform:rotate(90deg); }
.channel-label { flex:1; }

.channel-episodes {
  max-height:0; overflow:hidden; transition:max-height 0.3s ease;
}
.channel-episodes.open { max-height:5000px; }

/* --- Episode Buttons --- */
.episode-btn {
  display:flex; align-items:flex-start; gap:7px;
  width:100%; padding:5px 18px 5px 33px;
  background:transparent; border:none; cursor:pointer;
  font-family:'Outfit',sans-serif; font-size:11px;
  color:#555; text-align:left; line-height:1.35;
  transition:background 0.1s;
}
.episode-btn:hover { background:#F4F3EF; }
.episode-btn.active {
  background: var(--active-color, #E3120B);
  color:#fff;
}
.ep-dot { flex-shrink:0; margin-top:3px; font-size:8px; opacity:0.35; }
.episode-btn.active .ep-dot { opacity:1; }
.ep-info { min-width:0; flex:1; }
.ep-title {
  overflow:hidden; text-overflow:ellipsis; white-space:nowrap;
  font-weight:400;
}
.episode-btn.active .ep-title { font-weight:600; }
.ep-date { font-size:9.5px; opacity:0.4; margin-top:1px; }
.episode-btn.active .ep-date { opacity:0.75; }

/* --- Main --- */
.main {
  flex:1; overflow-y:auto; background:#F4F3EF;
  scroll-behavior:smooth;
}

/* --- Welcome --- */
.welcome {
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  height:100%; color:#bbb; font-family:'Outfit',sans-serif; gap:10px;
}
.welcome-icon { font-size:44px; opacity:0.25; }
.welcome-title { font-size:20px; font-weight:600; color:#888; }
.welcome-sub { font-size:13px; }

/* --- Spinner --- */
.spinner {
  display:flex; justify-content:center; align-items:center; height:100%;
}
.spinner-ring {
  width:32px; height:32px;
  border:3px solid #E5E2D9; border-top-color:#E3120B;
  border-radius:50%;
  animation:spin 0.7s linear infinite;
}
@keyframes spin { to { transform:rotate(360deg); } }

/* --- Article --- */
.article-wrap {
  max-width:780px; margin:0 auto; padding:36px 28px 80px;
  animation: contentIn 0.3s ease;
}
@keyframes contentIn {
  from { opacity:0; transform:translateY(10px); }
  to { opacity:1; transform:translateY(0); }
}

/* --- Episode Header --- */
.ep-header {
  background:#FDFCF9; border:1px solid #E5E2D9; border-radius:12px;
  padding:26px 28px; margin-bottom:24px; position:relative; overflow:hidden;
  box-shadow:0 1px 8px rgba(0,0,0,0.03);
}
.header-accent {
  position:absolute; top:0; left:0; right:0; height:3px;
}
.header-channel {
  font-family:'Outfit',sans-serif; font-size:10.5px; font-weight:600;
  letter-spacing:0.05em; text-transform:uppercase; margin-bottom:8px;
}
.header-title {
  font-family:'Source Serif 4',Georgia,serif;
  font-size:26px; font-weight:600; line-height:1.25;
  margin:0 0 12px; letter-spacing:-0.015em; color:#1a1a1a;
}
.header-meta {
  font-family:'Outfit',sans-serif; font-size:12.5px; color:#999;
  display:flex; align-items:center; flex-wrap:wrap;
}
.meta-dot { margin:0 9px; opacity:0.35; }
.meta-link { text-decoration:none; font-weight:500; }

/* --- Footer --- */
.ep-footer {
  border-top:1px solid #E5E2D9; padding-top:18px; margin-top:36px;
  font-family:'Outfit',sans-serif; font-size:11px; color:#ccc; text-align:center;
}

/* ===================================================
   CONTENT AREA — styles for rendered markdown HTML
   Only targets bare elements without inline styles.
   Inline-styled divs from markdown pass through untouched.
   =================================================== */

.ep-content h1 {
  font-family:'Source Serif 4',Georgia,serif;
  font-size:24px; font-weight:700; line-height:1.3;
  margin:36px 0 14px; color:#1a1a1a;
}
.ep-content h2 {
  font-family:'Source Serif 4',Georgia,serif;
  font-size:21px; font-weight:600; line-height:1.3;
  margin:32px 0 12px; color:#1a1a1a;
  padding-bottom:8px;
  border-bottom:2px solid #E3120B;
}
.ep-content h3 {
  font-family:'Source Serif 4',Georgia,serif;
  font-size:17px; font-weight:600; margin:24px 0 10px; color:#1a1a1a;
}
.ep-content p {
  font-size:15.5px; line-height:1.7; margin:14px 0; color:#2a2a2a;
}
.ep-content strong { color:#1a1a1a; font-weight:600; }
.ep-content em { font-style:italic; }

/* Key quote: ***bold italic*** renders as strong>em or em>strong */
.ep-content p strong em,
.ep-content p em strong {
  display:block;
  background:linear-gradient(135deg,#1f2937 0%,#111827 100%);
  color:white !important;
  padding:24px 28px;
  border-radius:12px;
  font-size:17px; font-style:italic; text-align:center;
  margin:20px 0; font-weight:500; line-height:1.55;
  box-shadow:0 4px 12px rgba(0,0,0,0.15);
}

.ep-content ol, .ep-content ul {
  margin:12px 0; padding-left:24px; color:#2a2a2a;
  font-size:15px; line-height:1.65;
}
.ep-content li { margin-bottom:6px; }

.ep-content blockquote {
  font-family:'JetBrains Mono',monospace;
  background:linear-gradient(135deg,#f3f4f6 0%,#e5e7eb 100%);
  border-left:3px solid #006BA2;
  border-radius:0 12px 12px 0;
  margin:20px 0; padding:18px 20px;
  font-style:italic; color:#006BA2;
}
.ep-content blockquote p { margin:0 0 6px; }
.ep-content blockquote p:last-child { margin:0; }

.ep-content hr {
  border:none; height:1px; background:#E5E2D9; margin:28px 0;
}

.ep-content table {
  width:100%; border-collapse:collapse; margin:16px 0; font-size:14px;
}
.ep-content th {
  text-align:left; padding:10px 14px; background:#F4F3EF;
  border-bottom:2px solid #E5E2D9;
  font-family:'Outfit',sans-serif; font-weight:600; font-size:12px;
  text-transform:uppercase; letter-spacing:0.04em; color:#888;
}
.ep-content td {
  padding:10px 14px; border-bottom:1px solid #EDEBE5; vertical-align:top;
}

.ep-content code {
  background:#EDEBE5; padding:2px 5px; border-radius:3px;
  font-family:'JetBrains Mono',monospace; font-size:13px;
}
.ep-content pre {
  background:#EDEBE5; padding:16px; border-radius:8px;
  overflow-x:auto; margin:16px 0;
}
.ep-content pre code { background:none; padding:0; }

/* Force white text inside dark-bg divs from markdown */
.ep-content div[style*="background: linear-gradient(135deg, #1f2937"],
.ep-content div[style*="background: linear-gradient(135deg, #1f2937"] *,
.ep-content div[style*="background: linear-gradient(135deg, #111827"],
.ep-content div[style*="background: linear-gradient(135deg, #111827"] * {
  color:white !important;
}

/* --- Guest Card (injected by JS) --- */
.guest-card {
  border:1px solid; border-radius:12px;
  padding:18px 22px; margin:16px 0 20px;
  font-size:15px; line-height:1.65; color:#444;
}
.guest-label {
  font-family:'Outfit',sans-serif; font-size:10.5px; font-weight:700;
  text-transform:uppercase; letter-spacing:0.06em; margin-bottom:6px;
}

/* --- Contents Card (injected by JS) --- */
.contents-card {
  background:#FDFCF9; border:1px solid #E5E2D9; border-radius:12px;
  padding:18px 22px; margin:16px 0 20px;
  box-shadow:0 1px 4px rgba(0,0,0,0.03);
}
.contents-label {
  font-family:'Outfit',sans-serif; font-size:11px; font-weight:700;
  text-transform:uppercase; letter-spacing:0.06em; margin-bottom:10px;
  color:#E3120B;
}
.contents-card ol {
  margin:0; padding-left:20px;
  font-family:'Outfit',sans-serif; font-size:14px; line-height:1.7; color:#555;
}

/* --- Key Quote Card (injected by JS) --- */
.key-quote-card {
  background:#1a1a1a; border-radius:12px;
  padding:32px 28px; margin:16px 0 20px; position:relative;
}
.kq-mark {
  position:absolute; top:14px; left:22px;
  font-size:48px; line-height:1; opacity:0.45;
  font-family:Georgia,serif;
}
.kq-text {
  font-size:18px; font-style:italic; line-height:1.6;
  color:#E5E2D9; text-align:center; padding:8px 16px 0;
  font-weight:400;
}

/* ===================================================
   RESPONSIVE
   =================================================== */
@media (max-width:1024px) {
  .mobile-toggle { display:flex; }
  .sidebar {
    position:fixed; left:0; top:0; height:100vh;
    transform:translateX(-100%); z-index:90;
    box-shadow:none;
  }
  .sidebar.mobile-open {
    transform:translateX(0);
    box-shadow:4px 0 20px rgba(0,0,0,0.12);
  }
  .sidebar.hidden { transform:translateX(-100%); width:272px; min-width:272px; }
  .main { margin-left:0; }
  .article-wrap { padding:70px 18px 60px; }
  .header-title { font-size:22px; }
  .ep-content h2 { font-size:18px; }
  .ep-content p { font-size:14.5px; }
}

@media (max-width:480px) {
  .sidebar { width:100%; min-width:100%; }
  .article-wrap { padding:60px 14px 50px; }
  .header-title { font-size:20px; }
  .ep-header { padding:20px 18px; }
}
'''

    def generate_viewer(self, output_file: str = "index.html"):
        print("Scanning for podcast episodes...")
        self.scan_episodes()

        print(f"Found {len(self.episodes)} episodes across {len(self.channels)} channels:")
        for channel, eps in self.channels.items():
            recent_indicator = " 🟢" if channel in self.recent_channels else ""
            print(f"  - {channel}: {len(eps)} episodes{recent_indicator}")

        if self.recent_channels:
            print(f"\nChannels with episodes in the last week ({len(self.recent_channels)}):")
            for channel in sorted(self.recent_channels):
                print(f"  🟢 {channel}")

        print("Generating HTML viewer...")
        html_content = self.generate_html()

        output_path = Path(output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        print(f"✅ Podcast viewer generated successfully: {output_path}")
        print(f"Open {output_path} in your browser to view the podcast analysis.")
        return str(output_path)


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Generate a modern podcast analysis viewer"
    )
    parser.add_argument(
        "--directory", "-d",
        default="/Users/rahulchaudhary/youtube_subs_extractor/output",
        help="Directory containing podcast .txt and .md files",
    )
    parser.add_argument(
        "--output", "-o",
        default="index.html",
        help="Output HTML file name (default: index.html)",
    )
    args = parser.parse_args()

    analyzer = PodcastAnalyzer(args.directory)
    analyzer.generate_viewer(args.output)


if __name__ == "__main__":
    main()
