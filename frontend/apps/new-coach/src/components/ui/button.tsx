import * as React from 'react';
import { Slot } from '@radix-ui/react-slot';
import { cva, type VariantProps } from 'class-variance-authority';

import { cn } from '@/lib/utils';

/**
 * Button component
 * ------------------
 * 1. Renders a styled button using Tailwind utility classes that map to the app's theme variables.
 * 2. Applies a solid gold background, white text, no border, rounded-md, and gold shadow for the default button.
 * 3. Uses deeper gold and larger shadow for hover/focus states.
 * 4. Supports dark mode by using dark: variants and dark theme variables.
 * 5. Allows additional className overrides via props.
 * 6. Forwards all other button props to the underlying <button> element or Slot.
 */
const buttonVariants = cva(
  // Base styles for all buttons
  "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-md text-sm font-medium transition-colors transition-shadow disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg:not([class*='size-'])]:size-4 shrink-0 [&_svg]:shrink-0 outline-none",
  {
    variants: {
      variant: {
        // Default: solid gold background, white text, no border, rounded-md, gold shadow
        default: [
          'bg-gold-500', // Gold background
          'text-white', // White text
          'border-0', // No border
          'rounded-md', // Standard border radius
          'px-2 py-4', // Padding
          'font-medium', // Font weight
          'transition-colors transition-shadow', // Smooth transitions
          'hover:bg-gold-600 hover:shadow-gold-sm', // Deeper gold and bigger shadow on hover
          'focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gold-600', // Focus ring
          'dark:bg-gold-600 dark:text-white dark:hover:bg-gold-700', // Dark mode
        ].join(' '),
        // Destructive: keep as is
        destructive:
          'bg-destructive text-white shadow-xs hover:bg-destructive/80 focus-visible:ring-destructive/20 dark:focus-visible:ring-destructive/40 dark:bg-destructive/60 dark:hover:bg-red-500/60',
        // Outline: gold border, gold text, white background
        outline: [
          'border border-gold-400',
          'bg-background',
          'text-gold-700',
          'hover:bg-gold-50 hover:text-gold-900',
          'dark:bg-gold-950 dark:text-gold-100 dark:border-gold-700',
          'dark:hover:bg-gold-900/50 dark:hover:text-gold-100',
        ].join(' '),
        // Secondary: lighter gold background, gold text
        secondary: [
          'bg-gold-100',
          'text-gold-900',
          'border border-gold-200',
          'hover:bg-gold-200 hover:text-gold-950',
          'dark:bg-gold-800 dark:text-gold-100 dark:border-gold-700',
          'dark:hover:bg-gold-700 dark:hover:text-gold-200',
        ].join(' '),
        // Ghost: transparent, gold text on hover
        ghost: [
          'hover:bg-gold-50 hover:text-gold-900',
          'dark:hover:bg-gold-900/50 dark:hover:text-gold-100',
        ].join(' '),
        // Link: gold underline
        link: 'text-gold-700 underline-offset-4 hover:underline dark:text-gold-200',
      },
      size: {
        default: 'px-6 py-2', // Match input height and padding
        sm: 'h-9 rounded-md gap-1.5 px-4 text-xs',
        lg: 'h-12 rounded-md px-8 text-lg',
        icon: 'size-8',
      },
    },
    defaultVariants: {
      variant: 'default',
      size: 'default',
    },
  }
);

function Button({
  className,
  variant,
  size,
  asChild = false,
  ...props
}: React.ComponentProps<'button'> &
  VariantProps<typeof buttonVariants> & {
    asChild?: boolean;
  }) {
  const Comp = asChild ? Slot : 'button';

  return (
    <Comp
      data-slot="button"
      className={cn(buttonVariants({ variant, size, className }))}
      {...props}
    />
  );
}

export { Button, buttonVariants };
