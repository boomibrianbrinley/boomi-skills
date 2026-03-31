# Boomi Components Reference

## Typography

### Font Import
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
```

Or via CSS `@import`:
```css
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
```

### Font Variables
```css
--font-sans: "Poppins", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
--font-mono: "JetBrains Mono", "Fira Code", "Source Code Pro", Menlo, Monaco, monospace;
--font-heading: "Poppins", -apple-system, BlinkMacSystemFont, sans-serif;
```

### Type Scale
| Token      | rem     | px  | Usage               |
|------------|---------|-----|---------------------|
| `--text-xs`  | 0.75rem | 12  | Captions, labels    |
| `--text-sm`  | 0.875rem| 14  | Secondary text      |
| `--text-base`| 1rem    | 16  | Body text           |
| `--text-lg`  | 1.125rem| 18  | Large body          |
| `--text-xl`  | 1.25rem | 20  | H4                  |
| `--text-2xl` | 1.5rem  | 24  | H3                  |
| `--text-3xl` | 1.875rem| 30  | H2                  |
| `--text-4xl` | 2.25rem | 36  | H1                  |
| `--text-5xl` | 3rem    | 48  | Display             |

### Font Weights
```css
--weight-light:    300;  /* Large display text */
--weight-normal:   400;  /* Body text */
--weight-medium:   500;  /* Emphasized text */
--weight-semibold: 600;  /* Subheadings */
--weight-bold:     700;  /* Primary headings */
```

### Line Heights
```css
--leading-tight:   1.25;
--leading-normal:  1.5;
--leading-relaxed: 1.75;
```

---

## Spacing System

```css
--space-1:  0.25rem;  /*  4px */
--space-2:  0.5rem;   /*  8px */
--space-3:  0.75rem;  /* 12px */
--space-4:  1rem;     /* 16px */
--space-6:  1.5rem;   /* 24px */
--space-8:  2rem;     /* 32px */
--space-12: 3rem;     /* 48px */
--space-16: 4rem;     /* 64px */
```

---

## Border Radius

```css
--radius-sm:   0.25rem;  /*  4px — small elements */
--radius-md:   0.5rem;   /*  8px — cards, buttons */
--radius-lg:   0.75rem;  /* 12px — larger containers */
--radius-xl:   1rem;     /* 16px — hero sections */
--radius-full: 9999px;   /* circular / pill shapes */
```

---

## Shadows

```css
--shadow-sm: 0 1px 2px 0 rgba(0,0,0,0.05);
--shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1);
--shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1);
--shadow-xl: 0 20px 25px -5px rgba(0,0,0,0.1);
```

---

## Base Reset & Body

```css
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: var(--font-sans);
    font-size: 16px;
    line-height: 1.6;
    color: var(--boomi-navy);
    background-color: var(--gray-50);
}
```

---

## Heading Styles

```css
h1 {
    font-size: 2.25rem;
    font-weight: 700;
    color: var(--boomi-navy);
    margin-bottom: 0.5rem;
}

h2 {
    font-size: 1.875rem;
    font-weight: 600;
    color: var(--boomi-navy);
    margin-top: 2rem;
    margin-bottom: 1rem;
    border-left: 4px solid var(--boomi-coral);
    padding-left: 1rem;
}

h3 {
    font-size: 1.5rem;
    font-weight: 600;
    color: var(--boomi-navy);
    margin-top: 1.5rem;
    margin-bottom: 0.75rem;
}
```

---

## Card Component

```css
.card {
    background-color: var(--boomi-white);
    border-radius: 0.5rem;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    border-top: 3px solid var(--boomi-coral);
}
```

---

## Badge / Pill Components

### Critical Rules
- `border-radius: 9999px` — always
- Padding ratio **1:3** (vertical:horizontal)
- `display: inline-flex; align-items: center;`
- `min-height` set to prevent collapse

```css
/* Default (medium) badge */
.badge {
    padding: 0.375rem 1.125rem;  /* 1:3 ratio */
    min-height: 2rem;
    border-radius: 9999px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 0.875rem;
    font-weight: 500;
    line-height: 1;
    white-space: nowrap;
    background-color: var(--boomi-coral);
    color: var(--boomi-white);
    margin: 0.25rem;
}

.badge-sm {
    padding: 0.25rem 0.75rem;    /* 1:3 ratio */
    min-height: 1.5rem;
    font-size: 0.75rem;
}

.badge-lg {
    padding: 0.5rem 1.5rem;      /* 1:3 ratio */
    min-height: 2.5rem;
    font-size: 1rem;
}

/* Color variants */
.badge-purple     { background-color: var(--boomi-purple); }
.badge-navy       { background-color: var(--boomi-navy); }
.badge-periwinkle { background-color: var(--boomi-periwinkle); }
.badge-blue       { background-color: var(--boomi-blue); }
.badge-green      { background-color: var(--boomi-green); }
```

---

## Button Component

```css
.btn-primary {
    background-color: var(--boomi-coral);
    color: var(--boomi-white);
    padding: 0.75rem 1.5rem;
    border: none;
    border-radius: 0.5rem;
    font-family: var(--font-sans);
    font-weight: 500;
    cursor: pointer;
    transition: background-color 0.2s;
}

