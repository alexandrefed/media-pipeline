#!/usr/bin/env python3
"""
Generate Claude Code Skills Technical Guide PDF
Focus on: Progressive Disclosure, Skill Creator double example, Technical Architecture
"""

import os
from datetime import datetime

from reportlab.lib.colors import HexColor, white
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


def create_skills_pdf():
    # Setup
    output_dir = "/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/docs"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "Claude_Code_Skills_Technical_Guide.pdf")

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
    )

    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Heading1"],
        fontSize=24,
        textColor=HexColor("#2C3E50"),
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName="Helvetica-Bold",
    )
    heading1_style = ParagraphStyle(
        "CustomHeading1",
        parent=styles["Heading1"],
        fontSize=18,
        textColor=HexColor("#34495E"),
        spaceAfter=12,
        spaceBefore=12,
        fontName="Helvetica-Bold",
    )
    heading2_style = ParagraphStyle(
        "CustomHeading2",
        parent=styles["Heading2"],
        fontSize=14,
        textColor=HexColor("#2980B9"),
        spaceAfter=10,
        spaceBefore=10,
        fontName="Helvetica-Bold",
    )
    heading3_style = ParagraphStyle(
        "CustomHeading3",
        parent=styles["Heading3"],
        fontSize=12,
        textColor=HexColor("#16A085"),
        spaceAfter=8,
        spaceBefore=8,
        fontName="Helvetica-Bold",
    )
    body_style = ParagraphStyle(
        "CustomBody",
        parent=styles["BodyText"],
        fontSize=10,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        leading=14,
    )
    code_style = ParagraphStyle(
        "Code",
        parent=styles["Code"],
        fontSize=9,
        leftIndent=20,
        rightIndent=20,
        spaceAfter=12,
        spaceBefore=12,
        backColor=HexColor("#F8F9FA"),
        borderColor=HexColor("#DEE2E6"),
        borderWidth=1,
        borderPadding=10,
    )
    callout_style = ParagraphStyle(
        "Callout",
        parent=styles["BodyText"],
        fontSize=10,
        leftIndent=20,
        rightIndent=20,
        spaceAfter=12,
        spaceBefore=12,
        backColor=HexColor("#E8F5E9"),
        borderColor=HexColor("#4CAF50"),
        borderWidth=2,
        borderPadding=10,
    )

    content = []

    # Title Page
    content.append(Spacer(1, 1.5 * inch))
    content.append(Paragraph("Claude Code Skills", title_style))
    content.append(Paragraph("Technical Deep-Dive", title_style))
    content.append(Spacer(1, 0.5 * inch))
    content.append(
        Paragraph(
            "Progressive Disclosure, Automatic Invocation, and Compositional Architecture",
            ParagraphStyle(
                "Subtitle",
                parent=body_style,
                alignment=TA_CENTER,
                fontSize=12,
                textColor=HexColor("#7F8C8D"),
            ),
        )
    )
    content.append(Spacer(1, 1 * inch))
    content.append(
        Paragraph(
            f"Generated: {datetime.now().strftime('%Y-%m-%d')}<br/>Sources: Sean Kochel & IndyDevDan",
            ParagraphStyle(
                "Meta",
                parent=body_style,
                alignment=TA_CENTER,
                fontSize=9,
                textColor=HexColor("#95A5A6"),
            ),
        )
    )
    content.append(PageBreak())

    # Executive Summary
    content.append(Paragraph("Executive Summary", heading1_style))
    content.append(
        Paragraph(
            "Claude Code Skills are agent-invoked, context-efficient features for packaging custom expertise into reusable solutions. They represent the highest-level compositional unit in Claude Code architecture, rated 8/10 for their ability to standardize workflow patterns through progressive disclosure and automatic invocation.",
            body_style,
        )
    )
    content.append(Spacer(1, 0.2 * inch))

    summary_data = [
        ["Feature", "Skills", "MCPs", "Sub-agents", "Slash Commands"],
        ["Agent-Invoked", "✓ YES", "✗ NO", "✓ YES", "✗ NO (Manual)"],
        ["Context Efficient", "✓ Progressive", "✗ Explodes", "✓ Isolated", "✓ Direct"],
        ["Context Persistence", "✓ Main", "✓ Main", "✗ Lost", "✓ Main"],
        ["Modularity", "HIGH", "Medium", "Medium", "Low"],
        ["Composition", "✓ All below", "✗ No skills", "✓ Commands", "✓ Skills"],
    ]

    summary_table = Table(
        summary_data, colWidths=[1.5 * inch, 1 * inch, 1 * inch, 1 * inch, 1.3 * inch]
    )
    summary_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), HexColor("#34495E")),
                ("TEXTCOLOR", (0, 0), (-1, 0), white),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 9),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), HexColor("#ECF0F1")),
                ("GRID", (0, 0), (-1, -1), 1, HexColor("#BDC3C7")),
                ("FONTSIZE", (0, 1), (-1, -1), 8),
                ("TOPPADDING", (0, 1), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
            ]
        )
    )
    content.append(summary_table)
    content.append(Spacer(1, 0.3 * inch))

    content.append(
        Paragraph(
            '<b>Core Quote (Sean Kochel):</b> "Skills are arguably a bigger deal than MCPs because they encode systematic methodologies, not just tool access—they teach Claude to work like experienced professionals."',
            callout_style,
        )
    )
    content.append(PageBreak())

    # Progressive Disclosure (DETAILED SECTION)
    content.append(
        Paragraph(
            "1. Progressive Disclosure: How Skills Load Context Incrementally", heading1_style
        )
    )
    content.append(
        Paragraph(
            "Progressive disclosure is the killer feature that makes skills context-efficient. Unlike MCP servers which 'explode your context window on bootup,' skills load resources incrementally only when needed.",
            body_style,
        )
    )

    content.append(Paragraph("The Three-Level Loading Mechanism", heading2_style))
    content.append(
        Paragraph("Skills use a lazy-loading architecture with three distinct levels:", body_style)
    )

    # Three levels table
    levels_data = [
        ["Level", "What Loads", "When", "Token Cost", "Purpose"],
        [
            "1. Metadata",
            "skill.json<br/>- Name<br/>- Description<br/>- Keywords",
            "Always<br/>(on startup)",
            "~50 tokens",
            "Agent decides<br/>if relevant",
        ],
        [
            "2. Instructions",
            "skill.md<br/>- How to use<br/>- When to use<br/>- Examples",
            "If agent<br/>detects match",
            "~500 tokens",
            "Agent reads<br/>workflow",
        ],
        [
            "3. Resources",
            "resources/<br/>- Files<br/>- Templates<br/>- Docs",
            "If executing<br/>skill",
            "Variable<br/>(1K-10K)",
            "Agent pulls<br/>what's needed",
        ],
    ]

    levels_table = Table(
        levels_data, colWidths=[1 * inch, 1.8 * inch, 1 * inch, 1 * inch, 1.3 * inch]
    )
    levels_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), HexColor("#8E44AD")),
                ("TEXTCOLOR", (0, 0), (-1, 0), white),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 9),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), HexColor("#EBDEF0")),
                ("GRID", (0, 0), (-1, -1), 1, HexColor("#C39BD3")),
                ("FONTSIZE", (0, 1), (-1, -1), 8),
                ("TOPPADDING", (0, 1), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
            ]
        )
    )
    content.append(levels_table)
    content.append(Spacer(1, 0.3 * inch))

    content.append(Paragraph("Level 1: Metadata Discovery", heading3_style))
    content.append(
        Paragraph(
            "On Claude Code startup, all skill metadata loads into the agent's awareness. This is lightweight (~50 tokens per skill) and tells the agent WHAT skills exist and WHEN to consider using them.",
            body_style,
        )
    )
    content.append(
        Paragraph(
            '<font name=\'Courier\' size=8>{<br/>  "name": "UI Guidelines Skill",<br/>  "description": "Ensures brand consistency for React components",<br/>  "keywords": ["component", "UI", "brand", "design system"],<br/>  "triggers": ["building component", "creating UI", "design consistency"]<br/>}</font>',
            code_style,
        )
    )

    content.append(Paragraph("Level 2: Instructions Loading", heading3_style))
    content.append(
        Paragraph(
            "When the agent detects a task matching skill keywords (e.g., user says 'create a button component'), it loads skill.md (~500 tokens). This provides the HOW—the systematic workflow the agent should follow.",
            body_style,
        )
    )
    content.append(
        Paragraph(
            "<font name='Courier' size=8># UI Guidelines Skill<br/><br/>## When to Use<br/>Automatically invoke when building React components.<br/><br/>## Workflow<br/>1. Check design system for existing patterns<br/>2. Load brand colors from resources/colors.json<br/>3. Apply typography from resources/typography.json<br/>4. Validate against component checklist<br/><br/>## Resources<br/>- resources/design-system.pdf<br/>- resources/brand-colors.json<br/>- resources/component-checklist.md</font>",
            code_style,
        )
    )

    content.append(Paragraph("Level 3: Resource Pulling", heading3_style))
    content.append(
        Paragraph(
            "Only if executing the skill does the agent pull actual resource files (1K-10K tokens). These might be design docs, code templates, configuration files—whatever the skill needs to complete its work.",
            body_style,
        )
    )

    content.append(
        Paragraph(
            "<b>Critical Comparison:</b> MCP servers load ALL tools and schemas on startup (explosion). Skills load metadata → instructions → resources progressively (precision).",
            callout_style,
        )
    )
    content.append(PageBreak())

    # The rest of the content continues with Skill Creator double example, composition hierarchy, etc.
    # Due to space constraints, I'll add the most critical sections

    # Skill Creator Double Example
    content.append(Paragraph("2. Skill Creator: The Meta-Skill (Double Example)", heading1_style))
    content.append(
        Paragraph(
            "Skill Creator demonstrates skills in two ways: (1) HOW it works as a skill itself, and (2) HOW it creates other skills. This 'meta-skill' pattern shows the full power of skills architecture.",
            body_style,
        )
    )

    content.append(Paragraph("Example A: Skill Creator AS a Skill", heading2_style))
    content.append(
        Paragraph("Skill Creator is itself a skill with progressive disclosure:", body_style)
    )
    content.append(
        Paragraph(
            "<font name='Courier' size=8>User: \"Create a skill for enforcing UI guidelines\"<br/><br/>→ Agent sees 'create a skill' in metadata keywords<br/>→ Agent loads Skill Creator instructions<br/>→ Agent asks targeted questions:<br/>   - What component types? (buttons, forms, modals)<br/>   - Where are guidelines? (.claude/system/design-system.md)<br/>   - When to invoke? (when building React components)<br/>   - What resources needed? (colors.json, typography.json)<br/>→ Agent generates skill.json + skill.md + resources/<br/>→ Agent packages as zip file<br/>→ User downloads and installs to .claude/skills/</font>",
            code_style,
        )
    )

    content.append(Paragraph("Example B: What Skill Creator CREATES", heading2_style))
    content.append(
        Paragraph("The UI Guidelines skill created by Skill Creator becomes:", body_style)
    )
    content.append(
        Paragraph(
            '<font name=\'Courier\' size=8>.claude/skills/ui-guidelines/<br/>├── skill.json (metadata - 50 tokens)<br/>│   {<br/>│     "name": "UI Guidelines",<br/>│     "keywords": ["component", "button", "form", "UI"],<br/>│     "triggers": ["create component", "build UI"]<br/>│   }<br/>├── skill.md (instructions - 500 tokens)<br/>│   # Apply brand standards to components<br/>│   ## Workflow<br/>│   1. Load colors from resources/colors.json<br/>│   2. Apply typography from resources/typography.json<br/>│   3. Validate component against checklist<br/>├── resources/<br/>│   ├── colors.json (200 tokens)<br/>│   ├── typography.json (150 tokens)<br/>│   └── checklist.md (300 tokens)</font>',
            code_style,
        )
    )

    content.append(
        Paragraph(
            "<b>The Meta Pattern:</b> Skill Creator is a skill that creates skills. This is 'build the thing that builds the thing'—a core agentic abstraction pattern.",
            callout_style,
        )
    )
    content.append(PageBreak())

    # Composition Hierarchy
    content.append(Paragraph("3. Composition Hierarchy: Skills at the Top", heading1_style))
    content.append(
        Paragraph(
            "Skills represent the highest compositional level in Claude Code architecture. Understanding this hierarchy is critical for knowing when to use which feature.",
            body_style,
        )
    )

    hier_data = [
        ["Level", "Feature", "Composes", "Invoked By"],
        ["TOP", "Skills", "MCPs + Sub-agents + Commands", "Agent (automatic)"],
        ["MIDDLE", "MCP Servers", "External APIs", "Agent + Skills"],
        ["MIDDLE", "Sub-agents", "Commands", "Agent + Skills"],
        ["MIDDLE", "Slash Commands", "Skills (recursive)", "User (manual)"],
        ["BOTTOM", "Prompts", "N/A (primitive)", "Everything"],
    ]

    hier_table = Table(hier_data, colWidths=[1 * inch, 1.5 * inch, 2 * inch, 1.8 * inch])
    hier_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), HexColor("#E74C3C")),
                ("TEXTCOLOR", (0, 0), (-1, 0), white),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 9),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (0, 1), HexColor("#FADBD8")),
                ("BACKGROUND", (0, 2), (0, 4), HexColor("#FEF5E7")),
                ("BACKGROUND", (0, 5), (0, 5), HexColor("#D5F4E6")),
                ("GRID", (0, 0), (-1, -1), 1, HexColor("#E67E73")),
                ("FONTSIZE", (0, 1), (-1, -1), 8),
                ("TOPPADDING", (0, 1), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    content.append(hier_table)
    content.append(Spacer(1, 0.3 * inch))

    content.append(
        Paragraph(
            '<b>Key Rule (IndyDevDan):</b> "Custom Slash Commands are the primitive of agentic coding. Master prompts before mastering compositional features. Everything is a prompt in the end (tokens in, tokens out)."',
            callout_style,
        )
    )
    content.append(PageBreak())

    # Conclusion
    content.append(Paragraph("4. When to Use Skills vs Alternatives", heading1_style))
    content.append(Paragraph("The Decision Framework", heading2_style))

    decision_points = [
        "<b>One-off task?</b> → Use Slash Command (don't over-engineer)",
        "<b>Managing problem DOMAIN?</b> → Use Skill (create, remove, list, merge operations)",
        "<b>External integration?</b> → Use MCP Server (Jira, databases, APIs)",
        "<b>Parallel isolated work?</b> → Use Sub-agent (context protection)",
        "<b>Automatic behavior?</b> → Use Skill (agent-invoked)",
        "<b>Manual trigger?</b> → Use Slash Command (user control)",
    ]

    content.append(
        ListFlowable(
            [ListItem(Paragraph(point, body_style), leftIndent=20) for point in decision_points],
            bulletType="bullet",
            start="circle",
        )
    )

    content.append(Paragraph("Final Rating & Verdict", heading2_style))
    content.append(Paragraph("Skills: <b>8/10</b> (IndyDevDan rating)", body_style))
    content.append(
        Paragraph(
            "Pros: Agent-invoked, context-efficient progressive disclosure, dedicated file system structure, composes all features below, higher compositional abstraction",
            body_style,
        )
    )
    content.append(
        Paragraph(
            "Cons: Doesn't go all the way (can't nest sub-agents, can't nest prompts in /commands directory within skill), reliability concerns when chaining multiple skills",
            body_style,
        )
    )
    content.append(
        Paragraph(
            "<b>Bottom Line:</b> Skills are canonized prompt engineering + modularity. Not revolutionary in capability, but valuable for standardization and shareability. Use for repeatable agent-invoked domain management, not one-off tasks.",
            callout_style,
        )
    )

    # Build PDF
    doc.build(content)
    print(f"✓ Skills Technical Guide PDF generated: {output_path}")
    return output_path


if __name__ == "__main__":
    create_skills_pdf()
