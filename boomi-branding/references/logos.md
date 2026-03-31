# Boomi Logo Reference

## Logo Variants Overview

| Variant                     | CSS Class                   | Background    | Width  | Height |
|-----------------------------|-----------------------------|---------------|--------|--------|
| 2-Color Wordmark (positive) | `.boomi-logo-2color`        | Light         | 150px  | 60px   |
| 1-Color Wordmark (positive) | `.boomi-logo-1color`        | Light         | 150px  | 60px   |
| 1-Color Wordmark (reversed) | `.boomi-logo-1color-reversed`| Dark         | 150px  | 60px   |
| 2-Color Wordmark (reversed) | `.boomi-logo-2color-reversed`| Dark         | 150px  | 44px   |
| Mark 1-Color Positive       | `.boomi-mark-1color`        | Light         | 50px   | 50px   |
| Mark 1-Color Reversed       | `.boomi-mark-1color-reversed`| Dark         | 50px   | 50px   |
| Mark 2-Color Reversed       | `.boomi-mark-2color-reversed`| Dark         | 50px   | 50px   |
| Mark 2-Color Large          | `.boomi-mark-2color-large`  | Any           | 100px  | 100px  |

## Which Logo to Use

- **Default (light backgrounds)**: `.boomi-logo-2color` — navy text + coral dot
- **Dark backgrounds**: `.boomi-logo-2color-reversed` — white text + coral dot
- **Single-color printing**: `.boomi-logo-1color` (navy) or `.boomi-logo-1color-reversed` (white)
- **Favicon / app icon / avatar**: `.boomi-mark-2color-large`
- **Footer on dark bg**: `.boomi-mark-1color-reversed`

## Sizing Rules

- Wordmark minimum digital width: **70px**
- Mark minimum digital width: **35px**
- Never reproduce below these minimums

## Clear Space

- Wordmark: clear space = height of the "i" dot on all sides
- Mark: clear space = 50% of the circular mark height on all sides

## Placement

- Preferred: top-left or top-center
- Corner: top-left or bottom-right
- Presentations/video: centered permitted (opening/closing slides)

## Logo Misuse — Never Do These

1. Use the mark as a substitute for the "o" in "boomi"
2. Rotate or skew the logo
3. Change logo colors or apply effects
4. Outline the logo
5. Add drop shadows or glows
6. Place on busy backgrounds without proper contrast
7. Stretch, distort, or alter proportions
8. Use old/outdated versions
9. Knockout the "b" and dot — use the 1-color version instead

## Logo Implementation — Inline SVG (Preferred Method)

**Always use inline SVG for the Boomi wordmark.** Do not use base64 CSS background images or external `<img src>` URL references for the primary wordmark. Inline SVG is preferred because:
- No network dependency (renders instantly, works offline/in demos)
- No CORS issues
- Crisp at any resolution
- No font-loading timing issues that cause fallback rendering artifacts

### Light Background — Use this SVG (navy + coral dot)

Source: `https://exosphere.boomi.com/docs/assets/images/brand-logo-light.svg`

> ⚠ The source file contains a hardcoded `<rect fill="#fff">` background. **Always strip this rect before embedding** so the logo renders transparently on any background color.

**Ready-to-embed (rect removed, transparent background):**
```html
<!-- Paste light-background inline SVG here (viewBox="0 0 211 60", .bl=navy, .bc=coral) -->
<!-- Source: https://exosphere.boomi.com/docs/assets/images/brand-logo-light.svg -->
<!-- Remove the <rect fill="#fff"> element before embedding -->
```

### Dark Background — Use this SVG (white + coral dot)

Source: `https://exosphere.boomi.com/docs/assets/images/brand-logo-dark.svg`

> This SVG is already transparent — embed as-is.
```html
<!-- Paste dark-background inline SVG here (viewBox="0 0 211 60", white text + coral dot) -->
<!-- Source: https://exosphere.boomi.com/docs/assets/images/brand-logo-dark.svg -->
```

