# Frontend Design Prompt

## Project Overview
Design and implement a modern, responsive web application frontend with the following specifications:

## Technical Stack
- React.js (Latest version)
- TypeScript for type safety
- Tailwind CSS for styling
- React Router for navigation
- Axios for API calls
- React Query for data fetching and caching
- Zustand for state management
- React Hook Form for form handling
- Yup for form validation

## Design System
1. Color Palette:
   - Primary: #3B82F6 (Blue)
   - Secondary: #10B981 (Green)
   - Accent: #F59E0B (Amber)
   - Background: #F9FAFB (Light Gray)
   - Text: #1F2937 (Dark Gray)
   - Error: #EF4444 (Red)
   - Success: #10B981 (Green)

2. Typography:
   - Primary Font: Inter
   - Secondary Font: Roboto
   - Base Font Size: 16px
   - Heading Sizes:
     - H1: 2.5rem
     - H2: 2rem
     - H3: 1.75rem
     - H4: 1.5rem
     - H5: 1.25rem
     - H6: 1rem

3. Spacing System:
   - Base Unit: 4px
   - Spacing Scale: 4, 8, 12, 16, 20, 24, 32, 40, 48, 64, 80, 96, 128

4. Component Library:
   - Buttons (Primary, Secondary, Outline, Text)
   - Input Fields (Text, Number, Email, Password)
   - Select Dropdowns
   - Checkboxes and Radio Buttons
   - Cards
   - Modals
   - Navigation Bars
   - Tables
   - Loading States
   - Error States
   - Success Messages

## Layout Structure
1. Main Layout:
   - Header with navigation
   - Sidebar (collapsible)
   - Main content area
   - Footer

2. Responsive Breakpoints:
   - Mobile: < 640px
   - Tablet: 640px - 1024px
   - Desktop: > 1024px

## Key Features
1. Authentication:
   - Login Page
   - Registration Page
   - Password Reset
   - Profile Management

2. Dashboard:
   - Overview Cards
   - Charts and Graphs
   - Recent Activity Feed
   - Quick Actions

3. Data Tables:
   - Sortable Columns
   - Filterable Data
   - Pagination
   - Export Options

4. Forms:
   - Multi-step Forms
   - Dynamic Form Fields
   - File Upload
   - Form Validation

## Performance Requirements
1. Loading Times:
   - First Contentful Paint < 1.5s
   - Time to Interactive < 3s
   - Largest Contentful Paint < 2.5s

2. Optimization:
   - Code Splitting
   - Lazy Loading
   - Image Optimization
   - Caching Strategy

## Accessibility Requirements
1. WCAG 2.1 AA Compliance
2. Keyboard Navigation
3. Screen Reader Support
4. Color Contrast
5. Focus Management

## Testing Requirements
1. Unit Tests:
   - Component Testing
   - Hook Testing
   - Utility Function Testing

2. Integration Tests:
   - Form Submissions
   - API Interactions
   - Navigation Flow

3. Performance Tests:
   - Load Testing
   - Memory Usage
   - CPU Usage

## Development Workflow
1. Git Branch Strategy:
   - main: Production
   - develop: Development
   - feature/*: New Features
   - bugfix/*: Bug Fixes
   - hotfix/*: Urgent Fixes

2. Code Review Process:
   - Pull Request Templates
   - Code Quality Checks
   - Automated Testing
   - Documentation Requirements

## Documentation
1. Component Documentation:
   - Props Interface
   - Usage Examples
   - Storybook Integration

2. API Documentation:
   - Endpoint Descriptions
   - Request/Response Examples
   - Error Handling

## Deployment
1. CI/CD Pipeline:
   - Automated Testing
   - Build Process
   - Deployment Strategy
   - Environment Configuration

2. Monitoring:
   - Error Tracking
   - Performance Monitoring
   - User Analytics

## Security Considerations
1. Authentication:
   - JWT Implementation
   - Session Management
   - CSRF Protection

2. Data Protection:
   - Input Sanitization
   - XSS Prevention
   - Secure Storage

## Browser Support
- Chrome (Latest 2 versions)
- Firefox (Latest 2 versions)
- Safari (Latest 2 versions)
- Edge (Latest 2 versions)

## Mobile Support
- iOS 13+
- Android 8+
- Responsive Design
- Touch Interactions

## Additional Requirements
1. Internationalization:
   - Multi-language Support
   - RTL Support
   - Date/Time Formatting

2. Analytics:
   - User Tracking
   - Event Tracking
   - Performance Metrics

3. SEO:
   - Meta Tags
   - Structured Data
   - Sitemap Generation

## Deliverables
1. Source Code:
   - Well-documented components
   - TypeScript interfaces
   - Test cases
   - Build configuration

2. Documentation:
   - Setup Guide
   - Component Library
   - API Documentation
   - Deployment Guide

3. Assets:
   - Design System
   - Icon Set
   - Image Assets
   - Font Files 