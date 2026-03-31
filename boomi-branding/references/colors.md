# Boomi Color Reference

## Primary Colors

| Name    | Hex       | RGB              | CMYK             | Usage                            |
|---------|-----------|------------------|------------------|----------------------------------|
| Coral   | `#FF7C69` | 255 / 124 / 105  | 0/65/63/0        | Primary brand, CTAs, processes   |
| Purple  | `#A93FA5` | 169 / 63 / 165   | 47/89/0/0        | Secondary brand, connectors      |
| Navy    | `#273E59` | 39 / 62 / 89     | 88/67/38/34      | Text, headers, APIs              |
| White   | `#FFFFFF` | 255/255/255      | 0/0/0/0          | Backgrounds                      |
| Black   | `#000000` | 0/0/0            | 0/0/0/100        | Strong contrast                  |

## Secondary Colors (Use sparingly — internal/technical docs only)

| Name        | Hex       | RGB             | CMYK          |
|-------------|-----------|-----------------|---------------|
| Periwinkle  | `#4E47E7` | 78/71/231       | 78/72/0/0     |
| Blue        | `#009EE2` | 0/158/226       | 77/40/0/0     |
| Green       | `#04C788` | 4/199/136       | 72/0/63/0     |
| Purple Alt  | `#A6327D` | 166/50/125      | 48/89/1/0     |

Secondary colors are only appropriate for:
- Lower-level web pages
- Internal presentations and documents
- Infographics and data visualizations
- Technical documentation

**Never** use secondary colors in primary brand communications.

## Neutral Colors

```css
--white: #FFFFFF;
--gray-50: #F9FAFB;
--gray-100: #F3F4F6;
--gray-200: #E5E7EB;
--gray-300: #D1D5DB;
--gray-600: #4B5563;
--gray-800: #1F2937;
--black: #000000;
```

## Accent Colors (Diagrams & Highlights)

```css
--accent-yellow: #F59E0B;   /* Warnings, attention */
--accent-red: #EF4444;      /* Errors, critical items */
--accent-teal: #14B8A6;     /* Supporting elements */
--accent-orange: #F97316;   /* API endpoints */
```

## Gradients

### Primary Brand Gradient (coral → purple)
```css
background: linear-gradient(135deg, #FF7C69 0%, #A93FA5 100%); /* diagonal */
background: linear-gradient(90deg, #FF7C69 0%, #A93FA5 100%);  /* horizontal */
background: linear-gradient(180deg, #FF7C69 0%, #A93FA5 100%); /* vertical */
```

Use the primary gradient for: hero sections, feature cards, CTAs, background accents.

### Secondary Gradients (internal use only)
```css
background: linear-gradient(135deg, #4E47E7 0%, #A6327D 100%); /* periwinkle → purple */
background: linear-gradient(135deg, #009EE2 0%, #04C788 100%); /* blue → green */
background: linear-gradient(135deg, #4E47E7 0%, #009EE2 100%); /* periwinkle → blue */
background: linear-gradient(135deg, #A6327D 0%, #04C788 100%); /* purple → green */
```

**Note**: When using gradients with coral, green, or blue, be aware of low-contrast
zones where the gradient passes through those hues — avoid placing body text there.

## Contrast Ratios & WCAG Compliance

| Background     | Text Color | Ratio   | AA Normal | AA Large | AAA Normal | AAA Large |
|----------------|------------|---------|-----------|----------|------------|-----------|
| Navy `#273E59` | White      | 14.21:1 | ✓         | ✓        | ✓          | ✓         |
| White `#FFF`   | Navy       | 14.21:1 | ✓         | ✓        | ✓          | ✓         |
| Navy `#273E59` | Coral      | 5.6:1   | ✓         | ✓        | ✗          | ✓         |
| Purple `#A93FA5`| White     | 6.25:1  | ✓         | ✓        | ✗          | ✓         |
| Periwinkle     | White      | 5.97:1  | ✓         | ✓        | ✗          | ✓         |
| Blue `#009EE2` | White      | 3.74:1  | ✗         | ✓        | ✗          | ✗         |
| Green `#04C788`| White      | 2.28:1  | ✗         | ✗        | ✗          | ✗         |

### WCAG Thresholds
- AA Normal text: ≥ 4.5:1
- AA Large text / graphics: ≥ 3:1
- AAA Normal text: ≥ 7:1
- AAA Large text: ≥ 4.5:1

### Do-Not-Use Combinations
- Green `#04C788` with white (any text size)
- White on green background
- Navy with periwinkle (too similar)
- Purple with coral (poor readability)
- Blue with periwinkle (too similar)

## Status Indicator Colors

```css
.status-success   { background-color: #04C788; } /* Green */
.status-processing{ background-color: #FF7C69; } /* Coral */
.status-info      { background-color: #009EE2; } /* Blue */
.status-warning   { background-color: #F59E0B; } /* Yellow */
.status-error     { background-color: #EF4444; } /* Red */
.status-paused    { background-color: #94A3B8; } /* Gray */
```

## Diagram Layer Colors

### Brand-Level Diagrams (primary palette only)
```css
--layer-process:   #FF7C69;  /* Coral — Boomi processes */
--layer-connector: #A93FA5;  /* Purple — connectors */
--layer-api:       #273E59;  /* Navy — APIs */
--layer-external:  #94A3B8;  /* Gray — external systems */
```

### Technical/Internal Diagrams (secondary palette allowed)
```css
--layer-data:        #A6327D;  /* secondary purple — databases */
--layer-application: #04C788;  /* secondary green — applications */
--layer-integration: #009EE2;  /* secondary blue — integrations */
--layer-workflow:    #4E47E7;  /* periwinkle — workflows */
--layer-event:       #F59E0B;  /* yellow — events/messaging */
--layer-external:    #94A3B8;  /* gray — external systems */
```

## Light / Dark Theme Defaults

### Light Theme
```
Background: #F9FAFB
Surface:    #FFFFFF
Text:       #273E59
Accent 1:   #FF7C69
Accent 2:   #A93FA5
```

### Dark Theme
```
Background: #273E59
Surface:    #1F2937
Text:       #F3F4F6
Accent 1:   #FF7C69
Accent 2:   #A93FA5
```