### Sizing

Both SVGs are authored at `211×60`. Adjust `width` and `height` attributes freely while preserving `viewBox="0 0 211 60"`. Recommended sizes:

| Context | width | height |
|---------|-------|--------|
| Page header | 160px | 46px |
| Report cover | 200px | 57px |
| Footer / compact | 120px | 34px |
| Minimum (digital) | 70px | 20px |

### Legacy: Embedded CSS Classes (Base64 SVG)

> ⚠ **Deprecated for wordmarks.** The base64 CSS background-image approach is retained below only for the Boomi mark/icon variants. For the primary wordmark, always use inline SVG per the section above.

```css
/* 2-Color Wordmark — DEPRECATED, use inline SVG above instead */
```

/* 1-Color Wordmark Positive — navy on light */
.boomi-logo-1color {
    background-image: url('data:image/svg+xml;base64,PHN2ZyBpZD0iTG9nb3MiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmlld0JveD0iMCAwIDIyNC4yNCA5MC4xOSI+PGRlZnM+PHN0eWxlPi5jbHMtMXtmaWxsOiMwMzNkNTg7fTwvc3R5bGU+PC9kZWZzPjxjaXJjbGUgY2xhc3M9ImNscy0xIiBjeD0iMTkwLjQ5IiBjeT0iMjIuNTIiIHI9IjMuNzEiLz48cGF0aCBjbGFzcz0iY2xzLTEiIGQ9Ik04MS4yOSwzMS4yNmExNS4wNiwxNS4wNiwwLDEsMSwwLDMwLjExLDE1LjA2LDE1LjA2LDAsMSwxLDAtMzAuMTFabTAsMjQuNTFhOS4yLDkuMiwwLDAsMCw5LjM5LTkuNDYsOS4zOSw5LjM5LDAsMSwwLTE4Ljc4LDBBOS4yLDkuMiwwLDAsMCw4MS4yOSw1NS43N1oiLz48cGF0aCBjbGFzcz0iY2xzLTEiIGQ9Ik0xMTUuNTMsMzEuMjZhMTUuMDYsMTUuMDYsMCwxLDEtMTUuMzUsMTUuMDVBMTQuOTIsMTQuOTIsMCwwLDEsMTE1LjUzLDMxLjI2Wm0wLDI0LjUxYTkuMiw5LjIsMCwwLDAsOS4zOS05LjQ2LDkuMzksOS4zOSwwLDEsMC0xOC43OCwwQTkuMiw5LjIsMCwwLDAsMTE1LjUzLDU1Ljc3WiIvPjxwYXRoIGNsYXNzPSJjbHMtMSIgZD0iTTE4Ny41MSw2MC4xMVYzMS45MmEuNjYuNjYsMCwwLDEsLjY2LS42Nmg0LjY1YS42NS42NSwwLDAsMSwuNjUuNjZWNjAuMTFhLjY2LjY2LDAsMCwxLS42NS42NmgtNC42NUEuNjcuNjcsMCwwLDEsMTg3LjUxLDYwLjExWiIvPjxwYXRoIGNsYXNzPSJjbHMtMSIgZD0iTTE3MC4xLDMxLjI2YTEyLDEyLDAsMCwwLTEwLjMzLDUuMzljLTEuODMtMy4zNC01LjMzLTUuMzktMTAuMjktNS4zOXMtNy44MywyLjc3LTguNzYsNC4yNVYzMC45M2EuNjUuNjUsMCwwLDAtMS0uNTZsLTQuODQsMi43OWEuMzUuMzUsMCwwLDAtLjE4LjNWNjAuMTFhLjY3LjY3LDAsMCwwLC42Ni42Nmg0LjY4YS42Ny42NywwLDAsMCwuNjYtLjY2VjQ0LjQ4YzAtNC43OSwzLjUyLTcuNTYsNy44Mi03LjU2czYuODEsMi43Nyw2LjgxLDcuNTZWNjAuMTFhLjY2LjY2LDAsMCwwLC42NS42Nmg0LjY5YS42Ni42NiwwLDAsMCwuNjUtLjY2di0xNmMuMTUtNC41NSwzLjYxLTcuMiw3LjgzLTcuMnM2LjgsMi43Nyw2LjgsNy41NlY2MC4xMWEuNjYuNjYsMCwwLDAsLjY1LjY2aDQuNjlhLjY2LjY2LDAsMCwwLC42NS0uNjZWNDMuMjFDMTgyLDM2LjIsMTc3LjgxLDMxLjI2LDE3MC4xLDMxLjI2WiIvPjxwYXRoIGNsYXNzPSJjbHMtMSIgZD0iTTQ2LjY2LDMxLjI2QTE1LjQ2LDE1LjQ2LDAsMCwwLDM2LDM1LjMyVjE1LjM4YS42Ni42NiwwLDAsMC0xLS41N2wtNC44MSwyLjc4YS4zNC4zNCwwLDAsMC0uMTcuM1Y2MC4xMWEuNjUuNjUsMCwwLDAsLjY1LjY1aDQuNjZhLjY1LjY1LDAsMCwwLC42NS0uNjV2LTIuOGExNS40NiwxNS40NiwwLDAsMCwxMC42Niw0LjA2LDE1LjA2LDE1LjA2LDAsMSwwLDAtMzAuMTFabTAsMjQuNTFhOS4yLDkuMiwwLDAsMS05LjM5LTkuNDYsOS4zOSw5LjM5LDAsMSwxLDE4Ljc4LDBBOS4yLDkuMiwwLDAsMS00Ni42Niw1NS43N1oiLz48L3N2Zz4=');
    background-repeat: no-repeat;
    background-size: contain;
    display: inline-block;
    width: 150px;
    height: 60px;
}

