FROM python:3.9

WORKDIR /usr/app/src
COPY . ./
RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "./pytestsimple/main.py"]
