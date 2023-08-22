# Knife Detection Model Training
Model - MobileNetV2-ATSS

## 전제 조건
```
Ubuntu 22.04 LTS
Python3.10.12
```
## 설치

#### Dataset 준비
```
1. 데이터셋 이미지 사진 촬영
2. cvat으로 annotation 만들기
3. Export annotation 
```

#### 패키지 설치
```
$ python3 -m venv .env
$ source .env/bin/activate
$ pip install -U pip
$ pip install -r requirements.txt
```
## Training

#### build
```
$ otx build --train-data-roots <DATASET_PATH>/ --model MobileNetV2-ATSS --workspace knife-detection
```

#### train
```
$ cd knife-detection
$ otx train params --learning_parameters.batch_size 2 --learning_parameters.num_iters 10
```

#### export
```
$ otx export
```

#### deploy
```
$ otx deploy --load-weights <XML_PATH>/openvino.xml 
```



