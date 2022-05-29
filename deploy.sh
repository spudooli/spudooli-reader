#!/bin/bash

echo "Copying the app..."

cp -p /home/dave/Sites/reader/reader/* /var/www/reader/reader/


echo "Deploying the static assets..."

cp -p /home/dave/Sites/reader/reader/static/* /var/www/reader/reader/static/
cp -p /home/dave/Sites/reader/reader/config.py /var/www/reader/reader/config.py

echo "Deploying the templates..."
cp -rp /home/dave/Sites/reader/reader/templates/* /var/www/reader/reader/templates/

echo "Clearing the production cache..."
rm -rf /var/www/reader/reader/__pycache__

echo "Restarting Gunicorn..."
cd /etc/systemd/system/
systemctl restart reader.spudooli.com.service

echo "Done"
