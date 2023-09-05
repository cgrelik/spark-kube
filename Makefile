setup:
	helm repo add airflow-stable https://airflow-helm.github.io/charts
	helm repo add spark-operator https://googlecloudplatform.github.io/spark-on-k8s-operator
	helm repo update

build:
	docker build . --tag cgrelik/airflow_spark_demo:latest -f ./airflow.dockerfile
	docker build ./spark/ --tag cgrelik/app_spark_demo:latest -f ./spark/sparkapp.dockerfile

update:
	helm upgrade --install spark-operator spark-operator/spark-operator --values spark-values.yaml --namespace spark-demo --create-namespace
	helm upgrade --install airflow-sparkdemo airflow-stable/airflow --values airflow-values.yaml --version 8.7.1 --namespace spark-demo
	kubectl apply -f ./k8s/rbac.yaml
