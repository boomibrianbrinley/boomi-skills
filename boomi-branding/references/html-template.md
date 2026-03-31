# Boomi HTML Page Template

Copy-paste ready template for any Boomi-branded HTML page.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document Title | Boomi</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <!-- Phosphor Icons (optional) -->
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@phosphor-icons/web@2.1.2/src/regular/style.css" />
    <style>
        :root {
            /* Primary */
            --boomi-coral: #FF7C69;
            --boomi-purple: #A93FA5;
            --boomi-navy: #273E59;
            --boomi-white: #FFFFFF;
            --boomi-black: #000000;

            /* Secondary */
            --boomi-periwinkle: #4E47E7;
            --boomi-blue: #009EE2;
            --boomi-green: #04C788;
            --boomi-purple-alt: #A6327D;

            /* Neutrals */
            --gray-50: #F9FAFB;
            --gray-100: #F3F4F6;
            --gray-200: #E5E7EB;
            --gray-300: #D1D5DB;
            --gray-600: #4B5563;
            --gray-800: #1F2937;

            /* Typography */
            --font-sans: "Poppins", -apple-system, BlinkMacSystemFont, sans-serif;
            --font-mono: "JetBrains Mono", "Fira Code", monospace;

            /* Shadows */
            --shadow-sm: 0 1px 2px 0 rgba(0,0,0,0.05);
            --shadow-md: 0 4px 6px -1px rgba(0,0,0,0.1);
            --shadow-lg: 0 10px 15px -3px rgba(0,0,0,0.1);
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: var(--font-sans);
            font-size: 16px;
            line-height: 1.6;
            color: var(--boomi-navy);
            background-color: var(--gray-50);
        }

        .container { max-width: 1200px; margin: 0 auto; padding: 2rem; }

        /* Header */
        header {
            background-color: var(--boomi-white);
            border-bottom: 3px solid var(--boomi-coral);
            padding: 1.5rem 0;
            margin-bottom: 2rem;
        }

        /* Logo CSS Classes */
        .boomi-logo-2color {
            background-image: url('data:image/svg+xml;base64,PHN2ZyBpZD0iTG9nb3MiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmlld0JveD0iMCAwIDIyNC4yNCA5MC4xOSI+PGRlZnM+PHN0eWxlPi5jbHMtMXtmaWxsOiNmZjdjNjY7fS5jbHMtMntmaWxsOiMwMzNkNTg7fTwvc3R5bGU+PC9kZWZzPjxjaXJjbGUgY2xhc3M9ImNscy0xIiBjeD0iMTkwLjQ5IiBjeT0iMjIuNTIiIHI9IjMuNzEiLz48cGF0aCBjbGFzcz0iY2xzLTIiIGQ9Ik04MS4yOSwzMS4yNmExNS4wNiwxNS4wNiwwLDEsMSwwLDMwLjExLDE1LjA2LDE1LjA2LDAsMSwxLDAtMzAuMTFabTAsMjQuNTFhOS4yLDkuMiwwLDAsMCw5LjM5LTkuNDYsOS4zOSw5LjM5LDAsMSwwLTE4Ljc4LDBBOS4yLDkuMiwwLDAsMCw4MS4yOSw1NS43N1oiLz48cGF0aCBjbGFzcz0iY2xzLTIiIGQ9Ik0xMTUuNTMsMzEuMjZhMTUuMDYsMTUuMDYsMCwxLDEtMTUuMzUsMTUuMDVBMTQuOTIsMTQuOTIsMCwwLDEsMTE1LjUzLDMxLjI2Wm0wLDI0LjUxYTkuMiw5LjIsMCwwLDAsOS4zOS05LjQ2LDkuMzksOS4zOSwwLDEsMC0xOC43OCwwQTkuMiw5LjIsMCwwLDAsMTE1LjUzLDU1Ljc3WiIvPjxwYXRoIGNsYXNzPSJjbHMtMiIgZD0iTTE4Ny41MSw2MC4xMVYzMS45MmEuNjYuNjYsMCwwLDEsLjY2LS42Nmg0LjY1YS42NS42NSwwLDAsMSwuNjUuNjZWNjAuMTFhLjY2LjY2LDAsMCwxLS42NS42NmgtNC42NUEuNjcuNjcsMCwwLDEsMTg3LjUxLDYwLjExWiIvPjxwYXRoIGNsYXNzPSJjbHMtMiIgZD0iTTE3MC4xLDMxLjI2YTEyLDEyLDAsMCwwLTEwLjMzLDUuMzljLTEuODMtMy4zNC01LjMzLTUuMzktMTAuMjktNS4zOXMtNy44MywyLjc3LTguNzYsNC4yNVYzMC45M2EuNjUuNjUsMCwwLDAtMS0uNTZsLTQuODQsMi43OWEuMzUuMzUsMCwwLDAtLjE4LjNWNjAuMTFhLjY3LjY3LDAsMCwwLC42Ni42Nmg0LjY4YS42Ny42NywwLDAsMCwuNjYtLjY2VjQ0LjQ4YzAtNC43OSwzLjUyLTcuNTYsNy44Mi03LjU2czYuODEsMi43Nyw2LjgxLDcuNTZWNjAuMTFhLjY2LjY2LDAsMCwwLC42NS42Nmg0LjY5YS42Ni42NiwwLDAsMCwuNjUtLjY2di0xNmMuMTUtNC41NSwzLjYxLTcuMiw3LjgzLTcuMnM2LjgsMi43Nyw2LjgsNy41NlY2MC4xMWEuNjYuNjYsMCwwLDAsLjY1LjY2aDQuNjlhLjY2LjY2LDAsMCwwLC42NS0uNjZWNDMuMjFDMTgyLDM2LjIsMTc3LjgxLDMxLjI2LDE3MC4xLDMxLjI2WiIvPjxwYXRoIGNsYXNzPSJjbHMtMiIgZD0iTTQ2LjY2LDMxLjI2QTE1LjQ2LDE1LjQ2LDAsMCwwLDM2LDM1LjMyVjE1LjM4YS42Ni42NiwwLDAsMC0xLS41N2wtNC44MSwyLjc4YS4zNC4zNCwwLDAsMC0uMTcuM1Y2MC4xMWEuNjUuNjUsMCwwLDAsLjY1LjY1aDQuNjZhLjY1LjY1LDAsMCwwLC42NS0uNjV2LTIuOGExNS40NiwxNS40NiwwLDAsMCwxMC42Niw0LjA2LDE1LjA2LDE1LjA2LDAsMSwwLDAtMzAuMTFabTAsMjQuNTFhOS4yLDkuMiwwLDAsMS05LjM5LTkuNDYsOS4zOSw5LjM5LDAsMSwxLDE4Ljc4LDBBOS4yLDkuMiwwLDAsMS00Ni42Niw1NS43N1oiLz48L3N2Zz4=');
            background-repeat: no-repeat;
            background-size: contain;
            display: inline-block;
            width: 150px;
            height: 60px;
        }

        /* Headings */
        h1 { font-size: 2.25rem; font-weight: 700; color: var(--boomi-navy); margin-bottom: 0.5rem; }
        h2 {
            font-size: 1.875rem; font-weight: 600; color: var(--boomi-navy);
            margin-top: 2rem; margin-bottom: 1rem;
            border-left: 4px solid var(--boomi-coral);
            padding-left: 1rem;
        }
        h3 { font-size: 1.5rem; font-weight: 600; color: var(--boomi-navy); margin-top: 1.5rem; margin-bottom: 0.75rem; }
        p { margin-bottom: 1rem; }

        /* Card */
        .card {
            background-color: var(--boomi-white);
            border-radius: 0.5rem;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: var(--shadow-sm);
            border-top: 3px solid var(--boomi-coral);
        }

        /* Badge */
        .badge {
            padding: 0.375rem 1.125rem;
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
        }
        .badge-purple     { background-color: var(--boomi-purple); }
        .badge-navy       { background-color: var(--boomi-navy); }
        .badge-periwinkle { background-color: var(--boomi-periwinkle); }

        /* Button */
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
        .btn-primary:hover { background-color: var(--boomi-purple); }

        /* Code */
        code {
            font-family: var(--font-mono);
            background-color: var(--gray-100);
            padding: 0.2rem 0.4rem;
            border-radius: 0.25rem;
            font-size: 0.9em;
        }

        .code-block {
            background: var(--gray-800);
            color: var(--gray-100);
            padding: 1.5rem;
            border-radius: 0.5rem;
            overflow-x: auto;
            font-family: var(--font-mono);
            font-size: 0.875rem;
            margin: 0;
            line-height: 1.6;
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

        /* Syntax highlighting */
        .code-keyword    { color: #FF7C69; }
        .code-string     { color: #04C788; }
        .code-number     { color: #4E47E7; }
        .code-comment    { color: #9CA3AF; font-style: italic; }
        .code-function   { color: #009EE2; }
        .code-property   { color: #A93FA5; }
        .code-punctuation{ color: #D1D5DB; }

        /* Footer */
        footer {
            margin-top: 4rem;
            padding-top: 2rem;
            border-top: 1px solid var(--gray-200);
            text-align: center;
            color: var(--gray-600);
            font-size: 0.875rem;
        }
    </style>
</head>
<body>
    <header>
        <div class="container" style="display: flex; align-items: center; gap: 1.5rem;">
            <div class="boomi-logo-2color" aria-label="Boomi"></div>
            <div>
                <h1>Page Title</h1>
                <p style="color: var(--gray-600); margin: 0;">Subtitle or description</p>
            </div>
        </div>
    </header>

    <main class="container">
        <div class="card">
            <h2>Section Title</h2>
            <p>Content goes here. Use <strong>Poppins</strong> font with navy text on white backgrounds
            for maximum readability (14.21:1 contrast ratio).</p>
            <span class="badge">Active</span>
            <span class="badge badge-purple" style="margin-left: 0.5rem;">v2.0</span>
        </div>

        <div class="card">
            <h3>Code Example</h3>
            <div style="position: relative; margin: 1rem 0;">
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
                <pre class="code-block code-block-with-header"><code><span class="code-keyword">const</span> result <span class="code-punctuation">=</span> <span class="code-function">processData</span><span class="code-punctuation">(</span><span class="code-string">"input"</span><span class="code-punctuation">);</span>
<span class="code-comment">// Output the result</span>
console<span class="code-punctuation">.</span><span class="code-function">log</span><span class="code-punctuation">(</span>result<span class="code-punctuation">);</span></code></pre>
            </div>
        </div>
    </main>

    <footer class="container">
        <p><strong>Boomi Integration</strong> | Powered by Boomi Branding Skill v1.0</p>
        <p style="margin-top: 0.5rem; font-size: 0.75rem; color: var(--gray-600);">
            Colors: Coral (#FF7C69) · Purple (#A93FA5) · Navy (#273E59) | Font: Poppins
        </p>
    </footer>

    <script>
        function copyCode(button) {
            const container = button.closest('[style*="relative"], .code-block-container');
            const codeBlock = container ? container.querySelector('code') : null;
            if (!codeBlock) return;
            const codeText = codeBlock.innerText || codeBlock.textContent;
            navigator.clipboard.writeText(codeText).then(() => {
                const orig = button.innerHTML;
                button.innerHTML = `<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"></polyline></svg> Copied!`;
                button.style.backgroundColor = 'rgba(4,199,136,0.2)';
                setTimeout(() => { button.innerHTML = orig; button.style.backgroundColor = 'rgba(255,255,255,0.1)'; }, 2000);
            });
        }
    </script>
</body>
</html>
```
