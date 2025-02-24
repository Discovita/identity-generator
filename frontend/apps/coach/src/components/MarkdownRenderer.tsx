import React from 'react';
import ReactMarkdown from 'react-markdown';
import rehypeRaw from 'rehype-raw';

interface MarkdownRendererProps {
  content: string;
}

const MarkdownRenderer = ({ content }: MarkdownRendererProps) => {
  return (
    <ReactMarkdown rehypePlugins={[rehypeRaw]}>
      {content}
    </ReactMarkdown>
  );
};

export default MarkdownRenderer;
