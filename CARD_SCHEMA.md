# Health Coach Card JSON Schema

This document defines the canonical JSON schema for all health coach cards. All card generators and processors MUST follow this format.

## Base Card Structure

```json
{
  "card_id": "string (required) - unique identifier, format: {card_type}_{subtype}_{3-digit-number}",
  "card_type": "string (required) - one of: insight, action_prompt, rich_format, sharing, connected_data, upload",
  "subtype": "string (optional) - depends on card_type, see Card Types section",
  "variant": "string (optional) - e.g., 'standard', 'with_image', 'with_graph'",

  "content": {
    // All user-facing content goes here - see Content Object section
  },

  "metadata": {
    // All generation/personalization metadata goes here - see Metadata Object section
  }
}
```

## Content Object

All display content MUST be inside the `content` object. Never put display fields at root level.

### Required Fields (All Card Types)

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `title` | string | 20-40 chars, 1 line | Main headline (use `title`, NOT `headline`) |
| `body` | string | 60-130 chars, 2-3 lines | Main explanatory text |

### Common Optional Fields

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `badge` | string | max 15 chars | Status indicator (e.g., "New", "Urgent") |
| `image` | string | URL or path | Illustration (PNG/SVG, max 500KB) |
| `source_label` | string | max 40 chars | Data attribution |
| `helper_text` | string | max 80 chars | Additional guidance |
| `context_label` | string | max 20 chars | Time/effort indicator |
| `footer` | string | max 60 chars | Bottom text |

### Action Fields

Use these exact field names - do NOT use alternatives like `cta_button`, `cta_primary`, `connect_action`:

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `primary_action` | string | max 25 chars | Main CTA button text |
| `secondary_action` | string | max 15 chars | Secondary action (e.g., "Skip", "Not now") |

### Stats Container

For displaying metrics. Use this structure, NOT `primary_stat`/`supporting_stat`/`dashboard_metrics`:

```json
{
  "stats_container": {
    "title": "string (optional)",
    "stats": [
      {
        "label": "string (required)",
        "value": "string (required)",
        "context": "string (optional) - additional explanation",
        "trend": "string (optional) - e.g., 'up', 'down', 'stable'"
      }
    ]
  }
}
```

### Interactive Elements (Action Prompt - Input Cards)

```json
{
  "interactive_element": {
    "type": "slider | mcq | word_cloud",
    "options": ["array of string choices (for mcq/word_cloud)"],
    "min_value": "number (for slider, default 0)",
    "max_value": "number (for slider, default 10)",
    "min_label": "string (for slider, max 12 chars)",
    "max_label": "string (for slider, max 12 chars)",
    "max_selections": "number (for word_cloud, default 3)"
  }
}
```

### Question/Answer (Action Prompt Cards)

```json
{
  "question": "string - the question text",
  "answer_choices": [
    {
      "label": "string (max 40 chars)",
      "value": "string (optional, for data storage)"
    }
  ]
}
```

### Accordion Items (Rich Format - FAQ)

```json
{
  "accordion_items": [
    {
      "question": "string (required)",
      "answer": "string (required)"
    }
  ]
}
```

### Data Visualization (Rich Format)

```json
{
  "visualization": {
    "type": "line_chart | bar_chart | gauge | timeline",
    "title": "string (optional)",
    "data_points": [
      {
        "label": "string",
        "value": "number or string",
        "date": "string (ISO format, optional)"
      }
    ],
    "x_axis_label": "string (optional)",
    "y_axis_label": "string (optional)"
  }
}
```

### Share Content (Sharing Cards)

```json
{
  "share_content": {
    "recipient_type": "doctor | coach | family | screener",
    "content_summary": "string (60-80 chars) - what's being shared",
    "share_methods": ["whatsapp", "link", "pdf", "email"],
    "privacy_note": "string (max 80 chars)",
    "pre_filled_message": "string (optional) - for WhatsApp/email"
  }
}
```

### Connected Data (Connected Data Cards)

```json
{
  "data_source_name": "string (e.g., 'Apple Watch', 'Google Calendar')",
  "data_source_icon": "string (URL or emoji)",
  "supported_integrations": ["array of integration names"]
}
```

### Upload Content (Upload Cards)

```json
{
  "upload_methods": ["upload_pdf", "whatsapp", "email_forward"],
  "accepted_formats": "string (e.g., 'PDF, JPG, PNG')"
}
```

### Progress Tracking (Action Prompt - Progress Cards)

```json
{
  "stepper": {
    "current_step": "number (1-indexed)",
    "total_steps": "number (3-5)",
    "steps": [
      {
        "label": "string",
        "status": "completed | current | upcoming",
        "badge": "string (optional)"
      }
    ]
  }
}
```

### Experiment/Habit Tracking

```json
{
  "experiment_steps": [
    {
      "step": "number",
      "instruction": "string"
    }
  ],

  "habit_tracker": [
    {
      "habit_name": "string",
      "adherence_display": "string (e.g., '5/7 days')",
      "adherence_percent": "number",
      "streak_days": "number (optional)",
      "status": "on_track | needs_attention | completed"
    }
  ]
}
```

## Metadata Object

All generation and personalization metadata MUST be in the `metadata` object.

