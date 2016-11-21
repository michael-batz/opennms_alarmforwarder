{% with messages = get_flashed_messages(with_categories=True) %}
    {% if messages %}
        {% for category, message in messages %}
            <div class="alert {{ category }} alert-dismissible" role="alert">
                <button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                {{ message }}
            </div>
        {% endfor %}
    {% endif %}
{% endwith %}
