CREATE SEQUENCE IF NOT EXISTS sales_id;

CREATE TABLE IF NOT EXISTS sales (
    id int primary key default nextval('goods_id'),
    good_id int references goods(id),
    quantity int,
    client_name text
);

--- Below code updates stock after new sale is created:
CREATE OR REPLACE FUNCTION update_stock_after_sale() RETURNS trigger AS $$
    BEGIN
        IF (SELECT stock FROM goods WHERE goods.id = NEW.good_id) < NEW.quantity THEN
            RAISE EXCEPTION 'out_of_stock';
        ELSE
            UPDATE goods SET stock = stock - NEW.quantity;
        END IF;
        RETURN NEW;
    END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS "update_stock_after_sale" ON sales;
CREATE TRIGGER "update_stock_after_sale" BEFORE INSERT ON sales
    FOR EACH ROW EXECUTE PROCEDURE update_stock_after_sale();