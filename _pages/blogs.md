---
layout: default
title: "Blogs"
permalink: /blogs/
author_profile: true
---

# Blogs

Welcome to my technical blog. Here I share my thoughts and research on AI, Agents, and more.

<div class="entries-grid">
  {% for post in site.posts %}
    {% include archive-single.html type="grid" %}
  {% endfor %}
</div>
