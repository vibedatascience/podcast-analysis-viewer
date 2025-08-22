#!/usr/bin/env python3
"""
Podcast Analysis Viewer - Ultra Clean Editorial Style
Programmatically generates a beautiful web interface for viewing podcast analysis
"""

import os
import re
import markdown
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import json

class PodcastAnalyzer:
    def __init__(self, directory: str = "output"):
        self.directory = Path(directory)
        self.episodes = []
        self.channels = {}
        
    def extract_metadata_from_txt(self, txt_file: Path) -> Dict:
        """Extract metadata from TXT file"""
        try:
            with open(txt_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            metadata = {}
            
            title_match = re.search(r'TITLE:\s*(.+)', content)
            if title_match:
                metadata['title'] = title_match.group(1).strip()
            
            channel_match = re.search(r'CHANNEL:\s*(.+)', content)
            if channel_match:
                metadata['channel'] = channel_match.group(1).strip()
            
            published_match = re.search(r'PUBLISHED:\s*(.+)', content)
            if published_match:
                metadata['published'] = published_match.group(1).strip()
            
            duration_match = re.search(r'DURATION:\s*(.+)', content)
            if duration_match:
                metadata['duration'] = duration_match.group(1).strip()
            
            views_match = re.search(r'VIEWS:\s*(.+)', content)
            if views_match:
                metadata['views'] = views_match.group(1).strip()
            
            url_match = re.search(r'URL:\s*(.+)', content)
            if url_match:
                metadata['url'] = url_match.group(1).strip()
            
            return metadata
            
        except Exception as e:
            print(f"Error reading {txt_file}: {e}")
            return {}
    
    def load_markdown_content(self, md_file: Path) -> str:
        """Load and return markdown content"""
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            print(f"Error reading {md_file}: {e}")
            return ""
    
    def scan_episodes(self):
        """Scan directory for podcast episode files"""
        self.episodes = []
        self.channels = {}
        
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
                'md_content': md_content
            }
            
            self.episodes.append(episode)
            
            channel = metadata.get('channel', 'Unknown')
            if channel not in self.channels:
                self.channels[channel] = []
            self.channels[channel].append(episode)
        
        self.episodes.sort(key=lambda x: x['metadata'].get('published', ''), reverse=True)
        
        for channel in self.channels:
            self.channels[channel].sort(key=lambda x: x['metadata'].get('published', ''), reverse=True)
    
    def generate_css(self) -> str:
        """Generate CSS styles for the Ultra Clean Editorial viewer"""
        return """
        @import url('https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600&display=swap');
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Crimson Text', Georgia, serif;
            line-height: 1.6;
            color: #000;
            background: #fff;
        }
        
        .container {
            display: flex;
            min-height: 100vh;
        }
        
        .sidebar {
            width: 320px;
            background: #fff;
            border-right: 1px solid #000;
            padding: 0;
            overflow-y: auto;
            position: fixed;
            height: 100vh;
        }
        
        .sidebar-header {
            padding: 50px 40px 40px 40px;
        }
        
        .sidebar h1 {
            font-size: 32px;
            font-weight: 300;
            margin: 0;
            font-family: 'Inter', -apple-system, sans-serif;
            letter-spacing: -0.5px;
        }
        
        .sidebar-content {
            padding: 0 40px 40px 40px;
        }
        
        .channel {
            margin-bottom: 35px;
        }
        
        .channel-name {
            font-size: 10px;
            font-weight: 600;
            margin: 0 0 15px 0;
            color: #000;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-family: 'Inter', -apple-system, sans-serif;
            cursor: default;
        }
        
        .episode-item {
            padding: 0;
            margin: 0 0 12px 0;
            background: transparent;
            cursor: pointer;
            font-size: 16px;
            line-height: 1.4;
            transition: none;
            color: #000;
        }
        
        .episode-item:hover {
            text-decoration: underline;
            text-underline-offset: 2px;
        }
        
        .episode-item.active {
            font-weight: 600;
            text-decoration: none;
        }
        
        .episode-title {
            font-weight: inherit;
            font-size: inherit;
            line-height: inherit;
            margin: 0;
        }
        
        .episode-date {
            display: none;
        }
        
        .main-content {
            flex: 1;
            margin-left: 320px;
            padding: 80px;
            background: #fff;
            min-height: 100vh;
        }
        
        .episode-container {
            max-width: 720px;
            margin: 0 auto;
        }
        
        .episode-header {
            margin-bottom: 60px;
            padding: 0;
            background: none;
            border: none;
            box-shadow: none;
        }
        
        .header-title {
            font-size: 48px;
            font-weight: 400;
            margin-bottom: 20px;
            line-height: 1.2;
            color: #000;
            font-family: 'Crimson Text', Georgia, serif;
        }
        
        .episode-meta {
            color: #666;
            font-size: 15px;
            line-height: 1.6;
            font-family: 'Inter', -apple-system, sans-serif;
            font-weight: 400;
        }
        
        .meta-separator {
            margin: 0 8px;
            color: #999;
        }
        
        .episode-content {
            font-size: 20px;
            line-height: 1.8;
            color: #000;
        }
        
        .guest-info {
            font-size: 18px;
            margin: 40px 0;
            padding: 0;
            background: none;
            border: none;
            border-radius: 0;
            color: #666;
            font-style: italic;
        }
        
        .key-quote {
            font-size: 32px;
            line-height: 1.4;
            font-style: italic;
            border-left: 3px solid #000;
            padding-left: 40px;
            margin: 60px 0;
            background: none;
            color: #000;
            text-align: left;
            border-radius: 0;
            box-shadow: none;
        }
        
        .contents-list {
            margin: 50px 0;
            padding: 0;
            background: none;
            border: none;
            border-radius: 0;
        }
        
        .contents-list h3 {
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-family: 'Inter', -apple-system, sans-serif;
            font-weight: 600;
            margin-bottom: 20px;
            color: #000;
        }
        
        .contents-list ol {
            margin: 0;
            padding-left: 0;
            list-style: none;
            counter-reset: item;
        }
        
        .contents-list li {
            counter-increment: item;
            margin-bottom: 12px;
            padding-left: 30px;
            position: relative;
            font-size: 18px;
            line-height: 1.6;
        }
        
        .contents-list li::before {
            content: counter(item);
            position: absolute;
            left: 0;
            font-family: 'Inter', -apple-system, sans-serif;
            font-size: 14px;
            color: #666;
        }
        
        .episode-content h1 {
            font-size: 36px;
            font-weight: 400;
            margin: 80px 0 30px 0;
            color: #000;
            border: none;
            padding: 0;
            font-family: 'Crimson Text', Georgia, serif;
        }
        
        .episode-content h2 {
            font-size: 11px;
            text-transform: uppercase;
            letter-spacing: 2px;
            font-family: 'Inter', -apple-system, sans-serif;
            font-weight: 600;
            margin: 60px 0 25px 0;
            color: #000;
            border: none;
            padding: 0;
        }
        
        .episode-content h3 {
            font-size: 24px;
            font-weight: 400;
            margin: 40px 0 20px 0;
            color: #000;
            font-family: 'Crimson Text', Georgia, serif;
        }
        
        .episode-content p {
            margin: 0 0 25px 0;
            text-align: left;
            line-height: 1.8;
            color: #000;
        }
        
        .episode-content blockquote {
            font-size: 24px;
            line-height: 1.5;
            font-style: italic;
            border-left: 2px solid #000;
            margin: 40px 0;
            padding-left: 30px;
            background: none;
            border-radius: 0;
            box-shadow: none;
            color: #000;
        }
        
        .episode-content blockquote p {
            margin-bottom: 0;
        }
        
        .episode-content strong {
            color: #000;
            font-weight: 600;
        }
        
        .episode-content em {
            color: #000;
            font-style: italic;
        }
        
        .episode-content ol, .episode-content ul {
            margin: 30px 0;
            padding-left: 0;
            color: #000;
        }
        
        .episode-content li {
            margin-bottom: 12px;
            line-height: 1.8;
            margin-left: 30px;
        }
        
        .episode-content code {
            background: #f5f5f5;
            padding: 2px 6px;
            border-radius: 2px;
            font-family: 'SF Mono', Monaco, monospace;
            font-size: 16px;
        }
        
        .episode-content pre {
            background: #f5f5f5;
            padding: 20px;
            border-radius: 0;
            overflow-x: auto;
            margin: 30px 0;
            border-left: 2px solid #000;
        }
        
        .episode-content pre code {
            background: none;
            padding: 0;
        }
        
        .welcome-message {
            text-align: center;
            padding: 100px 20px;
        }
        
        .welcome-message h2 {
            font-size: 36px;
            margin-bottom: 20px;
            color: #000;
            font-weight: 400;
            font-family: 'Crimson Text', Georgia, serif;
        }
        
        .welcome-message p {
            font-size: 18px;
            color: #666;
            max-width: 500px;
            margin: 0 auto;
            font-family: 'Inter', -apple-system, sans-serif;
        }
        
        .loading-spinner {
            width: 40px;
            height: 40px;
            margin: 100px auto;
            border: 2px solid #f0f0f0;
            border-top-color: #000;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .mobile-menu-toggle {
            display: none;
            position: fixed;
            top: 30px;
            left: 30px;
            z-index: 1001;
            background: #000;
            color: #fff;
            border: none;
            border-radius: 0;
            padding: 12px 16px;
            cursor: pointer;
            font-family: 'Inter', -apple-system, sans-serif;
            font-size: 14px;
            font-weight: 500;
        }
        
        @media (max-width: 1024px) {
            .main-content {
                padding: 60px 40px;
            }
        }
        
        @media (max-width: 768px) {
            .mobile-menu-toggle {
                display: block;
            }
            
            .sidebar {
                width: 100%;
                max-width: 380px;
                transform: translateX(-100%);
                transition: transform 0.3s ease;
                z-index: 1000;
                box-shadow: 0 0 30px rgba(0,0,0,0.1);
            }
            
            .sidebar.open {
                transform: translateX(0);
            }
            
            .sidebar-overlay {
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background: rgba(255, 255, 255, 0.9);
                z-index: 999;
            }
            
            .sidebar-overlay.show {
                display: block;
            }
            
            .main-content {
                margin-left: 0;
                padding: 100px 30px 50px 30px;
            }
            
            .header-title {
                font-size: 36px;
            }
            
            .episode-content {
                font-size: 18px;
            }
            
            .key-quote {
                font-size: 24px;
                padding-left: 20px;
                margin: 40px 0;
            }
            
            .episode-content h1 {
                font-size: 28px;
            }
            
            .episode-content h3 {
                font-size: 20px;
            }
            
            .episode-content blockquote {
                font-size: 20px;
                padding-left: 20px;
            }
        }
        
        @media (max-width: 480px) {
            .sidebar {
                width: 100%;
                max-width: none;
            }
            
            .main-content {
                padding: 80px 20px 40px 20px;
            }
            
            .header-title {
                font-size: 28px;
            }
            
            .episode-content {
                font-size: 16px;
            }
            
            .episode-meta {
                font-size: 13px;
            }
        }
        """
    
    def generate_javascript(self) -> str:
        """Generate JavaScript for interactivity"""
        episodes_json = []
        for episode in self.episodes:
            episodes_json.append({
                'title': episode['metadata'].get('title', 'Unknown Title'),
                'channel': episode['metadata'].get('channel', 'Unknown Channel'),
                'published': episode['metadata'].get('published', 'Unknown Date'),
                'duration': episode['metadata'].get('duration', 'Unknown Duration'),
                'views': episode['metadata'].get('views', 'Unknown Views'),
                'url': episode['metadata'].get('url', ''),
                'content': markdown.markdown(episode['md_content'], extensions=['tables', 'fenced_code'])
            })
        
        return f"""
        const episodes = {json.dumps(episodes_json, indent=2)};
        
        function showEpisode(episodeIndex) {{
            const episode = episodes[episodeIndex];
            if (!episode) return;
            
            document.querySelectorAll('.episode-item').forEach(item => {{
                item.classList.remove('active');
            }});
            document.querySelector(`[data-episode="${{episodeIndex}}"]`).classList.add('active');
            
            let processedContent = episode.content;
            
            processedContent = processedContent.replace(
                /<p><strong>Contents Covered:<\\/strong>([\\s\\S]*?)(?=<\\/p>|<p><strong>|<h\\d|$)/gi,
                (match, content) => {{
                    let items = [];
                    
                    const lines = content.split(/\\n|<br\\s*\\/?>/).filter(line => line.trim());
                    lines.forEach(line => {{
                        line = line.replace(/<[^>]*>/g, '').trim();
                        if (line.match(/^\\d+\\./)) {{
                            const cleaned = line.replace(/^\\d+\\.\\s*/, '').trim();
                            if (cleaned) items.push(cleaned);
                        }}
                    }});
                    
                    if (items.length === 0) {{
                        lines.forEach(line => {{
                            const cleaned = line.replace(/<[^>]*>/g, '').trim();
                            if (cleaned && cleaned !== 'Contents Covered:') {{
                                items.push(cleaned);
                            }}
                        }});
                    }}
                    
                    const itemsHtml = items.map(item => 
                        `<li>${{item}}</li>`
                    ).join('');
                    
                    return `<div class="contents-list">
                        <h3>Contents Covered</h3>
                        <ol>${{itemsHtml}}</ol>
                    </div>`;
                }}
            );
            
            processedContent = processedContent.replace(
                /<p><strong>Contents Covered:<\\/strong><\\/p>\\s*<ol>([\\s\\S]*?)<\\/ol>/gi,
                (match, listContent) => {{
                    return `<div class="contents-list">
                        <h3>Contents Covered</h3>
                        <ol>${{listContent}}</ol>
                    </div>`;
                }}
            );
            
            processedContent = processedContent.replace(
                /<p><strong>Guest:<\\/strong>([^<]*)<\\/p>/gi,
                (match, guestInfo) => {{
                    return `<div class="guest-info">Guest: ${{guestInfo.trim()}}</div>`;
                }}
            );
            
            processedContent = processedContent.replace(
                /<p><strong>Key Quote:<\\/strong>([\\s\\S]*?)<\\/p>/gi,
                (match, quote) => {{
                    const cleanQuote = quote
                        .replace(/<strong>|<\\/strong>/g, '')
                        .replace(/<em>|<\\/em>/g, '')
                        .replace(/<br\\s*\\/?>/g, ' ')
                        .replace(/\\*\\*\\*/g, '')
                        .trim();
                    
                    return `<div class="key-quote">"${{cleanQuote}}"</div>`;
                }}
            );
            
            processedContent = processedContent.replace(
                /<p><strong>Detailed Analysis:<\\/strong><\\/p>/gi,
                ''
            );
            
            const mainContent = document.querySelector('.main-content');
            
            mainContent.innerHTML = '<div class="loading-spinner"></div>';
            
            setTimeout(() => {{
                mainContent.innerHTML = `
                    <div class="episode-container">
                        <div class="episode-header">
                            <h1 class="header-title">${{episode.title}}</h1>
                            <div class="episode-meta">
                                ${{episode.published}}<span class="meta-separator">·</span>${{episode.duration}}${{episode.views ? `<span class="meta-separator">·</span>${{Number(episode.views.replace(/,/g, '')).toLocaleString()}} views` : ''}}
                            </div>
                        </div>
                        <div class="episode-content">
                            ${{processedContent}}
                        </div>
                    </div>
                `;
            }}, 300);
            
            window.scrollTo(0, 0);
        }}
        
        document.addEventListener('DOMContentLoaded', function() {{
            document.querySelectorAll('.episode-item').forEach((item, index) => {{
                item.addEventListener('click', () => showEpisode(index));
            }});
            
            if (episodes.length > 0) {{
                showEpisode(0);
            }}
        }});
        """
    
    def generate_html(self) -> str:
        """Generate the complete HTML viewer"""
        sidebar_html = ""
        episode_index = 0
        
        for channel_name, channel_episodes in self.channels.items():
            sidebar_html += f'<div class="channel">\n'
            sidebar_html += f'  <div class="channel-name">{channel_name}</div>\n'
            
            for episode in channel_episodes:
                title = episode['metadata'].get('title', 'Unknown Title')
                
                display_title = title if len(title) <= 50 else title[:47] + "..."
                
                sidebar_html += f'''
                    <div class="episode-item" data-episode="{episode_index}">
                        <div class="episode-title">{display_title}</div>
                    </div>
                '''
                episode_index += 1
            
            sidebar_html += '</div>\n'
        
        welcome_content = '''
        <div class="welcome-message">
            <h2>Select a Podcast</h2>
            <p>Choose an episode from the sidebar to view the analysis.</p>
        </div>
        ''' if self.episodes else '''
        <div class="welcome-message">
            <h2>No Episodes Found</h2>
            <p>Make sure you have both .txt and .md files in the directory.</p>
        </div>
        '''
        
        html_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Podcast Analysis</title>
            <style>
                {self.generate_css()}
            </style>
        </head>
        <body>
            <button class="mobile-menu-toggle" onclick="toggleMobileMenu()">Menu</button>
            <div class="sidebar-overlay" onclick="closeMobileMenu()"></div>
            
            <div class="container">
                <div class="sidebar" id="sidebar">
                    <div class="sidebar-header">
                        <h1>Podcasts.</h1>
                    </div>
                    <div class="sidebar-content">
                        {sidebar_html}
                    </div>
                </div>
                <div class="main-content">
                    {welcome_content}
                </div>
            </div>
            
            <script>
                {self.generate_javascript()}
                
                function toggleMobileMenu() {{
                    const sidebar = document.getElementById('sidebar');
                    const overlay = document.querySelector('.sidebar-overlay');
                    sidebar.classList.toggle('open');
                    overlay.classList.toggle('show');
                }}
                
                function closeMobileMenu() {{
                    const sidebar = document.getElementById('sidebar');
                    const overlay = document.querySelector('.sidebar-overlay');
                    sidebar.classList.remove('open');
                    overlay.classList.remove('show');
                }}
                
                document.addEventListener('click', function(e) {{
                    if (e.target.closest('.episode-item')) {{
                        if (window.innerWidth <= 768) {{
                            closeMobileMenu();
                        }}
                    }}
                }});
            </script>
        </body>
        </html>
        """
        
        return html_template
    
    def generate_viewer(self, output_file: str = "podcast_viewer.html"):
        """Generate the complete podcast analysis viewer"""
        print("Scanning for podcast episodes...")
        self.scan_episodes()
        
        print(f"Found {len(self.episodes)} episodes across {len(self.channels)} channels:")
        for channel, episodes in self.channels.items():
            print(f"  - {channel}: {len(episodes)} episodes")
        
        print("Generating HTML viewer...")
        html_content = self.generate_html()
        
        output_path = Path(output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ Podcast viewer generated successfully: {output_path}")
        print(f"Open {output_path} in your web browser to view the podcast analysis.")
        
        return str(output_path)

def main():
    """Main function to run the podcast analyzer"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate a beautiful podcast analysis viewer")
    parser.add_argument("--directory", "-d", default="output", 
                       help="Directory containing podcast files (default: output directory)")
    parser.add_argument("--output", "-o", default="podcast_viewer.html",
                       help="Output HTML file name (default: podcast_viewer.html)")
    
    args = parser.parse_args()
    
    analyzer = PodcastAnalyzer(args.directory)
    output_file = analyzer.generate_viewer(args.output)
    
    return output_file

if __name__ == "__main__":
    main()