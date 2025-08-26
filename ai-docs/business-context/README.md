# Business Context Documentation

This directory contains business domain knowledge and requirements that guide agent decision-making across different types of projects.

## Purpose

Provide agents with business context to make domain-appropriate technical decisions and ensure implementations align with business requirements.

## Content Guidelines

### Domain Knowledge
- Industry-specific patterns and requirements
- Regulatory and compliance considerations  
- Business process workflows and constraints
- Performance and scaling requirements

### Project Types
Different project types require different business context:
- **E-commerce**: Payment processing, inventory, customer management
- **Healthcare**: HIPAA compliance, patient data protection
- **Financial**: PCI compliance, audit trails, transaction integrity  
- **Cannabis**: Seed-to-sale tracking, state compliance, METRC integration
- **SaaS**: Multi-tenancy, subscription management, scaling patterns

### Agent Usage
- Agents reference business context before making architectural decisions
- Technical choices should align with business requirements
- Implementation patterns should consider domain constraints
- Quality gates should include business rule validation

## Note on Project-Specific Context

While this directory provides general business context patterns, each project should maintain its own `ai-docs/business-context/` with specific domain requirements, as seen in projects like lit-erp with cannabis ERP requirements.