FROM arm32v7/python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "-m", "run.run_forever", "--conf", "/usr/src/conf" ]