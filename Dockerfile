# base image  
FROM python:3.8   
# setup environment variable  
ENV DockerHOME=/home/app/webapp \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VERSION=1.4.2 \
    YOUR_ENV=development

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/install-poetry.py | python -
ENV PATH "/root/.local/bin:$PATH"

# set work directory  
RUN mkdir -p $DockerHOME  

# Add `poetry` to PATH
ENV PATH="${PATH}:${POETRY_VENV}/bin"
# where your code lives  
WORKDIR $DockerHOME  

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

# Install pipenv and compilation dependencies
# Install dependencies
COPY poetry.lock pyproject.toml ./
RUN poetry install

# copy whole project to your docker home directory. 
COPY . $DockerHOME  

# port where the Django app runs  
EXPOSE 8000  
# start server  
CMD python manage.py runserver  