/* 1-Color Wordmark Reversed — white on dark */
.boomi-logo-1color-reversed {
    background-image: url('data:image/svg+xml;base64,PHN2ZyBpZD0iTG9nb3MiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmlld0JveD0iMCAwIDIyNC4yNCA5MC4xOSI+PGRlZnM+PHN0eWxlPi5jbHMtMXtmaWxsOiNmZmY7fTwvc3R5bGU+PC9kZWZzPjxjaXJjbGUgY2xhc3M9ImNscy0xIiBjeD0iMTkwLjQ5IiBjeT0iMjIuNTIiIHI9IjMuNzEiLz48cGF0aCBjbGFzcz0iY2xzLTEiIGQ9Ik04MS4yOSwzMS4yNmExNS4wNiwxNS4wNiwwLDEsMSwwLDMwLjExLDE1LjA2LDE1LjA2LDAsMSwxLDAtMzAuMTFabTAsMjQuNTFhOS4yLDkuMiwwLDAsMCw5LjM5LTkuNDYsOS4zOSw5LjM5LDAsMSwwLTE4Ljc4LDBBOS4yLDkuMiwwLDAsMCw4MS4yOSw1NS43N1oiLz48cGF0aCBjbGFzcz0iY2xzLTEiIGQ9Ik0xMTUuNTMsMzEuMjZhMTUuMDYsMTUuMDYsMCwxLDEtMTUuMzUsMTUuMDVBMTQuOTIsMTQuOTIsMCwwLDEsMTE1LjUzLDMxLjI2Wm0wLDI0LjUxYTkuMiw5LjIsMCwwLDAsOS4zOS05LjQ2LDkuMzksOS4zOSwwLDEsMC0xOC43OCwwQTkuMiw5LjIsMCwwLDAsMTE1LjUzLDU1Ljc3WiIvPjxwYXRoIGNsYXNzPSJjbHMtMSIgZD0iTTE4Ny41MSw2MC4xMVYzMS45MmEuNjYuNjYsMCwwLDEsLjY2LS42Nmg0LjY1YS42NS42NSwwLDAsMSwuNjUuNjZWNjAuMTFhLjY2LjY2LDAsMCwxLS42NS42NmgtNC42NUEuNjcuNjcsMCwwLDEsMTg3LjUxLDYwLjExWiIvPjxwYXRoIGNsYXNzPSJjbHMtMSIgZD0iTTE3MC4xLDMxLjI2YTEyLDEyLDAsMCwwLTEwLjMzLDUuMzljLTEuODMtMy4zNC01LjMzLTUuMzktMTAuMjktNS4zOXMtNy44MywyLjc3LTguNzYsNC4yNVYzMC45M2EuNjUuNjUsMCwwLDAtMS0uNTZsLTQuODQsMi43OWEuMzUuMzUsMCwwLDAtLjE4LjNWNjAuMTFhLjY3LjY3LDAsMCwwLC42Ni42Nmg0LjY4YS42Ny42NywwLDAsMCwuNjYtLjY2VjQ0LjQ4YzAtNC43OSwzLjUyLTcuNTYsNy44Mi03LjU2czYuODEsMi43Nyw2LjgxLDcuNTZWNjAuMTFhLjY2LjY2LDAsMCwwLC42NS42Nmg0LjY5YS42Ni42NiwwLDAsMCwuNjUtLjY2di0xNmMuMTUtNC41NSwzLjYxLTcuMiw3LjgzLTcuMnM2LjgsMi43Nyw2LjgsNy41NlY2MC4xMWEuNjYuNjYsMCwwLDAsLjY1LjY2aDQuNjlhLjY2LjY2LDAsMCwwLC42NS0uNjZWNDMuMjFDMTgyLDM2LjIsMTc3LjgxLDMxLjI2LDE3MC4xLDMxLjI2WiIvPjxwYXRoIGNsYXNzPSJjbHMtMSIgZD0iTTQ2LjY2LDMxLjI2QTE1LjQ2LDE1LjQ2LDAsMCwwLDM2LDM1LjMyVjE1LjM4YS42Ni42NiwwLDAsMC0xLS41N2wtNC44MSwyLjc4YS4zNC4zNCwwLDAsMC0uMTcuM1Y2MC4xMWEuNjUuNjUsMCwwLDAsLjY1LjY1aDQuNjZhLjY1LjY1LDAsMCwwLC42NS0uNjV2LTIuOGExNS40NiwxNS40NiwwLDAsMCwxMC42Niw0LjA2LDE1LjA2LDE1LjA2LDAsMSwwLDAtMzAuMTFabTAsMjQuNTFhOS4yLDkuMiwwLDAsMS05LjM5LTkuNDYsOS4zOSw5LjM5LDAsMSwxLDE4Ljc4LDBBOS4yLDkuMiwwLDAsMS00Ni42Niw1NS43N1oiLz48L3N2Zz4=');
    background-repeat: no-repeat;
    background-size: contain;
    display: inline-block;
    width: 150px;
    height: 60px;
}

