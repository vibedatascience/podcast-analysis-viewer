# Podcast Analysis Viewer - Development Journal

## Project Overview
Create a programmatic podcast analysis viewer that takes TXT and MD file pairs and generates a beautiful web interface.

### File Structure Requirements
- **TXT files**: Contain metadata (title, channel, published date, duration, views, URL) and raw transcript
- **MD files**: Contain formatted analysis with guest info, key quotes, contents, sections with quotes and analysis

### Original Requirements
- Sidebar that auto-detects channel names and organizes episodes
- Main page with beautifully formatted content from MD files
- Dynamic title/channel detection from TXT files
- Format: "Title | Channel" with metadata (Published: Date • Duration: Time)
- Fully programmatic (no hardcoding)

---

## Development Progress

### ✅ Phase 1: Core Functionality (Initial Implementation)
**Date: 2025-08-28**

#### File Structure Analysis
- Analyzed existing podcast files in `output/` directory
- Found 57 episodes across 22 different channels including:
  - The Rest Is Politics, Lex Fridman, All-In Podcast, Ringer Movies, etc.
- Each episode has corresponding `*.txt` and `*_claude_artifact.md` files

#### Python Script Development (`podcast_viewer.py`)
Created comprehensive `PodcastAnalyzer` class with:

**Metadata Extraction:**
```python
def extract_metadata_from_txt(self, txt_file: Path) -> Dict:
    # Regex patterns to extract:
    # - TITLE: Episode title
    # - CHANNEL: Podcast channel name  
    # - PUBLISHED: Publication date
    # - DURATION: Episode length
    # - VIEWS: View count
    # - URL: YouTube/source URL
```

**Content Processing:**
- Automatic MD file pairing with TXT files
- Markdown to HTML conversion with extensions
- Episode grouping by channel
- Chronological sorting (newest first)

**HTML Generation:**
- Complete static website generation
- Responsive design with modern CSS (Inter font, CSS Grid/Flexbox)
- JavaScript for dynamic episode loading
- Mobile-responsive sidebar navigation

### ✅ Phase 2: Design & Styling Enhancement
**Date: 2025-08-28**

