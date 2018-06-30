INSERT INTO goods (
    name,
    stock
)
VALUES (
    :name,
    :stock
)
RETURNING *