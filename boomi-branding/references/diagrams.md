# Boomi Diagram Guidelines

## Component Shapes

| Component Type   | Shape                              |
|------------------|------------------------------------|
| Boomi Processes  | Rounded rectangle, coral gradient  |
| Connectors       | Small circle with connector icon   |
| Applications     | Rectangle with app icon            |
| Databases        | Cylinder or rectangle w/ DB icon   |
| APIs             | Hexagon or rectangle with API badge|
| Events/Messages  | Parallelogram or message icon      |
| External Systems | Dashed border rectangle            |
| AtomSphere       | Cloud shape, Boomi coral           |
| Data Transform   | Rectangle with transform icon (purple) |
| Decision         | Diamond with condition label       |

## Color Layers by Diagram Type

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

## Arrow / Connector Styles

| Type              | Style                              |
|-------------------|------------------------------------|
| Synchronous call  | Solid arrow                        |
| Asynchronous call | Dashed arrow                       |
| Data flow         | Bold arrow with data label         |
| Bidirectional     | Double-headed arrow                |
| Error/Exception   | Red dashed arrow                   |

## Text in Diagrams

| Usage          | Font            | Size    | Weight  |
|----------------|-----------------|---------|---------|
| Component names| Poppins         | 14–16px | SemiBold|
| Labels         | Poppins         | 12–14px | Regular |
| Descriptions   | Poppins         | 10–12px | Light   |

## Integration Pattern Colors

```css
--pattern-sync:      #FF7C69;  /* Coral — synchronous request-reply */
--pattern-async:     #A93FA5;  /* Purple — asynchronous messaging */
--pattern-batch:     #8B5CF6;  /* Batch processing */
--pattern-streaming: #10B981;  /* Real-time streaming */
--pattern-event:     #F59E0B;  /* Event-driven */
--pattern-scheduled: #273E59;  /* Navy — scheduled processes */
```

## Mermaid Configuration

Use this init block at the top of every Mermaid diagram for consistent Boomi branding:

```
%%{init: {
  'theme': 'base',
  'themeVariables': {
    'primaryColor': '#FFFFFF',
    'primaryTextColor': '#273E59',
    'primaryBorderColor': '#FF7C69',
    'lineColor': '#6B7280',
    'secondaryColor': '#F3F4F6',
    'tertiaryColor': '#FFE5E0',
    'fontSize': '14px',
    'fontFamily': 'Poppins, sans-serif'
  }
}}%%
```

## Boomi Component Label Format

```
Process:     "Process Name | v1.0"
Connector:   "Connector Type: Operation"
Shape:       "Shape Name (Type)"
Connection:  "Connection Profile Name"
```

## Best Practices

1. **Brand-level diagrams**: Use primary colors only (coral, purple, navy)
2. **Internal/technical diagrams**: May incorporate secondary colors
3. Use consistent shapes for Boomi component types across all diagrams
4. Limit colors to 4–5 per diagram for clarity
5. Include a legend for complex diagrams
6. Maintain adequate whitespace between nodes
7. Label all connections with data/operation names
8. Show error handling paths in red (`#EF4444`)
9. Show success paths in green (`#04C788`) for status diagrams
10. Use gray (`#94A3B8`) for external/third-party systems

## Example: Boomi Architecture Diagram Component Colors

**Brand-Level**
```
Boomi Process (Coral):     #FF7C69
Connector (Purple):        #A93FA5
API Endpoint (Navy):       #273E59
External System (Gray):    #94A3B8
```

**Technical/Internal**
```
Boomi Process (Coral):         #FF7C69
Connector (Purple):            #A93FA5
Database (Secondary Purple):   #A6327D
Application (Secondary Green): #04C788
Integration (Secondary Blue):  #009EE2
Workflow (Periwinkle):         #4E47E7
Event Queue (Yellow):          #F59E0B
External System (Gray):        #94A3B8
```
