FROM apache/spark-py

WORKDIR /opt/spark-demo/
COPY app.py /opt/spark-demo/
COPY games.csv /opt/spark-demo/