/* 2-Color Wordmark Reversed — white + coral on dark */
.boomi-logo-2color-reversed {
    background-image: url('data:image/svg+xml;base64,PHN2ZyBpZD0iTG9nb3MiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgd2lkdGg9IjE3OCIgaGVpZ2h0PSI1MiIgdmlld0JveD0iMCAwIDE3OCA1MiI+PGRlZnM+PHN0eWxlPi5jbHMtMXtmaWxsOiNmZjdjNjY7fS5jbHMtMntmaWxsOiNmZmY7fTwvc3R5bGU+PC9kZWZzPjxjaXJjbGUgY2xhc3M9ImNscy0xIiBjeD0iMTczIiBjeT0iOS40IiByPSI0Ii8+PHBhdGggY2xhc3M9ImNscy0yIiBkPSJNNTYsMTguN2ExNi4xLDE2LjEsMCwxLDEsLjgsMzIuMkg1NmExNi4xLDE2LjEsMCwwLDEtLjgtMzIuMlpNNTYsNDVhMTAsMTAsMCwwLDAsMTAuMS05LjZ2LS41YTEwLjEsMTAuMSwwLDEsMC0yMC4yLDBoMEE5Ljc4LDkuNzgsMCwwLDAsNTUuNSw0NVoiLz48cGF0aCBjbGFzcz0iY2xzLTIiIGQ9Ik05Mi43LDE4LjdBMTYuMSwxNi4xLDAsMSwxLDc2LjMsMzQuOEExNS45LDE1LjksMCwwLDEsOTIuMSwxOC43Wm0wLDI2LjNhMTAsMTAsMCwwLDAsMTAuMS05LjZ2LS41YTEwLjEsMTAuMSwwLDEsMC0yMC4yLDBoMEE5Ljc4LDkuNzgsMCwwLDAsOTIuMiw0NVoiLz48cGF0aCBjbGFzcz0iY2xzLTIiIGQ9Ik0xNjkuOCw0OS43VjE5LjRhLjY4LjY4LDAsMCwxLC43LS43aDVhLjY4LjY4LDAsMCwxLC43LjdoMFY0OS42YS42OC42OCwwLDAsMS0uNy43aC01QS42MS42MSwwLDAsMSwxNjkuOCw0OS43WiIvPjxwYXRoIGNsYXNzPSJjbHMtMiIgZD0iTTE1MS4xLDE4LjdBMTMuMSwxMy4xLDAsMCwwLDE0MCwyNC41Yy0yLTMuNi01LjctNS44LTExLTUuOGExMS4xLDExLjEsMCwwLDAtOS40LDQuNlYxOC40YS42OC42OCwwLDAsMC0uNy0uNy42LjYsMCwwLDAtLjQuMWwtNS4yLDNjLS4xLjEtLjIuMi0uMi4zVjQ5LjdhLjY4LjY4LDAsMCwwLC43LjdoNWEuNjguNjgsMCwwLDAsLjctLjdWMzIuOWMwLTUuMSwzLjgtOC4xLDguNC04LjFzNy4zLDMsNy4zLDguMVY0OS42YS42OC42OCwwLDAsMCwuNy43aDVhLjY4LjY4LDAsMCwwLC43LS43VjMyLjVjLjItNC45LDMuOS03LjcsOC40LTcuN3M3LjMsMyw3LjMsOC4xVjQ5LjdhLjY4LjY4LDAsMCwwLC43LjdoNWEuNjguNjgsMCwwLDAsLjctLjdWMzEuNUMxNjMuOSwyNCwxNTkuNCwxOC43LDE1MS4xLDE4LjdaIi8+PHBhdGggY2xhc3M9ImNscy0yIiBkPSJNMTguOSwxOC43QTE2LjE4LDE2LjE4LDAsMCwwLDcuNSwyMy4xVjEuN0EuNjguNjgsMCwwLDAsNi44LDEsLjYuNiwwLDAsMCw2LjQsMS4xbC01LjIsMy0uMi4zVjQ5LjZhLjY4LjY4LDAsMCwwLC43LjdoNWEuNjguNjgsMCwwLDAsLjctLjdoMHYtM0ExNi42MywxNi42MywwLDAsMCwxOC44LDUxYTE2LjEsMTYuMSwwLDAsMCwuOC0zMi4yLDEuNywxLjcsMCwwLDAtLjctLjFabTAsMjYuM0ExMCwxMCwwLDAsMSw4LjgsMzUuNHYtLjVhMTAuMSwxMC4xLDAsMCwxLDIwLjIsMEE5Ljc4LDkuNzgsMCwwLDEsMTkuNCw0NVoiLz48L3N2Zz4=');
    background-repeat: no-repeat;
    background-size: contain;
    display: inline-block;
    width: 150px;
    height: 44px;
}

