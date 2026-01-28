---
layout: default
title: "Blogs"
permalink: /blogs/
author_profile: true
---

# Blogs

Welcome to my technical blog. Here I share my thoughts and research on AI, Agents, and more.

{% for post in site.posts %}
## [{{ post.title }}]({{ post.url }})
*Published on {{ post.date | date: "%B %d, %Y" }}*

{{ post.excerpt | strip_html | truncatewords: 50 }}

---
{% endfor %}
