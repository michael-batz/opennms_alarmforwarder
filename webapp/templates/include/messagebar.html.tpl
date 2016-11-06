{% with messages = get_flashed_messages(with_categories=True) %}
    {% if messages %}
        {% for category, message in messages %}
            <div class="alert {{ category }}">{{ message }}</div>
        {% endfor %}
    {% endif %}
{% endwith %}
