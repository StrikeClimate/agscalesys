echo "BUILD START"
python3.12 -m pip install -r requirements.txt
python3.12 manage.py migrate
python3.12 manage.py initial_data
python3.12 manage.py collectstatic --noinput --clear
echo "BUILD END"