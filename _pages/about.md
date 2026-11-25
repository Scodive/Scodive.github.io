---
permalink: /
title: ""
excerpt: ""
author_profile: true
redirect_from: 
  - /about/
  - /about.html
---

{% if site.google_scholar_stats_use_cdn %}
{% assign gsDataBaseUrl = "https://cdn.jsdelivr.net/gh/" | append: site.repository | append: "@" %}
{% else %}
{% assign gsDataBaseUrl = "https://raw.githubusercontent.com/" | append: site.repository | append: "/" %}
{% endif %}
{% assign url = gsDataBaseUrl | append: "google-scholar-stats/gs_data_shieldsio.json" %}

<span class='anchor' id='about-me'></span>

<div class="home-page">
  <section class="home-bio">
    <p>Hi, I am Hengle Jiang. I am a PhD student at Department of Computer Science and Engineering, Southern University of Science and Technology, supervised by <a href="https://www.sustech.edu.cn/en/faculties/tangke.html">Prof. Ke Tang</a> (IEEE Fellow). I obtained my B.Eng. degree from the same department, where I was fortunate to be mentored by <a href="https://cse.sustech.edu.cn/faculty/~haoq/">Prof. Qi Hao</a> and <a href="https://scholar.google.com/citations?user=sCANNvMAAAAJ&hl=en">Prof. Dachuan Li</a>. I am also a research intern at <a href="https://xmouyang.github.io/Team/">MINSys Group</a> @ HKUST CSE, supervised by <a href="https://xmouyang.github.io">Prof. Xiaomin Ouyang</a>.</p>
    <p>I am always open to research collaborations. Feel free to reach out via <a href="mailto:jianghl2025@mail.sustech.edu.cn">email</a> or view my work on <a href="https://scholar.google.com/citations?user=VhsLK-gAAAAJ&hl=zh-TW">Google Scholar</a>.</p>
  </section>

  <section class="home-section">
    <h2 class="home-section__title" id="research-interests">Research Interests</h2>
    <p>My research focuses on building <strong>Safe, Robust, and Reliable autonomy systems</strong> that can operate effectively in complex, real-world environments.</p>
    <ul class="home-interests">
      <li><strong>Agent Safety</strong>: We investigate a new type of safety for LLM-based autonomous agents under non-adversarial settings. We introduce the concept of Agentic Pressure [<a href="https://arxiv.org/pdf/2609.05995">ICLR'26</a>, <a href="https://arxiv.org/pdf/2603.14975">ACL'26</a>] and find that agents sacrifice safety constraints to achieve task goals when placed under realistic operational pressure without any adversarial inputs. This work helps to bridge the gap between static benchmarks and dynamic real-world environments.</li>
      <li><strong>Agent Evaluation</strong>: We develop fine-grained, diagnostic assessment frameworks to better understand and quantify agent capabilities. MOAE is a self-evolving method that jointly optimizes agents for multiple objectives.</li>
    </ul>
  </section>

  <section class="home-section">
    <h2 class="home-section__title" id="news">News</h2>
    <ul class="home-timeline home-timeline--news">
      {% for item in site.data.news limit:6 %}
      <li>
        <span class="home-timeline__date">{{ item.date }}</span>
        <div class="home-timeline__body">
          <span class="home-timeline__text">{{ item.content }}</span>
          {% if item.papers %}
          <ul class="home-news-links">
            {% for paper in item.papers %}
            {% assign linked_pub = site.data.publications | where: "title", paper | first %}
            {% assign linked_post = site.posts | where: "title", paper | first %}
            <li>{% if linked_pub.paper %}<a href="{{ linked_pub.paper }}" target="_blank" rel="noopener">{{ paper }}</a>{% elsif linked_post %}<a href="{{ linked_post.url | relative_url }}">{{ paper }}</a>{% else %}{{ paper }}{% endif %}</li>
            {% endfor %}
          </ul>
          {% endif %}
        </div>
      </li>
      {% endfor %}
    </ul>

    {% if site.data.news.size > 6 %}
    <details class="news-details">
      <summary>Show older news</summary>
      <div class="news-hidden">
        <ul class="home-timeline home-timeline--news">
          {% for item in site.data.news offset:6 %}
          <li>
            <span class="home-timeline__date">{{ item.date }}</span>
            <div class="home-timeline__body">
              <span class="home-timeline__text">{{ item.content }}</span>
              {% if item.papers %}
              <ul class="home-news-links">
                {% for paper in item.papers %}
                {% assign linked_pub = site.data.publications | where: "title", paper | first %}
                {% assign linked_post = site.posts | where: "title", paper | first %}
                <li>{% if linked_pub.paper %}<a href="{{ linked_pub.paper }}" target="_blank" rel="noopener">{{ paper }}</a>{% elsif linked_post %}<a href="{{ linked_post.url | relative_url }}">{{ paper }}</a>{% else %}{{ paper }}{% endif %}</li>
                {% endfor %}
              </ul>
              {% endif %}
            </div>
          </li>
          {% endfor %}
        </ul>
      </div>
    </details>
    {% endif %}
  </section>

  <section class="home-section">
    <div class="home-section-head" id="selected-publications">
      <h2 class="home-section__title">Selected Publications</h2>
      <span class="home-section__note">* Equal contribution</span>
    </div>

    {% assign selected_pubs = site.data.publications | where: "selected", true %}
    <div class="pub-ledger pub-ledger--home">
      {% for pub in selected_pubs %}
        {% include pub-entry.html pub=pub heading_tag="h3" %}
      {% endfor %}
    </div>

    <div class="pub-home-more">
      <a href="/publications/">See all publications &rarr;</a>
    </div>
  </section>

  <section class="home-section">
    <h2 class="home-section__title" id="education">Education</h2>
    <ul class="home-timeline">
      <li>
        <span class="home-timeline__date">2025.09 – now</span>
        <div class="home-timeline__body">Doctor of Philosophy, Computer Science and Technology, SUSTech.</div>
      </li>
      <li>
        <span class="home-timeline__date">2021.09 – 2025.06</span>
        <div class="home-timeline__body">Bachelor of Engineering, Computer Science and Technology, SUSTech.</div>
      </li>
    </ul>
  </section>

  <section class="home-section">
    <h2 class="home-section__title" id="internships">Internships</h2>
    <ul class="home-timeline">
      <li>
        <span class="home-timeline__date">2024.08 – now</span>
        <div class="home-timeline__body"><a href="https://xmouyang.github.io/Team/">MINSys Group</a> @ HKUST CSE, Hong Kong SAR, China.</div>
      </li>
      <li>
        <span class="home-timeline__date">2022.06 – 2023.04</span>
        <div class="home-timeline__body">SZ DJI Technology Co.,Ltd.</div>
      </li>
    </ul>
  </section>

  <section class="home-section">
    <h2 class="home-section__title" id="teaching">Teaching</h2>
    <ul class="home-timeline">
      <li>
        <span class="home-timeline__date">2026 Spring</span>
        <div class="home-timeline__body">CS311H: Artificial Intelligence (Honor Track), SUSTech, Teaching Assistant</div>
      </li>
      <li>
        <span class="home-timeline__date">2025 Fall</span>
        <div class="home-timeline__body">CS112: Introduction to Python Programming, SUSTech, Teaching Assistant</div>
      </li>
    </ul>
  </section>

  <section class="home-section">
    <h2 class="home-section__title" id="services">Services</h2>
    <ul class="home-timeline">
      <li>
        <span class="home-timeline__date">2026</span>
        <div class="home-timeline__body">ICLR 2026 Workshop Reliable Autonomy, Reviewer</div>
      </li>
    </ul>
  </section>
</div>
