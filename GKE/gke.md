## コンテナイメージをGCRにPUSH

```
gcloud services enable containerregistry.googleapis.com
gcloud auth configure-docker
docker push gcr.io/${PROJECT_ID}/${IMAGE_NAME}:v1
```

## GKEクラスタ作成

```
# クラスタを作成
gcloud container clusters create ${CLUSTER_NAME} --num-nodes 1

# VMインスタンスを確認
gcloud compute instances list
```

## デプロイ
k8sではアプリケーションをPodで表す。  
Podはk8sでデプロイ可能な最小単位  

クラスタでアプリケーションを実行するためのDeploymentを作成する。  
Deployment Pod1つに対して１つのコンテナ  

```
# APP_NAME DockerイメージのDeploymentを作成する
kubectl create deployment ${APP_NAME} --image=gcr.io/${PROJECT_ID}/${IMAGE_NAME}:v1
# レプリカのベースラインを指定
kubectl scale deployment ${APP_NAME} --replicas=1
# 作成したPodを出力
kubectl get pods
```

## インターネット公開

```
# APP_NAMEデプロイ用のk8s Serviceを生成
kubectl expose deployment ${APP_NAME} --name=${APP_SERVICE_NAME} --type=LoadBalancer --port 80 --target-port 8080

# APP_SERVICE_NAMEのService詳細を取得 -> External_IPアドレスを確認
kubectl get service
```

## アプリケーション APP_NAMEの新しいバージョンをデプロイ

```
docker build -t gcr.io/${PROJECT_ID}/${APP_NAME}:v2 .
docker push gcr.io/${PROJECT_ID}/${APP_NAME}:v2
```

```
kubectl set image deployment/${APP_NAME} ${APP_NAME}=gcr.io/${PROJECT_ID}/${IMAGE_NAME}:v2
watch kubectl get pods
```