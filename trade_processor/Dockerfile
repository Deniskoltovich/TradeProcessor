# Pull base image
FROM python:3.10.6

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR .

# Install dependencies
RUN apt-get update && apt-get install -y git
RUN pip install pipenv
COPY Pipfile .
COPY Pipfile.lock .
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
RUN pipenv install --system
COPY . .

# Copy pre-commit configuration
COPY .pre-commit-config.yaml .
# Set up pre-commit hooks
RUN git init && pipenv run pre-commit install

ENTRYPOINT ["./entrypoint.sh"]