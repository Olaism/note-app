#! usr/bin/sh

file=db.sqlite3

if [ -e "$file" ]; then
    # Control will enter here if file exists
    rm $file
fi

# Admin credentials
username=admin
email=admin@example.com
password=passmeby

python3 manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser(username='$username', email='$email', password='$password')" | python3 manage.py shell