/* Boomi Mark — 1-Color Positive (Navy circle) */
.boomi-mark-1color {
    background-image: url('data:image/svg+xml;base64,PHN2ZyBpZD0iTGF5ZXJfMSIgZGF0YS1uYW1lPSJMYXllciAxIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA5MCA5MCI+PGRlZnM+PHN0eWxlPi5jbHMtMXtmaWxsOiMwNjNkNTg7fS5jbHMtMntmaWxsOiNmZmY7fTwvc3R5bGU+PC9kZWZzPjxnIGlkPSJCb29taV9JY29uX0xvZ29fMS1Db2xvcl9Qb3NpdGl2ZV9SR0IiIGRhdGEtbmFtZT0iQm9vbWkgSWNvbiBMb2dvIDEtQ29sb3IgUG9zaXRpdmUgUkdCIj48cGF0aCBjbGFzcz0iY2xzLTEiIGQ9Ik02OC43Niw0NUEyMy43NiwyMy43NiwwLDEsMSw0NSwyMS4yNCwyMy43NiwyMy43NiwwLDAsMSw2OC43Niw0NSIvPjxwYXRoIGNsYXNzPSJjbHMtMiIgZD0iTTQ3LDM5LjYzYTExLDExLDAsMCwwLTcuNTYsMi44OFYyOC4zN2EuNDYuNDYsMCwwLDAtLjY5LS40bC0zLjQxLDJhLjI0LjI0LDAsMCwwLS4xMi4yMVY2MC4wOGEuNDcuNDcsMCwwLDAsLjQ2LjQ2aDMuM2EuNDYuNDYsMCwwLDAsLjQ2LS40NnYtMkExMSwxMSwwLDAsMCw0Nyw2MWExMC42NywxMC42NywwLDEsMCwwLTIxLjM0TTQ3LDU3YTYuNyw2LjcsMCwxLDEsNi42Ni02LjdBNi41Myw2LjUzLDAsMCwxLDQ3LDU3Ii8+PHBhdGggY2xhc3M9ImNscy0yIiBkPSJNNjAuMjEsMzcuMTJhMi42MiwyLjYyLDAsMSwxLTIuNjItMi42MiwyLjYyLDIuNjIsMCwwLDEsMi42MiwyLjYyIi8+PC9nPjwvc3ZnPg==');
    background-repeat: no-repeat;
    background-size: contain;
    display: inline-block;
    width: 50px;
    height: 50px;
}

