---
title: "Throw"
---

# Throw

# Title: Throw -

This article describes alternatives and workarounds to mimic the**Throw**error handling directive.

Alternate solution
-------------------------------------------------------

To conditionally throw an error you may configure a module to make it optionally purposely fail during its operation. One possibility is to employmodule configured to optionally throw an error (BundleValidationError in this case):

*   force the scenario execution to stop and perform the rollback phase:Rollback

*   force the scenario execution to stop and perform the commit phase:Commit

*   stop the processing of a route:Ignore

*   stop the processing of a route and storing it in the queue of:Break

The following example shows the use of the Rollback directive:

Workaround - Using HTTP Module

Usecase- Retry after some time if there is no record found using Break Directive. Usually, this is crucial when your record doesn't update instantly and you would like to process it later on in automation. Using this Break directive could be handy with the lesser complexity of the setup.

Current Barrier- Make does not offer a module that would enable you to easily conditionally generate (throw) errors.

To give you a better understanding here is the current setup without modification:This scenario search in Zendesk if there is no use it won’t throw an error forcefully to search it again you would need to implement a complex procedure by saving the record.

Solution- To conditionally throw an error you may replace the module where you want to throw an error, with an HTTP module then perform the search in a second scenario linking the HTTP module using webhook with a second scenario. If no result found you can customize the module to throw an error

Scenario One -

*   Replace the Module where you want to throw an error with HTTP > Make a Request module

*   Configure the URL within the query parameter that you will get from the Custom Webhook module and add an optional query parameter to search for the email

*   Enable the advanced settings and check the evaluate all the states as errors.

*   Add a Break handler in that HTTP module and configure the setup to run later.

Scenario 2 -

1.   Setup Webhooks > Custom Webhooks as a trigger and copy the URL use it in the HTTP module as shown in the previous steps.

2.   Here use the Zendesk > Search for a User module use the parameter from the HTTP module to perform a query. Enable Continue the execution of the route even if the module returns no results

3.   Add a Router and create two routes

4.   Consecutively setup the webhook response module

The following example returning the result - You will notice when the Zendesk module executes the API it doesn’t send any error message but in the action, we’re replicating the error using the HTTP module.