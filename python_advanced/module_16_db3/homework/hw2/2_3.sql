SELECT
    o.order_no AS "номер_заказа",
    m.full_name AS "продавец",
    c.full_name AS "покупатель"
FROM 'order' o
JOIN 'customer' c ON o.customer_id = c.customer_id
JOIN 'manager' m ON o.manager_id = m.manager_id
WHERE c.city != m.city
ORDER BY o.order_no;