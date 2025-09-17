# Socratify Design System

## Overview

The Socratify Design System is a comprehensive, Apple-inspired design language that ensures visual consistency across our mobile (Expo) and web (Next.js) applications. Built on an 8pt grid system with sophisticated color tokens, spring physics animations, and semantic naming conventions.

## Core Principles

1. **Mobile-First**: Designed primarily for touch interfaces with minimum 44px touch targets
2. **Apple-Inspired**: Uses spring physics, subtle shadows, and refined typography
3. **Semantic Naming**: All tokens have meaningful names that describe their purpose
4. **Platform Adaptive**: Single source of truth that adapts to React Native and CSS variables
5. **Accessibility-First**: Proper contrast ratios and ARIA support built-in

## Design Tokens

### Color System

Our color system is built on semantic tokens that map to specific use cases:

#### Primary Tokens

| Token | Light Mode | Dark Mode | Usage |
|-------|------------|-----------|--------|
| `primary` | Orange 500 (#e55a2b) | Orange 500 (#ff7b2c) | Primary brand color, CTAs |
| `primaryForeground` | White | White | Text on primary backgrounds |
| `secondary` | Gray 200 | Gray 800 | Secondary actions, less emphasis |
| `secondaryForeground` | Gray 950 | Gray 100 | Text on secondary backgrounds |
| `accent` | Orange 50 | Orange 900 | Subtle brand accents |
| `accentForeground` | Orange 900 | Orange 100 | Text on accent backgrounds |

#### Surface Tokens

| Token | Light Mode | Dark Mode | Usage |
|-------|------------|-----------|--------|
| `background` | Gray 50 | #11181C | Main app background |
| `foreground` | Gray 950 | #ECEDEE | Main text color |
| `card` | White | Gray 900 | Card surfaces |
| `cardForeground` | Gray 950 | Gray 100 | Text on cards |
| `popover` | White | Gray 900 | Popover/modal backgrounds |
| `popoverForeground` | Gray 950 | Gray 100 | Text in popovers |

#### Semantic Tokens

| Token | Light Mode | Dark Mode | Usage |
|-------|------------|-----------|--------|
| `muted` | Gray 100 | Gray 800 | Disabled/subtle elements |
| `mutedForeground` | Gray 600 | Gray 400 | Text for muted elements |
| `destructive` | Red 500 | Red 400 | Errors, destructive actions |
| `destructiveForeground` | White | White | Text on destructive backgrounds |

#### Form Tokens

| Token | Light Mode | Dark Mode | Usage |
|-------|------------|-----------|--------|
| `border` | Gray 300 | Gray 700 | Default borders |
| `input` | Gray 300 | Gray 700 | Input field borders |
| `ring` | Orange 500 | Orange 400 | Focus rings |

#### Data Visualization

| Token | Purpose | Color |
|-------|---------|--------|
| `chart1` | Primary data | Orange |
| `chart2` | Secondary data | Emerald |
| `chart3` | Tertiary data | Blue |
| `chart4` | Quaternary data | Purple |
| `chart5` | Additional data | Amber |

### Spacing System (8pt Grid)

Based on an 8-point grid for consistent spatial relationships:

```typescript
const Spacing = {
  xxs: 2,   // 2px - Fine details, borders
  xs: 4,    // 4px - Minimal gaps
  sm: 8,    // 8px - Small gaps, icon spacing
  md: 16,   // 16px - Standard spacing
  lg: 24,   // 24px - Section spacing
  xl: 32,   // 32px - Large sections
  xxl: 48,  // 48px - Major sections
  xxxl: 64, // 64px - Screen-level spacing
};
```

### Border Radius

Consistent corner rounding for different UI elements:

```typescript
const BorderRadius = {
  xs: 4,     // Subtle rounding
  sm: 6,     // Small elements
  md: 8,     // Default
  lg: 12,    // Larger elements
  xl: 16,    // Cards, major containers
  xxl: 20,   // Modals, sheets
  button: 10,// Buttons
  card: 16,  // Cards
  input: 8,  // Input fields
  full: 9999,// Pills, fully rounded
};
```

### Typography Scale

Mobile-optimized typography with clear hierarchy:

```typescript
const Typography = {
  fontSize: {
    xs:   { size: 12, lineHeight: 16 },  // Captions
    sm:   { size: 14, lineHeight: 20 },  // Secondary text
    base: { size: 16, lineHeight: 24 },  // Body text
    lg:   { size: 18, lineHeight: 28 },  // Emphasized body
    xl:   { size: 20, lineHeight: 28 },  // Small headings
    "2xl":{ size: 24, lineHeight: 32 },  // Headings
    "3xl":{ size: 30, lineHeight: 36 },  // Large headings
    "4xl":{ size: 36, lineHeight: 40 },  // Display
    "5xl":{ size: 48, lineHeight: 48 },  // Large display
  },
  fontWeight: {
    normal: "400",
    medium: "500",
    semibold: "600",
    bold: "700",
    extrabold: "800",
  },
};
```

### Animation System

Apple-inspired spring physics for natural motion:

```typescript
const Animation = {
  duration: {
    fast: 150,    // Quick feedback
    normal: 250,  // Standard transitions
    slow: 350,    // Complex animations
  },
  spring: {
    gentle: { damping: 20, stiffness: 300, mass: 0.8 },
    bouncy: { damping: 15, stiffness: 400, mass: 0.6 },
    snappy: { damping: 25, stiffness: 500, mass: 0.5 },
    smooth: { damping: 18, stiffness: 350, mass: 0.9 },
  },
};
```

### Elevation (Shadows)

Layered depth system for visual hierarchy:

```typescript
const Elevation = {
  xs: "0px 1px 2px rgba(0, 0, 0, 0.05)",   // Subtle lift
  sm: "0px 2px 4px rgba(0, 0, 0, 0.08)",   // Cards
  md: "0px 4px 8px rgba(0, 0, 0, 0.12)",   // Dropdowns
  lg: "0px 8px 16px rgba(0, 0, 0, 0.16)",  // Modals
  xl: "0px 12px 24px rgba(0, 0, 0, 0.20)", // Popovers
};
```

## Implementation

### React Native (Expo)

Import from the centralized DesignSystem file:

```typescript
import DesignSystem from '@/constants/DesignSystem';

// Using color tokens
const styles = StyleSheet.create({
  container: {
    backgroundColor: DesignSystem.tokens.light.background,
    padding: DesignSystem.spacing.md,
    borderRadius: DesignSystem.borderRadius.card,
  },
  text: {
    color: DesignSystem.tokens.light.foreground,
    fontSize: DesignSystem.typography.fontSize.base.size,
  },
});

// Using animations
import { useButtonPressAnimation } from '@/utils/animations';

const MyButton = () => {
  const { animatedStyle, handlePressIn, handlePressOut } = useButtonPressAnimation();
  
  return (
    <Animated.View style={animatedStyle}>
      <Pressable onPressIn={handlePressIn} onPressOut={handlePressOut}>
        <Text>Press Me</Text>
      </Pressable>
    </Animated.View>
  );
};
```

### Next.js (Web)

CSS variables are automatically generated from the design system:

```css
/* Using CSS variables in Tailwind classes */
<div className="bg-background text-foreground rounded-card p-4">
  <h1 className="text-2xl font-bold text-primary">Hello</h1>
  <p className="text-muted-foreground">Description text</p>
</div>

/* Using in custom CSS */
.custom-element {
  background: hsl(var(--primary));
  border-radius: var(--radius-button);
  padding: var(--spacing-md);
}
```

### Tailwind Configuration

Both projects use Tailwind, configured to use our design tokens:

```javascript
// tailwind.config.js
module.exports = {
  theme: {
    extend: {
      colors: {
        primary: 'hsl(var(--primary))',
        secondary: 'hsl(var(--secondary))',
        // ... all other color tokens
      },
      borderRadius: {
        sm: 'var(--radius-sm)',
        md: 'var(--radius)',
        lg: 'var(--radius-lg)',
        // ... all other radius tokens
      },
    },
  },
};
```

## Component Patterns

### Buttons

Primary, secondary, and destructive variants with consistent styling:

```typescript
// Expo
<TouchableOpacity style={[
  styles.button,
  variant === 'primary' && styles.buttonPrimary,
  variant === 'secondary' && styles.buttonSecondary,
]}>
  <Text style={styles.buttonText}>{label}</Text>
</TouchableOpacity>

// Next.js
<Button variant="primary" size="md">
  Click Me
</Button>
```

### Cards

Elevated surfaces with consistent padding and shadows:

```typescript
// Expo
<View style={[styles.card, DesignSystem.elevation.sm]}>
  <Text style={styles.cardTitle}>Card Title</Text>
  <Text style={styles.cardContent}>Card content</Text>
</View>

// Next.js
<Card className="p-4">
  <CardHeader>Card Title</CardHeader>
  <CardContent>Card content</CardContent>
</Card>
```

## Accessibility

- **Minimum touch targets**: 44px on mobile
- **Color contrast**: WCAG AA compliant
- **Focus indicators**: Clear ring styles
- **ARIA labels**: Semantic roles and descriptions
- **Haptic feedback**: Tactile responses on mobile

## Migration Guide

### From Old Colors.ts

The new DesignSystem.ts is backwards compatible. Simply update imports:

```typescript
// Old
import { Colors } from '@/constants/Colors';
const color = Colors.light.text;

// New
import DesignSystem from '@/constants/DesignSystem';
const color = DesignSystem.tokens.light.foreground;
```

### From Hardcoded Values

Replace hardcoded colors and spacing with design tokens:

```typescript
// Old
style={{ backgroundColor: '#e55a2b', padding: 16 }}

// New
style={{ 
  backgroundColor: DesignSystem.tokens.light.primary,
  padding: DesignSystem.spacing.md 
}}
```

## Best Practices

1. **Always use semantic tokens** - Never hardcode colors or spacing
2. **Respect platform conventions** - iOS haptics on mobile, hover states on web
3. **Test in both light and dark modes** - Ensure proper contrast
4. **Use the animation system** - Consistent motion creates cohesion
5. **Follow the spacing grid** - 8pt increments for alignment
6. **Leverage TypeScript** - Use type safety for design tokens

## Tools & Resources

- **Expo Constants**: `/socratify-expo/constants/DesignSystem.ts`
- **Animation Utils**: `/socratify-expo/utils/animations.ts`
- **CSS Variables**: `/socratify-nextjs/app/globals.css`
- **Tailwind Config**: Both projects' `tailwind.config` files

## Future Enhancements

- [ ] Color palette generator for custom themes
- [ ] Figma design token sync
- [ ] Automated accessibility testing
- [ ] Dynamic theme switching
- [ ] Component library documentation site