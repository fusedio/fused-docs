@fused.udf
def udf(
    base_url: str = "https://docs.fused.io",
    mode: str = "curated",  # "curated" | "full"
    sitemap_path: str = "/sitemap.xml",
    site_title: str = "Fused Documentation",
    site_description: str = "Fused is an end-to-end cloud platform for data analytics, built around User Defined Functions (UDFs): Python functions that can be run via HTTPS requests from anywhere, without any install required.",
    max_pages: int = 0,  # 0 = no limit, useful for testing
    output_path: str = "",  # e.g. "fd://my_org/llms.txt" — leave empty to return as string
):
    """
    Generate an llms.txt file from any public docs site with a sitemap.

    Two modes:
    - "curated": one line per page — title, URL, short description
    - "full": full page content, lightly cleaned

    Works with any static docs site (Docusaurus, MkDocs, Astro, etc.).
    """
    import re
    import time
    import requests
    from xml.etree import ElementTree
    from bs4 import BeautifulSoup

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #

    def fetch(url: str, retries: int = 3, timeout: int = 15) -> str | None:
        headers = {"User-Agent": "llms-txt-generator/1.0 (sitemap crawler)"}
        for attempt in range(retries):
            try:
                r = requests.get(url, headers=headers, timeout=timeout)
                r.raise_for_status()
                return r.text
            except Exception as e:
                if attempt == retries - 1:
                    print(f"  ✗ Failed {url}: {e}")
                    return None
                time.sleep(1.5 ** attempt)

    def parse_sitemap(xml_text: str) -> list[str]:
        """Parse a sitemap or sitemap index and return all page URLs."""
        try:
            root = ElementTree.fromstring(xml_text)
        except ElementTree.ParseError:
            return []

        ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = []

        # Sitemap index — recurse into sub-sitemaps
        for sitemap_tag in root.findall("sm:sitemap", ns):
            loc = sitemap_tag.find("sm:loc", ns)
            if loc is not None and loc.text:
                sub_xml = fetch(loc.text.strip())
                if sub_xml:
                    urls.extend(parse_sitemap(sub_xml))

        # Regular sitemap
        for url_tag in root.findall("sm:url", ns):
            loc = url_tag.find("sm:loc", ns)
            if loc is not None and loc.text:
                urls.append(loc.text.strip())

        return urls

    def extract_page(html: str, url: str) -> dict:
        """
        Extract title, description, and main content from a docs page HTML.

        Tries common docs site content selectors in order:
        - <article> (Docusaurus, most static site generators)
        - .md-content (MkDocs)
        - .content, .documentation, main
        - Falls back to <body>
        """
        soup = BeautifulSoup(html, "html.parser")

        # Remove nav, sidebar, footer, TOC, scripts, styles
        for tag in soup.select(
            "nav, footer, aside, .sidebar, .toc, .table-of-contents, "
            ".navbar, .pagination, .edit-this-page, script, style, "
            "[class*='sidebar'], [class*='navbar'], [class*='footer'], "
            "[class*='toc'], [class*='pagination'], [class*='breadcrumb'], "
            "[aria-hidden='true']"
        ):
            tag.decompose()

        # Title — prefer <h1> inside content, fall back to <title>
        title = ""
        h1 = soup.find("h1")
        if h1:
            title = h1.get_text(strip=True)
        if not title:
            title_tag = soup.find("title")
            if title_tag:
                # Strip site name suffix (e.g. " | Fused Docs")
                title = re.sub(r"\s*[|–—-].*$", "", title_tag.get_text(strip=True))

        # Main content area
        content_el = (
            soup.find("article")
            or soup.find(class_=re.compile(r"md-content|markdown|content|documentation"))
            or soup.find("main")
            or soup.body
        )

        if content_el is None:
            return {"title": title, "description": "", "content": ""}

        raw_text = content_el.get_text(separator="\n", strip=True)

        # Description: first non-empty, non-heading paragraph-ish line (≥ 40 chars)
        description = ""
        for line in raw_text.splitlines():
            line = line.strip()
            if len(line) >= 40 and not line.startswith("#"):
                description = line[:160] + ("..." if len(line) > 160 else "")
                break

        # Full cleaned content: collapse excessive blank lines
        content = re.sub(r"\n{3,}", "\n\n", raw_text).strip()

        return {"title": title, "description": description, "content": content}

    # ------------------------------------------------------------------ #
    # Step 1: fetch + parse sitemap
    # ------------------------------------------------------------------ #

    sitemap_url = base_url.rstrip("/") + sitemap_path
    print(f"Fetching sitemap: {sitemap_url}")
    sitemap_xml = fetch(sitemap_url)
    if not sitemap_xml:
        raise RuntimeError(f"Could not fetch sitemap at {sitemap_url}")

    all_urls = parse_sitemap(sitemap_xml)
    print(f"Found {len(all_urls)} URLs in sitemap")

    # Filter to doc-like pages — skip tag pages, search, 404, assets
    skip_patterns = re.compile(
        r"/(tags?|search|404|sitemap|assets|_|static)/|"
        r"\.(xml|json|txt|png|jpg|svg|css|js)$",
        re.IGNORECASE,
    )
    page_urls = [u for u in all_urls if not skip_patterns.search(u)]
    page_urls = sorted(set(page_urls))  # deduplicate + stable order

    if max_pages > 0:
        page_urls = page_urls[:max_pages]

    print(f"Processing {len(page_urls)} doc pages (mode={mode})")

    # ------------------------------------------------------------------ #
    # Step 2: crawl pages
    # ------------------------------------------------------------------ #

    pages = []
    for i, url in enumerate(page_urls):
        html = fetch(url)
        if not html:
            continue
        page = extract_page(html, url)
        page["url"] = url
        pages.append(page)
        if (i + 1) % 20 == 0:
            print(f"  {i + 1}/{len(page_urls)} pages crawled...")
        time.sleep(0.1)  # be polite

    print(f"Successfully extracted {len(pages)} pages")

    # ------------------------------------------------------------------ #
    # Step 3: assemble llms.txt
    # ------------------------------------------------------------------ #

    header = f"# {site_title}\n\n> {site_description}\n\n"

    if mode == "curated":
        lines = [header]
        lines.append("## Pages\n")
        for p in pages:
            line = f"- [{p['title']}]({p['url']})"
            if p["description"]:
                line += f" - {p['description']}"
            lines.append(line)
        lines.append(
            f"\n---\n\nGenerated from {base_url} sitemap. "
            f"Total pages: {len(pages)}"
        )
        output = "\n".join(lines)

    else:  # full
        sep = "=" * 80
        sections = [header, sep + "\n"]
        for p in pages:
            sections.append(f"## {p['title']}")
            sections.append(f"URL: {p['url']}\n")
            if p["content"]:
                sections.append(p["content"])
            sections.append("\n" + sep + "\n")
        sections.append(
            f"\n---\n\nGenerated from {base_url} sitemap. "
            f"Total pages: {len(pages)}"
        )
        output = "\n".join(sections)

    # ------------------------------------------------------------------ #
    # Step 4: write or return
    # ------------------------------------------------------------------ #

    if output_path:
        import fused
        with fused.open(output_path, "w") as f:
            f.write(output)
        print(f"Written to {output_path}")
        return output_path
    else:
        return output
