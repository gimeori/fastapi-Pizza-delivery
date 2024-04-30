FROM python:3.12
RUN mkdir /pizza_app
WORKDIR /pizza_app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
WORKDIR /pizza_app
