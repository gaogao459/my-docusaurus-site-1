---
title: "Resume Error Handler"
sidebar_position: 8
---

# Resume Error Handler

Error handlers Resume error handler The **Resume** error handler replaces the module output with a substitute output when an error happens. You define the substitute output in the **Resume** error handler settings. The rest of the scenario uses the substitute output. Make processes the rest of the bundles in the scenario flow normally. For example: This demo scenario contains five modules. The scenario is useful for tests and showing the effect of an error handler: 1. **JSON** - **Parse JSON** provides test data in the form of an array of three record IDs.

**Iterator** splits the array into individual bundles. **Data store** - **Update a record**: Updates the data in the data store. **Data store** - **Update a record**: This module updates the data again. This time the module works differently. In the module mapping, there is a mapping that intentionally creates an error:  The mapping inserts a null value into the required **Key** field, which always creates the BundleValidationError.

**Slack** - **Send a message**: Sends a message to a private testing channel. This is how the example scenario looks: When we would run the example scenario, we would get the BundleValidationError: If we added the **Resume** error handler to the **Update a record** module, the **Resume** error handler would replace the bundle with the substitute mapping. When the module outputs an error, Make would use the substitute bundle instead. The third bundle runs through the scenario: You can use the **Resume** error handler when you have a substitute mapping that fixes the bundle and allows the data bundle to continue in the scenario flow.

You can also use the **Resume** error handler to add a placeholder that marks the data bundle to check later.

## For more information about error handling strategies check the .

Change the bundle when it causes an error With the **Resume** error handler, you can substitute the bundle that causes an error with your custom data. The custom data continue the rest of the scenario flow instead of the erroring bundle. In the **Resume** error handler settings, you get the same fields as in the handled module settings. In the error handler fields, you can provide custom data that Make uses instead of the bundle that caused the error.

For example, the following scenario outputs an error in the **Update a record** module: To change the erroring bundle for custom data and use them in the rest of the scenario, follow the steps: 1. Right-click the module that is causing the error. In the menu, select **Add error handler**. Select the **Resume** error handler. Fill in the **Resume** handler settings with your custom mapping. Save your scenario. You added the **Resume** error handler to your scenario. When an error occurs in the **Data store** module, the **Resume** error handler replaces the bundle with your custom mapping.