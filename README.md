# arjahck.github.io

The source of https://arjahck.github.io/, built by GitHub Pages (Jekyll). The home page lists every post in
`_posts/`, newest first.

**A new post:** add `_posts/YYYY-MM-DD-short-name.md` and push. It appears at `/YYYY/MM/DD/short-name/`.

```markdown
---
layout: post
title: The post title
description: One or two sentences for the list on the home page.
---

The text, in Markdown. Images go in `images/` and are linked as `![alt text](/images/name.png)`.
```

**A post that lives in another repository** (like the TSFM post): `layout: redirect` and
`external_url: /<repo-name>/` in the front matter, and no text. The home page links straight to it.
