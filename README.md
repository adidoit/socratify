# Socratify Monorepo

A unified monorepo for the Socratify learning platform, using AI-powered conversations to help users think critically about business and technology topics.

## 🏗️ Architecture

This monorepo uses **pnpm workspaces** with **Turborepo** for build orchestration.

### Projects Structure

```
apps/
├── nextjs/          # Next.js web application with API routes
└── expo/            # React Native mobile app (iOS/Android)

packages/
├── shared-types/    # Shared TypeScript/Zod type definitions
└── shared-pydantic/ # Python Pydantic models (generated from TypeScript)
```

## 🚀 Quick Start

### Prerequisites

- Node.js 18+
- pnpm 8+ (`npm install -g pnpm`)
- Python 3.9+ with uv (`pip install uv`)

### Installation

```bash
# Install all dependencies
pnpm install

# Generate Python types from TypeScript definitions
pnpm run generate:types
```

## 📦 Package Management

- **TypeScript/JavaScript**: We use `pnpm` for faster, more efficient package management
- **Python**: We use `uv` for blazing-fast Python dependency resolution

### Common Commands

```bash
# Install dependencies
pnpm install                 # Install all workspace dependencies

# Development
pnpm run dev                 # Start all apps in development mode
pnpm run build              # Build all apps
pnpm run test               # Run tests across all packages
pnpm run lint               # Lint all packages

# Type Generation
pnpm run generate:types     # Generate Pydantic models from TypeScript

# Clean
pnpm run clean              # Clean all build artifacts and node_modules
```

### App-Specific Commands

#### Next.js Web App
```bash
cd apps/nextjs
pnpm run dev                # Start development server
pnpm run build              # Build for production
pnpm run test:unit          # Run unit tests
pnpm run test:e2e           # Run E2E tests
```

#### Expo Mobile App
```bash
cd apps/expo
pnpm run start              # Start Expo development
pnpm run ios                # Run on iOS simulator
pnpm run android            # Run on Android emulator
```

## 🎯 Type System

We maintain a **single source of truth** for all types across TypeScript and Python:

### Architecture
```
Zod Schemas (packages/shared-types)
    ↓
    ├→ TypeScript Types (Next.js/Expo)
    ├→ Prisma JSON Types (typed database fields)
    └→ Pydantic Models (Python services)
```

### Generate Types
```bash
# Generate all types (JSON Schema + Pydantic)
pnpm run generate:types

# This runs:
# 1. Zod → JSON Schema conversion
# 2. JSON Schema → Pydantic conversion
```

### Key Features
- **Type Safety**: Prisma JSON fields are fully typed (no more `JsonValue`)
- **Validation**: Runtime validation with Zod (TypeScript) and Pydantic (Python)
- **Schema Evolution**: Support multiple versions during migration
- **Single Source**: Define once in Zod, use everywhere

See [TYPE_PIPELINE.md](./TYPE_PIPELINE.md) for detailed documentation.

## 🔧 Environment Setup

Each app has its own environment variables:

- `apps/nextjs/.env.local` - Next.js environment variables
- `apps/expo/.env` - Expo environment variables

## 🏭 CI/CD

### Deployments

- **Production**: Deploys from `main` branch
- **Preview**: Deploys from `preview` branch
- **Vercel**: Automatically deploys Next.js app
- **Expo**: Use EAS Build for mobile deployments

### Build Configuration

Turborepo handles build orchestration with proper caching and dependency management. The configuration is in `turbo.json`.

## 🧪 Testing

```bash
# Run all tests
pnpm run test

# Run specific app tests
pnpm run test --filter=socratify-nextjs
pnpm run test --filter=socratify
```

## 📝 Type System

We maintain a single source of truth for types:

1. **TypeScript Types** (`packages/shared-types`): Core type definitions using Zod
2. **Prisma Integration**: Uses `prisma-json-types-generator` for proper JSON field typing
3. **Python Types** (`packages/shared-pydantic`): Auto-generated from TypeScript definitions

### Type Pipeline

```
TypeScript/Zod → Prisma Types → Pydantic Models
      ↓              ↓                ↓
  Next.js App    Database      Python Services
      ↓
  Expo App
```

## 🤝 Contributing

1. Create a feature branch from `main`
2. Make your changes
3. Ensure all tests pass: `pnpm run test`
4. Run linting: `pnpm run lint`
5. Submit a pull request

## 📄 License

Private repository - all rights reserved.