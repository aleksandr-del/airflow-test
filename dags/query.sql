SELECT
    {% for department in params.departments %}
    count(DISTINCT CASE WHEN Department = '{{ department }}' THEN OrderId ELSE null END) AS {{ department}}_total_orders,
    sum(DISTINCT CASE WHEN Department = '{{ department }}' THEN Price ELSE 0 END) AS {{ department}}_total_amount{% if not loop.last %},{% endif %}
    {% endfor %}
    FROM {{ params.table_name }}
