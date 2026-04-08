---
layout: default
title: ""
permalink: /publications/
author_profile: true
---

{% assign pubs_by_year = site.data.publications | group_by: "year" | sort: "name" | reverse %}
{% for year_group in pubs_by_year %}
<div class="pub-year-group">
  <div class="pub-year-label" style="position: relative;">
    {{ year_group.name }}
    {% if forloop.first %}
    <span style="position: absolute; right: 0; bottom: 0.2em; font-size: 0.5em; font-weight: normal; color: #666; letter-spacing: normal;">* Equal contribution</span>
    {% endif %}
  </div>
  {% for pub in year_group.items %}
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
{% endfor %}
