---
title: "Ignore Error Handler"
sidebar_position: 7
---

# Ignore Error Handler

Error handlers Ignore error handler The **Ignore** error handler ignores the error and removes the bundle from the scenario flow. The scenario run continues with the next bundle. You can use the **Ignore** error handler when you know that there can be incorrect data in your scenario and they don't have an impact on your processes. The **Ignore** error handler prevents turning off the scenario when there's an error and marks the scenario run as a success even in case of errors. For example: This demo scenario contains five modules.

The scenario is useful for tests and showing the effect of an error handler: 1. **JSON** - **Parse JSON** provides test data in the form of an array of three record IDs. **Iterator** splits the array into individual bundles. **Data store** - **Update a record**: Updates the data in the data store. **Data store** - **Update a record**: This module updates the data again. This time the module works differently. In the module mapping, there is a mapping that intentionally creates an error:  The mapping inserts a null value into the required **Key** field, which always creates the BundleValidationError.

**Slack** - **Send a message**: Sends a message to a private testing channel. This is how the example scenario looks: When we would run the example scenario, we would get the BundleValidationError: If we added the **Ignore** error handler to the **Update a record** module, the **Ignore** error handler would remove the bundle from the scenario flow. The bundle doesn't enter the fifth (**Send a message**) module. The third bundle runs through the scenario: For more information about error handling strategies check the .

Keep your scenario running regardless of errors With the **Ignore** error handler, you can remove the bundle that causes an error from the scenario flow and process the rest of the bundles in the scenario. In addition, Make will keep running your scenario on schedule instead of disabling scheduling because of an error. For example, the following scenario outputs an error in the **Update a record** module: To ignore the error and keep your scenario running regardless of errors, follow the steps: 1.

Right-click the module that is causing the error. In the menu, select **Add error handler**. Select the **Ignore** error handler. Save your scenario. Your scenario keeps running regardless of errors. When an error occurs in the **Data store** module, the **Ignore** error handler removes the bundle from the scenario flow. Always Active Clear