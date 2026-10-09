SELECT
    c.full_name AS "имя_покупателя",
    m.full_name AS "имя_продавца",
    o.purchase_amount AS "сумма",
    o.date AS "дата"
FROM 'order' o
JOIN 'customer' c ON o.customer_id = c.customer_id
LEFT JOIN 'manager' m ON o.manager_id = m.manager_id
ORDER BY o.date, o.order_no;