/* Boomi Mark — 1-Color Reversed (White circle) */
.boomi-mark-1color-reversed {
    background-image: url('data:image/svg+xml;base64,PHN2ZyBpZD0iTGF5ZXJfMSIgZGF0YS1uYW1lPSJMYXllciAxIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA5MCA5MCI+PGRlZnM+PHN0eWxlPi5jbHMtMXtmaWxsOiNmZmY7fS5jbHMtMntmaWxsOiMwNjNkNTg7fTwvc3R5bGU+PC9kZWZzPjxnIGlkPSJCb29taV9JY29uX0xvZ29fMS1Db2xvcl9SZXZlcnNlZF9SR0IiIGRhdGEtbmFtZT0iQm9vbWkgSWNvbiBMb2dvIDEtQ29sb3IgUmV2ZXJzZWQgUkdCIj48cGF0aCBjbGFzcz0iY2xzLTEiIGQ9Ik02OC43Niw0NUEyMy43NiwyMy43NiwwLDEsMSw0NSwyMS4yNCwyMy43NiwyMy43NiwwLDAsMSw2OC43Niw0NSIvPjxwYXRoIGNsYXNzPSJjbHMtMiIgZD0iTTQ3LDM5LjYzYTExLDExLDAsMCwwLTcuNTYsMi44OFYyOC4zN2EuNDYuNDYsMCwwLDAtLjY5LS40bC0zLjQxLDJhLjI0LjI0LDAsMCwwLS4xMi4yMVY2MC4wOGEuNDcuNDcsMCwwLDAsLjQ2LjQ2aDMuM2EuNDYuNDYsMCwwLDAsLjQ2LS40NnYtMkExMSwxMSwwLDAsMCw0Nyw2MWExMC42NywxMC42NywwLDEsMCwwLTIxLjM0TTQ3LDU3YTYuNyw2LjcsMCwxLDEsNi42Ni02LjdBNi41Myw2LjUzLDAsMCwxLDQ3LDU3Ii8+PHBhdGggY2xhc3M9ImNscy0yIiBkPSJNNjAuMjEsMzcuMTJhMi42MiwyLjYyLDAsMSwxLTIuNjItMi42MiwyLjYyLDIuNjIsMCwwLDEsMi42MiwyLjYyIi8+PC9nPjwvc3ZnPg==');
    background-repeat: no-repeat;
    background-size: contain;
    display: inline-block;
    width: 50px;
    height: 50px;
}

