# CLAUDE_template.md

**Template for new project CLAUDE.md files - Copy and customize for each project**

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Planning & Documentation Practices

### Planning Directory Structure
- **Active Plans**: `ai-docs/planning/active/` - Current development plans requiring implementation
- **Backlog Plans**: `ai-docs/planning/backlog/` - Future planned work and feature requests
- **Completed Plans**: `ai-docs/planning/completed/` - Archived completed work for reference

### Planning Guidelines
- **Before Creating Plans**: Always check existing active plans to avoid duplication
- **Plan Creation**: Follow the template and guidelines in `ai-docs/planning/active/CLAUDE.md`
- **Plan Naming**: Use descriptive names: `feature-enhancement-plan.md`
- **Plan Lifecycle**: Active → Completed → Archived (never delete completed plans)
- **Business Context**: All plans must include domain-specific business requirements

### Documentation Structure
- **Technical Guides**: `ai-docs/` directory for architecture and implementation patterns
- **Planning Documents**: `ai-docs/planning/` for project management and feature development
- **Business Context**: `ai-docs/business-context/` for domain knowledge and requirements

### Codebase Documentation (ALWAYS check before implementing)

**CRITICAL: Read relevant ai-docs/ before any implementation work**

#### When to Check ai-docs/
- **Before implementing any feature** - Check for existing patterns and requirements
- **When encountering new concepts** - Search ai-docs/ for documented approaches
- **Before making architectural decisions** - Review established patterns and standards
- **When stuck or unsure** - Use documentation-specialist agent to research ai-docs/

#### Core Technical Guides
**TODO: Customize these links for your project's tech stack**
- **Planning Execution**: `ai-docs/planning/active/CLAUDE.md` - Development workflow and best practices
- **Framework Architecture**: `ai-docs/[framework]-architecture.md` - App patterns and components
- **Database**: `ai-docs/[orm]-guide.md` - Schema design and query patterns  
- **State Management**: `ai-docs/[state-solution]-guide.md` - Client state organization
- **Validation**: `ai-docs/[validation]-guide.md` - Form validation and data schemas
- **UI Components**: `ai-docs/[ui-library]-guide.md` - Component library usage
- **Authentication**: `ai-docs/[auth-solution].md` - User management and session handling
- **Testing**: `ai-docs/[testing]-guide.md` - Unit and integration testing patterns

## Business Context

**TODO: Replace with your domain-specific context**

This is a **[PROJECT TYPE]** with specialized requirements:
- **Domain Requirements**: [Industry regulations, compliance needs, specialized workflows]
- **User Types**: [Different user roles and their permissions/workflows]
- **Data Requirements**: [Special data handling, audit trails, reporting needs]
- **Integration Needs**: [Third-party APIs, external systems, compliance reporting]
- **Performance Considerations**: [Scaling requirements, data volumes, response times]

## Essential Development Workflow

### Quality Gates (REQUIRED before commits)
**TODO: Customize commands for your project**
```bash
[package-manager] lint && [package-manager] typecheck && [package-manager] test
```
**ALL** must pass before any commit. No exceptions.

### Key Development Commands
**TODO: Customize for your project's scripts**
```bash
[package-manager] dev              # Start development server
[package-manager] build            # Production build verification
[package-manager] db:generate      # Generate migrations after schema changes
[package-manager] db:studio        # Database management interface
[package-manager] test:setup       # Initialize test database
```

### Testing & Manual QA
- **Unit Tests**: [Testing framework] for [components/functions/services]
- **Manual Testing**: Use Playwright MCP tools for browser-based workflows
- **Mock Data**: Use [mock data approach] for realistic test scenarios

## Architecture Overview

### Tech Stack Foundation
**TODO: Update with your actual tech stack**
- **Framework**: [Next.js/React/Vue/Angular] - [specific patterns used]
- **Language**: [TypeScript/JavaScript] - [strict typing requirements]
- **Database**: [ORM] with [Database] - [specific patterns]
- **State Management**: [Solution] - [client-side patterns]
- **UI Library**: [Library] - [component system details]
- **Authentication**: [Solution] - [auth patterns]

### Database Schema & Types
**TODO: Customize for your database solution**

#### Schema Location
- **Schema Files**: All tables defined in `[schema-directory]/` with proper relations
- **Generated Types**: Import from `[types-location]` for [ORM]-generated types
- **Type Organization**: Domain-specific types in `[type-files]`

#### Database Patterns
- **Data Layer**: Place in `[data-layer-location]/` organized by business domain
- **Transactions**: Use `[transaction-method]` for multi-step operations
- **Relations**: Use [ORM] relations for type-safe joins
- **Validation**: [Validation library] schemas for all inputs

### Core Architecture Patterns

#### Data Fetching & Mutations
**TODO: Customize for your framework**
- **Preference**: [Server Actions/API Routes/GraphQL/REST]
- **Location**: `[api-directory]/` organized by domain
- **Validation**: Always validate inputs with [validation library]
- **Results**: Return consistent format: `{ success: boolean, data?, errors? }`
- **Error Handling**: [Error handling patterns]

#### State Management
- **Server State**: [How server state is managed]
- **Client State**: [Client state solution] in `[store-location]/`
- **URL State**: [Router] routing and parameters

#### Component Organization
**TODO: Customize for your component structure**
```
components/
├── ui/              # UI library components (DO NOT modify)
├── [domain]/        # Business domain components
└── layout/          # Layout-specific components
```

### Business Domain Structure
**TODO: Define your business domains**

The application is organized around core business domains:

#### [Domain 1] (`[directory]/`)
- [Key responsibilities and features]
- [Specific patterns and requirements]

#### [Domain 2] (`[directory]/`)
- [Key responsibilities and features]
- [Specific patterns and requirements]

