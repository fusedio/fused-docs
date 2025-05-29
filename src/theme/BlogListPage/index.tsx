import React, { useState } from 'react';
import clsx from 'clsx';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import BlogLayout from '@theme/BlogLayout';
import BlogListPaginator from '@theme/BlogListPaginator';
import { BlogPostProvider } from '@docusaurus/plugin-content-blog/lib/client/contexts.js';
import type { Props } from '@theme/BlogListPage';
import Link from '@docusaurus/Link';
import useBaseUrl from '@docusaurus/useBaseUrl';
import BlogListPageStructuredData from '@theme/BlogListPage/StructuredData';
import styles from './styles.module.css';

const CATEGORIES = {
  all: 'All',
  news: 'News',
  technical: 'Technical blogs',
  use_cases: 'Use cases',
  uncategorized: 'Uncategorized',
} as const;

function formatDate(dateString: string): string {
  const date = new Date(dateString);
  return new Intl.DateTimeFormat('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  }).format(date);
}

type CategoryKey = keyof typeof CATEGORIES;

interface BlogPostFrontMatter {
  category?: CategoryKey;
  image?: string;
}

function BlogPostCard({
  category,
  title,
  date,
  authors,
  permalink,
  image,
  showCategory,
}: {
  category: CategoryKey;
  title: string;
  date: string;
  authors: any[];
  permalink: string;
  image?: string;
  showCategory: boolean;
}): JSX.Element {
  const imageUrl = image ? useBaseUrl(image) : undefined;
  const fallbackLogoUrl = useBaseUrl('/img/logo-black-bg-transparent.svg');
  
  return (
    <Link
      to={permalink}
      className={styles.blogCard}
    >
      {imageUrl ? (
        <div className={styles.cardImage}>
          <img src={imageUrl} alt={title} />
          {showCategory && (
            <div className={styles.cardCategory}>
              {CATEGORIES[category] || 'Uncategorized'}
            </div>
          )}
        </div>
      ) : (
        <div className={styles.cardHeader}>
          <img src={fallbackLogoUrl} alt="Fused Logo" className={styles.fallbackLogo} />
          {showCategory && (
            <div className={styles.cardCategory}>
              {CATEGORIES[category] || 'Uncategorized'}
            </div>
          )}
        </div>
      )}
      <div className={styles.cardContent}>
        <h3 className={styles.cardTitle}>
          {title}
        </h3>
        <div className={styles.cardMeta}>
          <span>{formatDate(date)}</span>
          <span>{authors.map(author => author.name).join(', ')}</span>
        </div>
      </div>
    </Link>
  );
}

export default function BlogListPage(props: Props): JSX.Element {
  const { metadata, items } = props;
  const {
    siteConfig: { title: siteTitle },
  } = useDocusaurusContext();

  const [searchQuery, setSearchQuery] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<CategoryKey>('all');

  const filteredItems = items.filter(({ content: BlogPostContent }) => {
    const frontMatter = BlogPostContent.metadata.frontMatter as BlogPostFrontMatter | undefined;
    const title = BlogPostContent.metadata.title.toLowerCase();
    const authors = BlogPostContent.metadata.authors?.map(author => author.name.toLowerCase()).join(' ') || '';
    const searchLower = searchQuery.toLowerCase();
    
    const matchesSearch = searchQuery === '' || 
      title.includes(searchLower) || 
      authors.includes(searchLower);
      
    const matchesCategory =
      selectedCategory === 'all' ||
      frontMatter?.category === selectedCategory;
      
    return matchesSearch && matchesCategory;
  });

  return (
    <>
      <BlogListPageStructuredData {...props} />
      <BlogLayout
        title="Blog"
        description="Read about Fused's latest News, Use cases, and Technical blogs."
        sidebar={undefined}
      >
        <div className={styles.blogContainer}>
          <div className={styles.searchAndFilters}>
            {/* Search Bar */}
            <input
              type="search"
              placeholder="Search by title or author..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className={styles.searchInput}
            />

            {/* Category Filters */}
            <div className={styles.categoryFilters}>
              {Object.entries(CATEGORIES).filter(([key]) => key !== 'uncategorized').map(([key, value]) => (
                <button
                  key={key}
                  onClick={() => setSelectedCategory(key as CategoryKey)}
                  className={clsx(
                    styles.categoryButton,
                    selectedCategory === key
                      ? styles.categoryButtonActive
                      : styles.categoryButtonInactive
                  )}
                >
                  {value}
                </button>
              ))}
            </div>
          </div>

          {/* Blog Posts Grid */}
          <div className={styles.blogGrid}>
            {filteredItems.map(({ content: BlogPostContent }) => {
              const frontMatter = BlogPostContent.metadata.frontMatter as BlogPostFrontMatter | undefined;
              return (
                <BlogPostProvider
                  key={BlogPostContent.metadata.permalink}
                  content={BlogPostContent}
                >
                  <BlogPostCard
                    category={frontMatter?.category || 'uncategorized'}
                    title={BlogPostContent.metadata.title}
                    date={BlogPostContent.metadata.date}
                    authors={BlogPostContent.metadata.authors || []}
                    permalink={BlogPostContent.metadata.permalink}
                    image={frontMatter?.image}
                    showCategory={selectedCategory === 'all'}
                  />
                </BlogPostProvider>
              );
            })}
          </div>

          <BlogListPaginator metadata={metadata} />
        </div>
      </BlogLayout>
    </>
  );
}
