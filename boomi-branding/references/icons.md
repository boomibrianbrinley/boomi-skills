# Boomi Icons Reference — Phosphor Icons

## CDN Setup

### Single Weight (Recommended)
```html
<!-- Regular weight — most common, use .ph class -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@phosphor-icons/web@2.1.2/src/regular/style.css" />
```

### All Weights (full library ~3MB)
```html
<script src="https://cdn.jsdelivr.net/npm/@phosphor-icons/web@2.1.2"></script>
```

### Individual Weight Links
```html
<!-- Pick only what you need -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@phosphor-icons/web@2.1.2/src/thin/style.css" />
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@phosphor-icons/web@2.1.2/src/light/style.css" />
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@phosphor-icons/web@2.1.2/src/regular/style.css" />
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@phosphor-icons/web@2.1.2/src/bold/style.css" />
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@phosphor-icons/web@2.1.2/src/fill/style.css" />
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@phosphor-icons/web@2.1.2/src/duotone/style.css" />
```

## Basic Usage

```html
<i class="ph ph-house"></i>
<i class="ph ph-database" style="color: #04C788;"></i>
<i class="ph ph-warning" style="color: #FF7C69;"></i>
```

## Styling with Boomi Colors

```css
.ph {
    font-size: 24px;
    color: var(--boomi-blue);   /* default blue */
}

/* Common patterns */
.icon-success { color: var(--boomi-green);      font-size: 24px; }
.icon-warning { color: var(--boomi-coral);      font-size: 24px; }
.icon-info    { color: var(--boomi-blue);       font-size: 24px; }
.icon-data    { color: var(--boomi-purple);     font-size: 24px; }
.icon-nav     { color: var(--boomi-navy);       font-size: 20px; }
```

## Common Icon Patterns

### Navigation
```html
<i class="ph ph-house"        style="color: #273E59;"></i>
<i class="ph ph-arrow-right"  style="color: #009EE2;"></i>
<i class="ph ph-arrow-left"   style="color: #009EE2;"></i>
<i class="ph ph-caret-down"   style="color: #273E59;"></i>
<i class="ph ph-list"         style="color: #273E59;"></i>
```

### Actions
```html
<i class="ph ph-plus-circle"  style="color: #04C788;"></i>
<i class="ph ph-check-circle" style="color: #04C788;"></i>
<i class="ph ph-x-circle"     style="color: #FF7C69;"></i>
<i class="ph ph-pencil"       style="color: #009EE2;"></i>
<i class="ph ph-trash"        style="color: #EF4444;"></i>
<i class="ph ph-download"     style="color: #009EE2;"></i>
<i class="ph ph-upload"       style="color: #04C788;"></i>
```

### Status
```html
<i class="ph ph-warning-circle" style="color: #FF7C69;"></i>
<i class="ph ph-info-circle"    style="color: #009EE2;"></i>
<i class="ph ph-check-circle"   style="color: #04C788;"></i>
<i class="ph ph-x-circle"       style="color: #EF4444;"></i>
<i class="ph ph-clock"          style="color: #F59E0B;"></i>
<i class="ph ph-pause-circle"   style="color: #94A3B8;"></i>
```

### Data & Integration
```html
<i class="ph ph-database"         style="color: #A93FA5;"></i>
<i class="ph ph-chart-line"       style="color: #009EE2;"></i>
<i class="ph ph-cloud-arrow-up"   style="color: #04C788;"></i>
<i class="ph ph-cloud-arrow-down" style="color: #009EE2;"></i>
<i class="ph ph-arrows-left-right"style="color: #4E47E7;"></i>
<i class="ph ph-plugs"            style="color: #A93FA5;"></i>
<i class="ph ph-gear"             style="color: #273E59;"></i>
<i class="ph ph-funnel"           style="color: #009EE2;"></i>
```

### Boomi-Specific
```html
<i class="ph ph-atom"             style="color: #FF7C69;"></i>   <!-- Boomi Atom -->
<i class="ph ph-cloud"            style="color: #009EE2;"></i>   <!-- Cloud integration -->
<i class="ph ph-flow-arrow"       style="color: #4E47E7;"></i>   <!-- Process flow -->
<i class="ph ph-shuffle"          style="color: #A93FA5;"></i>   <!-- Data transform -->
<i class="ph ph-calendar"         style="color: #273E59;"></i>   <!-- Scheduled process -->
<i class="ph ph-bell"             style="color: #F59E0B;"></i>   <!-- Event/alert -->
```

## Best Practices

1. **Consistency**: Use the same icon weight throughout your project
2. **Default size**: 24px for body text; scale up for headers and emphasis
3. **Color**: Always pair with Boomi brand colors
4. **Accessibility**: Pair icons with descriptive text or `aria-label`
5. **Performance**: Load only the weight(s) you need

## Known Issues & Pitfalls

### ⚠ Icons inside `<h2>` tags cause overlay/rendering bugs
Phosphor icon font glyphs inside block-level heading tags (`<h2>`, `<h3>`) can render with incorrect positioning or overlay adjacent elements. **Never place `<i class="ph ...">` directly inside a heading tag.**

**Fix:** Wrap the icon and heading text together in a flex container outside the heading, or place the icon in a sibling element:
```html
<!-- ✗ Wrong -->
<h2><i class="ph ph-segments"></i> Segments</h2>

<!-- ✓ Correct -->
<div style="display:flex;align-items:center;gap:.5rem;">
  <i class="ph ph-segments"></i>
  <h2 style="margin:0">Segments</h2>
</div>
```

### ⚠ Decorative icons in label-only containers
Do not add icons to short label elements (nav headers, section labels, badges) purely for decoration. If the label text is already self-explanatory, the icon adds visual noise and can render unexpectedly depending on the container's font/line-height context.

**Rule:** Only add a Phosphor icon to a container if it meaningfully distinguishes the item (e.g. status icons, action icons, category icons in a list). If you find yourself reaching for `ph-list`, `ph-folder`, or `ph-tag` next to a text label, omit the icon.

### ⚠ Icons in sticky headers are especially prone to fallback glyph rendering
Phosphor Icons load asynchronously via CDN. In `position: sticky` headers, the icon font may not be fully initialized before the element paints, causing glyphs to render as fallback characters (boxes, folder symbols, etc.) that persist visibly. **Avoid placing Phosphor icons in sticky headers entirely.** Use text-only labels, SVG, or CSS shapes instead for header-level UI elements.

### ⚠ Icons in flex containers need `flex-shrink: 0`
When an icon sits inside a flex row next to wrapping text, the icon can collapse or disappear. Always set `flex-shrink: 0` on the `<i>` element:
```css
.icon-inline { flex-shrink: 0; margin-top: 1px; /* optical alignment */ }
```

## Accessibility Pattern

```html
<!-- Icon with visible label -->
<span style="display: inline-flex; align-items: center; gap: 0.5rem;">
    <i class="ph ph-check-circle" style="color: #04C788;" aria-hidden="true"></i>
    <span>Connected</span>
</span>

<!-- Icon-only button -->
<button aria-label="Delete process">
    <i class="ph ph-trash" aria-hidden="true"></i>
</button>
```
