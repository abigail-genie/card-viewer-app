import streamlit as st
import json
from datetime import datetime

# Page config
st.set_page_config(
    page_title="Health Coach Card Viewer",
    page_icon="🏥",
    layout="wide"
)

# Custom CSS - Simple and minimal
st.markdown("""
<style>
    .card {
        border: 1px solid #ddd;
        padding: 20px;
        margin-bottom: 20px;
        border-radius: 4px;
    }
    .card-type-badge {
        display: inline-block;
        padding: 4px 8px;
        border: 1px solid #666;
        font-size: 0.75em;
        font-weight: 600;
        text-transform: uppercase;
        margin-bottom: 12px;
    }
    .card-title {
        font-size: 1.3em;
        font-weight: 700;
        margin-bottom: 12px;
        margin-top: 8px;
    }
    .card-body {
        line-height: 1.6;
        margin-bottom: 16px;
    }
    .metadata-tag {
        display: inline-block;
        padding: 4px 8px;
        border: 1px solid #999;
        font-size: 0.75em;
        margin-right: 8px;
        margin-bottom: 8px;
    }
    .card-cta {
        border: 2px solid #333;
        padding: 10px 16px;
        text-align: center;
        font-weight: 600;
        margin-bottom: 12px;
    }
    .card-rationale {
        border-left: 3px solid #999;
        padding: 12px;
        font-size: 0.85em;
        margin-top: 12px;
        background: #fafafa;
    }
    .stats-container {
        border: 1px solid #ddd;
        padding: 16px;
        margin: 16px 0;
    }
    .stat-item {
        text-align: center;
        padding: 8px;
    }
    .stat-value {
        font-size: 1.5em;
        font-weight: bold;
    }
    .stat-label {
        font-size: 0.8em;
        margin-top: 4px;
    }
    .section-box {
        border: 1px solid #ddd;
        padding: 12px;
        margin: 12px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("# 🏥 Health Coach Card Viewer")
st.markdown("**Interactive demo of personalized health coaching cards**")

# File uploader - accept up to 10 files
uploaded_files = st.file_uploader(
    "Upload card pack JSON files (up to 10)",
    type=['json'],
    accept_multiple_files=True,
    help="Upload JSON files containing generated health coach cards"
)

def render_card(card, index):
    """Render a single card with all its components"""

    # Get card metadata
    card_type = card.get('card_type', card.get('type', 'insight'))
    type_class = card_type.lower().replace(' ', '-').replace('_', '-')

    # Get content (nested or direct)
    content = card.get('content', {})
    title = content.get('title') or content.get('headline') or card.get('title', 'Untitled')
    body = content.get('body') or card.get('body', '')
    badge = content.get('badge', '')
    helper_text = content.get('helper_text', '')
    context_label = content.get('context_label', '')

    # Get metadata
    motivation_class = card.get('motivation_variant') or card.get('metadata', {}).get('motivation_variant', 'neutral')
    category_class = card.get('medical_vs_lifestyle') or card.get('metadata', {}).get('category', 'lifestyle')
    complexity = card.get('persona_complexity') or card.get('metadata', {}).get('persona_complexity', '')

    # Get CTA (multiple formats)
    cta_primary = content.get('cta_primary', {})
    cta_button = content.get('cta_button', {})
    cta_simple = card.get('cta', {})
    primary_action = content.get('primary_action') or content.get('connect_action') or cta_primary.get('label', '') or cta_button.get('label', '') or cta_simple.get('text', '')
    secondary_action = content.get('secondary_action', '')

    # Get rationale
    rationale = card.get('metadata', {}).get('rationale', '')

    # Get key takeaways
    key_takeaways = content.get('key_takeaways', [])

    # Get stats
    stats_container = content.get('stats_container')
    stats_array = []
    if stats_container:
        if isinstance(stats_container, list):
            stats_array = stats_container
        elif isinstance(stats_container, dict) and 'stats' in stats_container:
            stats_array = stats_container['stats']

    # Get interactive element
    interactive = content.get('interactive_element')

    # Get labels
    category_label = content.get('category_label')
    source_label = content.get('source_label')
    data_source_name = content.get('data_source_name')

    # Get accordion items
    accordion_items = content.get('accordion_items', [])

    # Get summary sections
    summary_sections = content.get('summary_sections', [])

    # Get visual elements
    visual_elements = content.get('visual_elements', {})

    # Get stats variations
    stats = content.get('stats', [])
    primary_stat = content.get('primary_stat')
    supporting_stat = content.get('supporting_stat')
    dashboard_metrics = content.get('dashboard_metrics', [])

    # Get source citation
    source_citation = content.get('source_citation', '')
    footer = content.get('footer', '')

    # Get question/answer choices (for action_prompt cards)
    question_data = content.get('question', '')
    # Handle both string and dict formats for question
    if isinstance(question_data, dict):
        question = question_data.get('text', '')
        # Get answer_choices from question dict or from content directly
        answer_choices = question_data.get('answer_choices', content.get('answer_choices', []))
    else:
        question = question_data
        answer_choices = content.get('answer_choices', [])

    # Get supporting data
    supporting_data = content.get('supporting_data', [])

    # Check if card has any displayable content (use raw values, not defaults)
    has_actual_title = content.get('title') or content.get('headline') or card.get('title')
    has_content = (
        has_actual_title or body or question or
        (answer_choices and len(answer_choices) > 0) or
        badge or category_label or data_source_name or
        (stats and len(stats) > 0 and any(stat.get('label') or stat.get('value') for stat in stats)) or
        (primary_stat and (primary_stat.get('label') or primary_stat.get('value'))) or
        (supporting_stat and (supporting_stat.get('label') or supporting_stat.get('value'))) or
        (supporting_data and len(supporting_data) > 0 and any(data.get('label') or data.get('value') for data in supporting_data)) or
        (dashboard_metrics and len(dashboard_metrics) > 0 and any(metric.get('metric_name') or metric.get('current') for metric in dashboard_metrics)) or
        (visual_elements and isinstance(visual_elements, dict) and visual_elements.get('chart_type')) or
        (accordion_items and len(accordion_items) > 0 and any(item.get('question') or item.get('answer') for item in accordion_items)) or
        (summary_sections and len(summary_sections) > 0 and any(section.get('title') or section.get('metrics') for section in summary_sections)) or
        (key_takeaways and len(key_takeaways) > 0 and any(takeaway for takeaway in key_takeaways if takeaway)) or
        (stats_array and len(stats_array) > 0 and any(stat.get('value') or stat.get('label') for stat in stats_array)) or
        (interactive and interactive.get('type')) or
        primary_action or secondary_action or
        helper_text or context_label or source_label or footer or source_citation
    )

    # Only render card if it has content
    if not has_content:
        return

    # Render card
    with st.container():
        # CONTENT BOX - Start wrapper
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div style="border: 3px solid #333; padding: 24px; margin-bottom: 16px; background: #ffffff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">', unsafe_allow_html=True)

        # Extract last 3 digits from card_id for header
        card_id_str = str(card.get('card_id', ''))
        if card_id_str:
            # Get last 3 characters (digits or otherwise)
            card_number = card_id_str[-3:] if len(card_id_str) >= 3 else card_id_str
            header_text = f"Card #{card_number}"
        else:
            header_text = "Card Information"

        # Header with card number
        st.markdown(f'<div style="font-weight: 700; margin-bottom: 16px; color: #333; font-size: 0.9em; text-transform: uppercase; letter-spacing: 0.5px; border-bottom: 2px solid #333; padding-bottom: 8px;">📄 {header_text}</div>', unsafe_allow_html=True)

        # Card type badge - only show if not default or if there's meaningful content
        if card_type != 'insight' or has_actual_title:
            st.markdown(f'<div class="card-type-badge">{card_type.replace("_", " ")}</div>', unsafe_allow_html=True)

        # Badges
        if badge:
            st.markdown(f'<span class="metadata-tag">{badge}</span>', unsafe_allow_html=True)

        if category_label:
            st.markdown(f'<span class="metadata-tag">{category_label}</span>', unsafe_allow_html=True)

        if data_source_name:
            st.markdown(f'<div style="border: 1px solid #ddd; padding: 8px 12px; display: inline-flex; align-items: center; gap: 8px; margin: 12px 0;"><span>⌚</span><span style="font-size: 0.9em;">{data_source_name}</span></div>', unsafe_allow_html=True)

        # Title and body
        st.markdown(f'<div class="card-title">{title}</div>', unsafe_allow_html=True)
        if body:
            st.markdown(f'<div class="card-body">{body}</div>', unsafe_allow_html=True)

        # Question (for action_prompt cards)
        if question:
            st.markdown(f'<div style="margin: 16px 0; font-weight: 600;">{question}</div>', unsafe_allow_html=True)

        # Answer choices (for action_prompt cards)
        if answer_choices:
            choices_html = '<div style="border: 1px solid #ddd; padding: 12px; margin: 12px 0;">'
            for choice in answer_choices:
                choice_label = choice if isinstance(choice, str) else choice.get('label', '')
                choices_html += f'<div style="padding: 8px; border: 1px solid #ccc; margin: 8px 0; cursor: pointer;">☐ {choice_label}</div>'
            choices_html += '</div>'
            st.markdown(choices_html, unsafe_allow_html=True)

        # Stats variations
        valid_stats = [stat for stat in stats if stat.get('label') or stat.get('value')] if stats else []
        if valid_stats:
            st.markdown('<div class="section-box">', unsafe_allow_html=True)
            for stat in valid_stats:
                cols = st.columns([2, 1, 2])
                with cols[0]:
                    st.markdown(f"**{stat.get('label', '')}**")
                with cols[1]:
                    st.markdown(f"<div style='font-size: 1.2em; font-weight: bold;'>{stat.get('value', '')}</div>", unsafe_allow_html=True)
                with cols[2]:
                    context = stat.get('context', '')
                    visual = stat.get('visual', '')
                    caption_text = f"{context} {visual}".strip()
                    if caption_text:
                        st.caption(caption_text)
            st.markdown('</div>', unsafe_allow_html=True)

        # Primary & Supporting stats
        has_primary = primary_stat and (primary_stat.get('label') or primary_stat.get('value'))
        has_supporting = supporting_stat and (supporting_stat.get('label') or supporting_stat.get('value'))
        if has_primary or has_supporting:
            stats_html = '<div class="section-box">'
            if has_primary:
                stats_html += f"<p><strong>{primary_stat.get('label', '')}:</strong> {primary_stat.get('value', '')}</p>"
            if has_supporting:
                stats_html += f"<p><strong>{supporting_stat.get('label', '')}:</strong> {supporting_stat.get('value', '')}</p>"
            stats_html += '</div>'
            st.markdown(stats_html, unsafe_allow_html=True)
            if has_primary and primary_stat.get('context'):
                st.caption(primary_stat['context'])
            if has_supporting and supporting_stat.get('context'):
                st.caption(supporting_stat['context'])

        # Supporting data
        valid_supporting = [data for data in supporting_data if data.get('label') or data.get('value')] if supporting_data else []
        if valid_supporting:
            data_html = '<div class="section-box">'
            for data in valid_supporting:
                data_html += f"<p><strong>{data.get('label', '')}:</strong> {data.get('value', '')}</p>"
            data_html += '</div>'
            st.markdown(data_html, unsafe_allow_html=True)
            for data in valid_supporting:
                if data.get('context'):
                    st.caption(data['context'])

        # Dashboard metrics (rich format)
        valid_metrics = [m for m in dashboard_metrics if m.get('metric_name') or m.get('current')] if dashboard_metrics else []
        if valid_metrics:
            st.markdown('<div class="section-box">', unsafe_allow_html=True)
            st.markdown("**Health Metrics Dashboard**")
            for metric in valid_metrics:
                cols = st.columns([3, 1, 1, 1, 1])
                with cols[0]:
                    st.markdown(f"**{metric.get('metric_name', '')}**")
                with cols[1]:
                    st.metric("Baseline", metric.get('baseline', ''))
                with cols[2]:
                    st.metric("Current", metric.get('current', ''))
                with cols[3]:
                    change = metric.get('change', '')
                    st.metric("Change", change)
                with cols[4]:
                    percent = metric.get('percent_change', '')
                    trend = metric.get('trend_arrow', '')
                    caption_text = f"{percent} {trend}".strip()
                    if caption_text:
                        st.caption(caption_text)
            st.markdown('</div>', unsafe_allow_html=True)

        # Visual elements note
        if visual_elements and isinstance(visual_elements, dict):
            chart_type = visual_elements.get('chart_type', '')
            data_points = visual_elements.get('data_points', [])
            if chart_type:
                st.markdown(f'<div style="border: 1px solid #ddd; padding: 12px; margin: 12px 0; background: #fafafa;">📊 Chart: {chart_type}</div>', unsafe_allow_html=True)
                valid_points = [dp for dp in data_points if dp.get('label') or dp.get('value')] if data_points else []
                for dp in valid_points:
                    st.caption(f"{dp.get('label', '')}: {dp.get('value', '')}")

        # Accordion items
        if accordion_items:
            for item in accordion_items:
                if item.get('question') or item.get('answer'):
                    with st.expander(item.get('question', '')):
                        st.markdown(item.get('answer', ''))

        # Summary sections
        if summary_sections:
            for section in summary_sections:
                if section.get('title') or section.get('metrics'):
                    st.markdown(f"### {section.get('title', '')}")
                    metrics = section.get('metrics', [])
                    if metrics:
                        for metric in metrics:
                            if metric.get('label') or metric.get('value'):
                                cols = st.columns([2, 1, 1, 1])
                                with cols[0]:
                                    st.markdown(f"**{metric.get('label', '')}**")
                                if 'baseline' in metric and metric['baseline']:
                                    with cols[1]:
                                        st.metric("Baseline", metric['baseline'])
                                with cols[2]:
                                    st.metric("Current", metric.get('value', ''))
                                if 'change' in metric and metric['change']:
                                    with cols[3]:
                                        st.metric("Change", metric['change'])
                                if metric.get('detail'):
                                    st.caption(metric['detail'])

        # Key takeaways
        if key_takeaways and any(takeaway for takeaway in key_takeaways if takeaway):
            st.markdown("**Key Takeaways:**")
            for takeaway in key_takeaways:
                if takeaway:
                    st.markdown(f"- {takeaway}")

        # Stats container
        valid_stats_array = [stat for stat in stats_array if stat.get('value') or stat.get('label')] if stats_array else []
        if valid_stats_array:
            st.markdown('<div class="stats-container">', unsafe_allow_html=True)
            if stats_container and isinstance(stats_container, dict) and stats_container.get('title'):
                st.markdown(f"**{stats_container['title']}**")

            cols = st.columns(len(valid_stats_array))
            for idx, stat in enumerate(valid_stats_array):
                with cols[idx]:
                    st.markdown(f'<div class="stat-item"><div class="stat-value">{stat.get("value", "")}</div><div class="stat-label">{stat.get("label", "")}</div></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        # Interactive element
        if interactive and interactive.get('type'):
            st.info(f"Interactive: {interactive.get('type', '')} " +
                   (f"({len(interactive.get('words', []))} options)" if 'words' in interactive else '') +
                   (f" - Select up to {interactive.get('max_selections', '')}" if 'max_selections' in interactive else ''))

        # CTAs
        if primary_action:
            st.markdown(f'<div class="card-cta">{primary_action}</div>', unsafe_allow_html=True)

        if secondary_action:
            st.markdown(f'<div style="text-align: center; margin-top: 8px; border: 1px solid #999; padding: 8px;">{secondary_action}</div>', unsafe_allow_html=True)

        # Helper text
        if helper_text or context_label:
            caption_text = f"{helper_text} {context_label}".strip()
            if caption_text:
                st.caption(caption_text)

        if source_label:
            st.caption(f"Source: {source_label}")

        # Footer and source citation
        if footer:
            st.caption(footer)

        if source_citation:
            st.caption(f"Source: {source_citation}")

        # Close content box
        st.markdown('</div>', unsafe_allow_html=True)

        # METADATA - COLLAPSIBLE
        with st.expander("📋 METADATA", expanded=False):
            # Build metadata HTML
            metadata_html = '<div style="border: 2px solid #666; padding: 20px; background: #fafafa;">'

            # Card identification
            if card.get('card_id'):
                metadata_html += f"<p><strong>Card ID:</strong> {card['card_id']}</p>"

            # Card type info
            metadata_html += f"<p><strong>Card Type:</strong> {card_type}</p>"
            if card.get('subtype'):
                metadata_html += f"<p><strong>Subtype:</strong> {card['subtype']}</p>"
            if card.get('variant'):
                metadata_html += f"<p><strong>Variant:</strong> {card['variant']}</p>"

            # Personalization
            metadata_html += f"<p><strong>Motivation Variant:</strong> {motivation_class}</p>"
            metadata_html += f"<p><strong>Medical vs Lifestyle:</strong> {category_class.replace('_', ' ')}</p>"
            if complexity:
                metadata_html += f"<p><strong>Persona Complexity:</strong> {complexity}</p>"

            # Milestone
            if card.get('milestone'):
                metadata_html += f"<p><strong>Milestone:</strong> {card['milestone']}</p>"

            # Metadata details
            metadata = card.get('metadata', {})
            if metadata:
                metadata_html += "<hr><p><strong>Detailed Metadata:</strong></p>"

                if metadata.get('rationale'):
                    metadata_html += f"<p><strong>Rationale:</strong> {metadata['rationale']}</p>"

                if metadata.get('scheduler_priority'):
                    metadata_html += f"<p><strong>Scheduler Priority:</strong> {metadata['scheduler_priority']}</p>"

                if metadata.get('mock_engagement'):
                    metadata_html += f"<p><strong>Mock Engagement:</strong> {metadata['mock_engagement']}</p>"

                if metadata.get('curiosity_hook'):
                    metadata_html += f"<p><strong>Curiosity Hook:</strong> {metadata['curiosity_hook']}</p>"

                if metadata.get('data_sources_used'):
                    metadata_html += f"<p><strong>Data Sources Used:</strong> {metadata['data_sources_used']}</p>"

                if metadata.get('dyk_source'):
                    metadata_html += f"<p><strong>DYK Source:</strong> {metadata['dyk_source']}</p>"

                # Show any other metadata fields
                for key, value in metadata.items():
                    if key not in ['rationale', 'scheduler_priority', 'mock_engagement', 'curiosity_hook', 'data_sources_used', 'dyk_source']:
                        metadata_html += f"<p><strong>{key.replace('_', ' ').title()}:</strong> {value}</p>"

            metadata_html += '</div>'
            st.markdown(metadata_html, unsafe_allow_html=True)

        # Close card
        st.markdown('</div>', unsafe_allow_html=True)

# Main content
if uploaded_files:
    # Limit to 10 files
    if len(uploaded_files) > 10:
        st.warning(f"⚠️ You uploaded {len(uploaded_files)} files. Only the first 10 will be processed.")
        uploaded_files = uploaded_files[:10]

    # Create tabs for each file
    if len(uploaded_files) == 1:
        # Single file - no tabs needed
        try:
            data = json.load(uploaded_files[0])
            cards = data.get('generated_cards') or data.get('cards', [])
            user_context = data.get('user_context', {})

            if not cards:
                st.warning("No cards found in the uploaded JSON file.")
            else:
                # Display stats
                st.markdown("---")
                col1, col2, col3, col4 = st.columns(4)

                with col1:
                    st.metric("Total Cards", len(cards))

                with col2:
                    medical_count = sum(1 for c in cards if 'medical' in (c.get('medical_vs_lifestyle', '') or c.get('metadata', {}).get('category', '')).lower())
                    st.metric("Medical", medical_count)

                with col3:
                    lifestyle_count = sum(1 for c in cards if 'lifestyle' in (c.get('medical_vs_lifestyle', '') or c.get('metadata', {}).get('category', '')).lower())
                    st.metric("Lifestyle", lifestyle_count)

                with col4:
                    phase = user_context.get('scheduler_phase', 'Unknown')
                    st.metric("Phase", phase)

                st.markdown("---")

                # Display cards
                for idx, card in enumerate(cards):
                    render_card(card, idx)

        except json.JSONDecodeError:
            st.error("Invalid JSON file. Please upload a valid JSON file.")
        except Exception as e:
            st.error(f"Error loading file: {str(e)}")
    else:
        # Multiple files - use tabs
        tab_names = [f.name.replace('.json', '').replace('-', ' ').title() for f in uploaded_files]
        tabs = st.tabs(tab_names)

        for tab, uploaded_file in zip(tabs, uploaded_files):
            with tab:
                try:
                    # Load JSON
                    data = json.load(uploaded_file)

                    # Extract cards
                    cards = data.get('generated_cards') or data.get('cards', [])
                    user_context = data.get('user_context', {})

                    if not cards:
                        st.warning(f"No cards found in {uploaded_file.name}")
                    else:
                        # Display stats
                        st.markdown("---")
                        col1, col2, col3, col4 = st.columns(4)

                        with col1:
                            st.metric("Total Cards", len(cards))

                        with col2:
                            medical_count = sum(1 for c in cards if 'medical' in (c.get('medical_vs_lifestyle', '') or c.get('metadata', {}).get('category', '')).lower())
                            st.metric("Medical", medical_count)

                        with col3:
                            lifestyle_count = sum(1 for c in cards if 'lifestyle' in (c.get('medical_vs_lifestyle', '') or c.get('metadata', {}).get('category', '')).lower())
                            st.metric("Lifestyle", lifestyle_count)

                        with col4:
                            phase = user_context.get('scheduler_phase', 'Unknown')
                            st.metric("Phase", phase)

                        st.markdown("---")

                        # Display cards
                        for idx, card in enumerate(cards):
                            render_card(card, idx)

                except json.JSONDecodeError:
                    st.error(f"Invalid JSON in {uploaded_file.name}. Please upload a valid JSON file.")
                except Exception as e:
                    st.error(f"Error loading {uploaded_file.name}: {str(e)}")
else:
    st.info("👆 Upload JSON files to view the cards")
    st.markdown("""
    ### Expected JSON Format

    Your JSON file should contain either:
    - `generated_cards` array with card objects
    - `cards` array with card objects
    - Optional: `user_context` object with metadata

    Example structure:
    ```json
    {
      "user_context": {
        "scheduler_phase": "Explore"
      },
      "generated_cards": [
        {
          "card_type": "insight",
          "content": {
            "title": "Card Title",
            "body": "Card body text..."
          },
          "medical_vs_lifestyle": "medical",
          "motivation_variant": "performance"
        }
      ]
    }
    ```
    """)
