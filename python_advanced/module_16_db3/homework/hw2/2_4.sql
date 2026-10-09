SELECT
    c.full_name AS "покупатель",
    o.order_no AS "номер_заказа"
FROM 'order' o
JOIN 'customer' c ON o.customer_id = c.customer_id
WHERE o.manager_id IS NULL
ORDER BY o.order_no;