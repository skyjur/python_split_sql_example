INSERT INTO sales (
    good_id,
    quantity,
    client_name
)
VALUES (
    :good_id,
    :quantity,
    :client_name
)
RETURNING *