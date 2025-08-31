# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Socratify is a monorepo containing multiple interconnected projects for a learning platform that uses AI-powered conversations to help users think critically about business and technology topics.

## Key Projects

- **socratify-expo**: React Native mobile app (iOS/Android) using Expo SDK 52
- **socratify-nextjs**: Next.js 14 web application with API routes
- **socratify-agent**: Content generation pipeline (stories and exercises)
- **socratify-evals**: LLM evaluation framework using PromptFoo

Ignore all other projects. They are irrelevant

## Common Development Commands

### Mobile App (socratify-expo)

```bash
cd socratify-expo
npm start                # Start Expo development
npm run ios             # Run on iOS simulator
npm run android         # Run on Android emulator
npm run web             # Run web version
npm test                # Run tests (watch mode)
npm run lint            # Run Expo linter
```

### Web App (socratify-nextjs)

```bash
cd socratify-nextjs
npm run dev             # Start development server
npm run build           # Build for production
npm test                # Run unit tests
npm run test:e2e        # Run E2E tests
npm run test:api        # Run API tests
npm run lint            # Run ESLint

# Database operations
npm run migrate:preview  # Run migrations (preview)
npm run seed:preview     # Seed database (preview)
npm run sotw:preview     # Seed story of the week
```

### Python Backend (socratify-backend-python)

```bash
cd socratify-backend-python
poetry install          # Install dependencies
poetry run pytest       # Run tests
```

### Story Generation (socratify-agent)

The agent follows a 10-step pipeline:

1. Convert JSON to cleaned Markdown
2. Generate draft exercises
3. Score exercises
4. Create summary and filter
5. Generate final JSON
6. Create images (cover, mental model, entity)
7. Sync to R2 storage

#### Agent Search Tools

The agent provides 4 unified search tools via wrapper script:

```bash
cd socratify-agent/exercises/v2/tools
python image/search/search_wrapper.py <search_type> --query "<term>" --limit <number>
```

**Available search types:**
- `business_model`: Find business model concepts and explanations
- `mental_model`: Find mental models and thinking frameworks  
- `cover`: Find cover images for exercises
- `exercise`: Find existing exercises by topic/company

**Examples:**
```bash
python image/search/search_wrapper.py business_model --query "freemium" --limit 3
python image/search/search_wrapper.py mental_model --query "first principles" --limit 2
python image/search/search_wrapper.py cover --query "AI" --limit 2
python image/search/search_wrapper.py exercise --query "tesla" --limit 1
```

### Evaluations (socratify-evals)

```bash
cd socratify-evals
promptfoo eval          # Run evaluations
promptfoo view          # View results
```

## Architecture & Key Patterns

### Tech Stack

- **Frontend**: TypeScript, React Native (Expo), Next.js, NativeWind/Tailwind CSS
- **Backend**: Python (FastAPI), Prisma ORM
- **Authentication**: Clerk (both mobile and web)
- **Payments**: RevenueCat (mobile), Stripe (web)
- **AI/LLM**: OpenAI, Anthropic, Google Generative AI
- **Observability**: Langsmith for LLM tracking

### Project Structure

```
/app          # Next.js app directory
/components   # React components
/hooks        # Custom React hooks
/lib          # Utility functions
/types        # TypeScript type definitions
/store        # State management (Zustand)
/contexts     # React contexts
```

### Development Guidelines

1. **TypeScript**: Use strict typing, avoid `any`, define explicit interfaces
2. **Imports**: Group by source (React → third-party → local), use `@/*` path alias
3. **Components**: PascalCase naming, functional with hooks, include "use client" directive when needed
4. **Error Handling**: Use try/catch blocks with custom error classes and contextual logging
5. **Testing**: Write tests for new features, run tests before committing
6. **Code Style**: Follow existing patterns in the codebase, no dark mode implementations

### Database Operations

The Next.js app uses Prisma ORM with PostgreSQL. Always run migrations before seeding:

```bash
npm run migrate:preview  # Apply migrations
npm run seed:preview     # Seed initial data
```

### Key Environment Variables

- `CLERK_SECRET_KEY`: Authentication
- `DATABASE_URL`: PostgreSQL connection
- `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`: AI providers
- `STRIPE_SECRET_KEY`: Payment processing
- `LANGSMITH_API_KEY`: LLM observability

## Important Notes

- The mobile app (Expo) and web app (Next.js) share similar functionality but have separate codebases
- Always check existing CLAUDE.md files in individual projects for project-specific guidance
- Use the established testing frameworks (Jest for Expo, Vitest/Playwright for Next.js)
- Follow the existing code patterns and avoid creating new files unless necessary
