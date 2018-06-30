CREATE SEQUENCE IF NOT EXISTS goods_id;

CREATE TABLE IF NOT EXISTS goods (
    id int primary key default nextval('goods_id'),
    name text,
    stock int
);