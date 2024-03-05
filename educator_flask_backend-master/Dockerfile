FROM python:3.9

ENV FLASK_APP api.py
ENV azure_region replace

ENV azure_subscription replace
ENV openai_api_key replace

RUN mkdir -p /app/src
WORKDIR /app/src
COPY . .
RUN bash aeneas_dependencies.sh
RUN pip install numpy; pip install aeneas
RUN pip install sentence-transformers; pip install -r requirements.txt
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]