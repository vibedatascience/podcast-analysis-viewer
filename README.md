# Podcast Analysis Viewer

Live at: https://vibedatascience.github.io/podcast-analysis-viewer/

A static site generator that transforms podcast transcript files (`.txt`) and AI-generated analysis files (`.md`) into a beautiful, searchable web interface.

---

## System Architecture

```mermaid
flowchart TB
    subgraph Input["Input Directory"]
        TXT["*.txt files<br/>(metadata + transcript)"]
        MD["*_claude_artifact.md files<br/>(AI analysis)"]
    end

    subgraph PodcastAnalyzer["podcast_viewer.py"]
        SCAN["scan_episodes()"]
        EXTRACT["extract_metadata_from_txt()"]
        LOAD["load_markdown_content()"]
        GEN["generate_html()"]

        SCAN --> EXTRACT
        SCAN --> LOAD
        EXTRACT --> GEN
        LOAD --> GEN
    end

    subgraph Output["Output"]
        HTML["index.html<br/>(complete static site)"]
    end

    TXT --> SCAN
    MD --> SCAN
    GEN --> HTML

    subgraph Deploy["Deployment"]
        CRON["Cron Job<br/>(update_podcast_viewer.sh)"]
        GH["GitHub Pages"]
    end

    HTML --> CRON
    CRON --> GH
```

---

## File Processing Pipeline

```mermaid
flowchart LR
    subgraph Step1["1. Scan"]
        A["Find all<br/>YYYY-MM-DD_*.txt"]
    end

    subgraph Step2["2. Extract Metadata"]
        B["Parse TXT for:<br/>TITLE, CHANNEL,<br/>PUBLISHED, DURATION,<br/>VIEWS, URL"]
    end

    subgraph Step3["3. Pair Files"]
        C["Match TXT with<br/>*_claude_artifact.md"]
    end

    subgraph Step4["4. Group & Sort"]
        D["Group by channel<br/>Sort by date (newest first)"]
    end

    subgraph Step5["5. Generate HTML"]
        E["Build complete<br/>static website"]
    end

    A --> B --> C --> D --> E
```

---

## TXT File Structure

The `.txt` files contain metadata headers followed by the raw transcript:

```
TITLE: Episode Title Here
CHANNEL: Podcast Channel Name
PUBLISHED: 2025-01-28
DURATION: 1:23:45
VIEWS: 123,456
URL: https://youtube.com/watch?v=xxxxx

[Raw transcript content below...]
```

### Metadata Extraction (Regex Patterns)

| Field | Regex Pattern | Example |
|-------|--------------|---------|
| Title | `TITLE:\s*(.+)` | `TITLE: How AI is Changing Everything` |
| Channel | `CHANNEL:\s*(.+)` | `CHANNEL: Lex Fridman` |
| Published | `PUBLISHED:\s*(.+)` | `PUBLISHED: 2025-01-28` |
| Duration | `DURATION:\s*(.+)` | `DURATION: 2:15:30` |
| Views | `VIEWS:\s*(.+)` | `VIEWS: 1,234,567` |
| URL | `URL:\s*(.+)` | `URL: https://youtube.com/watch?v=abc123` |

---

## MD File Processing

The `*_claude_artifact.md` files contain AI-generated analysis. The script converts markdown to HTML and applies special formatting:

```mermaid
flowchart TB
    subgraph Input["Raw Markdown"]
        RAW["*_claude_artifact.md"]
    end

    subgraph Convert["Python markdown library"]
        MD2HTML["markdown.markdown()<br/>extensions: tables, fenced_code"]
    end

    subgraph JSProcess["JavaScript Content Processing"]
        GUEST["Guest: sections"]
        QUOTE["Key Quote: sections"]
        CONTENTS["Contents Covered: sections"]
        CLEANUP["Remove redundant headings"]
    end

    subgraph Styled["Styled Output"]
        GUEST_CARD["Blue gradient card"]
        QUOTE_CARD["Dark dramatic card"]
        CONTENTS_CARD["Gray gradient card"]
    end

    RAW --> MD2HTML
    MD2HTML --> JSProcess

    GUEST --> GUEST_CARD
    QUOTE --> QUOTE_CARD
    CONTENTS --> CONTENTS_CARD
```

---

## Content Transformation Rules

### 1. Guest Information

**Input (Markdown):**
```markdown
**Guest:** John Smith, CEO of TechCorp, AI researcher
```

**Output (Styled HTML):**
```html
<div style="background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
            border: 1px solid #bfdbfe; border-radius: 12px; padding: 1.5rem;">
    <strong>Guest:</strong> John Smith, CEO of TechCorp, AI researcher
</div>
```

**Visual:** Light blue gradient card

---

### 2. Key Quotes

**Input (Markdown):**
```markdown
**Key Quote:** "The future of AI is not about replacing humans, it's about augmenting human capability."
```

**Output (Styled HTML):**
```html
<div style="background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
            color: white; border-radius: 12px; padding: 2rem;
            font-style: italic; text-align: center;">
    "The future of AI is not about replacing humans..."
</div>
```

**Visual:** Dark dramatic card with white italic text

---

### 3. Contents Covered

