FROM python:3.10.0

# 작업 디렉토리 설정
WORKDIR /dcz

# 의존성 파일 복사 및 설치
COPY ./requirements.txt /dcz/requirements.txt
RUN pip install --no-cache-dir -r /dcz/requirements.txt

# python-dotenv 추가 설치
RUN pip install python-dotenv

# 프로젝트 파일 복사
COPY . /dcz/

# 포트 노출
EXPOSE 80

# 애플리케이션 실행 커맨드
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]