/* Boomi Mark — 2-Color Reversed (White + Navy + Coral dot) */
.boomi-mark-2color-reversed {
    background-image: url('data:image/svg+xml;base64,PHN2ZyBpZD0iTGF5ZXJfMSIgZGF0YS1uYW1lPSJMYXllciAxIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCA5MCA5MCI+PGRlZnM+PHN0eWxlPi5jbHMtMXtmaWxsOiNmZmY7fS5jbHMtMntmaWxsOiMwNjNkNTg7fS5jbHMtM3tmaWxsOiNmOTdjNjc7fTwvc3R5bGU+PC9kZWZzPjxnIGlkPSJCb29taV9JY29uX0xvZ29fMi1Db2xvcl9SZXZlcnNlZF9SR0IiIGRhdGEtbmFtZT0iQm9vbWkgSWNvbiBMb2dvIDItQ29sb3IgUmV2ZXJzZWQgUkdCIj48cGF0aCBjbGFzcz0iY2xzLTEiIGQ9Ik02OC43Niw0NUEyMy43NiwyMy43NiwwLDEsMSw0NSwyMS4yNCwyMy43NiwyMy43NiwwLDAsMSw2OC43Niw0NSIvPjxwYXRoIGNsYXNzPSJjbHMtMiIgZD0iTTQ3LDM5LjYzYTExLDExLDAsMCwwLTcuNTYsMi44OFYyOC4zN2EuNDYuNDYsMCwwLDAtLjY5LS40bC0zLjQxLDJhLjI0LjI0LDAsMCwwLS4xMi4yMVY2MC4wOGEuNDcuNDcsMCwwLDAsLjQ2LjQ2aDMuM2EuNDYuNDYsMCwwLDAsLjQ2LS40NnYtMkExMSwxMSwwLDAsMCw0Nyw2MWExMC42NywxMC42NywwLDEsMCwwLTIxLjM0TTQ3LDU3YTYuNyw2LjcsMCwxLDEsNi42Ni02LjdBNi41Myw2LjUzLDAsMCwxLDQ3LDU3Ii8+PHBhdGggY2xhc3M9ImNscy0zIiBkPSJNNjAuMjEsMzcuMTJhMi42MiwyLjYyLDAsMSwxLTIuNjItMi42MiwyLjYyLDIuNjIsMCwwLDEsMi42MiwyLjYyIi8+PC9nPjwvc3ZnPg==');
    background-repeat: no-repeat;
    background-size: contain;
    display: inline-block;
    width: 50px;
    height: 50px;
}

