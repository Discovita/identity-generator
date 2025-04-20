import React from 'react';

/**
 * AssistantMessage Component
 * -------------------------
 * Renders a chat bubble for assistant messages with gold/neutral theme.
 * Usage: <AssistantMessage>Message content</AssistantMessage>
 *
 * Tailwind styles match the original assistant message style in ChatInterface.
 *
 * Props:
 * - children: React.ReactNode (message content)
 * - ...props: any additional props for the div
 */
export const AssistantMessage: React.FC<
  React.PropsWithChildren<React.HTMLAttributes<HTMLDivElement>>
> = ({ children, ...props }) => (
  <div
    className="_AssistantMessage mb-4 p-3.5 pr-4 pl-4 rounded-t-[18px] rounded-br-[18px] rounded-bl-[6px] max-w-[75%] leading-[1.5] shadow-sm animate-fadeIn break-words mr-auto bg-gold-200 border-l-[3px] border-l-gold-600 dark:bg-transparent dark:border-r-[1px] dark:border-r-gold-600 dark:border-t-[1px] dark:border-t-gold-600 dark:border-b-[1px] dark:border-b-gold-600 dark:text-gold-200"
    {...props}
  >
    {children}
  </div>
);
