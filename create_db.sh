sudo -u postgres psql -c "create role example with login password 'example'"
sudo -u postgres psql -c "create database example owner example"