```json
{
  "metadata": {
    "motivation_variant": "fear | achievement | curiosity | neutral",
    "medical_vs_lifestyle": "medical | lifestyle",
    "persona_complexity": "low | medium | high",
    "rationale": "string - why this card was generated/selected",
    "scheduler_priority": "number (1-10, 10 = highest)",
    "data_sources_used": ["array of source names"],
    "milestone": "string (optional) - user journey milestone",
    "generated_at": "string (ISO timestamp)",
    "cbt_technique": "string (optional) - behavioral technique used"
  }
}
```

## Card Types Reference

### 1. Insight Card
- **card_type**: `"insight"`
- **subtype**: `null` or `"standard"`, `"with_image"`, `"with_graph"`
- **Required content**: `title`, `body`, `secondary_action`
- **Optional content**: `image`, `stats_container`, `source_label`, `badge`

### 2. Action Prompt Card
- **card_type**: `"action_prompt"`
- **subtype**: `"input"`, `"cta"`, or `"progress"`
- **Required content**: `title`, `body`, `primary_action`, `secondary_action`

#### Input Subtype
- **Additional required**: `interactive_element`
- **Optional**: `question`, `answer_choices`, `context_label`, `helper_text`

#### CTA Subtype
- **Optional**: `category_label`, `image`, `icon`

#### Progress Subtype
- **Additional required**: `stepper`

### 3. Rich Format Card
- **card_type**: `"rich_format"`
- **subtype**: `"data_viz"`, `"health_report"`, or `"faq"`

#### Data Viz Subtype
- **Additional required**: `visualization`
- **Optional**: `source_label`

#### Health Report Subtype
- **Additional required**: `summary_sections` (array of collapsible sections)

#### FAQ Subtype
- **Additional required**: `accordion_items`

### 4. Sharing Card
- **card_type**: `"sharing"`
- **Required content**: `title`, `body`, `share_content`

### 5. Connected Data Card
- **card_type**: `"connected_data"`
- **Required content**: `title`, `body`, `data_source_name`, `primary_action`
- **Optional**: `secondary_action`, `data_source_icon`

### 6. Upload Card
- **card_type**: `"upload"`
- **Required content**: `title`, `body`, `upload_methods`
- **Optional**: `secondary_action`, `helper_text`, `accepted_formats`

## Validation Rules

1. **Character limits are strict** - truncate or rewrite if exceeded
2. **Required fields must be present** - never omit required fields
3. **Use exact field names** - no synonyms (e.g., use `title` not `headline`)
4. **All content in `content` object** - never at root level
5. **All metadata in `metadata` object** - never at root level
6. **card_id format**: `{type}_{subtype}_{number}` (e.g., `insight_standard_001`)
7. **Arrays must have items** - don't include empty arrays
8. **Stats must have both label and value** - skip if either is missing

## Example Cards

### Insight Card

```json
{
  "card_id": "insight_standard_001",
  "card_type": "insight",
  "subtype": "standard",

  "content": {
    "title": "Your sleep improved this week",
    "body": "You averaged 7.5 hours of sleep, up from 6.8 hours last week. Consistent bedtimes are paying off.",
    "secondary_action": "Learn More",
    "stats_container": {
      "stats": [
        {"label": "This week", "value": "7.5h", "trend": "up"},
        {"label": "Last week", "value": "6.8h"}
      ]
    },
    "source_label": "Apple Watch"
  },

  "metadata": {
    "motivation_variant": "achievement",
    "medical_vs_lifestyle": "lifestyle",
    "persona_complexity": "medium",
    "rationale": "User showed 10% improvement in sleep duration; reinforcing positive behavior",
    "scheduler_priority": 7,
    "data_sources_used": ["apple_watch_sleep"]
  }
}
```

### Action Prompt - Input Card

```json
{
  "card_id": "action_prompt_input_002",
  "card_type": "action_prompt",
  "subtype": "input",

  "content": {
    "title": "How are you feeling today?",
    "body": "A quick check-in helps us personalize your health insights and track patterns over time.",
    "interactive_element": {
      "type": "slider",
      "min_value": 1,
      "max_value": 10,
      "min_label": "Not great",
      "max_label": "Excellent"
    },
    "primary_action": "Submit",
    "secondary_action": "Skip",
    "context_label": "30 seconds"
  },

  "metadata": {
    "motivation_variant": "curiosity",
    "medical_vs_lifestyle": "lifestyle",
    "persona_complexity": "low",
    "rationale": "Daily mood tracking for pattern detection",
    "scheduler_priority": 5,
    "data_sources_used": []
  }
}
```

### Connected Data Card

```json
{
  "card_id": "connected_data_wearable_003",
  "card_type": "connected_data",

  "content": {
    "title": "Unlock sleep insights",
    "body": "Connect your Apple Watch to see detailed sleep stages, heart rate during sleep, and personalized recommendations.",
    "data_source_name": "Apple Watch",
    "data_source_icon": "watch",
    "primary_action": "Connect Apple Watch",
    "secondary_action": "Maybe later"
  },

  "metadata": {
    "motivation_variant": "curiosity",
    "medical_vs_lifestyle": "lifestyle",
    "persona_complexity": "low",
    "rationale": "User uploaded labs but has no wearable connected; sleep data would enhance insights",
    "scheduler_priority": 6,
    "data_sources_used": []
  }
}
```

## Migration Notes

When updating existing cards to this schema:

1. Move all root-level content fields into `content` object
2. Rename `headline` to `title`
3. Consolidate CTA fields to `primary_action`/`secondary_action`
4. Consolidate stat fields to `stats_container`
5. Move personalization fields to `metadata` object
6. Add missing required fields with placeholder values
7. Remove empty arrays and null optional fields
