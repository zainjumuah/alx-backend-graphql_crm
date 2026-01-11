#!/usr/bin/env python3

from datetime import datetime, timedelta
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# GraphQL endpoint
GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"

# Setup GraphQL client
transport = RequestsHTTPTransport(
    url=GRAPHQL_ENDPOINT,
    verify=True,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=False)

# Calculate date range (last 7 days)
seven_days_ago = (datetime.utcnow() - timedelta(days=7)).isoformat()

# GraphQL query
query = gql("""
query GetRecentOrders($date: DateTime!) {
  orders(orderDate_Gte: $date) {
    id
    customer {
      email
    }
  }
}
""")

# Execute query
result = client.execute(query, variable_values={"date": seven_days_ago})

# Log file
log_file = "/tmp/order_reminders_log.txt"
timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

with open(log_file, "a") as f:
    for order in result.get("orders", []):
        f.write(
            f"{timestamp} - Order ID: {order['id']}, Customer Email: {order['customer']['email']}\n"
        )

print("Order reminders processed!")
