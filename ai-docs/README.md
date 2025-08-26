# AI Documentation System

This directory contains **structured documentation** designed to provide context and guidance to Claude Code and specialized agents. The ai-docs system creates a knowledge base that enables more effective development by making project patterns, architectural decisions, and business requirements easily discoverable.

## What is ai-docs?

The ai-docs system is a **standardized documentation structure** that provides project context to AI development tools. Unlike traditional documentation meant only for humans, ai-docs is optimized for both human readability and AI consumption.

**Key Concepts:**
- **Discoverable:** Agents can automatically find relevant guidance  
- **Structured:** Consistent organization across projects
- **Actionable:** Provides specific implementation patterns, not just theory
- **Contextual:** Includes business requirements alongside technical patterns

**Reference:** This structure follows Claude Code best practices for agent-readable documentation.

## Purpose & Agent Integration

**How Agents Use ai-docs:**
- **All agents** read `ai-docs/` to understand project context before starting work
- **project-manager** maintains planning document lifecycle 
- **feature-architect-planner** creates plans in `planning/active/`
- **documentation-specialist** researches and creates library guides
- **backend-database-engineer** & **frontend-ui-specialist** follow established patterns
- **code-quality-reviewer** references testing standards and quality gates

## Directory Structure

### Core Documentation
```
ai-docs/
├── README.md                    # This guide
├── architecture/                # System design and patterns
├── business-context/           # Domain-specific requirements
├── library-guides/             # Technology integration guides  
├── planning/                   # Feature planning workflow
│   ├── active/                # Currently being implemented
│   ├── backlog/               # Future planned work
│   └── completed/             # Archived completed plans
└── troubleshooting/           # Common issues and solutions
```

### Real Example: Cannabis ERP (lit-erp)

Based on the lit-erp project structure:

#### Architecture Documentation
- `nextjs-architecture.md` - App Router patterns, Server Components
- `manufacturing-architecture.md` - Production workflow specifics
- `architecture-diagram.md` - System overview and data flow

#### Library Integration Guides  
- `drizzle-orm-guide.md` - Database ORM patterns and relationships
- `zustand-nextjs-guide.md` - Client state management
- `better-auth.md` - Authentication and session handling
- `shadcn-ui-guide.md` - UI component library usage
- `tailwind-v4-guide.md` - Styling conventions
- `zod-guide.md` - Form validation and data schemas
- `playwright-testing.md` - Testing patterns and QA workflows

#### Business Context
- Cannabis compliance requirements (METRC integration)
- Customer tier system (Gold/Silver/Bronze)
- Multi-location inventory tracking
- Seed-to-sale traceability requirements

#### Planning Workflow
- **Active**: `manufacturing-rooms-implementation-plan.md`, `data-management-consolidation.md`
- **Backlog**: Future features like CRM enhancements, calendar integration
- **Completed**: Reference for lessons learned and successful patterns

## Usage Patterns by Agent

### project-manager
```
1. Reviews ai-docs/planning/active/ for current project status
2. Moves completed plans from active/ → completed/
3. Identifies planning gaps or outdated documentation
4. Provides status summaries referencing specific planning docs
```

### feature-architect-planner
```
1. Reads ai-docs/architecture/ to understand system design
2. Reviews ai-docs/business-context/ for domain requirements
3. Checks ai-docs/library-guides/ for technology constraints
4. Creates detailed plans in ai-docs/planning/active/
5. References existing patterns from completed/ plans
```

### backend-database-engineer
```
1. Follows patterns in ai-docs/drizzle-orm-guide.md
2. Implements Server Actions per ai-docs/nextjs-architecture.md
3. Ensures compliance per ai-docs/business-context/
4. References api patterns from completed implementations
```

### frontend-ui-specialist  
```
1. Uses component patterns from ai-docs/shadcn-ui-guide.md
2. Follows responsive design standards in ai-docs/
3. Implements themes per ai-docs/tailwind-v4-guide.md
4. Ensures accessibility compliance per quality standards
```

### code-quality-reviewer
```
1. Runs quality gates defined in project CLAUDE.md
2. Follows testing patterns from ai-docs/playwright-testing.md
3. Validates against architecture requirements
4. Checks business logic compliance
```

### documentation-specialist
```
1. Creates new library guides in ai-docs/library-guides/
2. Updates architecture docs when patterns change
3. Maintains troubleshooting knowledge base
4. Researches and documents new technologies
```

## Creating Project-Specific ai-docs

### Step 1: Copy Template Structure
```bash
mkdir -p ai-docs/{architecture,business-context,library-guides,planning/{active,backlog,completed},troubleshooting}
```

### Step 2: Create Core Documentation
- **Architecture**: Document your tech stack patterns
- **Business Context**: Domain-specific requirements and constraints
- **Library Guides**: Integration patterns for your key technologies
- **Planning**: Active feature development plans

### Step 3: Establish Quality Gates
Document in your project CLAUDE.md:
- Required commands (lint, typecheck, test)
- File organization rules (300-line limit)
- Code quality standards
- Agent usage priorities for your domain

## Example: Cannabis ERP Business Context

```markdown
# Cannabis ERP Business Requirements

## Compliance Framework
- METRC integration for seed-to-sale tracking
- State-specific regulations per location
- Batch-level traceability requirements
- Chain of custody documentation

## Customer Tier System
- Gold: Premium pricing, priority support
- Silver: Standard business accounts  
- Bronze: Basic tier with limited features

## Multi-Location Operations
- Inventory tracked per facility
- Location-based picking optimization
- Cross-location transfer tracking
- Facility-specific compliance rules
```

This structured approach ensures agents have complete project context and can make informed decisions aligned with your specific business and technical requirements.