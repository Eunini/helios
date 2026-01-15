# Helios Frontend

Next.js-based dashboard for Helios AI Operations Manager.

## Overview

The frontend provides a modern, responsive interface for managing retail business operations. It communicates with the Helios backend API for all business logic and AI agent coordination.

## Tech Stack

- **Framework**: Next.js 14+
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **HTTP**: Axios
- **Auth**: NextAuth.js (ready for integration)
- **UI Components**: Custom + Shadcn

## Installation

```bash
# Install dependencies
npm install

# Configure environment
cp .env.example .env.local
# Edit .env.local with your backend URL

# Run development server
npm run dev
```

Server: http://localhost:3000

## Scripts

```bash
npm run dev        # Development server with hot reload
npm run build      # Production build
npm run start      # Start production server
npm run lint       # ESLint checking
npm run type-check # TypeScript type checking
```

## Project Structure

```
frontend/
├── app/
│   ├── layout.tsx          # Root layout
│   ├── page.tsx            # Landing page
│   ├── globals.css         # Global styles
│   └── dashboard/
│       ├── layout.tsx      # Dashboard layout
│       ├── page.tsx        # Main dashboard
│       ├── inventory/      # Inventory section
│       ├── customers/      # Customers section
│       ├── staff/          # Staff section
│       └── insights/       # Analytics section
│
├── components/
│   ├── ui/                 # Base UI components
│   │   ├── button.tsx
│   │   ├── card.tsx
│   │   ├── input.tsx
│   │   └── textarea.tsx
│   ├── dashboard/          # Dashboard components
│   │   ├── header.tsx
│   │   ├── sidebar.tsx
│   │   └── stats-card.tsx
│   └── chat/               # Chat interface
│       └── chat-interface.tsx
│
├── lib/
│   ├── api.ts              # API client wrapper
│   └── utils.ts            # Utility functions
│
└── public/                 # Static assets
```

## Features

### Dashboard

- **Real-time Metrics**: Total cash, inventory value, daily sales, customer count
- **Recent Transactions**: Latest sales with customer info
- **Quick Stats**: Product count, staff count, low stock items
- **AI Chat Interface**: Natural language task submission

### Navigation

- Overview (main dashboard)
- Inventory Management
- Customer Management
- Staff Management
- Business Insights

### Components

- **StatsCard**: Display key metrics with icons and trends
- **ChatInterface**: Send natural language commands
- **Sidebar**: Navigation menu with active states
- **Header**: Date and user info
- **UI Components**: Button, Card, Input, Textarea

## API Integration

### Axios Client

All API calls use a centralized Axios client in `lib/api.ts`:

```typescript
import api from "@/lib/api";

// Example calls
const task = await api.submitTask("Add 50 bottles of Coke", "normal");
const state = await api.getBusinessState();
const products = await api.listProducts();
```

### Error Handling

- Global error interceptor
- User-friendly error messages
- Automatic retry ready

## Styling

### Tailwind CSS

Custom Tailwind configuration with:

- Primary blue colors
- Responsive breakpoints
- Dark mode support (ready)

```css
/* Global styles in app/globals.css */
@tailwind base;
@tailwind components;
@tailwind utilities;
```

## Component Examples

### Stats Card

```tsx
<StatsCard
  title="Daily Sales"
  value={5000}
  trend="up"
  trendValue={12}
  icon="📈"
/>
```

### Chat Interface

```tsx
<ChatInterface />
```

### Button

```tsx
<Button variant="primary" size="lg">
  Click Me
</Button>
```

## Environment Variables

```
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXTAUTH_SECRET=your_32_char_secret
NEXTAUTH_URL=http://localhost:3000
```

## Development

### Type Checking

```bash
npm run type-check
```

### Code Quality

- ESLint configured
- TypeScript strict mode
- Prettier formatting

### Hot Reload

Changes automatically reload during `npm run dev`

## Production Build

```bash
# Build
npm run build

# Start production server
npm run start
```

## Deployment

### Vercel (Recommended)

```bash
npm i -g vercel
vercel login
vercel
```

### Docker

```bash
docker build -t helios-frontend .
docker run -p 3000:3000 helios-frontend
```

### Environment for Production

- Update `NEXT_PUBLIC_API_URL` to production backend
- Use strong `NEXTAUTH_SECRET`
- Set `NEXTAUTH_URL` to production domain

## Performance

- Static optimization
- Image optimization ready
- Code splitting
- CSS optimization
- Fast refresh during development

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Common Issues

**API Connection Error**

- Check `NEXT_PUBLIC_API_URL` in .env.local
- Verify backend is running on correct port
- Check CORS settings in backend

**TypeScript Errors**

- Run `npm run type-check`
- Check tsconfig.json
- Import types correctly

**Styling Issues**

- Clear node_modules: `rm -rf node_modules && npm install`
- Rebuild Tailwind: `npm run build`

## Future Enhancements

- Dark mode toggle
- Real-time WebSocket updates
- Advanced charts and analytics
- Mobile app version
- Authentication integration
- Offline mode
- Multi-language support

## Support

For frontend-specific issues, check:

- Next.js docs: https://nextjs.org/docs
- Tailwind docs: https://tailwindcss.com/docs
- Component-specific code

---

**Helios Frontend v1.0.0**
