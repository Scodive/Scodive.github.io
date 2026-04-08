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

Hi, I am Hengle Jiang. I am a PhD student at Department of Computer Science and Engineering, Southern University of Science and Technology, supervised by [Prof. Ke Tang](https://www.sustech.edu.cn/en/faculties/tangke.html) (IEEE Fellow). I obtained my B.Eng. degree from the same department, where I was fortunate to be mentored by [Prof. Qi Hao](https://cse.sustech.edu.cn/faculty/~haoq/) and Dr. Dachuan Li. I am also a research intern at [MINSys Group](https://xmouyang.github.io/Team/) @ HKUST CSE, supervised by [Prof. Xiaomin Ouyang](https://xmouyang.github.io). 

I'm always open to collaboration! If you have any research idea or want to work together in any project, feel free to reach out — I’d love to connect (jianghl2025@mail.sustech.edu.cn, hjiangbg@connect.ust.hk).

# Research Interest
My research focuses on building Safe, Robust, and Reliable autonomy systems that can operate effectively in complex, real-world environments. I focus on:

- Agent Safety & Evaluation: Investigating "Agentic Pressure" to understand and mitigate safety risks and "normative drift" in LLM-based autonomous agents.

- Embodied Robustness & Uncertainty: Developing uncertainty quantification for VLMs Autonomous Driving and view-invariant 3D Human Pose Estimation to ensure reliable perception in the wild.




# News
<ul>
{% for item in site.data.news limit:6 %}
  <li style="margin-bottom: 0.5em;">
    <em>{{ item.date }}</em>: {{ item.content }}
    {% if item.papers %}
    <ul style="list-style-type: circle; padding-left: 7.9em; margin-left: 0em; margin-bottom: 0; margin-top: 0.2em; font-size: 0.95em; color: #00369f;">
      {% for paper in item.papers %}
      <li>{{ paper }}</li>
      {% endfor %}
    </ul>
    {% endif %}
  </li>
{% endfor %}
</ul>

{% if site.data.news.size > 6 %}
<details class="news-details">
<summary>Show older news</summary>
<div class="news-hidden">
  <ul>
  {% for item in site.data.news offset:6 %}
    <li style="margin-bottom: 0.5em;">
      <em>{{ item.date }}</em>: {{ item.content }}
      {% if item.papers %}
      <ul style="list-style-type: circle; padding-left: 1.5em; margin-left: 3.7em; margin-bottom: 0; margin-top: 0.2em; font-size: 0.95em; color: #00369f;">
        {% for paper in item.papers %}
        <li>{{ paper }}</li>
        {% endfor %}
      </ul>
      {% endif %}
    </li>
  {% endfor %}
  </ul>
</div>
</details>
{% endif %}

<!-- # 🎖 Honors and Awards -->



# Educations
- *2025.09 - now*, Doctor of Philosophy, Computer Science and Technology, SUSTech.
- *2021.09 - 2025.06*, Bachelor of Engineering, Computer Science and Technology, SUSTech.


# Internships
- *2024.08 - now*, [MINSys Group](https://xmouyang.github.io/Team/) @ HKUST CSE, Hong Kong SAR, China.
- *2022.06 - 2023.04*, SZ DJI Technology Co.,Ltd.


# Teaching
- 2026 Spring, CS311H: Artificial Intelligence (Honor Track), SUSTech, Teaching Assistant
- 2025 Fall, CS112: Introduction to Python Programming, SUSTech, Teaching Assistant

# Services
- ICLR 2026 Workshop Reliable Autonomy, Reviewer

<h1 id="selected-publications" style="position: relative;">
  Selected Publications
  <span style="position: absolute; right: 0; bottom: 0.2em; font-size: 0.5em; font-weight: normal; color: #666; letter-spacing: normal;">* Equal contribution</span>
</h1>

{% assign selected_pubs = site.data.publications | where: "selected", true %}
<div class="pub-year-group">
  {% for pub in selected_pubs %}
  <div class="pub-card">
    <div class="pub-card-image">
      {% if pub.image %}
        <img src="{{ pub.image }}" alt="{{ pub.title }}">
      {% else %}
        <span class="pub-no-image">📄</span>
      {% endif %}
    </div>
    <div class="pub-card-body">
      <div class="pub-card-title">
        {% if pub.paper and pub.paper != "#" %}
          <a href="{{ pub.paper }}" target="_blank">{{ pub.title }}</a>
        {% else %}
          {{ pub.title }}
        {% endif %}
      </div>
      <div>
        <span class="pub-card-venue">{{ pub.venue_short }}</span>
        <span class="pub-card-venue-full">{{ pub.venue }}</span>
      </div>
      <div class="pub-card-authors">{{ pub.authors }}</div>
      {% if pub.abstract %}
      <div class="pub-card-abstract">{{ pub.abstract }}</div>
      {% endif %}
      <div class="pub-card-links">
        {% if pub.paper %}<a href="{{ pub.paper }}" class="pub-link-paper" target="_blank"><i class="fas fa-file-pdf"></i> Paper</a>{% endif %}
        {% if pub.code %}<a href="{{ pub.code }}" class="pub-link-code" target="_blank"><i class="fab fa-github"></i> Code</a>{% endif %}
        {% if pub.project %}<a href="{{ pub.project }}" class="pub-link-project" target="_blank"><i class="fas fa-globe"></i> Project</a>{% endif %}
        {% if pub.video %}<a href="{{ pub.video }}" class="pub-link-video" target="_blank"><i class="fab fa-youtube"></i> Video</a>{% endif %}
      </div>
    </div>
  </div>
  {% endfor %}
</div>

<div style="margin-top: -1em; margin-bottom: 2em; text-align: left;">
  <a href="/publications/" style="font-weight: bold; text-decoration: underline;">See all publications &rarr;</a>
</div>