#!/bin/bash

# Absolute path to project
PROJECT_DIR="/path/to/my/project"
PYTHON_BIN="$PROJECT_DIR/venv/bin/python"
MANAGE_PY="$PROJECT_DIR/manage.py"

# Timestamp
TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

# Run Django shell command
DELETED_COUNT=$(
  $PYTHON_BIN $MANAGE_PY shell -c "
from datetime import timedelta
from django.utils import timezone
from crm.models import Customer

one_year_ago = timezone.now() - timedelta(days=365)

qs = Customer.objects.filter(
    orders__isnull=True,
    created_at__lt=one_year_ago
)

count = qs.count()
qs.delete()
print(count)
"
)

# Log result
echo "$TIMESTAMP - Deleted $DELETED_COUNT inactive customers" >> /tmp/customer_cleanup_log.txt
