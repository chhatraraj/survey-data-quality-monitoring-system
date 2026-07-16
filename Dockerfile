FROM python:3.12-slim

# ----------------------------------------
# Python Configuration
# ----------------------------------------

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ----------------------------------------
# Working Directory
# ----------------------------------------

WORKDIR /app

# ----------------------------------------
# Install Dependencies
# ----------------------------------------

COPY requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ----------------------------------------
# Copy Application
# ----------------------------------------

COPY . .

# ----------------------------------------
# Default Command
# ----------------------------------------

CMD ["python", "-m", "src.main"]