.btn-primary:hover {
    background-color: var(--boomi-purple);
}

.btn-secondary {
    background-color: transparent;
    color: var(--boomi-coral);
    padding: 0.75rem 1.5rem;
    border: 2px solid var(--boomi-coral);
    border-radius: 0.5rem;
    font-family: var(--font-sans);
    font-weight: 500;
    cursor: pointer;
    transition: all 0.2s;
}

.btn-secondary:hover {
    background-color: var(--boomi-coral);
    color: var(--boomi-white);
}
```

---

## Process Card (Boomi-Specific)

```css
.process-card {
    background-color: var(--boomi-white);
    border-radius: 0.5rem;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    border-left: 4px solid var(--boomi-coral);
}

.process-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1rem;
}

.process-details p {
    margin: 0.5rem 0;
    font-size: 0.875rem;
}
```

```html
<div class="process-card">
    <div class="process-header">
        <h3>Process Name</h3>
        <span class="badge">Active</span>
    </div>
    <div class="process-details">
        <p><strong>Environment:</strong> Production</p>
        <p><strong>Atom:</strong> PROD-ATOM-01</p>
        <p><strong>Schedule:</strong> Every 15 minutes</p>
    </div>
</div>
```

---

## Connection Status Indicator

```css
.connection-status {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.875rem;
}

.status-dot {
    width: 10px;
    height: 10px;
    border-radius: 50%;
}

.status-success    { background-color: #04C788; }
.status-warning    { background-color: #F59E0B; }
.status-error      { background-color: #EF4444; }
.status-processing { background-color: #FF7C69; }
.status-info       { background-color: #009EE2; }
.status-paused     { background-color: #94A3B8; }
```

```html
<div class="connection-status">
    <span class="status-dot status-success"></span>
    <span>Connected</span>
</div>
```

---

## Code Blocks with Syntax Highlighting

### CSS
```css
.code-block {
    background: var(--gray-800);
    color: var(--gray-100);
    padding: 1.5rem;
    border-radius: 0.5rem;
    overflow-x: auto;
    font-family: var(--font-mono);
    font-size: 0.875rem;
    line-height: 1.6;
    margin: 0;
}

.code-block-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: var(--boomi-navy);
    color: var(--boomi-white);
    padding: 0.75rem 1rem;
    border-radius: 0.5rem 0.5rem 0 0;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.code-block-with-header { border-radius: 0 0 0.5rem 0.5rem; }

.copy-button {
    padding: 0.25rem 0.75rem;
    min-height: 1.5rem;
    border-radius: 0.25rem;
    border: 1px solid rgba(255,255,255,0.2);
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.75rem;
    font-weight: 500;
    font-family: var(--font-sans);
    background-color: rgba(255,255,255,0.1);
    color: var(--boomi-white);
    cursor: pointer;
    transition: all 0.2s;
}

.copy-button:hover { background-color: var(--boomi-coral); border-color: var(--boomi-coral); }

/* Syntax highlighting using Boomi brand palette */
.code-keyword    { color: #FF7C69; }   /* Coral — keywords */
.code-string     { color: #04C788; }   /* Green — strings */
.code-number     { color: #4E47E7; }   /* Periwinkle — numbers */
.code-comment    { color: #9CA3AF; font-style: italic; }
.code-function   { color: #009EE2; }   /* Blue — functions */
.code-property   { color: #A93FA5; }   /* Purple — properties */
.code-punctuation{ color: #D1D5DB; }   /* Light gray */
```

### Copy Button JavaScript
```javascript
function copyCode(button) {
    const container = button.closest('.code-block-container');
    const codeBlock = container.querySelector('code');
    const codeText = codeBlock.innerText || codeBlock.textContent;

    navigator.clipboard.writeText(codeText).then(() => {
        const originalText = button.innerHTML;
        button.innerHTML = `
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="20 6 9 17 4 12"></polyline>
            </svg> Copied!`;
        button.style.backgroundColor = 'rgba(4, 199, 136, 0.2)';
        setTimeout(() => {
            button.innerHTML = originalText;
            button.style.backgroundColor = 'rgba(255,255,255,0.1)';
        }, 2000);
    });
}
```

### HTML Structure
```html
<div class="code-block-container">
    <div class="code-block-header">
        <span>JavaScript</span>
        <button class="copy-button" onclick="copyCode(this)">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
            </svg>
            Copy
        </button>
    </div>
    <pre class="code-block code-block-with-header"><code><span class="code-keyword">const</span> result <span class="code-punctuation">=</span> <span class="code-function">processData</span><span class="code-punctuation">(</span><span class="code-string">"input"</span><span class="code-punctuation">);</span></code></pre>
</div>
```

---

## Layout Helpers

```css
.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem;
}

header {
    background-color: var(--boomi-white);
    border-bottom: 3px solid var(--boomi-coral);
    padding: 1.5rem 0;
    margin-bottom: 2rem;
}

footer {
    margin-top: 4rem;
    padding-top: 2rem;
    border-top: 1px solid var(--gray-200);
    text-align: center;
    color: var(--gray-600);
    font-size: 0.875rem;
}
```
