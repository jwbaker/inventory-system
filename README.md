# inventory-system
A Django-based inventory system. Developed for the University of Waterloo Department of Mechanical Engineering, in collaboration with Science Computing

## Installing on a new machine:

1. Install Python 2.7.9, [virtualenv](https://virtualenv.pypa.io/en/latest/), and [pip](https://pip.pypa.io/en/latest/index.html)
2. Create and activate a virtual environment
2. Install packages using `requirements/base.txt`:  
  `pip install -r requirements/base.txt`
3. The django_case module may need to be installed manually. If so, the code and installation instructions can be found [here](https://bitbucket.org/amjoconn/django-cas)
4. Copy `local_settings.template` to `local_settings.py`
5. Add a value to the `SECRET_KEY` setting in `local_settings.py`:  
  1. In the terminal, run the following command:  
     `python -c 'import random; import string; print "".join([random.SystemRandom().choice(string.digits + string.letters + "!$&()*+,-./:;<=>?@[]^_{|}~") for i in range(100)])'`
  2. Copy and paste the output into `local_settings.py`, in-between the quotation marks following `SECRET_KEY`
6. Run migrations. From the project root directory:  
   `python manage.py migrate`
7. Load initial authentication data. From the project root directory:  
   `python manage.py loaddata fixtures/initial_auth.json`
