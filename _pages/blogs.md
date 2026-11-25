---
layout: default
title: "Blogs"
permalink: /blogs/
author_profile: true
---

{% assign lead_post = site.posts | first %}
{% assign lead_excerpt_en = lead_post.excerpt | remove: " English / 中文." | strip_html | normalize_whitespace %}
{% assign lead_excerpt_zh = lead_post.excerpt_zh | default: lead_excerpt_en | strip_html | normalize_whitespace %}

<div class="blog-index" id="blog-index" lang="en">
  <header class="blog-index__header">
    <div class="blog-index__header-text">
      <h1 class="blog-index__title" data-en="Blogs" data-zh="博客">Blogs</h1>
      <p class="blog-index__intro" data-en="Research essays on LLM agents, evaluation design, and model migration." data-zh="关于 LLM Agent、评测设计与模型迁移的研究随笔。">Research essays on LLM agents, evaluation design, and model migration.</p>
    </div>
    <div class="blog-lang-toggle" role="tablist" aria-label="Blog language">
      <button type="button" role="tab" data-blog-lang="en" aria-selected="true" aria-pressed="true" lang="en">English</button>
      <button type="button" role="tab" data-blog-lang="zh" aria-selected="false" aria-pressed="false" lang="zh-CN">中文</button>
    </div>
  </header>

  {% if lead_post %}
  <article class="blog-lead" itemscope itemtype="http://schema.org/CreativeWork">
    <div class="blog-lead__body">
      <h2 class="blog-lead__title" itemprop="headline">
        <a href="{{ lead_post.url | relative_url }}"
           data-href-en="{{ lead_post.url | relative_url }}"
           data-href-zh="{{ lead_post.url | relative_url }}#bm-content-zh"
           data-en="{{ lead_post.title | escape }}"
           data-zh="{{ lead_post.title_zh | default: lead_post.title | escape }}"
           rel="permalink">{{ lead_post.title }}</a>
      </h2>
      <p class="blog-lead__excerpt" itemprop="description"
         data-en="{{ lead_excerpt_en | escape }}"
         data-zh="{{ lead_excerpt_zh | escape }}">{{ lead_excerpt_en }}</p>
      <p class="blog-entry__meta"
         data-en="{{ lead_post.date | date: '%B %-d, %Y' }}{% if lead_post.topic %} · {{ lead_post.topic }}{% endif %}{% if lead_post.reading_time %} · {{ lead_post.reading_time }}{% endif %}"
         data-zh="{{ lead_post.date | date: '%Y 年 %-m 月 %-d 日' }}{% if lead_post.topic_zh %} · {{ lead_post.topic_zh }}{% endif %}{% if lead_post.reading_time_zh %} · {{ lead_post.reading_time_zh }}{% endif %}">
        {{ lead_post.date | date: "%B %-d, %Y" }}{% if lead_post.topic %} · {{ lead_post.topic }}{% endif %}{% if lead_post.reading_time %} · {{ lead_post.reading_time }}{% endif %}
      </p>
      <a class="blog-lead__cta"
         href="{{ lead_post.url | relative_url }}"
         data-href-en="{{ lead_post.url | relative_url }}"
         data-href-zh="{{ lead_post.url | relative_url }}#bm-content-zh">
        <span data-en="Read essay" data-zh="阅读全文">Read essay</span>
        <svg class="blog-arrow" width="16" height="16" viewBox="0 0 16 16" fill="none" aria-hidden="true">
          <path d="M3.5 8H12.5M12.5 8L8.5 4M12.5 8L8.5 12" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
      </a>
    </div>
    {% if lead_post.figure_en %}
    <a class="blog-figure-frame"
       href="{{ lead_post.url | relative_url }}"
       data-href-en="{{ lead_post.url | relative_url }}"
       data-href-zh="{{ lead_post.url | relative_url }}#bm-content-zh"
       aria-label="{{ lead_post.title | escape }}">
      <img src="{{ lead_post.figure_en | relative_url }}"
           data-src-en="{{ lead_post.figure_en | relative_url }}"
           data-src-zh="{{ lead_post.figure_zh | default: lead_post.figure_en | relative_url }}"
           data-alt-en="{{ lead_post.figure_alt_en | default: lead_post.title | escape }}"
           data-alt-zh="{{ lead_post.figure_alt_zh | default: lead_post.title_zh | escape }}"
           alt="{{ lead_post.figure_alt_en | default: lead_post.title | escape }}">
    </a>
    {% endif %}
  </article>
  {% endif %}

  <div class="blog-ledger">
    {% for post in site.posts offset:1 %}
    {% assign row_excerpt_en = post.excerpt | remove: " English / 中文." | strip_html | normalize_whitespace %}
    {% assign row_excerpt_zh = post.excerpt_zh | default: row_excerpt_en | strip_html | normalize_whitespace %}
    <article class="blog-row{% unless post.figure_en %} blog-row--text-only{% endunless %}" itemscope itemtype="http://schema.org/CreativeWork">
      <div class="blog-row__body">
        <h2 class="blog-row__title" itemprop="headline">
          <a href="{{ post.url | relative_url }}"
             data-href-en="{{ post.url | relative_url }}"
             data-href-zh="{{ post.url | relative_url }}#bm-content-zh"
             data-en="{{ post.title | escape }}"
             data-zh="{{ post.title_zh | default: post.title | escape }}"
             rel="permalink">{{ post.title }}</a>
        </h2>
        <p class="blog-row__excerpt" itemprop="description"
           data-en="{{ row_excerpt_en | escape }}"
           data-zh="{{ row_excerpt_zh | escape }}">{{ row_excerpt_en }}</p>
        <p class="blog-entry__meta"
           data-en="{{ post.date | date: '%B %-d, %Y' }}{% if post.topic %} · {{ post.topic }}{% endif %}{% if post.reading_time %} · {{ post.reading_time }}{% endif %}"
           data-zh="{{ post.date | date: '%Y 年 %-m 月 %-d 日' }}{% if post.topic_zh %} · {{ post.topic_zh }}{% endif %}{% if post.reading_time_zh %} · {{ post.reading_time_zh }}{% endif %}">
          {{ post.date | date: "%B %-d, %Y" }}{% if post.topic %} · {{ post.topic }}{% endif %}{% if post.reading_time %} · {{ post.reading_time }}{% endif %}
        </p>
      </div>
      {% if post.figure_en %}
      <a class="blog-figure-frame blog-figure-frame--compact"
         href="{{ post.url | relative_url }}"
         data-href-en="{{ post.url | relative_url }}"
         data-href-zh="{{ post.url | relative_url }}#bm-content-zh"
         aria-label="{{ post.title | escape }}">
        <img loading="lazy"
             src="{{ post.figure_en | relative_url }}"
             data-src-en="{{ post.figure_en | relative_url }}"
             data-src-zh="{{ post.figure_zh | default: post.figure_en | relative_url }}"
             data-alt-en="{{ post.figure_alt_en | default: post.title | escape }}"
             data-alt-zh="{{ post.figure_alt_zh | default: post.title_zh | escape }}"
             alt="{{ post.figure_alt_en | default: post.title | escape }}">
      </a>
      {% endif %}
    </article>
    {% endfor %}
  </div>
</div>

<script src="{{ '/assets/js/blog-index.js' | relative_url }}" defer></script>
