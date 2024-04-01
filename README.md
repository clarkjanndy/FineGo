### Follow these following steps to run the system on your local machine.

1.  Clone this repository.
  ```
  git clone https://github.com/clarkjanndy/IBuy.git
  ```

2. Create python virtual enviroment.
  ```
  python -m venv .env
  ```
> **_NOTE:_**  Make sure you are on the root folder of the project.

3. Activate python environment.
  ```
  source .env/Scripts/activate
  ```

4. Install requirements.
 ```
 pip install -r requirements.txt
 ```

5. Migrate database.
 ```
 python manage.py migrate
 ```

6. Load fixtures.
 ```
 python manage.py loaddata fixtures/initial.json
 ```

7. Run Webserver.
 ```
 python manage.py runserver
 ```

8. Run Background tasks by opening a new terminal.
 ```
 source .env/Scripts/activate
 ```
 ```
  python manage.py process_tasks
 ```

You can now visit the running website via [http:localhost:8000](http:localhost:8000). Default username is 'admin@gmail.com', default pasword is 'admin'.
You can also visit the Django Admin Site via [http:localhost:8000/database](http:localhost:8000/django-admin)

