from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient, SubscriptionClient
from azure.mgmt.rdbms.mysql import MySQLManagementClient
from azure.mgmt.rdbms.mysql.models import ServerForCreate, ServerPropertiesForDefaultCreate, ServerVersion
from azure.mgmt.monitor import MonitorManagementClient

from datetime import datetime, timedelta

# Acquire a credential object using CLI-based authentication.
credential = DefaultAzureCredential()

RESOURCE_GROUP_NAME = 'rg-test-02'
LOCATION = "westus"

# get first available subscrition (for msi we know there should be only one)
subscription_id = next(SubscriptionClient(credential).subscriptions.list()).subscription_id
resource_client = ResourceManagementClient(credential, subscription_id=subscription_id)

resource_name = "db-aftest-failover-db1"
resources = resource_client.resources.list(f"name eq '{resource_name}'")
# for r in resources:
#     print(r)

# for resource_group in resource_client.resource_groups.list():
#     print(resource_group)

# for r in resource_client.resources.list():
#     # print(r)
#     print(f"{r.name}: {r.type}")


# resource_id = (
#     "subscriptions/{}/"
#     "resourceGroups/{}/"
#     "providers/Microsoft.Compute/virtualMachines/{}"
# ).format(subscription_id, RESOURCE_GROUP_NAME, "vm-aftest-mysqlclient")

resource_id = (
    "/subscriptions/{}/"
    "resourceGroups/{}/"
    "providers/Microsoft.DBforMySQL/flexibleServers/{}"
).format(subscription_id, RESOURCE_GROUP_NAME, "db-aftest-failover-db1")

# create client
client = MonitorManagementClient(
    credential,
    subscription_id
)

# You can get the available metrics of this specific resource
# for metric in client.metric_definitions.list(resource_id):
#     # azure.monitor.models.MetricDefinition
#     print("{}: id={}, unit={}".format(
#         metric.name.localized_value,
#         metric.name.value,
#         metric.unit
#     ))

event_time_frame = datetime.now().date() - timedelta(days=7)
# print(f"resource_id: {resource_id}")
# resource_id = "/subscriptions/2edfba36-5aaa-4ec3-a8d7-59c2e7c0de5c/resourceGroups/rg-test-02/providers/Microsoft.DBforMySQL/flexibleServers/db-aftest-failover-db1"
filter = f"eventTimestamp ge '{event_time_frame}' and resourceUri eq '{resource_id}'"
select = ",".join([
    "resourceId",
    "eventTimestamp",
    "eventName",
    "operationName",
    "resourceGroupName",
])

"""
/subscriptions/2edfba36-5aaa-4ec3-a8d7-59c2e7c0de5c/
resourceGroups/rg-test-02/
providers/Microsoft.DBforMySQL/flexibleServers/
db-aftest-failover-db1
"""

for entry in client.activity_logs.list(filter, select):
    print(f"operation_name: {entry.operation_name}")
    print(f"event_name: {entry.event_name}")
    # print(f"entry: {entry}")
    exit
