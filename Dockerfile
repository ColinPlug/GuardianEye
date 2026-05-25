FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p data/satellietbeelden \
    data/satellietbeelden_test \
    data/satellietbeelden_test_pool \
    data/satelliet_payload/afbeeldingen \ 
    data/satelliet_payload/metadata \
    data/inspectie_beelden \ 
    visuals

RUN chmod +x menu.sh

ENV YOLO_CONFIG_DIR=/tmp/Ultralytics

CMD ["./menu.sh"]