## Manual Testing with Playwright MCP

### Browser-Based Testing Tools
- **Purpose**: Manual QA and workflow validation (NOT automated test suite)
- **Tools Available**: Playwright MCP for browser automation and form testing
- **Usage**: Test complex user workflows, form submissions, navigation flows
- **Integration**: Use for validating UI changes and end-to-end business processes

### Test User Credentials
**TODO: Set up test credentials**
- **Email**: `test@example.com`
- **Password**: `password123`
- **Role**: [Admin role with appropriate permissions]
- **Status**: [Account status and verification state]

## Specialized Agent Usage & Orchestration

### Available Agent Types
- **project-manager**: Planning documentation management, project state tracking, context maintenance
- **backend-database-engineer**: Database schema, migrations, server actions, API routes
- **frontend-ui-specialist**: UI components, styling, visual elements, design system
- **feature-architect-planner**: Complex feature planning with architectural considerations
- **file-refactor-organizer**: Breaking down large files (>300 lines), code organization
- **git-workflow-specialist**: Branch strategies, commit hygiene, parallel development
- **code-quality-reviewer**: Comprehensive code review of commits and changes
- **documentation-specialist**: Technical documentation creation in ai-docs/

### Agent Orchestration Patterns for [PROJECT TYPE]
**TODO: Create domain-specific orchestration examples**

#### Complete Feature Implementation (e.g., [Example Feature])
```
1. Use project-manager to review active plans in ai-docs/planning/active/
2. Use feature-architect-planner if implementation plan missing
3. Use documentation-specialist to research [domain-specific requirements]
4. Use git-workflow-specialist to create feature branch
5. Use backend-database-engineer for:
   - [Domain logic] in [backend-location]/
   - Database migrations for [data requirements]
   - [API pattern] with [validation] validation
6. Use frontend-ui-specialist for:
   - [UI components] in components/[domain]/
   - [UI updates] using [UI library]
7. Use code-quality-reviewer to run: [quality commands]
8. Use file-refactor-organizer if any files exceed 300 lines
9. Use project-manager to move plan to completed/
```

#### [Domain-Specific Feature] Development
**TODO: Add more domain-specific patterns**
```
1. Use project-manager to check [domain] plans
2. Use backend-database-engineer for:
   - [Schema updates] in [schema-location]/
   - [Server logic] with [specific requirements]
3. Use frontend-ui-specialist for [UI components] in components/[domain]/
4. Use code-quality-reviewer for [domain] validation
5. Use documentation-specialist to document [compliance/integration patterns]
```

### Project-Specific Quality Gates

Before ANY feature is complete:
- [ ] `[lint-command]` passes (no errors/warnings)
- [ ] `[typecheck-command]` passes ([language] strict)
- [ ] `[test-command]` passes (all tests)
- [ ] Files under 300 lines (use file-refactor-organizer)
- [ ] [Data operations] use [validation/transaction patterns]
- [ ] [Domain-specific requirements] met
- [ ] Planning docs updated in ai-docs/planning/

### [PROJECT TYPE] Agent Priorities
**TODO: Define domain-specific priorities**

1. **[Priority 1]**: Always use [agent] for [requirement]
2. **[Priority 2]**: Use [agent] for all [type of changes]
3. **[Priority 3]**: Never skip `[command]` via [agent]
4. **[Priority 4]**: [Specific business logic pattern]
5. **[Priority 5]**: Use [UI pattern] ([agent])

### Proactive Agent Usage

Automatically use agents when:
- Files exceed 300 lines → file-refactor-organizer
- New [integration] → documentation-specialist first
- [Domain changes] → backend-database-engineer for [calculations]
- [Workflow updates] → feature-architect-planner for impact analysis
- Multiple features active → git-workflow-specialist for worktrees
- Before ANY commit → code-quality-reviewer for quality gates

## Code Quality Standards

### [Language] Requirements
- **Strict Mode**: No `any` types, no type assertions
- **File Size**: Keep files under 300 lines
- **Domain Organization**: Organize by business domain, not technical layers

### Database & Forms
**TODO: Customize for your data patterns**
- **Schema Types**: Use [ORM] schema types for all database operations
- **Validation**: [Validation library] schemas for all form inputs and API data
- **Permissions**: Call `[permission-check]` for protected operations
- **Error Handling**: No `console.*` in production code; use typed errors

### Component Patterns
**TODO: Customize for your framework**
- **[Component Type]**: Default for [use case]
- **[Component Type]**: Only when [specific need]
- **Error Boundaries**: Implement proper error and loading states

## [Framework-Specific Patterns]
**TODO: Add framework-specific guidance**

[Include any framework-specific patterns, like Next.js params/searchParams, Vue composition patterns, etc.]

## Mock Data & Development Setup

### Quick Start Development
**TODO: Customize for your project**
- **Mock Data**: Use [mock data approach] for realistic test data
- **Available Data**: [List of available mock data types]
- **Templates**: Located in `[template-location]/` for testing
- **Database Management**: Use `[db-command]` for direct database access

---

## Template Customization Checklist

When creating a new project CLAUDE.md from this template:

- [ ] Replace all **[PLACEHOLDERS]** with actual values
- [ ] Update **TODO** sections with project-specific information
- [ ] Customize tech stack and architecture details
- [ ] Define business domain and requirements
- [ ] Set up proper development commands
- [ ] Create domain-specific agent orchestration examples
- [ ] Add framework-specific patterns and guidance
- [ ] Set up test credentials and mock data approaches
- [ ] Remove this checklist section

This template provides a comprehensive foundation while maintaining the separation between:
- **Output Styles**: Workflow orchestration modes (research/planning/execution)
- **Universal CLAUDE.md**: Agent delegation patterns
- **Project CLAUDE.md**: Domain context and tech stack specifics