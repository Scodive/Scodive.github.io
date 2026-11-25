---
layout: default
title: "Publications"
permalink: /publications/
author_profile: true
---

<div class="pub-index">
  <header class="pub-index__header">
    <h1 class="pub-index__title">Publications</h1>
    <span class="pub-index__note">* Equal contribution</span>
  </header>

  {% assign pubs_by_year = site.data.publications | group_by: "year" | sort: "name" | reverse %}
  {% for year_group in pubs_by_year %}
  <section class="pub-year-group">
    <h2 class="pub-year-label">{{ year_group.name }}</h2>
    <div class="pub-ledger">
      {% for pub in year_group.items %}
        {% include pub-entry.html pub=pub heading_tag="h3" %}
      {% endfor %}
    </div>
  </section>
  {% endfor %}
</div>
