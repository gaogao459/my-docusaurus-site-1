---
title: "Types of warnings"
---

# Types of warnings

# Title: Types of warnings -

Within a scenario, you can have numerous modules and item mappings. Together, they create your scenario. Each of these elements can create an event that might need your attention -- a warning.

A warning can also be the result of handling an error with the . With the warning Make informs you that the **Break** error handler created an  of your scenario.

The main difference between a warning and an error is, that a warning doesn't disable the scheduling of your scenario and warnings don't count into the .

When a module returns a warning, Make highlights the module with the "Warning" sign. To check the error type, click the thought bubble above the module.

When you use error handling, you will see a warning when the error handler activates. In the example, the  handled the . The error handler activation turned the original error into a warning.

ExecutionInterruptedError
--------------------------------------------------------------------------

A module outputs the ExecutionInterruptedError when the scenario runs for more than 40 minutes (5 minutes for the Free subscription). The module that is currently processing data outputs the warning.

When a module outputs the ExecutionInterruptedError the scenario ends with a warning. The scenario doesn't process the remaining bundles. Make will keep scheduling further scenario runs.

To fix the ExecutionInterruptedError, consider strategies to optimize your scenario:

*   Split your scenario. You can use the combination of the following modules: For example, if you are processing a lot of bundles in a scenario with 20 modules and the scenario ends with the ExecutionInterruptedError, you can split the scenario into two scenarios with 10 modules each.

*   Set the search modules' **Limit** to a lower number to reduce the amount of data processed by the scenario.

*   Check the API documentation of the apps you use in the scenario. If the app’s API has a suitable endpoint that supports batch requests, you can use the **JSON aggregator** and the **HTTP** app to send your data in batches. In addition, you save on operation usage.

OutOfSpaceError
----------------------------------------------------------------

Data store modules output the OutOfSpaceError when Make cannot store any more data in the data store. You also get the OutOfSpaceError when you fill your incomplete execution storage.

If a module outputs the OutOfSpaceError with no error handling, the scenario ends with a warning. The scenario doesn't process the remaining bundles. Make will keep scheduling further scenario runs.

To fix the OutOfSpaceError in a scenario, you can use a backup data store with the . You should also check the data in the data store or your incomplete execution storage. You can also review the Make.