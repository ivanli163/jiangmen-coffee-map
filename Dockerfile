FROM python:3.9-slim

WORKDIR /app

# Copy server requirements
COPY server/requirements.txt ./server/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r server/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# Copy everything
COPY . .

# Expose port
ENV PORT=80
EXPOSE 80

# Run gunicorn
# Note: we are in /app. app.py is in server/.
# So module is server.app:app
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 server.app:app