# 베이스 이미지 설정
FROM python:3.12-slim

# 작업 디렉토리 설정 (container 안쪽)
WORKDIR /contacts

# 작업 디렉토리에 모든 파일 복사
COPY . .

# requirements.txt 복사 및 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 컨테이너가 실행할 명령
CMD ["python", "app.py"]