---
title: "Introduction to errors and warnings"
---

# Introduction to errors and warnings

# Title: Introduction to errors and warnings -

Sometimes, automation doesn't go the way you planned and takes a wrong turn. When this happens, Make gives you a warning or an error based on the situation.

You can also assume another point of view on errors and warnings: They protect your scenario by preventing the processing of unexpected data, and therefore saving operations usage.

Errors in Make
---------------------------------------------------------------------------------

Errors notify you that your Make encountered an unexpected event that is not handled by an . Because of the situation, you should check the scenario.

A module outputs an error when the module receives incorrect data from the previous modules or the module app. When you open your scenario in the scenario editor, Make highlights the module that outputs the error with the "Caution" sign:

When a module outputs an error, Make stops the current scenario run and starts the . The rollback phase reverts changes if possible and puts back the  to the time before the scenario run.

When there are scenario runs that end with an error, Make disables further scheduling of the scenario. Disabling the scenario allows you to check the error and prevents consuming operations on scenario runs that finish with an error.

The most common situations when a module outputs an error include:

*   Mapping a value to a required field in a module when the value is sometimes empty and causes missing required data.

*   When you exhaust your resources in the third-party app. For example, when you can't store more data in the app.

*   When the app is unavailable. For example, when the app is down for maintenance.

*   When there is a change to your authentication or authorization in the app and you don't update your connection. For example, when your API key expires or when you change teams and lose access to some of the app features.

The best way to deal with errors in your scenario is to use an error handler. An error handler connects to a module with the error handling route. When the module outputs an error, the error handling route activates and runs the error handler.

When all errors are handled, Make keeps scheduling scenario runs instead of disabling the scenario.

Error notifications
--------------------------------------------------------------------------------------

When an error happens and the error is not handled by any error handler, Make sends you an email notification:

Make also sends out a notification when your scenario gets disabled because of repeated errors.

You can learn more about Make email notifications and their settings .

Warnings in Make
------------------------------------------------------------------------------------

Warnings alert you that there was an issue during the scenario run, but not as serious as an error. Also, scenarios can have the warning status when there were errors handled with your error handling.

When a module in a scenario returns a warning, your scenario keeps running and stays enabled. But it's a good idea to check the  for the cause of the warning.

The situations when you get a warning include:

*   When you use up all of the capacity of a data store in your scenario.

*   When the duration of the scenario run exceeds the time limit for your subscription.

Learn more about warnings .