**Input (Markdown):**
```markdown
**Contents Covered:**
1. Introduction to machine learning
2. Neural network architectures
3. Real-world applications
```

**Output (Styled HTML):**
```html
<div style="background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
            border: 1px solid #d1d5db; border-radius: 12px; padding: 1.5rem;">
    <h3 style="color: #2563eb;">Contents Covered:</h3>
    <ol>
        <li>Introduction to machine learning</li>
        <li>Neural network architectures</li>
        <li>Real-world applications</li>
    </ol>
</div>
```

**Visual:** Gray gradient card with blue heading

---

### 4. Standard Markdown Elements

| Markdown | CSS Styling |
|----------|-------------|
| `# H1` | 24px, bold, margin-top: 36px |
| `## H2` | Primary blue, 2px bottom border |
| `### H3` | 17px, semi-bold |
| `> blockquote` | JetBrains Mono font, blue border, gray gradient |
| `**bold**` | font-weight: 600 |
| `*italic*` | Primary blue color |
| `***bold italic***` | Dark card with white text (key quote style) |

---

## JavaScript Content Processing Flow

```mermaid
flowchart TD
    A["showEpisode(index)"] --> B["Get episode from JSON array"]
    B --> C["Process content with regex replacements"]

    C --> D{"Match: Contents Covered:?"}
    D -->|Yes| E["Wrap in gray gradient card<br/>Convert to ordered list"]
    D -->|No| F{"Match: Guest:?"}

    F -->|Yes| G["Wrap in blue gradient card"]
    F -->|No| H{"Match: Key Quote:?"}

    H -->|Yes| I["Wrap in dark card<br/>Clean up formatting"]
    H -->|No| J{"Match: Detailed Analysis:?"}

    J -->|Yes| K["Remove redundant heading"]
    J -->|No| L["Keep as-is"]

    E --> M["Update DOM"]
    G --> M
    I --> M
    K --> M
    L --> M

    M --> N["Scroll to top"]
```

---

## Recent Episodes Detection

```mermaid
flowchart LR
    A["Parse published date"] --> B{"Date within<br/>last 7 days?"}
    B -->|Yes| C["Add channel to<br/>recent_channels set"]
    B -->|No| D["Skip"]
    C --> E["Show 'NEW' badge<br/>with glow animation"]
```

**Supported Date Formats:**
- `%Y-%m-%d` (2025-01-28)
- `%d/%m/%Y` (28/01/2025)
- `%m/%d/%Y` (01/28/2025)
- `%B %d, %Y` (January 28, 2025)

---

## URL Permalink Structure

```mermaid
flowchart LR
    A["Episode Data"] --> B["Extract YouTube ID<br/>or use episode index"]
    B --> C["Generate channel slug"]
    C --> D["Create permalink:<br/>#channel-slug/youtube-id"]

    E["URL Hash Change"] --> F["Parse hash"]
    F --> G["Find matching episode"]
    G --> H["Expand channel<br/>Show episode"]
```

**Format:** `#channel-slug/youtube-id` or `#channel-slug/episode-N`

**Example:** `#lex-fridman/abc123xyz`

---

## HTML Generation Structure

```mermaid
flowchart TB
    subgraph Page["Generated index.html"]
        subgraph Head["<head>"]
            CSS["Embedded CSS<br/>(~900 lines)"]
        end

        subgraph Body["<body>"]
            TOGGLE["Mobile menu toggle button"]
            OVERLAY["Sidebar overlay (mobile)"]

            subgraph Container["div.container"]
                subgraph Sidebar["div.sidebar"]
                    HEADER["Sidebar header<br/>(title + coffee link)"]
                    CHANNELS["Channel list<br/>(collapsible groups)"]
                end

                subgraph Main["div.main-content"]
                    EPISODE["Episode container<br/>(header + content)"]
                end
            end
        end

        SCRIPT["Embedded JavaScript<br/>(episodes JSON + functions)"]
    end
```

---

## Cron Job Workflow

```mermaid
sequenceDiagram
    participant Cron
    participant Script as podcast_viewer.py
    participant Git
    participant GitHub as GitHub Pages

    Cron->>Script: Run python podcast_viewer.py
    Script->>Script: Scan input directory
    Script->>Script: Process all episodes
    Script->>Script: Generate index.html
    Script-->>Cron: Done

    Cron->>Git: Check for changes
    alt Changes detected
        Git->>Git: git add index.html
        Git->>Git: git commit
        Git->>GitHub: git push
        GitHub->>GitHub: Deploy to Pages
    else No changes
        Git-->>Cron: Skip
    end
```

---

## File Structure

```
podcast-analysis-viewer/
├── .github/              # GitHub Actions workflows
├── .gitignore            # Ignored files (cron.log, venv, etc.)
├── .nojekyll             # Disable Jekyll processing
├── .trigger              # Cron trigger file
├── README.md             # This file
├── claude.md             # Development journal / instructions
├── index.html            # Generated static site (served by GitHub Pages)
├── podcast_viewer.py     # Main Python script
└── update_podcast_viewer.sh  # Shell script for cron updates
```

---

## Dependencies

- Python 3.x
- `markdown` library (with `tables` and `fenced_code` extensions)
- Standard library: `pathlib`, `re`, `json`, `datetime`
