#!/usr/bin/env python3
"""
Podcast Analysis Viewer
Programmatically generates a beautiful web interface for viewing podcast analysis
"""

import os
import re
import markdown
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import json

class PodcastAnalyzer:
    def __init__(self, directory: str = "output"):
        self.directory = Path(directory)
        self.episodes = []
        self.channels = {}
        self.recent_channels = set()
        
    def extract_metadata_from_txt(self, txt_file: Path) -> Dict:
        """Extract metadata from TXT file"""
        try:
            with open(txt_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            metadata = {}
            
            # Extract title
            title_match = re.search(r'TITLE:\s*(.+)', content)
            if title_match:
                metadata['title'] = title_match.group(1).strip()
            
            # Extract channel
            channel_match = re.search(r'CHANNEL:\s*(.+)', content)
            if channel_match:
                metadata['channel'] = channel_match.group(1).strip()
            
            # Extract published date
            published_match = re.search(r'PUBLISHED:\s*(.+)', content)
            if published_match:
                metadata['published'] = published_match.group(1).strip()
            
            # Extract duration
            duration_match = re.search(r'DURATION:\s*(.+)', content)
            if duration_match:
                metadata['duration'] = duration_match.group(1).strip()
            
            # Extract views
            views_match = re.search(r'VIEWS:\s*(.+)', content)
            if views_match:
                metadata['views'] = views_match.group(1).strip()
            
            # Extract URL
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
        self.recent_channels = set()
        
        # Calculate date threshold for "recent" episodes (1 week from today)
        today = datetime.now()
        one_week_ago = today - timedelta(days=7)
        
        # Find all TXT files
        txt_files = list(self.directory.glob("*.txt"))
        
        for txt_file in txt_files:
            # Skip if not a podcast episode file
            if not re.match(r'\d{4}-\d{2}-\d{2}_', txt_file.name):
                continue
                
            # Extract metadata
            metadata = self.extract_metadata_from_txt(txt_file)
            if not metadata:
                continue
            
            # Find corresponding MD file
            md_filename = txt_file.stem + "_claude_artifact.md"
            md_file = self.directory / md_filename
            
            if not md_file.exists():
                print(f"Warning: No corresponding MD file found for {txt_file.name}")
                continue
            
            # Load markdown content
            md_content = self.load_markdown_content(md_file)
            
            episode = {
                'txt_file': txt_file,
                'md_file': md_file,
                'metadata': metadata,
                'md_content': md_content
            }
            
            self.episodes.append(episode)
            
            # Group by channel
            channel = metadata.get('channel', 'Unknown')
            if channel not in self.channels:
                self.channels[channel] = []
            self.channels[channel].append(episode)
            
            # Check if this episode is recent (within last week)
            published_str = metadata.get('published', '')
            if published_str:
                try:
                    # Try common date formats
                    episode_date = None
                    for date_format in ['%Y-%m-%d', '%d/%m/%Y', '%m/%d/%Y', '%B %d, %Y']:
                        try:
                            episode_date = datetime.strptime(published_str, date_format)
                            break
                        except ValueError:
                            continue
                    
                    # If we found a valid date and it's recent, mark this channel as recent
                    if episode_date and episode_date >= one_week_ago:
                        self.recent_channels.add(channel)
                except Exception as e:
                    pass  # Skip date parsing errors
        
        # Sort episodes by date (newest first)
        self.episodes.sort(key=lambda x: x['metadata'].get('published', ''), reverse=True)
        
        # Sort episodes within each channel
        for channel in self.channels:
            self.channels[channel].sort(key=lambda x: x['metadata'].get('published', ''), reverse=True)
        
        # Sort channels by their latest episode date
        sorted_channels = sorted(
            self.channels.items(),
            key=lambda x: x[1][0]['metadata'].get('published', '') if x[1] else '',
            reverse=True
        )
        self.channels = dict(sorted_channels)
    
    def generate_css(self) -> str:
        """Generate CSS styles for the viewer"""
        return """
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:ital@0;1&display=swap');
        
        :root {
            --primary: #2563eb;
            --primary-dark: #1d4ed8;
            --secondary: #64748b;
            --accent: #f59e0b;
            --bg: #f8fafc;
            --surface: #ffffff;
            --surface-hover: #f1f5f9;
            --text: #1e293b;
            --text-light: #64748b;
            --border: #e2e8f0;
            --shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1), 0 1px 2px -1px rgb(0 0 0 / 0.1);
            --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Arial, sans-serif;
            line-height: 1.6;
            color: var(--text);
            background-color: var(--bg);
        }
        
        .container {
            display: flex;
            min-height: 100vh;
        }
        
        .sidebar {
            width: 300px;
            background: var(--surface);
            border-right: 1px solid var(--border);
            padding: 0;
            overflow-y: auto;
            position: fixed;
            height: 100vh;
            box-shadow: var(--shadow);
        }
        
        .sidebar-header {
            padding: 16px 20px 12px 20px;
            border-bottom: 1px solid var(--border);
            background: var(--surface-hover);
        }
        
        .coffee-link {
            display: inline-flex;
            align-items: center;
            gap: 4px;
            font-size: 10px;
            color: var(--text-light);
            text-decoration: none;
            opacity: 0.6;
            transition: opacity 0.2s ease;
            margin-top: 8px;
        }
        
        .coffee-link:hover {
            opacity: 1;
            color: var(--primary);
        }
        
        .coffee-icon {
            width: 12px;
            height: 12px;
            filter: opacity(0.6);
        }
        
        .sidebar h1 {
            font-size: 13px;
            font-weight: 600;
            color: var(--text-light);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin: 0;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        
        .sidebar-icon {
            width: 16px;
            height: 16px;
            background: url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTYiIGhlaWdodD0iMTYiIHZpZXdCb3g9IjAgMCAxNiAxNiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTcgN0M3IDUuODk1NDMgNi4xMDQ1NyA1IDUgNUM1IDUuODk1NDMgNC4xMDQ1NyA3IDMgN0MzIDguMTA0NTcgMy44OTU0MyA5IDUgOUM2LjEwNDU3IDkgNyA4LjEwNDU3IDcgN1oiIHN0cm9rZT0iIzZlNmU3MyIgc3Ryb2tlLXdpZHRoPSIxLjIiLz4KPHN0cm9rZSBzdHJva2U9IiM2ZTZlNzMiIGQ9Im03IDcgNC41IDQuNSIgc3Ryb2tlLXdpZHRoPSIxLjIiLz4KPC9zdmc+') no-repeat center;
        }
        
        .sidebar-content {
            padding: 8px 0;
        }
        
        .channel {
            margin-bottom: 0;
        }
        
        .channel-name {
            font-size: 12px;
            font-weight: 600;
            margin: 0;
            padding: 8px 20px 4px 20px;
            color: var(--secondary);
            text-transform: uppercase;
            letter-spacing: 0.3px;
            background: none;
            border: none;
            border-radius: 0;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: background-color 0.15s ease;
        }
        
        .channel-recent-badge {
            font-size: 8px;
            font-weight: 700;
            padding: 2px 4px;
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: white;
            border-radius: 6px;
            flex-shrink: 0;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            box-shadow: 0 2px 4px rgba(16, 185, 129, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.2);
            animation: glow-pulse 2s ease-in-out infinite;
            border: 1px solid rgba(255, 255, 255, 0.1);
            margin-left: auto;
        }
        
        @keyframes glow-pulse {
            0%, 100% { 
                box-shadow: 0 2px 4px rgba(16, 185, 129, 0.3), 
                           inset 0 1px 0 rgba(255, 255, 255, 0.2),
                           0 0 8px rgba(16, 185, 129, 0.4);
                transform: scale(1);
            }
            50% { 
                box-shadow: 0 2px 6px rgba(16, 185, 129, 0.4), 
                           inset 0 1px 0 rgba(255, 255, 255, 0.3),
                           0 0 12px rgba(16, 185, 129, 0.6);
                transform: scale(1.05);
            }
        }
        
        .channel-name:hover {
            background: var(--surface-hover);
        }
        
        .channel-arrow {
            font-size: 10px;
            transition: transform 0.15s ease;
            color: var(--secondary);
        }
        
        .channel-arrow.expanded {
            transform: rotate(90deg);
        }
        
        .channel-episodes {
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.25s ease;
        }
        
        .channel-episodes.expanded {
            max-height: 1000px;
        }
        
        .episode-item {
            padding: 4px 20px 4px 28px;
            margin: 0;
            background: transparent;
            border-radius: 0;
            cursor: pointer;
            transition: background-color 0.15s ease;
            font-size: 11px;
            border: none;
            display: flex;
            align-items: center;
            gap: 6px;
            color: var(--text);
        }
        
        .episode-item:hover {
            background: var(--surface-hover);
            transform: none;
        }
        
        .episode-item.active {
            background: var(--primary);
            color: white;
        }
        
        .episode-icon {
            width: 12px;
            height: 12px;
            background: url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iNiIgY3k9IjYiIHI9IjUiIHN0cm9rZT0iIzY5Njk2OSIgc3Ryb2tlLXdpZHRoPSIxLjIiIGZpbGw9Im5vbmUiLz4KPHBhdGggZD0iTTQuNSAzLjVWOC41TDguNSA2TDQuNSAzLjVaIiBmaWxsPSIjNjk2OTY5Ii8+Cjwvc3ZnPg==') no-repeat center;
            flex-shrink: 0;
        }
        
        .episode-item.active .episode-icon {
            background: url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPGNpcmNsZSBjeD0iNiIgY3k9IjYiIHI9IjUiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMS4yIiBmaWxsPSJub25lIi8+CjxwYXRoIGQ9Ik00LjUgMy41VjguNUw4LjUgNkw0LjUgMy41WiIgZmlsbD0id2hpdGUiLz4KPC9zdmc+') no-repeat center;
        }
        
        .episode-details {
            flex: 1;
            min-width: 0;
        }
        
        .episode-title {
            font-weight: 400;
            font-size: 11px;
            line-height: 1.4;
            margin-bottom: 1px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }
        
        .episode-date {
            font-size: 10px;
            opacity: 0.5;
            margin: 0;
        }
        
        .main-content {
            flex: 1;
            margin-left: 300px;
            padding: 40px;
            background: var(--bg);
            min-height: 100vh;
        }
        
        .episode-container {
            max-width: 800px;
            margin: 0 auto;
            background: var(--surface);
            border-radius: 12px;
            padding: 2rem;
            box-shadow: var(--shadow-lg);
        }
        
        .episode-header {
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 2rem;
            box-shadow: var(--shadow-lg);
            margin-bottom: 2rem;
            position: relative;
            overflow: hidden;
        }
        
        
        .header-title {
            font-size: 1.5rem;
            font-weight: 700;
            margin-bottom: 0.75rem;
            line-height: 1.3;
            color: var(--text);
            max-width: calc(100% - 50px);
        }
        
        .episode-meta {
            color: var(--text-light);
            font-size: 1rem;
            line-height: 1.4;
            font-weight: 500;
        }
        
        .meta-separator {
            margin: 0 0.75rem;
            opacity: 0.6;
        }
        
        .episode-content {
            max-width: none;
            margin: 0;
            font-size: 15px;
            line-height: 1.6;
            color: var(--text);
        }
        
        /* Document-style cards for all content sections */
        .content-card {
            background: linear-gradient(135deg, #f8fafc 0%, #f1f5f9 100%);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: var(--shadow);
            margin: 1.5rem 0;
            position: relative;
            overflow: hidden;
        }
        
        
        /* Guest Information Card */
        .guest-info {
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
            border: 1px solid #bfdbfe;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: var(--shadow);
            margin: 1.5rem 0;
            position: relative;
            overflow: hidden;
        }
        
        
        /* Key Quote - Document card style */
        .key-quote {
            background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
            color: white;
            border: 1px solid #374151;
            border-radius: 12px;
            padding: 2rem;
            box-shadow: var(--shadow-lg);
            font-size: 1.1rem;
            font-style: italic;
            text-align: center;
            margin: 1.5rem 0;
            position: relative;
            overflow: hidden;
        }
        
        
        /* Contents List Card */
        .contents-list {
            background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
            border: 1px solid #d1d5db;
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: var(--shadow);
            margin: 1.5rem 0;
            position: relative;
            overflow: hidden;
        }
        
        
        /* Section Quote Card */
        .section-quote {
            font-family: 'JetBrains Mono', monospace;
            background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
            border: 1px solid var(--primary);
            border-radius: 12px;
            padding: 1.5rem;
            box-shadow: var(--shadow);
            font-style: italic;
            color: var(--primary);
            margin: 1.5rem 0;
            position: relative;
            overflow: hidden;
        }
        
        
        .episode-content h1 {
            font-size: 24px;
            font-weight: 700;
            margin: 36px 0 16px 0;
            color: var(--text);
            border: none;
            padding: 0;
        }
        
        .episode-content h2 {
            color: var(--primary);
            border-bottom: 2px solid var(--primary);
            padding-bottom: 0.5rem;
            font-size: 1.3rem;
            font-weight: 600;
            margin: 32px 0 12px 0;
        }
        
        .episode-content h3 {
            font-size: 17px;
            font-weight: 600;
            margin: 24px 0 10px 0;
            color: var(--text);
        }
        
        .episode-content p {
            margin: 1rem 0;
            text-align: left;
            line-height: 1.6;
            color: var(--text);
        }
        
        /* Enhanced blockquotes */
        .episode-content blockquote {
            font-family: 'JetBrains Mono', monospace;
            background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
            border: 1px solid var(--primary);
            border-radius: 12px;
            margin: 1.5rem 0;
            padding: 1.5rem;
            box-shadow: var(--shadow);
            font-style: italic;
            color: var(--primary);
            position: relative;
            overflow: hidden;
        }
        
        
        .episode-content blockquote p {
            margin-bottom: 8px;
        }
        
        .episode-content blockquote p:last-child {
            margin-bottom: 0;
        }
        
        /* Style for key quotes (***text***) */
        .episode-content p strong em,
        .episode-content p em strong {
            display: block;
            background: #111827;
            color: white;
            padding: 2rem;
            border-radius: 12px;
            font-size: 1.1rem;
            font-style: italic;
            text-align: center;
            margin: 1.5rem -1rem;
            font-weight: 500;
        }
        
        .episode-content strong {
            color: var(--text);
            font-weight: 600;
        }
        
        .episode-content em {
            color: var(--primary);
            font-style: italic;
            font-weight: 500;
        }
        
        .episode-content ol, .episode-content ul {
            margin: 1rem 0;
            padding-left: 1.5rem;
            color: var(--text);
        }
        
        .episode-content li {
            margin-bottom: 8px;
            line-height: 1.6;
        }
        
        .episode-content code {
            background: #f5f5f7;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'SF Mono', Monaco, 'Courier New', monospace;
            font-size: 13px;
        }
        
        .episode-content pre {
            background: #f5f5f7;
            padding: 16px;
            border-radius: 6px;
            overflow-x: auto;
            margin: 20px 0;
        }
        
        .episode-content pre code {
            background: none;
            padding: 0;
        }
        
        .welcome-message {
            text-align: center;
            padding: 60px 20px;
            color: var(--text-light);
        }
        
        .welcome-message h2 {
            font-size: 2rem;
            margin-bottom: 15px;
            color: var(--text);
        }
        
        .welcome-message p {
            font-size: 1.1rem;
            max-width: 500px;
            margin: 0 auto;
        }
        
        /* Loading Spinner */
        .loading-spinner {
            width: 40px;
            height: 40px;
            margin: 40px auto;
            border: 4px solid var(--border);
            border-top-color: var(--primary);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* Mobile Menu Toggle */
        .mobile-menu-toggle {
            display: none;
            position: fixed;
            top: 20px;
            left: 20px;
            z-index: 1001;
            background: var(--primary);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px;
            cursor: pointer;
            box-shadow: var(--shadow);
            font-size: 16px;
            transition: all 0.2s ease;
            width: 44px;
            height: 44px;
            align-items: center;
            justify-content: center;
        }
        
        .mobile-menu-toggle:hover {
            background: var(--primary-dark);
            transform: scale(1.05);
        }
        
        .mobile-menu-toggle:active {
            transform: scale(0.95);
        }
        
        /* Hide button when sidebar is open */
        .mobile-menu-toggle.hidden {
            opacity: 0;
            pointer-events: none;
        }
        
        /* Mobile Responsive Design */
        @media (max-width: 768px) {
            .mobile-menu-toggle {
                display: flex;
            }
            
            .sidebar {
                width: 280px;
                transform: translateX(-100%);
                transition: transform 0.3s ease;
                z-index: 1000;
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
                background: rgba(0, 0, 0, 0.5);
                z-index: 999;
                opacity: 0;
                transition: opacity 0.3s ease;
            }
            
            .sidebar-overlay.show {
                display: block;
                opacity: 1;
            }
            
            /* Add close button to sidebar when open */
            .sidebar.open::before {
                content: '×';
                position: absolute;
                top: 20px;
                right: 20px;
                font-size: 24px;
                color: var(--text-light);
                cursor: pointer;
                z-index: 1001;
                width: 30px;
                height: 30px;
                display: flex;
                align-items: center;
                justify-content: center;
                border-radius: 50%;
                background: var(--surface-hover);
                transition: all 0.2s ease;
            }
            
            .sidebar.open::before:hover {
                background: var(--border);
                color: var(--text);
            }
            
            .main-content {
                margin-left: 0;
                padding: 70px 20px 20px 20px;
            }
            
            .episode-container {
                padding: 1.5rem;
                border-radius: 8px;
            }
            
            .episode-header {
                margin-bottom: 1.5rem;
                padding: 1.5rem;
            }
            
            .header-title {
                font-size: 1.2rem;
            }
            
            .episode-meta {
                font-size: 0.9rem;
            }
            
            .episode-content {
                font-size: 14px;
            }
            
            .episode-content h1 {
                font-size: 20px;
            }
            
            .episode-content h2 {
                font-size: 1.1rem;
            }
            
            .episode-content h3 {
                font-size: 15px;
            }
            
            /* Adjust special sections for mobile */
            .key-quote,
            .section-quote {
                padding: 1rem;
                margin: 1rem -0.5rem;
            }
            
            .guest-info,
            .contents-list {
                padding: 1rem;
            }
        }
        
        @media (max-width: 480px) {
            .sidebar {
                width: 100%;
            }
            
            .episode-container {
                padding: 1rem;
            }
            
            .episode-header {
                margin-bottom: 1rem;
                padding: 1rem;
            }
            
            .header-title {
                font-size: 1.1rem;
            }
            
            .episode-meta {
                font-size: 0.8rem;
            }
            
            .meta-separator {
                margin: 0 0.5rem;
            }
            
            .episode-content {
                font-size: 13px;
            }
        }
        """
    
    def generate_javascript(self) -> str:
        """Generate JavaScript for interactivity"""
        episodes_json = []
        for i, episode in enumerate(self.episodes):
            # Extract YouTube ID from URL
            url = episode['metadata'].get('url', '')
            youtube_id = ''
            if 'youtube.com/watch?v=' in url:
                youtube_id = url.split('v=')[1].split('&')[0]
            elif 'youtu.be/' in url:
                youtube_id = url.split('youtu.be/')[1].split('?')[0]
            
            episodes_json.append({
                'index': i,  # Add explicit index for debugging
                'title': episode['metadata'].get('title', 'Unknown Title'),
                'channel': episode['metadata'].get('channel', 'Unknown Channel'),
                'published': episode['metadata'].get('published', 'Unknown Date'),
                'duration': episode['metadata'].get('duration', 'Unknown Duration'),
                'views': episode['metadata'].get('views', 'Unknown Views'),
                'url': url,
                'youtube_id': youtube_id,
                'content': markdown.markdown(episode['md_content'], extensions=['tables', 'fenced_code'])
            })
        
        return f"""
        const episodes = {json.dumps(episodes_json, indent=2)};
        
        function showEpisode(episodeIndex, updateUrl = true) {{
            const episode = episodes[episodeIndex];
            if (!episode) return;
            
            // Update active episode in sidebar
            document.querySelectorAll('.episode-item').forEach(item => {{
                item.classList.remove('active');
            }});
            document.querySelector(`[data-episode="${{episodeIndex}}"]`).classList.add('active');
            
            // Update URL for permalink functionality
            if (updateUrl) {{
                const channelSlug = episode.channel.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
                const identifier = episode.youtube_id || `episode-${{episodeIndex}}`;
                window.history.pushState(null, '', `#${{channelSlug}}/${{identifier}}`);
            }}
            
            // Process and enhance content formatting
            let processedContent = episode.content;
            
            // Format "Contents Covered:" sections - handle both markdown list formats
            processedContent = processedContent.replace(
                /<p><strong>Contents Covered:<\\/strong>([\\s\\S]*?)(?=<\\/p>|<p><strong>|<h\\d|$)/gi,
                (match, content) => {{
                    // Extract list items from various formats
                    let items = [];
                    
                    // Try to match numbered list items (1., 2., etc)
                    const lines = content.split(/\\n|<br\\s*\\/?>/).filter(line => line.trim());
                    lines.forEach(line => {{
                        // Clean up the line
                        line = line.replace(/<[^>]*>/g, '').trim();
                        if (line.match(/^\\d+\\./)) {{
                            const cleaned = line.replace(/^\\d+\\.\\s*/, '').trim();
                            if (cleaned) items.push(cleaned);
                        }}
                    }});
                    
                    if (items.length === 0) {{
                        // If no numbered items found, treat each line as an item
                        lines.forEach(line => {{
                            const cleaned = line.replace(/<[^>]*>/g, '').trim();
                            if (cleaned && cleaned !== 'Contents Covered:') {{
                                items.push(cleaned);
                            }}
                        }});
                    }}
                    
                    const itemsHtml = items.map(item => 
                        `<li style="margin: 0.5rem 0;">${{item}}</li>`
                    ).join('');
                    
                    return `<div style="background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%); border: 1px solid #d1d5db; border-radius: 12px; padding: 1.5rem; box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1); margin: 1.5rem 0; position: relative; overflow: hidden;">
                        <h3 style="color: #2563eb; margin-top: 0; margin-bottom: 1rem; font-size: 1.1rem;">Contents Covered:</h3>
                        <ol style="margin: 0; padding-left: 1.5rem; line-height: 1.6;">${{itemsHtml}}</ol>
                    </div>`;
                }}
            );
            
            // Also handle markdown-style lists in content
            processedContent = processedContent.replace(
                /<p><strong>Contents Covered:<\\/strong><\\/p>\\s*<ol>([\\s\\S]*?)<\\/ol>/gi,
                (match, listContent) => {{
                    return `<div style="background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%); border: 1px solid #d1d5db; border-radius: 12px; padding: 1.5rem; box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1); margin: 1.5rem 0; position: relative; overflow: hidden;">
                        <h3 style="color: #2563eb; margin-top: 0; margin-bottom: 1rem; font-size: 1.1rem;">Contents Covered:</h3>
                        <ol style="margin: 0; padding-left: 1.5rem; line-height: 1.6;">${{listContent}}</ol>
                    </div>`;
                }}
            );
            
            // Format "Guest:" sections with proper styling
            processedContent = processedContent.replace(
                /<p><strong>Guest:<\\/strong>([^<]*)<\\/p>/gi,
                (match, guestInfo) => {{
                    return `<div style="background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%); border: 1px solid #bfdbfe; border-radius: 12px; padding: 1.5rem; box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1); margin: 1.5rem 0; position: relative; overflow: hidden;">
                        <strong style="color: #1e293b;">Guest:</strong> ${{guestInfo.trim()}}
                    </div>`;
                }}
            );
            
            // Format "Key Quote:" sections with dark dramatic style
            processedContent = processedContent.replace(
                /<p><strong>Key Quote:<\\/strong>([\\s\\S]*?)<\\/p>/gi,
                (match, quote) => {{
                    // Clean up the quote
                    const cleanQuote = quote
                        .replace(/<strong>|<\\/strong>/g, '')
                        .replace(/<em>|<\\/em>/g, '')
                        .replace(/<br\\s*\\/?>/g, ' ')
                        .replace(/\\*\\*\\*/g, '')
                        .trim();
                    
                    return `<div style="background: linear-gradient(135deg, #1f2937 0%, #111827 100%); color: white; border: 1px solid #374151; border-radius: 12px; padding: 2rem; box-shadow: 0 10px 15px -3px rgb(0 0 0 / 0.1); font-size: 1.1rem; font-style: italic; text-align: center; margin: 1.5rem 0; position: relative; overflow: hidden;">
                        ${{cleanQuote}}
                    </div>`;
                }}
            );
            
            // Remove redundant "Detailed Analysis:" heading
            processedContent = processedContent.replace(
                /<p><strong>Detailed Analysis:<\\/strong><\\/p>/gi,
                ''
            );
            
            // Update main content
            const mainContent = document.querySelector('.main-content');
            
            // Show loading spinner briefly
            mainContent.innerHTML = '<div class="loading-spinner"></div>';
            
            setTimeout(() => {{
                mainContent.innerHTML = `
                    <div class="episode-container">
                        <div class="episode-header">
                            <h2 class="header-title">${{episode.title}}</h2>
                            <div class="episode-meta">
                                ${{episode.channel}}<span class="meta-separator">•</span>${{episode.published}}<span class="meta-separator">•</span>${{episode.duration}}${{episode.views ? `<span class="meta-separator">•</span>${{Number(episode.views.replace(/,/g, '')).toLocaleString()}} views` : ''}}
                            </div>
                        </div>
                        <div class="episode-content">
                            ${{processedContent}}
                        </div>
                    </div>
                `;
            }}, 300);
            
            // Scroll to top
            window.scrollTo(0, 0);
        }}
        
        // Function to expand a channel and show episode
        function expandChannelAndShowEpisode(channelName, episodeIndex = null) {{
            // Find the channel by name
            const channelSlug = channelName.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
            const channelId = `episodes_${{channelSlug.replace(/-/g, '_')}}`;
            const arrowId = `arrow_${{channelSlug.replace(/-/g, '_')}}`;
            
            const channelEpisodes = document.getElementById(channelId);
            const channelArrow = document.getElementById(arrowId);
            
            if (channelEpisodes && channelArrow) {{
                channelEpisodes.classList.add('expanded');
                channelArrow.classList.add('expanded');
            }}
            
            // If specific episode index provided, show it
            if (episodeIndex !== null && episodes[episodeIndex]) {{
                showEpisode(episodeIndex, false); // Don't update URL again
            }} else {{
                // Show first episode of this channel
                const channelEpisodes = episodes.filter(ep => ep.channel === channelName);
                if (channelEpisodes.length > 0) {{
                    // Find the index of the first episode for this channel
                    const firstEpisodeIndex = episodes.findIndex(ep => ep.channel === channelName);
                    if (firstEpisodeIndex !== -1) {{
                        showEpisode(firstEpisodeIndex, false);
                    }}
                }}
            }}
        }}
        
        // Function to handle URL hash changes and deep linking
        function handleUrlHash() {{
            const hash = window.location.hash.slice(1); // Remove #
            if (!hash) return false;
            
            // Parse hash format: channel-slug/youtube-id or channel-slug/episode-123
            const parts = hash.split('/');
            if (parts.length >= 1) {{
                const channelSlug = parts[0];
                const channelName = episodes.find(ep => 
                    ep.channel.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '') === channelSlug
                )?.channel;
                
                if (channelName) {{
                    let episodeIndex = null;
                    
                    if (parts[1]) {{
                        const identifier = parts[1];
                        
                        // Try to find episode by YouTube ID first
                        episodeIndex = episodes.findIndex(ep => ep.youtube_id === identifier);
                        
                        // If not found and it's an episode-123 format, parse it
                        if (episodeIndex === -1 && identifier.startsWith('episode-')) {{
                            const indexFromUrl = parseInt(identifier.replace('episode-', ''));
                            if (indexFromUrl >= 0 && indexFromUrl < episodes.length) {{
                                episodeIndex = indexFromUrl;
                            }}
                        }}
                    }}
                    
                    expandChannelAndShowEpisode(channelName, episodeIndex);
                    return true;
                }}
            }}
            return false;
        }}
        
        document.addEventListener('DOMContentLoaded', function() {{
            // Add click handlers to episode items
            document.querySelectorAll('.episode-item').forEach((item) => {{
                const episodeIndex = parseInt(item.getAttribute('data-episode'));
                item.addEventListener('click', () => showEpisode(episodeIndex));
            }});
            
            // Handle deep linking from URL hash
            const hashHandled = handleUrlHash();
            
            // Show first episode by default if no hash was handled
            if (!hashHandled && episodes.length > 0) {{
                // Show latest episode (first in array since sorted by date) by default
                showEpisode(0, false); // Don't update URL for default load
                
                // Also expand the channel containing the first episode
                const firstEpisode = document.querySelector('.episode-item[data-episode="0"]');
                if (firstEpisode) {{
                    const channel = firstEpisode.closest('.channel');
                    if (channel) {{
                        const channelEpisodes = channel.querySelector('.channel-episodes');
                        const channelArrow = channel.querySelector('.channel-arrow');
                        if (channelEpisodes && channelArrow) {{
                            channelEpisodes.classList.add('expanded');
                            channelArrow.classList.add('expanded');
                        }}
                    }}
                }}
            }}
            
            // Listen for hash changes (back/forward buttons)
            window.addEventListener('hashchange', handleUrlHash);
        }});
        """
    
    def generate_html(self) -> str:
        """Generate the complete HTML viewer"""
        sidebar_html = ""
        
        # Generate sidebar content - use the same order as self.episodes
        for channel_name, channel_episodes in self.channels.items():
            channel_id = channel_name.replace(' ', '_').replace("'", '').replace('"', '').replace('-', '_').lower()
            sidebar_html += f'<div class="channel">\n'
            sidebar_html += f'  <div class="channel-name" onclick="toggleChannel(\'{channel_id}\')">\n'
            sidebar_html += f'    <span class="channel-arrow" id="arrow_{channel_id}">▶</span>\n'
            sidebar_html += f'    {channel_name}\n'
            
            # Add recent badge if this channel has episodes from last week
            if channel_name in self.recent_channels:
                sidebar_html += f'    <span class="channel-recent-badge" title="New episode in last week">NEW</span>\n'
            
            sidebar_html += f'  </div>\n'
            sidebar_html += f'  <div class="channel-episodes" id="episodes_{channel_id}">\n'
            
            for episode in channel_episodes:
                title = episode['metadata'].get('title', 'Unknown Title')
                published = episode['metadata'].get('published', 'Unknown Date')
                
                # Find the correct index in self.episodes array
                correct_index = -1
                for i, ep in enumerate(self.episodes):
                    if (ep['metadata'].get('title') == episode['metadata'].get('title') and 
                        ep['metadata'].get('channel') == episode['metadata'].get('channel') and
                        ep['metadata'].get('published') == episode['metadata'].get('published')):
                        correct_index = i
                        break
                
                # Truncate long titles
                display_title = title if len(title) <= 45 else title[:42] + "..."
                
                sidebar_html += f'''
                    <div class="episode-item" data-episode="{correct_index}">
                        <div class="episode-icon"></div>
                        <div class="episode-details">
                            <div class="episode-title">{display_title}</div>
                            <div class="episode-date">{published}</div>
                        </div>
                    </div>
                '''
            
            sidebar_html += '  </div>\n'
            sidebar_html += '</div>\n'
        
        # Generate welcome message for main content
        welcome_content = '''
        <div class="welcome-message">
            <h2>📻 Podcast Analysis Viewer</h2>
            <p>Select an episode from the sidebar to view detailed analysis and insights.</p>
        </div>
        ''' if self.episodes else '''
        <div class="welcome-message">
            <h2>📻 Podcast Analysis Viewer</h2>
            <p>No podcast episodes found. Make sure you have both .txt and .md files in the directory.</p>
        </div>
        '''
        
        html_template = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Podcast Analysis Viewer</title>
            <style>
                {self.generate_css()}
            </style>
        </head>
        <body>
            <button class="mobile-menu-toggle" onclick="toggleMobileMenu()" aria-label="Toggle menu">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M3 12H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M3 6H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M3 18H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
            </button>
            <div class="sidebar-overlay" onclick="closeMobileMenu()"></div>
            
            <div class="container">
                <div class="sidebar" id="sidebar">
                    <div class="sidebar-header">
                        <h1><span class="sidebar-icon"></span>Podcast Episodes</h1>
                        <a href="https://buymeacoffee.com/rahulxc" target="_blank" class="coffee-link" title="Support this project">
                            <svg class="coffee-icon" viewBox="0 0 24 24" fill="currentColor">
                                <path d="M18.5 3h-13C4.67 3 4 3.67 4 4.5v5.15c0 3.29 2.68 5.95 5.97 5.95h2.06c3.29 0 5.97-2.66 5.97-5.95V4.5C18 3.67 17.33 3 16.5 3zm1.5 6.65c0 2.43-1.97 4.4-4.4 4.4h-2.2c-2.43 0-4.4-1.97-4.4-4.4V5h11v4.65z"/>
                                <path d="M20 8.5h-1.5v1.15c0 .55-.45 1-1 1s-1-.45-1-1V8.5H20c.55 0 1-.45 1-1s-.45-1-1-1h-3.5c-.55 0-1 .45-1 1v3.15c0 1.66 1.34 3 3 3s3-1.34 3-3V8.5z"/>
                                <circle cx="7.5" cy="7.5" r="1"/>
                                <circle cx="12.5" cy="7.5" r="1"/>
                            </svg>
                            Buy me a coffee
                        </a>
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
                
                function toggleChannel(channelId) {{
                    const episodes = document.getElementById('episodes_' + channelId);
                    const arrow = document.getElementById('arrow_' + channelId);
                    
                    if (episodes.classList.contains('expanded')) {{
                        episodes.classList.remove('expanded');
                        arrow.classList.remove('expanded');
                    }} else {{
                        episodes.classList.add('expanded');
                        arrow.classList.add('expanded');
                    }}
                }}
                
                // Mobile menu functions
                function toggleMobileMenu() {{
                    const sidebar = document.getElementById('sidebar');
                    const overlay = document.querySelector('.sidebar-overlay');
                    const toggleButton = document.querySelector('.mobile-menu-toggle');
                    
                    const isOpen = sidebar.classList.contains('open');
                    
                    if (isOpen) {{
                        closeMobileMenu();
                    }} else {{
                        sidebar.classList.add('open');
                        overlay.classList.add('show');
                        toggleButton.classList.add('hidden');
                        
                        // Prevent body scrolling when menu is open
                        document.body.style.overflow = 'hidden';
                    }}
                }}
                
                function closeMobileMenu() {{
                    const sidebar = document.getElementById('sidebar');
                    const overlay = document.querySelector('.sidebar-overlay');
                    const toggleButton = document.querySelector('.mobile-menu-toggle');
                    
                    sidebar.classList.remove('open');
                    overlay.classList.remove('show');
                    toggleButton.classList.remove('hidden');
                    
                    // Restore body scrolling
                    document.body.style.overflow = '';
                }}
                
                // Close mobile menu when episode is selected or close button clicked
                document.addEventListener('click', function(e) {{
                    // Close when episode item is clicked
                    if (e.target.closest('.episode-item')) {{
                        if (window.innerWidth <= 768) {{
                            closeMobileMenu();
                        }}
                    }}
                    
                    // Close when clicking the X button on sidebar (pseudo-element click detection)
                    if (e.target.classList.contains('sidebar') && e.target.classList.contains('open')) {{
                        const rect = e.target.getBoundingClientRect();
                        const clickX = e.clientX - rect.left;
                        const clickY = e.clientY - rect.top;
                        
                        // Check if click is in the close button area (top-right corner)
                        if (clickX > rect.width - 50 && clickY < 50) {{
                            closeMobileMenu();
                        }}
                    }}
                }});
                
                // Handle escape key to close mobile menu
                document.addEventListener('keydown', function(e) {{
                    if (e.key === 'Escape' && window.innerWidth <= 768) {{
                        const sidebar = document.getElementById('sidebar');
                        if (sidebar.classList.contains('open')) {{
                            closeMobileMenu();
                        }}
                    }}
                }});
                
                // Close menu when window is resized to desktop size
                window.addEventListener('resize', function() {{
                    if (window.innerWidth > 768) {{
                        closeMobileMenu();
                    }}
                }});
                
                // The channel with the latest episode will be expanded automatically when showing the latest episode
            </script>
        </body>
        </html>
        """
        
        return html_template
    
    def generate_viewer(self, output_file: str = "index.html"):
        """Generate the complete podcast analysis viewer"""
        print("Scanning for podcast episodes...")
        self.scan_episodes()
        
        print(f"Found {len(self.episodes)} episodes across {len(self.channels)} channels:")
        for channel, episodes in self.channels.items():
            recent_indicator = " 🟢" if channel in self.recent_channels else ""
            print(f"  - {channel}: {len(episodes)} episodes{recent_indicator}")
        
        if self.recent_channels:
            print(f"\nChannels with episodes in the last week ({len(self.recent_channels)}):")
            for channel in sorted(self.recent_channels):
                print(f"  🟢 {channel}")
        
        print("Generating HTML viewer...")
        html_content = self.generate_html()
        
        # Generate HTML in the current working directory, not the input directory
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
    parser.add_argument("--output", "-o", default="index.html",
                       help="Output HTML file name (default: index.html)")
    
    args = parser.parse_args()
    
    analyzer = PodcastAnalyzer(args.directory)
    output_file = analyzer.generate_viewer(args.output)
    
    return output_file

if __name__ == "__main__":
    main()