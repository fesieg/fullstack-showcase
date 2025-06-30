# Bottle Return System - Frontend

## Prerequisites

- Node.js (version 16 or higher) or Bun
- npm or bun package manager
- Backend API running on `http://localhost:8000`

## Setup Instructions

### 1. Install Dependencies

```bash
npm install
# or
bun install
```

### 2. Environment Configuration

Create a `.env` file in the frontend root directory:

```env
VITE_API_TOKEN=your-api-token-here
```

This must match the token configured in the backend .env.

The backend API URL is configured to `http://localhost:8000/api` by default.

### 3. Development Server

Start the development server:

```bash
npm run dev
# or
bun run dev
```

The application will be available at `http://localhost:5173`

Built files will be in the `dist/` directory.

## Available Scripts

- `npm / bun run dev` - Start development server
- `npm / bun run build` - Build for production
- `npm / bun run test` - Run tests in watch mode
- `npx / bunx vitest --run` - Run tests once
- `npm / bun run lint` - Run ESLint

## Project Structure

```
src/
├── components/          # React components
│   ├── AddBottleForm.tsx       # Form for adding new bottles
│   ├── BottleBalanceSection.tsx # Balance display and redeem button
│   └── BottleTable.tsx         # Table displaying bottles
├── lib/                # Utility libraries
│   ├── api.ts          # Axios API client and endpoints
│   └── format.ts       # Formatting utilities (currency, dates)
├── types/              # TypeScript type definitions
│   └── Bottle.ts       # Bottle type definitions
├── test/               # Test setup and utilities
│   └── setup.ts        # Vitest configuration
├── App.tsx             # Main application component
├── App.scss            # Global application styles
└── main.tsx            # Application entry point
```