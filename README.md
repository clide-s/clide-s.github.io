# news.sys

A daily news digest generated entirely by Claude. Every morning at 5am, an automated script prompts Claude to create a fresh static webpage summarizing the day's news—each edition with a unique aesthetic direction informed by the mood and themes of the headlines. Claude designs and generates complete HTML pages from scratch, responding aesthetically to the content.

**Live site:** [http://edilc.github.io/](https://edilc.github.io/)
---

## How It Works

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│GitHub Actions│────▶│   Claude    │────▶│  index.html │────▶│ GitHub Pages│
│  5am EST    │     │  designs &  │     │   pushed    │     │   serves    │
│             │     │  generates  │     │             │     │             │
└─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
```

1. A GitHub Actions workflow runs daily at 5am EST
2. Claude's multi-agent system:
   - Searches for and gathers current news articles
   - Curates the top 10 stories
   - Analyzes themes and mood across the selected articles
   - Designs and generates a complete HTML page from scratch
3. The generated `index.html` is committed and pushed to this repository
4. GitHub Pages serves the updated site

Each day's design is different—not through random variation, but through intentional response to the news itself. A day heavy with government scandals might render as classified documents; breakthrough scientific discoveries might appear as naturalist field notes.

---

## The Design Prompt

The Builder agent receives this comprehensive prompt that guides its aesthetic design process. It emphasizes responding to the news thematically while maintaining technical requirements:

~~~
Create a static web page for "news.sys" — a daily news digest by Claude.

## Content Requirements
- 10 news headlines from various sources
- Each headline should be clickable to expand and reveal: a longer summary and source links
- No numbered items. No "live feed" text. No 'active monitoring' text. No auto-animations (user-triggered only).

## Aesthetic Process (IMPORTANT)

**Step 1: Analyze the news.** Before designing, identify:
- The dominant mood across today's stories (ominous, hopeful, absurd, bureaucratic, scientific, chaotic, contemplative, urgent, mundane, surreal)
- Recurring themes or domains (politics, technology, nature, conflict, discovery, economy, culture)
- Any single story dramatic enough to anchor the visual tone

**Step 2: Commit to ONE aesthetic direction.** Based on your analysis, choose a specific visual concept. Don't blend—commit. Examples of directions (use these as inspiration, not a checklist):

| News Mood | Possible Aesthetic Direction |
|-----------|------------------------------|
| Government/bureaucracy heavy | Classified documents, redacted files, manila folders, typewriter text, official stamps |
| Science/nature discoveries | Field notebook, naturalist illustrations, specimen labels, botanical drawings, parchment textures |
| Tech/cyber news | Terminal interface, phosphor glow, scan lines, monospace everything, ASCII decorations |
| Economic/financial | Stock ticker aesthetic, ledger paper, banking forms, serif authority, green/black |
| Absurd/weird news | Tabloid collage, ransom note typography, clip art chaos, garish colors |
| Conflict/crisis | Broadcast interruption, emergency alert, high contrast, stark warnings |
| Cultural/arts | Editorial magazine, gallery exhibition, refined typography, generous whitespace |
| Mundane/local news | Community bulletin board, pushpins, handwritten notes, cork texture |

**Step 3: Design with intention.** Your chosen direction should influence:
- **Layout structure**: Single column? Split pane? Card grid? Sidebar index? Dossier format?
- **Typography**: Bureaucratic serifs? Playful handwriting? Cold monospace? Elegant editorial?
- **Color palette**: Derive from concept (manila/red for classified, green/cream for naturalist, amber/black for terminal)
- **Decorative elements**: ASCII art, SVG illustrations, borders, stamps, textures, dividers—all should reinforce the theme
- **Information density**: Sparse and contemplative? Dense and urgent?

**Step 4: Create 1-3 thematic visual elements.** These should feel integral, not decorative:
- Small SVG illustrations reflecting dominant story themes
- ASCII art headers or dividers
- Thematic icons or stamps
- Textural backgrounds (subtle)

**Step 5: Create a design rationale.** Write a brief one-line explanation of today's aesthetic choice, e.g.:
> "field notebook (3 stories on species discovery, 2 on climate research)"

## Technical Requirements
- Generate CSS styling that reflects today's aesthetic
- Generate article HTML with proper semantic structure
- Each article must use: class="article" (wrapper), class="article-header" (clickable header with title), class="article-details" (expandable content)
- Readable and functional—aesthetic experimentation should never compromise usability
- Responsive (works on mobile)
- Accessible (proper contrast, semantic HTML, ARIA attributes)
- Can use Google Fonts if needed (via @import in CSS)

## What to Avoid
- Blending all inspirations into generic "retro-tech minimalist"
- Color/font swaps as the only variation
- Decorative elements that don't connect to content
- Cluttered or illegible results
- The same layout every time
~~~

---

## Repository Structure

```
.
├── .github/
│   └── workflows/
│       └── generate-daily-news.yml  # GitHub Actions workflow
├── src/                             # Multi-agent pipeline source code
│   ├── agents/                      # Gatherer, Curator, and Builder agents
│   ├── models/                      # Data models
│   ├── prompts/                     # Agent prompts (including design prompt)
│   └── utils/                       # Logging and utilities
├── generate_news.py                 # Main generation script
├── index.html                       # The daily-generated news page
└── README.md                        # You are here
```

---

## Automation

The entire workflow is automated using GitHub Actions:

- **Schedule:** Daily at 5:00 AM EST (10:00 AM UTC)
- **Workflow:** `.github/workflows/generate-daily-news.yml`
- **Trigger:** Can also be manually triggered from the Actions tab

The workflow:
1. Deletes the previous `index.html`
2. Runs `generate_news.py` which executes a multi-agent pipeline:
   - Gatherer agents search for and collect news articles
   - Curator agent selects the top 10 stories
   - Builder agent analyzes themes and designs a complete HTML page from scratch
3. The generated page is committed and pushed to the repository
4. GitHub Pages automatically deploys the update

---

## Running Locally

To generate a news page manually:

```bash
# Ensure ANTHROPIC_API_KEY is set in your environment
uv run generate_news.py > index.html
```

The output is a single static HTML file with no dependencies. Just open `index.html` in a browser.

---

## Why?

This is an experiment in AI-generated editorial design. Traditional news aggregators apply the same template to every story. news.sys asks: *what if the design itself was responsive to the news?*

Some days feel like emergency broadcasts. Others feel like quiet naturalist observations. The aesthetic should reflect that.

---

## License

The generation prompt and automation scripts are released under MIT. Individual news summaries link back to their original sources.

---

<p align="center">
  <em>news by Claude</em>
</p>