#### Advanced CSS Implementation
**Modern Design System:**
- CSS custom properties (variables) for consistent theming
- Primary blue (#2563eb), clean grays, proper typography scale
- Document-style cards with gradient backgrounds
- Box shadows and rounded corners for depth

**Component Styling:**
- **Sidebar**: Fixed 300px width, collapsible channels with arrows
- **Episode Items**: Compact list with titles, dates, and play icons
- **Main Content**: Centered 800px max-width container
- **Episode Header**: Gradient background with title and metadata
- **Content Cards**: Specialized styling for different content types

**Special Content Formatting:**
- **Guest Info Cards**: Light blue gradient backgrounds
- **Key Quotes**: Dark dramatic styling with italic text
- **Contents Lists**: Gray gradient with numbered/bulleted lists
- **Section Quotes**: Monospace font with blue borders

#### JavaScript Interactivity
**Dynamic Episode Loading:**
```javascript
function showEpisode(episodeIndex) {
    // Update active states
    // Process and enhance content formatting
    // Handle special sections (Guest, Key Quotes, Contents)
    // Update main content with loading animation
}
```

**Sidebar Functionality:**
- Collapsible channel groups with smooth animations
- Active episode highlighting
- Click handlers for episode selection

### ✅ Phase 3: User Experience Improvements
**Date: 2025-08-28**

#### Smart Defaults & Sorting
**Latest Episode Priority:**
- Episodes sorted by publication date (newest first)
- Channels sorted by their latest episode date
- **Latest episode loads automatically** on page open
- Channel containing latest episode auto-expands

**Content Enhancement:**
- Removed folded corner pseudo-elements for cleaner design
- Improved content processing for better markdown rendering
- Enhanced quote and guest information formatting
- Loading spinner animations for smooth transitions

#### GitHub Pages Deployment
- Repository: `vibedatascience/podcast-analysis-viewer`
- Automated deployment via GitHub Actions
- Live site: https://vibedatascience.github.io/podcast-analysis-viewer/

### ✅ Phase 4: Mobile Experience Optimization
**Date: 2025-08-28**

#### Advanced Mobile Controls
**Professional Mobile Menu:**
```html
<button class="mobile-menu-toggle" aria-label="Toggle menu">
    <svg><!-- Professional hamburger icon --></svg>
</button>
```

**Sidebar Behavior:**
- Hidden by default on mobile (≤768px breakpoint)
- Slides in from left with smooth animation
- Dark overlay prevents background interaction
- Body scroll locking when menu is open

**Multiple Close Methods:**
1. **X Close Button**: Appears in sidebar top-right corner
2. **Overlay Tap**: Clicking outside sidebar closes it
3. **Episode Selection**: Auto-closes after choosing episode
4. **Keyboard**: Escape key support
5. **Resize Detection**: Auto-closes when switching to desktop

**Enhanced Interactions:**
- Toggle button hides when sidebar is open
- Smooth transitions and hover effects
- Proper touch target sizing (44px minimum)
- Accessibility improvements (ARIA labels)

### ✅ Phase 5: Recent Episode Indicators
**Date: 2025-08-28**

#### Dynamic "NEW" Badge System
**Programmatic Recent Detection:**
```python
# Calculate date threshold for "recent" episodes (1 week from today)
today = datetime.now()
one_week_ago = today - timedelta(days=7)

# Check if episode is recent and mark channel
if episode_date and episode_date >= one_week_ago:
    self.recent_channels.add(channel)
```

**Smart Date Parsing:**
- Supports multiple date formats: `%Y-%m-%d`, `%d/%m/%Y`, `%m/%d/%Y`, `%B %d, %Y`
- Graceful fallback for parsing errors
- No hardcoded dates or channel names - fully dynamic

**Visual Design:**
- **Cool "NEW" Badge**: Text-based instead of simple dot
- **Gradient Background**: Green gradient from `#10b981` to `#059669`
- **Glow Animation**: Pulsing effect with shadow and scale changes
- **Professional Styling**: Rounded corners, inner shadow, subtle border
- **Smart Positioning**: Right-aligned with `margin-left: auto`

**CSS Implementation:**
```css
.channel-recent-badge {
    font-size: 8px;
    font-weight: 700;
    padding: 2px 4px;
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: white;
    border-radius: 6px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    animation: glow-pulse 2s ease-in-out infinite;
    margin-left: auto;
}
```

**Current Active Indicators:**
- Lenny's Podcast **NEW** (2025-08-28)
- The Totally Football Show **NEW** (2025-08-28)  
- Libero **NEW** (2025-08-26)
- The Seen and the Unseen **NEW** (2025-08-25)

---

## Technical Architecture

### File Processing Pipeline
1. **Scan Directory**: Find all TXT files with date prefix pattern
2. **Extract Metadata**: Parse TXT files for episode information
3. **Load Content**: Read corresponding MD files
4. **Group & Sort**: Organize by channel, sort by date
5. **Generate HTML**: Create complete static website

### Responsive Design Strategy
- **Desktop**: Fixed sidebar (300px) + main content
- **Tablet**: Same layout with adjusted padding
- **Mobile**: Hidden sidebar with overlay menu system

### Performance Optimizations
- Single HTML file with embedded CSS/JS
- Client-side episode switching (no page reloads)
- Optimized loading animations
- Efficient DOM updates

---

## Current State & Statistics

### Content Analysis
- **49 total episodes** processed successfully  
- **15 different channels** automatically detected
- **File pairing**: 49 TXT files with corresponding MD files
- **Content types**: Politics, Tech, Sports, Movies, History, etc.
- **Recent episodes**: 4 channels with episodes from last 7 days

### Features Implemented
✅ Automatic channel detection and grouping  
✅ Dynamic metadata extraction (title, date, duration, views)  
✅ Responsive sidebar navigation with collapsible channels  
✅ Latest episode auto-loading on page open  
✅ Mobile-first design with professional menu controls  
✅ Clean card-based content formatting  
✅ Keyboard accessibility and proper ARIA labels  
✅ GitHub Pages deployment with automatic updates  
✅ **NEW**: Dynamic "NEW" badges for channels with recent episodes (last 7 days)  
✅ **NEW**: Programmatic date detection without hardcoding  
✅ **NEW**: Animated gradient badges with glow effects  

### Technical Specifications
- **Languages**: Python 3, HTML5, CSS3, JavaScript ES6+
- **Libraries**: Python `markdown`, `pathlib`, `re`, `json`
- **CSS Features**: Custom properties, Flexbox, Grid, animations
- **Responsive**: Mobile-first with 768px breakpoint
- **Deployment**: GitHub Pages with static HTML generation

---

## Future Enhancements (Potential)

### Search & Filtering
- Episode search functionality
- Channel filtering options
- Date range filtering
- Tag-based organization

### Content Features
- Episode bookmarking
- Reading progress tracking
- Export functionality
- Dark mode toggle

### Performance
- Lazy loading for large episode lists
- Search indexing
- Content compression
- Progressive Web App (PWA) features

---

**Status**: ✅ **COMPLETE - Fully Functional Production Ready**  
**Deployment**: https://vibedatascience.github.io/podcast-analysis-viewer/  
**Last Updated**: 2025-08-28 (Evening Session - Added "NEW" Badge System)