#!/usr/bin/env python3
"""
Generate Scout-Plan-Build Workflow Guide PDF
Comprehensive documentation of the three-phase development workflow
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


def create_scout_plan_build_pdf():
    """Create comprehensive Scout-Plan-Build workflow PDF"""

    # Output path
    output_dir = "/Users/alex/Desktop/ClaudeMCP/AI-Knowledge-Base-PRD/docs"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "Scout-Plan-Build_Workflow_Guide.pdf")

    # Create PDF
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

    # Custom styles
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

    ParagraphStyle(
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

    # Build content
    content = []

    # Title Page
    content.append(Spacer(1, 1.5 * inch))
    content.append(Paragraph("Scout-Plan-Build", title_style))
    content.append(Paragraph("Workflow Guide", title_style))
    content.append(Spacer(1, 0.5 * inch))
    content.append(
        Paragraph(
            "Context-Efficient Three-Phase Development Workflow<br/>Using Sub-Agents and Strategic Delegation",
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
            f"Generated: {datetime.now().strftime('%Y-%m-%d')}<br/>Source: IndyDevDan Tactical Agentic Coding",
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
            "The Scout-Plan-Build workflow is a three-phase development pattern that dramatically reduces context "
            "consumption and accelerates development through strategic delegation to specialized sub-agents.",
            body_style,
        )
    )
    content.append(Spacer(1, 0.2 * inch))

    summary_data = [
        ["Metric", "Traditional Approach", "Scout-Plan-Build", "Improvement"],
        ["Context Usage", "50-90%", "15-25%", "70% savings"],
        ["Development Time", "120 minutes", "95 minutes", "21% faster"],
        ["Cost per Task", "$2.00", "$1.00", "50% cheaper"],
        ["File Discovery", "Manual search", "Parallel agents", "4x faster"],
    ]

    summary_table = Table(summary_data, colWidths=[2 * inch, 1.5 * inch, 1.5 * inch, 1.3 * inch])
    summary_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), HexColor("#34495E")),
                ("TEXTCOLOR", (0, 0), (-1, 0), white),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 10),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), HexColor("#ECF0F1")),
                ("GRID", (0, 0), (-1, -1), 1, HexColor("#BDC3C7")),
                ("FONTSIZE", (0, 1), (-1, -1), 9),
                ("TOPPADDING", (0, 1), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
            ]
        )
    )
    content.append(summary_table)
    content.append(Spacer(1, 0.3 * inch))

    content.append(
        Paragraph(
            "<b>Key Insight:</b> The R&D Framework (Reduce and Delegate) - Delegate file search and discovery to cheap "
            "sub-agents, preserving your primary agent's context for planning and execution.",
            callout_style,
        )
    )
    content.append(PageBreak())

    # Architecture Overview
    content.append(Paragraph("1. Architecture Overview", heading1_style))
    content.append(
        Paragraph(
            "Scout-Plan-Build is a three-phase workflow that separates concerns and optimizes model usage at each stage:",
            body_style,
        )
    )
    content.append(Spacer(1, 0.2 * inch))

    # Phase descriptions
    phases = [
        ("SCOUT", "4 parallel sub-agents search codebase", "Cheap models (free/fast)", "5 minutes"),
        (
            "PLAN",
            "Primary agent designs implementation",
            "Expensive model (reasoning)",
            "30 minutes",
        ),
        ("BUILD", "Primary agent executes changes", "Expensive model (code quality)", "60 minutes"),
    ]

    phase_data = [["Phase", "Description", "Model Selection", "Duration"]] + list(phases)
    phase_table = Table(phase_data, colWidths=[1.2 * inch, 2.5 * inch, 1.8 * inch, 1 * inch])
    phase_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), HexColor("#2980B9")),
                ("TEXTCOLOR", (0, 0), (-1, 0), white),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 10),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), HexColor("#EBF5FB")),
                ("GRID", (0, 0), (-1, -1), 1, HexColor("#AED6F1")),
                ("FONTSIZE", (0, 1), (-1, -1), 9),
                ("TOPPADDING", (0, 1), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    content.append(phase_table)
    content.append(Spacer(1, 0.3 * inch))

    content.append(Paragraph("Core Philosophy", heading2_style))
    content.append(
        Paragraph('The workflow follows the "R&D Framework" principle from IndyDevDan:', body_style)
    )

    philosophy_items = [
        "<b>Reduce</b>: Minimize context consumption in primary agent",
        "<b>Delegate</b>: Offload discovery to specialized cheap sub-agents",
        "<b>Preserve</b>: Save expensive model capacity for high-value work (planning, building)",
        "<b>Parallelize</b>: Run multiple sub-agents simultaneously for 4x speed",
    ]

    content.append(
        ListFlowable(
            [ListItem(Paragraph(item, body_style), leftIndent=20) for item in philosophy_items],
            bulletType="bullet",
            start="circle",
        )
    )
    content.append(PageBreak())

    # Scout Phase Deep-Dive
    content.append(Paragraph("2. Scout Phase: Discovery with Sub-Agents", heading1_style))
    content.append(Paragraph("Purpose", heading2_style))
    content.append(
        Paragraph(
            "The Scout phase delegates codebase discovery to 4 parallel sub-agents using cheap/free models. "
            "This preserves the primary agent's context window (saving 80% of context that would be consumed by manual search).",
            body_style,
        )
    )

    content.append(Paragraph("Sub-Agent Architecture", heading2_style))
    scout_agents = [
        ["Sub-Agent", "Model", "Cost", "Search Target", "Output"],
        ["Scout 1", "Gemini Flash", "Free", "Frontend components", "relevant_files.md"],
        ["Scout 2", "Gemini Light", "Free", "Backend API routes", "relevant_files.md"],
        ["Scout 3", "Codex", "$0.01/1K", "Database schemas", "relevant_files.md"],
        ["Scout 4", "Claude Haiku", "$0.25/1M", "Business logic", "relevant_files.md"],
    ]

    scout_table = Table(
        scout_agents, colWidths=[1 * inch, 1.2 * inch, 0.9 * inch, 1.8 * inch, 1.3 * inch]
    )
    scout_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), HexColor("#16A085")),
                ("TEXTCOLOR", (0, 0), (-1, 0), white),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 9),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), HexColor("#D5F4E6")),
                ("GRID", (0, 0), (-1, -1), 1, HexColor("#7DCEA0")),
                ("FONTSIZE", (0, 1), (-1, -1), 8),
                ("TOPPADDING", (0, 1), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
            ]
        )
    )
    content.append(scout_table)
    content.append(Spacer(1, 0.2 * inch))

    content.append(Paragraph("Implementation", heading2_style))
    content.append(
        Paragraph(
            "<font name='Courier' size=9><b>/scout command implementation:</b></font>", body_style
        )
    )
    content.append(
        Paragraph(
            "<font name='Courier' size=8>"
            "# Launch 4 parallel sub-agents<br/>"
            "# Each searches different codebase section<br/>"
            "# Output: workspace/scout_results.md with file paths and line numbers<br/>"
            "<br/>"
            "Sub-Agent 1 → Search apps/mobile/ for React Native components<br/>"
            "Sub-Agent 2 → Search apps/api/ for tRPC procedures<br/>"
            "Sub-Agent 3 → Search packages/database/ for schemas<br/>"
            "Sub-Agent 4 → Search packages/training-engine/ for business logic<br/>"
            "<br/>"
            "# Consolidate results into single reference document<br/>"
            "# Primary agent reads summary (not entire codebase)<br/>"
            "# Result: 80% context window saved"
            "</font>",
            code_style,
        )
    )

    content.append(Paragraph("Output Format", heading2_style))
    content.append(
        Paragraph(
            "Each sub-agent outputs structured findings to <b>relevant_files.md</b>:", body_style
        )
    )
    content.append(
        Paragraph(
            "<font name='Courier' size=8>"
            "## Frontend Components (Scout 1)<br/>"
            "- apps/mobile/src/screens/WorkoutScreen.tsx:45-120<br/>"
            "  → Voice command handling implementation<br/>"
            "- apps/mobile/src/components/VoiceButton.tsx:12-85<br/>"
            "  → Speech recognition UI component<br/>"
            "<br/>"
            "## Backend API (Scout 2)<br/>"
            "- apps/api/src/routers/workout.ts:78-145<br/>"
            "  → Workout logging tRPC procedures<br/>"
            "<br/>"
            "## Database Schemas (Scout 3)<br/>"
            "- packages/database/neo4j/schemas/exercises.cypher:1-50<br/>"
            "  → Exercise node structure and relationships"
            "</font>",
            code_style,
        )
    )

    content.append(
        Paragraph(
            "<b>Critical Advantage:</b> Primary agent reads 500-line summary instead of searching 50,000+ lines of code. "
            "Context preserved for actual work.",
            callout_style,
        )
    )
    content.append(PageBreak())

    # Plan Phase Deep-Dive
    content.append(Paragraph("3. Plan Phase: Strategic Design", heading1_style))
    content.append(Paragraph("Purpose", heading2_style))
    content.append(
        Paragraph(
            "The Plan phase uses the primary agent (expensive model with strong reasoning) to design the implementation "
            "based on scout findings. This is where Claude 4.5 Sonnet's reasoning capabilities are essential.",
            body_style,
        )
    )

    content.append(Paragraph("Primary Agent Workflow", heading2_style))
    plan_steps = [
        "<b>Read Scout Results</b>: Load relevant_files.md summary (500 lines vs 50K)",
        "<b>Scrape Documentation</b>: Pull necessary API docs, patterns, examples locally",
        "<b>Design Architecture</b>: Create implementation plan with file structure",
        "<b>Generate Specifications</b>: Detailed requirements for build phase",
        "<b>Save to AI_docs/</b>: Persist plan for reuse and reference",
    ]

    content.append(
        ListFlowable(
            [ListItem(Paragraph(step, body_style), leftIndent=20) for step in plan_steps],
            bulletType="1",
            start="1",
        )
    )

    content.append(Paragraph("Planning Mode Best Practices", heading2_style))
    content.append(
        Paragraph("Always use Planning Mode (Shift+Tab) during this phase to:", body_style)
    )

    planning_benefits = [
        "Review plans before execution (prevent manifestation hell)",
        "Catch architectural issues early (2 minutes vs 30 minutes of wasted work)",
        "Adjust approach based on constraints discovered",
        "Save tokens by not building wrong thing",
    ]

    content.append(
        ListFlowable(
            [
                ListItem(Paragraph(benefit, body_style), leftIndent=20)
                for benefit in planning_benefits
            ],
            bulletType="bullet",
            start="circle",
        )
    )

    content.append(Paragraph("Example Plan Output", heading2_style))
    content.append(
        Paragraph(
            "<font name='Courier' size=8>"
            "# Voice Workout Feature Implementation Plan<br/>"
            "<br/>"
            "## Architecture<br/>"
            "1. Frontend: VoiceWorkoutScreen.tsx<br/>"
            "   - React Native Voice integration<br/>"
            "   - Real-time transcription display<br/>"
            "   - Error handling for speech recognition<br/>"
            "<br/>"
            "2. Backend: workout.router.ts<br/>"
            "   - tRPC procedure: logWorkoutViaVoice<br/>"
            "   - Input validation with Zod<br/>"
            "   - Neo4j integration for exercise lookup<br/>"
            "<br/>"
            "3. State Management<br/>"
            "   - React Query for server state<br/>"
            "   - Zustand for voice recognition state<br/>"
            "<br/>"
            "## Dependencies<br/>"
            "- react-native-voice: ^3.2.4<br/>"
            "- @trpc/server: ^11.0.0<br/>"
            "- zod: ^3.22.4<br/>"
            "<br/>"
            "## Testing Strategy<br/>"
            "- Unit tests: Voice parsing logic<br/>"
            "- Integration tests: tRPC procedures<br/>"
            "- E2E tests: Full voice workflow with Detox"
            "</font>",
            code_style,
        )
    )

    content.append(
        Paragraph(
            "<b>Time Investment:</b> 30 minutes for comprehensive plan saves 2-3 hours of rework from poor architecture.",
            callout_style,
        )
    )
    content.append(PageBreak())

    # Build Phase Deep-Dive
    content.append(Paragraph("4. Build Phase: Execution", heading1_style))
    content.append(Paragraph("Purpose", heading2_style))
    content.append(
        Paragraph(
            "The Build phase executes the plan created in phase 2, using the primary agent's code generation "
            "capabilities while maintaining quality and consistency.",
            body_style,
        )
    )

    content.append(Paragraph("Execution Strategy", heading2_style))
    build_steps = [
        "<b>Load Plan</b>: Reference AI_docs/ specifications",
        "<b>Implement by Module</b>: Break into logical chunks (frontend → backend → tests)",
        "<b>Validate Incrementally</b>: Test each module before moving to next",
        "<b>Use Git Worktrees</b>: Isolate development from main branch",
        "<b>Document as You Go</b>: Update README, inline comments, API docs",
    ]

    content.append(
        ListFlowable(
            [ListItem(Paragraph(step, body_style), leftIndent=20) for step in build_steps],
            bulletType="1",
            start="1",
        )
    )

    content.append(Paragraph("Quality Checks", heading2_style))
    quality_checklist = [
        "TypeScript compilation passes (no any types)",
        "Tests written and passing (>80% coverage target)",
        "Linting passes (ESLint + Prettier)",
        "Performance acceptable (60fps animations, <200ms API responses)",
        "Error handling implemented (user-friendly messages)",
        "Documentation complete (JSDoc for public APIs)",
    ]

    content.append(
        ListFlowable(
            [ListItem(Paragraph(check, body_style), leftIndent=20) for check in quality_checklist],
            bulletType="bullet",
            start="square",
        )
    )

    content.append(Paragraph("Git Worktrees Integration", heading2_style))
    content.append(
        Paragraph(
            "The Build phase benefits from git worktrees for parallel isolated development:",
            body_style,
        )
    )
    content.append(
        Paragraph(
            "<font name='Courier' size=8>"
            "# Create isolated worktree for feature<br/>"
            "git worktree add ../voice-feature feature/voice-workout<br/>"
            "<br/>"
            "# Develop in isolation<br/>"
            "cd ../voice-feature<br/>"
            "# Build, test, verify<br/>"
            "<br/>"
            "# Merge when ready<br/>"
            "git checkout main<br/>"
            "git merge feature/voice-workout<br/>"
            "<br/>"
            "# Clean up<br/>"
            "git worktree remove ../voice-feature"
            "</font>",
            code_style,
        )
    )

    content.append(
        Paragraph(
            "<b>Benefit:</b> Main branch stays clean while feature is developed. No conflicts, no interruptions.",
            callout_style,
        )
    )
    content.append(PageBreak())

    # R&D Framework
    content.append(Paragraph("5. R&D Framework: Reduce and Delegate", heading1_style))
    content.append(
        Paragraph(
            "The R&D Framework is the philosophical foundation of Scout-Plan-Build, addressing the core problem: "
            "context window consumption kills development velocity.",
            body_style,
        )
    )

    content.append(Paragraph("The Problem: Context Window Crisis", heading2_style))
    context_problems = [
        "System prompts consume 5-10% of context window",
        "MCP tools (even unused) consume ~2% per tool",
        "Conversation history consumes 50-90% on complex tasks",
        "<b>Autocompact buffer consumes 22% (critical to disable!)</b>",
        "File search operations consume massive context",
    ]

    content.append(
        ListFlowable(
            [
                ListItem(Paragraph(problem, body_style), leftIndent=20)
                for problem in context_problems
            ],
            bulletType="bullet",
            start="square",
        )
    )

    content.append(Paragraph("The Solution: Strategic Delegation", heading2_style))
    content.append(
        Paragraph("Instead of having the primary expensive agent search codebases:", body_style)
    )

    solution_comparison = [
        ["Approach", "Context Consumed", "Cost", "Time", "Quality"],
        ["Traditional<br/>(Primary agent searches)", "50-90%", "$2.00", "120 min", "Variable"],
        ["R&D Framework<br/>(Sub-agents search)", "15-25%", "$1.00", "95 min", "Consistent"],
    ]

    solution_table = Table(
        solution_comparison, colWidths=[2 * inch, 1.5 * inch, 1 * inch, 1 * inch, 1 * inch]
    )
    solution_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), HexColor("#E74C3C")),
                ("TEXTCOLOR", (0, 0), (-1, 0), white),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 9),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (0, 1), HexColor("#FADBD8")),
                ("BACKGROUND", (0, 2), (0, 2), HexColor("#D5F4E6")),
                ("GRID", (0, 0), (-1, -1), 1, HexColor("#E67E73")),
                ("FONTSIZE", (0, 1), (-1, -1), 9),
                ("TOPPADDING", (0, 1), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    content.append(solution_table)
    content.append(Spacer(1, 0.2 * inch))

    content.append(Paragraph("Critical Configuration", heading2_style))
    content.append(
        Paragraph("<b>ALWAYS Disable Autocompact</b> (IndyDevDan - Critical Insight):", body_style)
    )
    content.append(
        Paragraph(
            "<font name='Courier' size=10><b>/config autocompact false</b></font>", code_style
        )
    )
    content.append(
        Paragraph(
            "This saves 22% of context window (44K tokens on Claude 4.5 Sonnet's 200K limit). "
            "Autocompact compresses conversation history automatically, but consumes precious context doing so. "
            "For Scout-Plan-Build workflows where every token counts, disable it.",
            callout_style,
        )
    )
    content.append(PageBreak())

    # Practical Example
    content.append(Paragraph("6. Real-World Example: Voice Workout Feature", heading1_style))
    content.append(
        Paragraph(
            "This example demonstrates the Scout-Plan-Build workflow for implementing a voice-driven workout logging feature.",
            body_style,
        )
    )

    content.append(Paragraph("User Story", heading2_style))
    content.append(
        Paragraph(
            "As a hybrid athlete, I want to log workout data using voice commands during training so I don't need to "
            "interrupt my session to type on my phone.",
            body_style,
        )
    )

    content.append(Paragraph("Phase 1: Scout (5 minutes)", heading2_style))
    content.append(
        Paragraph("Launch 4 parallel sub-agents to discover relevant files:", body_style)
    )
    content.append(
        Paragraph(
            "<font name='Courier' size=8>"
            "Sub-Agent 1 (Gemini Flash - Free):<br/>"
            "  → apps/mobile/src/screens/WorkoutScreen.tsx<br/>"
            "  → apps/mobile/src/components/VoiceButton.tsx<br/>"
            "  → apps/mobile/src/hooks/useVoiceRecognition.ts<br/>"
            "<br/>"
            "Sub-Agent 2 (Gemini Light - Free):<br/>"
            "  → apps/api/src/routers/workout.ts<br/>"
            "  → apps/api/src/services/workoutService.ts<br/>"
            "  → apps/api/src/middleware/auth.ts<br/>"
            "<br/>"
            "Sub-Agent 3 (Codex - $0.01):<br/>"
            "  → packages/database/neo4j/exercises.cypher<br/>"
            "  → packages/database/neo4j/workouts.cypher<br/>"
            "<br/>"
            "Sub-Agent 4 (Haiku - $0.05):<br/>"
            "  → packages/training-engine/src/logWorkout.ts<br/>"
            "  → packages/training-engine/src/parseVoiceInput.ts<br/>"
            "<br/>"
            "<b>Output:</b> workspace/scout_results.md (550 lines)<br/>"
            "<b>Cost:</b> $0.06 total<br/>"
            "<b>Time:</b> 5 minutes (parallel execution)"
            "</font>",
            code_style,
        )
    )

    content.append(Paragraph("Phase 2: Plan (30 minutes)", heading2_style))
    content.append(
        Paragraph(
            "Primary agent (Claude 4.5 Sonnet) reads scout results and creates implementation plan:",
            body_style,
        )
    )
    content.append(
        Paragraph(
            "<font name='Courier' size=8>"
            "<b>Planning Mode Enabled (Shift+Tab)</b><br/>"
            "<br/>"
            "1. Architecture Review<br/>"
            "   ✓ Existing voice hooks can be reused<br/>"
            "   ✓ Need new tRPC procedure for voice input<br/>"
            "   ✓ Neo4j exercise lookup already exists<br/>"
            "<br/>"
            "2. Implementation Plan<br/>"
            "   → Frontend: Extend VoiceButton component<br/>"
            "   → Backend: New logWorkoutViaVoice procedure<br/>"
            "   → Parsing: Create parseVoiceWorkoutInput function<br/>"
            "   → State: Add voice recording state to Zustand<br/>"
            "<br/>"
            "3. Dependencies (none new required)<br/>"
            "   ✓ react-native-voice already installed<br/>"
            "   ✓ tRPC router already configured<br/>"
            "<br/>"
            "4. Testing Strategy<br/>"
            "   → Unit: Voice parsing logic<br/>"
            "   → Integration: tRPC procedure<br/>"
            "   → E2E: Full voice workflow<br/>"
            "<br/>"
            "<b>Plan saved to:</b> AI_docs/voice-workout-feature.md<br/>"
            "<b>Cost:</b> $0.40<br/>"
            "<b>Time:</b> 30 minutes"
            "</font>",
            code_style,
        )
    )

    content.append(Paragraph("Phase 3: Build (60 minutes)", heading2_style))
    content.append(Paragraph("Primary agent executes the plan:", body_style))
    content.append(
        Paragraph(
            "<font name='Courier' size=8>"
            "1. Create git worktree for isolation<br/>"
            "   git worktree add ../voice-feature feature/voice-workout<br/>"
            "<br/>"
            "2. Implement frontend (20 minutes)<br/>"
            "   ✓ VoiceButton.tsx - Add workout mode<br/>"
            "   ✓ WorkoutScreen.tsx - Integrate voice button<br/>"
            "   ✓ useVoiceRecognition.ts - Add workout parsing<br/>"
            "<br/>"
            "3. Implement backend (20 minutes)<br/>"
            "   ✓ workout.router.ts - New tRPC procedure<br/>"
            "   ✓ workoutService.ts - Voice logging logic<br/>"
            "   ✓ parseVoiceInput.ts - Natural language parsing<br/>"
            "<br/>"
            "4. Write tests (15 minutes)<br/>"
            "   ✓ parseVoiceInput.test.ts - 8 test cases<br/>"
            "   ✓ workout.test.ts - Integration tests<br/>"
            "   ✓ WorkoutScreen.test.tsx - Component tests<br/>"
            "<br/>"
            "5. Validation (5 minutes)<br/>"
            "   ✓ TypeScript compilation passes<br/>"
            "   ✓ All tests passing (100% coverage)<br/>"
            "   ✓ Linting passes<br/>"
            "   ✓ Manual testing on iOS/Android<br/>"
            "<br/>"
            "<b>Cost:</b> $0.54<br/>"
            "<b>Time:</b> 60 minutes<br/>"
            "<br/>"
            "<b>TOTAL COST:</b> $1.00<br/>"
            "<b>TOTAL TIME:</b> 95 minutes<br/>"
            "<br/>"
            "<b>vs Traditional (single agent):</b> $2.00, 120 minutes"
            "</font>",
            code_style,
        )
    )

    content.append(
        Paragraph(
            "<b>Result:</b> 50% cost savings, 21% time savings, better code quality through structured workflow.",
            callout_style,
        )
    )
    content.append(PageBreak())

    # Best Practices
    content.append(Paragraph("7. Best Practices and Patterns", heading1_style))

    content.append(Paragraph("Model Selection Strategy", heading2_style))
    model_selection = [
        ["Phase", "Task", "Recommended Model", "Rationale"],
        ["Scout", "File discovery", "Gemini Flash/Light", "Free, fast, good at search"],
        ["Scout", "Code analysis", "Codex", "Cheap, understands code structure"],
        ["Scout", "Complex patterns", "Claude Haiku", "Better reasoning than Gemini"],
        ["Plan", "Architecture design", "Claude 4.5 Sonnet", "Best reasoning capabilities"],
        ["Build", "Code generation", "Claude 4.5 Sonnet", "Highest quality output"],
        ["Build", "Simple edits", "Switch to Cursor", "Save expensive tokens"],
    ]

    model_table = Table(model_selection, colWidths=[1 * inch, 1.5 * inch, 1.7 * inch, 2.3 * inch])
    model_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), HexColor("#8E44AD")),
                ("TEXTCOLOR", (0, 0), (-1, 0), white),
                ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 9),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), HexColor("#EBDEF0")),
                ("GRID", (0, 0), (-1, -1), 1, HexColor("#C39BD3")),
                ("FONTSIZE", (0, 1), (-1, -1), 8),
                ("TOPPADDING", (0, 1), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 1), (-1, -1), 8),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ]
        )
    )
    content.append(model_table)
    content.append(Spacer(1, 0.2 * inch))

    content.append(Paragraph("When to Use Scout-Plan-Build", heading2_style))
    use_cases = [
        "<b>Large codebases</b>: When file discovery would consume 50%+ context",
        "<b>Complex features</b>: Multi-component implementations across frontend/backend/database",
        "<b>Unfamiliar codebase</b>: Learning phase where exploration is needed",
        "<b>Refactoring</b>: Need to understand impact across multiple files",
        "<b>Performance optimization</b>: Requires analyzing patterns across codebase",
    ]

    content.append(
        ListFlowable(
            [ListItem(Paragraph(case, body_style), leftIndent=20) for case in use_cases],
            bulletType="bullet",
            start="circle",
        )
    )

    content.append(Paragraph("When NOT to Use Scout-Plan-Build", heading2_style))
    avoid_cases = [
        "<b>Simple edits</b>: Single file changes (use Claude Code directly or Cursor)",
        "<b>Bug fixes</b>: When exact file is known (no discovery needed)",
        "<b>Documentation</b>: Writing docs doesn't need codebase search",
        "<b>Small projects</b>: <1000 lines of code (overhead not worth it)",
        "<b>Rapid iteration</b>: Early prototyping where architecture changes frequently",
    ]

    content.append(
        ListFlowable(
            [ListItem(Paragraph(case, body_style), leftIndent=20) for case in avoid_cases],
            bulletType="bullet",
            start="square",
        )
    )

    content.append(Paragraph("Context Management Tips", heading2_style))
    context_tips = [
        "Disable autocompact buffer: <b>/config autocompact false</b> (saves 22%)",
        "Clear context between phases: <b>clear</b> or <b>/compact</b>",
        "Monitor usage: <b>/context</b> to check current consumption",
        "Use Planning Mode: <b>Shift+Tab</b> to review before execution",
        "Save work frequently: Preserve plans to AI_docs/ for reuse",
        "Switch tools strategically: Use Cursor for high-volume simple edits",
    ]

    content.append(
        ListFlowable(
            [ListItem(Paragraph(tip, body_style), leftIndent=20) for tip in context_tips],
            bulletType="1",
            start="1",
        )
    )
    content.append(PageBreak())

    # Troubleshooting
    content.append(Paragraph("8. Troubleshooting and Common Pitfalls", heading1_style))

    content.append(Paragraph("Problem: Sub-Agents Find Irrelevant Files", heading2_style))
    content.append(
        Paragraph("<b>Symptom:</b> Scout phase returns files unrelated to the feature.", body_style)
    )
    content.append(
        Paragraph(
            "<b>Solution:</b> Improve search prompts with specific keywords and file patterns.",
            body_style,
        )
    )
    content.append(
        Paragraph(
            "<font name='Courier' size=8>"
            "# Bad prompt<br/>"
            '"Find files related to workouts"<br/>'
            "<br/>"
            "# Good prompt<br/>"
            '"Find files containing:<br/>'
            "- Voice recognition hooks (useVoice, react-native-voice)<br/>"
            "- Workout logging functions (logWorkout, saveWorkout)<br/>"
            "- Exercise database queries (Neo4j Cypher, exercise nodes)<br/>"
            '- tRPC workout procedures (workout.router.ts)"'
            "</font>",
            code_style,
        )
    )

    content.append(Paragraph("Problem: Plan Phase Takes Too Long", heading2_style))
    content.append(
        Paragraph("<b>Symptom:</b> 30-minute plan phase extends to 60+ minutes.", body_style)
    )
    content.append(
        Paragraph(
            "<b>Solution:</b> Break down into smaller features, use iterative planning.", body_style
        )
    )
    content.append(
        Paragraph(
            "Instead of planning entire voice workout system, plan MVP first:<br/>"
            "1. Voice recording only (10 min plan)<br/>"
            "2. Then add exercise parsing (10 min plan)<br/>"
            "3. Then add Neo4j integration (10 min plan)",
            body_style,
        )
    )

    content.append(Paragraph("Problem: Context Window Still Fills Up", heading2_style))
    content.append(
        Paragraph("<b>Symptom:</b> Even with Scout-Plan-Build, hitting context limits.", body_style)
    )
    content.append(Paragraph("<b>Checklist:</b>", body_style))

    context_checklist = [
        "✓ Autocompact disabled? <font name='Courier'>/config autocompact false</font>",
        "✓ Context cleared between phases? <font name='Courier'>clear</font> or <font name='Courier'>/compact</font>",
        "✓ Scout results summarized? Should be <500 lines, not full files",
        "✓ Using free models for scouts? Gemini Flash/Light cost nothing",
        "✓ Planning Mode enabled? Prevents token waste on wrong implementations",
        "✓ Switching to Cursor for simple edits? Save expensive tokens",
    ]

    content.append(
        ListFlowable(
            [ListItem(Paragraph(item, body_style), leftIndent=20) for item in context_checklist],
            bulletType="bullet",
            start="square",
        )
    )

    content.append(Paragraph("Problem: Sub-Agents Don't Execute in Parallel", heading2_style))
    content.append(
        Paragraph(
            "<b>Symptom:</b> Scouts run sequentially, taking 20 minutes instead of 5.", body_style
        )
    )
    content.append(
        Paragraph(
            "<b>Solution:</b> Use proper sub-agent invocation (Claude Code feature). "
            "Ensure you're using Task tool with subagent_type parameter, not sequential commands.",
            body_style,
        )
    )

    content.append(PageBreak())

    # Conclusion
    content.append(Paragraph("9. Conclusion and Next Steps", heading1_style))
    content.append(
        Paragraph(
            "Scout-Plan-Build transforms development velocity through strategic context management and model selection. "
            "By delegating discovery to cheap sub-agents and preserving expensive model capacity for high-value work, "
            "you achieve 50% cost savings and 21% time savings while improving code quality.",
            body_style,
        )
    )

    content.append(Paragraph("Key Takeaways", heading2_style))
    key_takeaways = [
        "<b>R&D Framework is fundamental</b>: Reduce context needs, Delegate to sub-agents",
        "<b>Model selection matters</b>: Free/cheap for discovery, expensive for reasoning",
        "<b>Context is precious</b>: Disable autocompact, clear frequently, use Planning Mode",
        "<b>Parallel execution is powerful</b>: 4 sub-agents = 4x speed for discovery",
        "<b>Planning prevents rework</b>: 30-minute plan saves 2-3 hours of bad implementations",
        "<b>Tools complement each other</b>: Claude Code for planning, Cursor for building",
    ]

    content.append(
        ListFlowable(
            [
                ListItem(Paragraph(takeaway, body_style), leftIndent=20)
                for takeaway in key_takeaways
            ],
            bulletType="bullet",
            start="circle",
        )
    )

    content.append(Paragraph("Implementation Checklist", heading2_style))
    implementation_steps = [
        "☐ Configure Claude Code: <font name='Courier'>/config autocompact false</font>",
        "☐ Create custom slash commands: /scout, /plan, /build",
        "☐ Set up model selection for sub-agents (Gemini Flash/Light, Codex, Haiku)",
        "☐ Create workspace/scout_results.md template",
        "☐ Create AI_docs/ directory for plans",
        "☐ Practice on small feature first (e.g., add button to UI)",
        "☐ Scale to complex features (e.g., voice workout logging)",
        "☐ Measure results: Track cost, time, context usage",
        "☐ Iterate and optimize: Refine prompts, adjust model selection",
    ]

    content.append(
        ListFlowable(
            [ListItem(Paragraph(step, body_style), leftIndent=20) for step in implementation_steps],
            bulletType="bullet",
            start="square",
        )
    )

    content.append(Paragraph("Additional Resources", heading2_style))
    resources = [
        "<b>IndyDevDan</b> - Tactical Agentic Coding course (source of R&D Framework)",
        "<b>Carl Vellotti</b> - Hybrid strategy and cost optimization techniques",
        "<b>Claude Code Documentation</b> - Official sub-agent and planning mode guides",
        "<b>Context Engineering</b> - .claude/ folder structure best practices",
    ]

    content.append(
        ListFlowable(
            [ListItem(Paragraph(resource, body_style), leftIndent=20) for resource in resources],
            bulletType="bullet",
            start="square",
        )
    )

    content.append(Spacer(1, 0.5 * inch))
    content.append(
        Paragraph(
            "Start with one feature. Master the workflow. Scale your development velocity.",
            ParagraphStyle(
                "Final",
                parent=body_style,
                alignment=TA_CENTER,
                fontSize=12,
                textColor=HexColor("#2C3E50"),
                fontName="Helvetica-Bold",
            ),
        )
    )

    # Build PDF
    doc.build(content)
    print(f"✓ Scout-Plan-Build PDF generated: {output_path}")
    return output_path


if __name__ == "__main__":
    create_scout_plan_build_pdf()
