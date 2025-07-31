import React from 'react';
import clsx from 'clsx';
import {useBlogPost} from '@docusaurus/theme-common/internal';
import BlogPostAuthor from '@theme/BlogPostAuthor';
import type {Props} from '@theme/BlogPostAuthors';

import styles from './styles.module.css';

export default function BlogPostAuthors({
  className,
}: Props): JSX.Element | null {
  const {
    metadata: {authors},
    isBlogPostPage,
  } = useBlogPost();
  const authorsCount = authors.length;
  if (authorsCount === 0) {
    return null;
  }
  
  return (
    <div
      className={clsx(
        'margin-top--md margin-bottom--sm',
        styles.blogPostAuthorsContainer,
        className,
      )}>
      {authors.map((author, idx) => (
        <div
          className={styles.blogPostAuthor}
          key={idx}>
          <BlogPostAuthor
            author={{
              ...author,
            }}
          />
        </div>
      ))}
    </div>
  );
} 