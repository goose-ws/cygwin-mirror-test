FROM python:3.14-alpine

# Prevent Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1
# Ensure stdout/stderr are flushed immediately (crucial for progress bars)
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

COPY cygwin_mirror_test.py .

RUN chmod +x cygwin_mirror_test.py

ENTRYPOINT ["python", "./cygwin_mirror_test.py"]

# Default arguments
CMD ["--workers", "20"]