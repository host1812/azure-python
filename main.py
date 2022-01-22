from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient, SubscriptionClient
from azure.mgmt.rdbms.mysql import MySQLManagementClient
from azure.mgmt.rdbms.mysql.models import ServerForCreate, ServerPropertiesForDefaultCreate, ServerVersion


# Acquire a credential object using CLI-based authentication.
credential = DefaultAzureCredential()

RESOURCE_GROUP_NAME = 'rg-aftest-02'
LOCATION = "westus"

# get first available subscrition (for msi we know there should be only one)
subscription = next(SubscriptionClient(credential).subscriptions.list())
resource_client = ResourceManagementClient(credential, subscription_id=subscription.subscription_id)

for r in resource_client.resources.list():
    print(f"{r.name}: {r.type}")
