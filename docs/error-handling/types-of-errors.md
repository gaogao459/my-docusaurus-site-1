---
title: "Types of errors"
---

# Types of errors

# Title: Types of errors -

Within a scenario, you can have numerous modules and item mappings. Together, they create your scenario. Each of these elements can create an unexpected event -- an error. Make categorizes errors based on their origin and their cause.

For example, the ConnectionError happens when the app is unavailable because of maintenance or downtime on the third-party side and Make can’t connect to the app servers.

When a module returns an error, Make highlights the module with the "Caution" sign. To check the error type, click the thought bubble above the module:

Make follows the standard error codes and their definitions. Note that it is possible that the third party may not fully comply with the standard.

AccountValidationError
---------------------------------------------------------------------

A module outputs the AccountValidationError when Make cannot authenticate you in the third-party app. For example, when you change your credentials in the app or your credentials expire and you don't update them in the connection, the app module will output the AccountValidationError.

If a module outputs the AccountValidationError, the scenario ends with an error. When your scenario finishes with an error for the  in a row, Make disables the scheduling of your scenario.

To fix the AccountValidationError, review your credentials in the app and the connection in Make. If necessary, create a new connection for the app. If you are getting the AccountValidationError frequently, contact our .

BundleValidationError
--------------------------------------------------------------------

A module outputs the BundleValidationError when the bundle entering the module doesn't pass validation. Validation means that before processing a bundle in a module, Make checks whether data types match in the module mappings and whether there are no missing values in the module required fields.

For example, you get the BundleValidationError when you map text to a module settings field that requires a date, or when you map an empty value to a required field in the module settings.

If a module outputs the BundleValidationError with no error handling, the scenario ends with an error. When your scenario finishes with an error for the  in a row, Make disables the scheduling of your scenario.

The best way to handle this error is to review your mapping in the module settings.

ConnectionError
--------------------------------------------------------------

A module outputs the ConnectionError when the third-party app is unavailable. For example, the third-party service might be offline because of maintenance. This error uses the .

The default handling of the ConnectionError depends on the following attributes:

*   scenario scheduling

*   enabling of the incomplete executions

|  | Incomplete executions disabled | Incomplete executions enabled |
| --- | --- | --- |
| Scheduled scenario | Make pauses the scheduling of the scenario for 20 minutes. Make doesn't rerun the scenario. | Make pauses the scheduling of the scenario for 20 minutes. Make retries the incomplete execution with the incomplete execution . |
| Instant scenario | Make reruns the incomplete execution with the scenario. | Make retries the incomplete execution with the incomplete execution . |

DataError
--------------------------------------------------------

A module outputs the DataError when data sent by the module doesn't pass validation on the third-party side. For example, when you try to create a tweet with the **Twitter**>**Create a Tweet** module that has more than 280 characters, the **Create a Tweet** module outputs the DataError because tweets have a maximum length of 280 characters.

Another situation when you get the DataError is when you map an incorrect data type to a function. For example, when you map data with the text data type to the  function.

If a module outputs the DataError with no error handling, the scenario ends with an error. When your scenario finishes with an error for the  in a row, Make disables the scheduling of your scenario.

To fix the DataError, review your mapping and identify the reason why the error happens. If you cannot fix the error with different mapping, you can use the  and  error handlers.

DataSizeLimitExceededError
-------------------------------------------------------------------------

A module outputs the DataSizeLimitExceededError when you run out of data transfer quota. Your data transfer limit is calculated from the operations limit.

If a module outputs the DataSizeLimitExceededError with no error handling, the scenario ends with an error. Because the DataSizeLimitExceededError is a fatal error, Make immediately disables the scenario scheduling, regardless of the .

DuplicateDataError
-----------------------------------------------------------------

A module outputs the DuplicateDataError when you send the same data to a module that doesn't allow duplicates. For example, when you try to create a new user in an app and the user's e-mail address has to be unique, but the e-mail address is used already. The module outputs the DuplicateDataError, because the e-mail address is registered with another user already.

If a module outputs the DuplicateDataError with no error handling, the scenario ends with an error. When your scenario finishes with an error for the  in a row, Make disables the scheduling of your scenario.

If you get the DuplicateDataError in your scenario, you should review your scenario design. For example, if you are using a database, you could first check if the database record exists with a search module. Or with the email example, you could just ignore the error with the .

IncompleteDataError
------------------------------------------------------------------

A module outputs the IncompleteDataError when the module can get only part of the data from the third-party app.

