# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Design System

**📐 IMPORTANT: This repository uses a unified design system. See `/DESIGN_SYSTEM.md` for complete documentation.**

The design system provides:
- Consistent color tokens, spacing, typography across all projects
- Platform-adaptive implementation (React Native for Expo, CSS variables for Next.js)
- Apple-inspired animations and interactions
- Full TypeScript support with semantic naming

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

1. **TypeScript**: Use strict typing, avoid `as any` casts - prefer explicit interfaces, type guards (`Array.isArray()`, `typeof`), and proper generic typing
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
- Use the established testing frameworks (Jest for unit/integration/database/AI testing, Playwright for API/E2E testing)
- Follow the existing code patterns and avoid creating new files unless necessary

# Socratify Types Development Guide

## Overview

This project contains the shared type system used across all Socratify projects. It serves as the single source of truth for API contracts, data validation, and TypeScript type definitions.

## Project Structure

```
sources/zod/                    # Zod schema definitions
├── goal-synthesis-*.ts         # Goal synthesis API schemas
├── goal-synthesis-common.ts    # Shared goal synthesis types
├── conversation-*.ts           # Conversation and exercise types
└── [other-api-schemas].ts      # Additional API schemas

generated/                      # Auto-generated outputs (never edit manually)
├── typescript/                 # TypeScript type definitions
├── zod/                        # Zod schema exports
├── json-schema/                # JSON Schema definitions
└── pydantic/                   # Python Pydantic models
```

## Development Workflow

### Complete API Type-Safe Development Process

**Step 1: Design API Contract in socratify-types**
```typescript
// sources/zod/user-track-management.ts
import { z } from 'zod';

export const CreateUserTrackRequestSchema = z.object({
  trackName: z.string().min(1).max(100).describe('User-provided track name'),
  goalDescription: z.string().min(10).describe('Detailed goal description'),
  targetRole: z.string().optional().describe('Desired job role'),
  experienceLevel: z.enum(['entry', 'mid', 'senior']),
  timeframe: z.object({
    hoursPerWeek: z.number().min(1).max(40),
    totalWeeks: z.number().min(4).max(52)
  })
});

export const CreateUserTrackResponseSchema = z.object({
  success: z.boolean(),
  trackId: z.string().uuid().optional(),
  exerciseCount: z.number().optional(),
  estimatedCompletion: z.string().optional(),
  error: z.string().optional()
});

export type CreateUserTrackRequest = z.infer<typeof CreateUserTrackRequestSchema>;
export type CreateUserTrackResponse = z.infer<typeof CreateUserTrackResponseSchema>;
```

**Step 2: Generate Types Across All Projects**
```bash
cd ../socratify-nextjs
npm run generate:types  # Updates both Next.js and Expo automatically
```

**Step 3: Server-Side Implementation (Next.js)**
```typescript
// app/api/user-tracks/route.ts
import { CreateUserTrackRequestSchema, CreateUserTrackResponse } from '@/types/generated/db/zod/user-track-management';

export async function POST(request: NextRequest) {
  // Runtime validation with Zod schema
  const body = await request.json();
  const validatedData = CreateUserTrackRequestSchema.parse(body);
  
  // Business logic with full type safety
  const track = await createUserTrack(validatedData);
  
  // Type-safe response
  const response: CreateUserTrackResponse = {
    success: true,
    trackId: track.uuid,
    exerciseCount: track.exercises.length,
    estimatedCompletion: `${validatedData.timeframe.totalWeeks} weeks`
  };
  
  return NextResponse.json(response);
}
```

**Step 4: Client-Side Service (Expo)**
```typescript
// services/trackService.ts - Mobile API client
import type { CreateUserTrackRequest, CreateUserTrackResponse } from '@/types/generated/db/typescript/user-track-management';

export const createTrack = async (trackData: CreateUserTrackRequest): Promise<CreateUserTrackResponse> => {
  const response = await apiClient.post<CreateUserTrackResponse>('/api/user-tracks', trackData);
  return response.data; // Fully typed response with IntelliSense
};
```

**Step 5: React Hook Integration (Expo)**
```typescript
// hooks/useTrackCreation.ts - Type-safe React hook
import type { CreateUserTrackRequest } from '@/types/generated/db/typescript/user-track-management';

export const useTrackCreation = () => {
  const createNewTrack = async (request: CreateUserTrackRequest) => {
    const result = await createTrack(request);
    
    if (result.success) {
      console.log(`Created track ${result.trackId} with ${result.exerciseCount} exercises`);
    } else {
      console.error(`Track creation failed: ${result.error}`);
    }
    
    return result;
  };
  
  return { createNewTrack };
};
```

