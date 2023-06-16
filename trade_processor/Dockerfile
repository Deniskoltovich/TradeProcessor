# Pull base image
FROM python:3.10.6

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR .

# Install dependencies
RUN pip install pipenv
COPY Pipfile .
COPY Pipfile.lock .
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
RUN pipenv install --system
COPY . .
ENTRYPOINT ["./entrypoint.sh"]