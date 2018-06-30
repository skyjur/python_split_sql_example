SELECT goods.id, goods.name, sum(sales.quantity) as total_sales_quantity
FROM goods LEFT JOIN sales ON
    goods.id = sales.good_id
GROUP BY
    goods.id, goods.name
ORDER BY
    goods.name;