For example, when you are uploading new photos to Google Photos and you have a scenario that downloads the photos at the same time. Make tries to download the photo that you are currently uploading. The photo file won't be complete and the Google Photos module will output the IncompleteDataError.

If a module outputs the IncompleteDataError with no error handling, the scenario ends with an error. Make pauses the scenario for 20 minutes and then runs the scenario again until the scenario succeeds or reaches the .

InconsistencyError
-----------------------------------------------------------------

A module outputs the InconsistencyError when an error happens during the scenario. This error can occur when you make changes to a data store with two scenarios that run at the same time. If one scenario encounters an error and attempts to undo the changes in the rollback phase, but the other scenario already finished making changes, the changes cannot be safely undone and you get the InconsistencyError from the data store module in the first scenario.

For example, imagine two people making changes in the same part of a file. One of them saves changes before the other. What happens with the changes from the other person?

If a module outputs the InconsistencyError with no error handling, the scenario ends with an error. Because the InconsistencyError is a fatal error, Make immediately disables the scenario scheduling, regardless of the .

To fix the InconsistencyError, check your data and fix the data if necessary. If you are getting the InconsistencyError frequently, check the scenarios that use the database.

MaxFileSizeExceededError
-----------------------------------------------------------------------

A module outputs the MaxFileSizeExceededError when you try to process a file that exceeds the maximum file size. The maximum file size differs based on your organization's subscription. You can check the maximum file sizes in the Make.

For example, if you use the **Google Drive**>**Move a file** module in an organization with the Core plan to move a file larger than 100 MB, you would get the MaxFileSizeExceededError.

If a module outputs the MaxFileSizeExceededError with no error handling, the scenario ends with an error. When your scenario finishes with an error for the  in a row, Make disables the scheduling of your scenario.

To fix the MaxFileSizeError, you have to either make the file smaller (compress or split the file) or upgrade your organization's subscription plan.

ModuleTimeoutError
-----------------------------------------------------------------

A module outputs the ModuleTimeoutError when the module is requesting or processing data for more than 40 seconds. For example, this error can happen when you are retrieving a large amount of data from the app or when the app has reduced availability.

The default handling of the ModuleTimeoutError depends on the following attributes:

*   scenario scheduling

*   enabling of the incomplete executions

|  | Incomplete executions disabled | Incomplete executions enabled |
| --- | --- | --- |
| Scheduled scenario | Make pauses the scheduling of the scenario for 20 minutes. Make doesn't rerun the scenario. | Make pauses the scheduling of the scenario for 20 minutes. Make retries the incomplete execution with the incomplete execution . |
| Instant scenario | Make reruns the incomplete execution with the scenario. | Make retries the incomplete execution with the incomplete execution . |

OperationsLimitExceededError
---------------------------------------------------------------------------

A module outputs the OperationsLimitExceededError when you run out of operations. Your operations limit is set with your organization's subscription. You can check your operations limit in the Make.

If a module outputs the OperationsLimitExceededError, the scenario ends with an error. Because the OperationsLimitExceededError is a fatal error, Make immediately disables the scenario scheduling, regardless of the .

RateLimitError
-------------------------------------------------------------

A module outputs the RateLimitError when you make too many requests over a time period to the app API. This error uses the  and follows the  rules of the third party.

For example, the  modules output the RateLimitError when you reach the number of API calls per minute based on your .

The default handling of the RateLimitError depends on the following attributes:

*   scenario scheduling

*   enabling of the incomplete executions

|  | Incomplete executions disabled | Incomplete executions enabled |
| --- | --- | --- |
| Scheduled scenario | Make pauses the scheduling of the scenario for 20 minutes. Make doesn't rerun the scenario. | Make pauses the scheduling of the scenario for 20 minutes. Make retries the incomplete execution with the incomplete execution . |
| Instant scenario | Make reruns the incomplete execution with the scenario. | Make retries the incomplete execution with the incomplete execution . |

RuntimeError
-----------------------------------------------------------

A module outputs the RuntimeError when the error reported by the third-party app doesn't meet the criteria for any other error type. For example, you get the RuntimeError when you use up all your tokens with the **OpenAI**>**Create a Completion** module.

If a module outputs the RuntimeError with no error handling, the scenario ends with an error. When your scenario finishes with an error for the  in a row, Make disables the scheduling of your scenario.

There's no general rule to fixing the RuntimeError. Check the error message in the scenario history or try to reproduce the error with the .