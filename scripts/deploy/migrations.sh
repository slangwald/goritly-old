cd ../../

DBS="website_1 website_2"
for DB in $DBS 
do
	python manage.py migrate utils --database=$DB
done