**Key Benefits:**
- **End-to-end type safety**: From database to mobile UI
- **Runtime validation**: Zod schemas catch bad data at API boundaries  
- **IntelliSense everywhere**: Full autocomplete in both Next.js and Expo
- **Single source of truth**: API contract defined once, used everywhere
- **Automatic updates**: Type changes propagate to all consuming projects

### Modifying Existing Schemas

1. **Update Zod schema** in the appropriate file under `sources/zod/`
2. **Regenerate types** by running `npm run generate:types` from `socratify-nextjs`
3. **Update consuming code** in other projects if breaking changes were made

## Schema Conventions

### Field Naming

- Use camelCase for field names: `userGoal`, `companyAnalysis`
- Be descriptive but concise: `needsCompanySelection` not `needsSelection`

### Optional vs Required

- Use `.optional()` for truly optional fields
- Use `.nullable()` for fields that can be null
- Use both for fields that can be missing or null: `.nullable().optional()`

### Validation

- Add meaningful descriptions: `.describe('User-selected goal from predefined options')`
- Use appropriate Zod validators: `.min(1)`, `.max(100)`, `.email()`, etc.
- Define enums for constrained string values:

```typescript
export const StatusSchema = z.enum(["pending", "completed", "failed"]);
```

### Complex Objects

- Break complex objects into smaller, reusable schemas
- Use composition with `.extend()` for inheritance
- Prefer flat structures over deeply nested ones

## Type Generation Process

When `npm run generate:types` is run from `socratify-nextjs`:

1. **Reads** all Zod schemas from `sources/zod/`
2. **Generates TypeScript types** in `generated/typescript/`
3. **Creates Zod exports** in `generated/zod/`
4. **Builds JSON schemas** in `generated/json-schema/`
5. **Produces Pydantic models** in `generated/pydantic/`
6. **Copies types** to both `socratify-nextjs` and `socratify-expo`

## Best Practices

### Schema Design

- Start with the API contract design before implementation
- Consider both request and response schemas
- Think about backward compatibility when modifying existing schemas
- Use composition and reusability where possible

### Validation Strategy

- Client-side validation should use TypeScript types (mobile app)
- Server-side validation should use Zod schemas (API routes)
- Both get generated from the same source for consistency

### Breaking Changes

- Coordinate schema changes with all consuming projects
- Consider versioning for major API changes (e.g., `goal-synthesis-v5.ts`)
- Test thoroughly after regenerating types

## Common Patterns

### API Versioning

```typescript
// goal-synthesis-v4.ts
export const GoalSynthesisV4RequestSchema =
  BaseGoalSynthesisRequestSchema.extend({
    newField: z.string().optional(),
  });

export const GoalSynthesisV4ResponseSchema =
  GoalSynthesisV3ResponseSchema.extend({
    enhancedField: EnhancedFieldSchema,
  });
```

### Shared Base Types

```typescript
// goal-synthesis-common.ts
export const BaseGoalSynthesisRequestSchema = z.object({
  userGoal: z.string(),
  userStartingLevel: z.string(),
  userGoalInputText: z.string(),
});
```

### Complex Field Handling

```typescript
// For fields that may be returned as strings by AI models but should be objects
companyLogos: z.any().describe('Map of company name to logo URL'),
// Better than z.record(z.string()) which causes Gemini API issues
```

## Important Notes

- **Never manually edit** files in `generated/` - they are automatically overwritten
- **⚠️ Critical**: Never edit generated types directly - always fix exports and schemas in socratify-types source files to survive regeneration
- **Always regenerate types** after modifying any schema
- **Test API endpoints** after schema changes to ensure validation works
- **Coordinate with team** when making breaking changes to shared schemas
- **Use descriptive commit messages** when updating schemas: "Add industry context to goal synthesis V4"

## Integration with Other Projects

### socratify-nextjs (Backend)

- Uses Zod schemas for request/response validation
- Imports from `@/types/generated/db/zod/[schema-name]`
- Runs the type generation process

### socratify-expo (Mobile)

- Uses TypeScript types for compile-time safety
- Imports from `@/types/generated/db/typescript/[schema-name]`
- Receives updated types automatically after regeneration

### socratify-agent (Content Generation)

- May use Pydantic models for Python-based AI processing
- Generated models provide same validation guarantees
