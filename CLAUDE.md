# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Socratify is a monorepo containing multiple interconnected projects for a learning platform that uses AI-powered conversations to help users think critically about business and technology topics.

## Key Projects

- **socratify-expo**: React Native mobile app (iOS/Android) using Expo SDK 52 - The main user-facing mobile application where users complete AI-powered learning exercises. Contains comprehensive conversation components, onboarding flows, and premium UI/UX patterns.

- **socratify-nextjs**: Next.js 14 web application with API routes - Backend API server and web interface. Contains all AI processing endpoints, database operations, authentication, and business logic. The mobile app consumes APIs from this project.

- **socratify-types**: TypeScript type definitions and Zod schemas - Shared type system used across all projects. Contains API request/response schemas, database models, and validation logic. This is automatically generated from Zod schemas.

- **socratify-agent**: Content generation pipeline (stories and exercises) - AI-powered content creation system that generates learning exercises, stories, and educational materials.

- **socratify-evals**: LLM evaluation framework using PromptFoo - Testing and evaluation system for AI model performance.

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

# Skills matrix seeding (after copying files from agent)
npx tsx scripts/seed-canonical-skills.ts  # Seed skills and relationships
```

### Python Backend (socratify-backend-python)

```bash
cd socratify-backend-python
uv sync                 # Install dependencies
uv run pytest           # Run tests
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

#### Skills Matrix Pipeline

The agent also generates a comprehensive skills matrix for 140+ MBA-coveted roles:

```bash
cd socratify-agent/skills/matrix

# Generate all role skills (parallel processing)
python generate_role_skills.py --workers 5

# Deduplicate to create canonical skills  
python deduplicate_skills.py

# Convert to JSON format
python convert_to_json.py

# Generate skill relationships
python generate_skill_relationships.py

# Copy outputs to Next.js for seeding
cp canonical/canonical_skills.json ../../socratify-nextjs/data/curated-tracks/
cp canonical/skill-relationships.json ../../socratify-nextjs/data/curated-tracks/
```

See `socratify-agent/skills/matrix/README.md` for full pipeline documentation.

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

### Type System (socratify-types)

The `socratify-types` project contains the shared type system used across all Socratify projects. It serves as the single source of truth for API contracts and data validation.

#### When to Use socratify-types:

1. **Adding New API Endpoints**: Always define request/response schemas in `socratify-types/sources/zod/` before implementing APIs
2. **Modifying Existing APIs**: Update the corresponding Zod schema, then regenerate types
3. **Data Validation**: All API endpoints use Zod schemas for request/response validation
4. **Cross-Project Consistency**: Ensures mobile app and backend use identical type definitions

#### Key Files:
- `sources/zod/goal-synthesis-*.ts` - Goal synthesis API schemas
- `sources/zod/goal-synthesis-common.ts` - Shared goal synthesis types
- `sources/zod/conversation-*.ts` - Conversation and exercise types

#### Type Generation Workflow:
```bash
cd socratify-nextjs
npm run generate:types  # Generates TypeScript types from Zod schemas
```

This command:
- Reads Zod schemas from `socratify-types/sources/zod/`
- Generates TypeScript definitions for all projects
- Updates `socratify-nextjs/types/generated/db/`
- Updates `socratify-expo/types/generated/db/`
- Creates Python Pydantic models for backend integration

#### Example Usage:
```typescript
// In API route (socratify-nextjs)
import { GoalSynthesisV4RequestSchema } from '@/types/generated/db/zod/goal-synthesis-v4';

// In mobile app (socratify-expo) 
import type { GoalSynthesisV4Response } from '@/types/generated/db/typescript/goal-synthesis-v4';
```

**Important**: Always run `npm run generate:types` after modifying any Zod schema to ensure all projects stay in sync.

**⚠️ Critical**: Never edit generated types directly - always fix exports and schemas in socratify-types source files to survive regeneration.

### Key Environment Variables

- `CLERK_SECRET_KEY`: Authentication
- `DATABASE_URL`: PostgreSQL connection
- `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`: AI providers
- `STRIPE_SECRET_KEY`: Payment processing
- `LANGSMITH_API_KEY`: LLM observability

## Important Notes

- The mobile app (Expo) and web app (Next.js) share similar functionality but have separate codebases
- **Always check existing CLAUDE.md files in individual projects for project-specific guidance**
- Use the established testing frameworks (Jest for both Expo and Next.js, Playwright for API/E2E testing)
- Follow the existing code patterns and avoid creating new files unless necessary

### Project Relationships

**Mobile App ↔ Backend API Flow:**
1. **socratify-expo** (mobile app) makes HTTP requests to API endpoints
2. **socratify-nextjs** (backend) processes requests and returns responses  
3. **socratify-types** ensures both projects use identical TypeScript interfaces

**Type Safety Chain:**
- Modify Zod schema in `socratify-types/sources/zod/`
- Run `npm run generate:types` from `socratify-nextjs`
- Both mobile app and backend automatically get updated TypeScript types
- API validation uses the same Zod schemas for runtime type checking

**Development Workflow:**
1. Design API contract in `socratify-types` (Zod schema)
2. Generate types with `npm run generate:types`
3. Implement API endpoint in `socratify-nextjs` using generated schema
4. Consume API in `socratify-expo` using generated TypeScript types
5. Write comprehensive tests (Jest for unit/integration/database, Playwright for API/E2E)

## Testing Infrastructure Status

### ✅ Production-Ready Testing (100% Test Health Achieved)

Both primary projects now have robust testing infrastructure:

**socratify-expo:** 143/143 tests passing (100% success rate)
- Jest with React Native Testing Library
- Comprehensive component testing with haptic/animation mocking
- Mobile-optimized test patterns

**socratify-nextjs:** 23/23 test suites passing (100% success rate) 
- Jest for unit, integration, database, and AI service testing
- Prisma database mocking with direct export patterns
- OpenAI/Google GenAI service mocking
- Node.js shims for AI service compatibility

### Key Testing Patterns Established

**Database Testing (Prisma):**
```typescript
// Use direct mock exports, not nested defaults
const mockPrisma = {
  userSkill: { findUnique: jest.fn(), create: jest.fn() },
};
jest.mock('@/lib/db', () => mockPrisma);
```

**AI Service Testing (OpenAI/Google GenAI):**
```typescript
// Mock AI services before importing modules
jest.mock('openai', () => ({ 
  default: jest.fn(() => ({ chat: { completions: { parse: jest.fn() }}}))
}));
```

**Framework Standardization:**
- **Jest**: All unit, integration, database, and AI service testing
- **Playwright**: API endpoints and E2E user journeys
- **No Vitest**: Fully migrated to Jest for consistency
- When editing prompt files for LLMs, leverage Anthropic and OpenAI best practices. Use xml to tag large sections. Provide clear guidance. Do not put any 
 meta-commentary or changelog type comments in the prompt