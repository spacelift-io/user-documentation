# ServiceNow

{% if is_saas() %}
!!! Info
    This feature is only available to Enterprise plan. Please check out our [pricing page](https://spacelift.io/pricing){: rel="nofollow"} for more information.
{% endif %}

## About the integration

The ServiceNow integration with Spacelift enables seamless automation and management of infrastructure as code by leveraging ServiceNow's service catalog capabilities.
By integrating Spacelift [Blueprints](../../concepts/blueprint/README.md) with ServiceNow,
users can create service catalog items that facilitate the provisioning of Spacelift [stacks](../../concepts/stack/README.md) directly from ServiceNow.

## Setup Guide

### Setup a User in ServiceNow

To enable Spacelift to create resources on the ServiceNow side, you need to set up a dedicated user account. Follow these steps:

1. Navigate to **System Security > Users and Groups > Users**.
2. Click on **New** to create a new user.
3. Fill out the form. The only required field is the **User ID**. Once completed, click **Submit**.
4. Go to the details of the newly created user and generate a password. You can uncheck the **Password needs reset** option in the user details or go through the reset flow.
5. Navigate to the **Roles** tab and add the following roles:
    - `web_service_admin`: Allows the creation of "REST Message".
    - `business_rule_admin`: Allows the creation of "Business Rule".
    - `catalog_admin`: Allows the creation of "Catalog Item".
6. Save the changes.

### Create Integration in Spacelift

To create an integration with ServiceNow in Spacelift, follow these steps:

1. Navigate to **ServiceNow Integration > Create Integration**.

    ![Creating the ServiceNow integration.](<../../assets/screenshots/external-integration/create_integration_step_1.png>)

2. Fill in the details in the form:
    - **Name of the Integration**: Provide a name for the integration.
    - **Space**: Select the space where the integration will be created. This will determine which blueprints can be attached to this integration.
    - **Description**: Optionally, provide a description for the integration.
    - **Integration Base URL**: Enter the base URL of your ServiceNow instance, e.g., `https://{id}.service-now.com`.
    - **Username**: Enter the username for the account created in [the previous step](#setup-a-user-in-servicenow).
    - **Password**: Enter the password for the account created in [the previous step](#setup-a-user-in-servicenow).
3. Click **Create** to finalize the integration setup.

    ![Creating the ServiceNow integration.](<../../assets/screenshots/external-integration/create_integration_step_2.png>)

After completing these steps, Spacelift will create a "REST Message" on the ServiceNow side (found under **System Web Services > Outbound > REST Message**) with the authorization details, which will be used for authentication in Spacelift.

### Attaching Integration to Blueprint

The integration itself does not perform any actions until it is explicitly attached to a blueprint. To create a service catalog item, follow these steps:

1. Navigate to **Blueprints**.
2. Select the blueprint you want to use to create a service catalog item.
3. Go to the **Integrations** tab.

    ![Attaching integration to blueprint.](<../../assets/screenshots/external-integration/attach_integration_step_1.png>)

4. Click **Attach Integration**.
5. Select the integration created in [the previous step](#create-integration-in-spacelift).
6. Click **Attach**.

    ![Attaching integration to blueprint.](<../../assets/screenshots/external-integration/attach_integration_step_2.png>)

After completing these steps, Spacelift will create the following resources on the ServiceNow side:

- **Service Catalog Item**: Found under **Service Catalog > Catalog Definition > Maintain Items**, along with variables that need to be passed to the blueprint to create a stack.
- **Business Rule**: Found under **System Definition > Business Rules**, with a custom script that transforms ServiceNow variables into blueprint input and calls the Spacelift API to create a stack based on the blueprint.

Feel free to adjust any of these resources to suit your needs.

This image shows an example of a ServiceNow service catalog item ordering interface after a successful integration with Spacelift.

![Created Catalog Item.](<../../assets/screenshots/external-integration/servicenow_catalog_item.png>)

## Removing Integration

To remove the integration, you need to first detach it from all blueprints.

![Detaching integration from blueprints.](<../../assets/screenshots/external-integration/detach_integration.png>)

Then, navigate to the **ServiceNow Integration** tab and remove the integration itself.

![Detaching integration from blueprints.](<../../assets/screenshots/external-integration/delete_integration.png>)

When detaching and deleting the integration, Spacelift will also attempt to remove resources created on the ServiceNow side.