/* Boomi Mark — 2-Color Large (2000×2000 for favicons/app icons) */
.boomi-mark-2color-large {
    background-image: url('data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iVVRGLTgiPz48c3ZnIGlkPSJMYXllcl8xIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyMDAwIiBoZWlnaHQ9IjIwMDAiIHZpZXdCb3g9IjAgMCAyMDAwIDIwMDAiPjxkZWZzPjxzdHlsZT4uY2xzLTF7ZmlsbDojMDAzZDU4O30uY2xzLTJ7ZmlsbDojZmZmO30uY2xzLTN7ZmlsbDojZmY3YzY2O308L3N0eWxlPjwvZGVmcz48ZyBpZD0iQm9vbWlfSWNvbl9Mb2dvXzItQ29sb3JfUG9zaXRpdmVfUkdCIj48Zz48cGF0aCBjbGFzcz0iY2xzLTEiIGQ9Ik0xOTM3LjMyLDEwMDBjMCw1MTcuNjctNDE5LjY2LDkzNy4zMy05MzcuMzMsOTM3LjMzUzYyLjY3LDE1MTcuNjcsNjIuNjcsMTAwMCw0ODIuMzMsNjIuNjgsMTAwMCw2Mi42OHM5MzcuMzMsNDE5LjY2LDkzNy4zMyw5MzcuMzMiLz48cGF0aCBjbGFzcz0iY2xzLTIiIGQ9Ik0xMDc2LjksNzg4LjA5Yy0xMTguMzQsMC0yMjIuMTUsNDIuODEtMjk4LjA4LDExMy41M1YzNDQuMDhjMC0xNC4wNS0xNS4yMS0yMi44My0yNy4zOC0xNS44MWwtMTM0LjQyLDc3LjYxYy0yLjk5LDEuNzItNC44Miw0LjktNC44Miw4LjM2VjE1OTQuNzFjMCwxMC4wOCw4LjE3LDE4LjI2LDE4LjI1LDE4LjI2aDEzMC4xMmMxMC4wNywwLDE4LjI1LTguMTgsMTguMjUtMTguMjZ2LTc4LjQxYzc1LjkzLDcwLjcxLDE3OS43NCwxMTMuNTMsMjk4LjA4LDExMy41MywyNDUuNzksMCw0MjkuMjktMTg0LjM0LDQyOS4yOS00MjAuODdzLTE4My40OS00MjAuODctNDI5LjI5LTQyMC44N20wLDY4NS4xOGMtMTUyLjM1LDAtMjYyLjYyLTExNS4zMi0yNjIuNjItMjY0LjMxczExMC4yNy0yNjQuMzIsMjYyLjYyLTI2NC4zMiwyNjIuNjIsMTE1LjMzLDI2Mi42MiwyNjQuMzItMTEwLjI3LDI2NC4zMS0yNjIuNjIsMjY0LjMxIi8+PHBhdGggY2xhc3M9ImNscy0zIiBkPSJNMTYwMC4yLDY4OS4yMWMwLDU3LjEyLTQ2LjMxLDEwMy40My0xMDMuNDMsMTAzLjQzcy0xMDMuNDMtNDYuMzEtMTAzLjQzLTEwMy40Myw0Ni4zMS0xMDMuNDMsMTAzLjQzLTEwMy40MywxMDMuNDMsNDYuMzEsMTAzLjQzLDEwMy40MyIvPjwvZz48L2c+PC9zdmc+');
    background-repeat: no-repeat;
    background-size: contain;
    display: inline-block;
    width: 100px;
    height: 100px;
}
```

## HTML Usage Examples

```html
<!-- Header on light background — inline SVG wordmark -->
<header style="display:flex; align-items:center; padding: 1rem 2rem; background:#fff;">
    <a href="/" aria-label="Boomi home">
        <!-- paste light inline SVG here, width="160" height="46" -->
    </a>
    <nav style="margin-left:auto;">
        Application Name
    </nav>
</header>

<!-- Header on dark/navy background — inline SVG wordmark -->
<header style="display:flex; align-items:center; padding: 1rem 2rem; background:#273E59;">
    <a href="/" aria-label="Boomi home">
        <!-- paste dark inline SVG here, width="160" height="46" -->
    </a>
    <nav style="margin-left:auto; color:#fff;">
        Application Name
    </nav>
</header>

<!-- Footer on dark background — mark only (compact) -->
<footer style="background: var(--boomi-navy); display:flex; align-items:center; gap:1rem; padding:1rem 2rem;">
    <div class="boomi-mark-1color-reversed"></div>
    <p style="color:#fff; margin:0;">© 2026 Boomi, LP</p>
</footer>
```
