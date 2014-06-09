DB_NAME="m_koltsov"
echo "CREATE USER 'koltsov'@'localhost' IDENTIFIED BY '1234';
CREATE DATABASE ${DB_NAME}; GRANT ALL PRIVILEGES ON ${DB_NAME}.* TO koltsov" | mysql -uroot -p1234
