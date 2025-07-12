---
title: "Errors That Dont Create Incomplete Executions"
sidebar_position: 6
---

# Errors That Dont Create Incomplete Executions

Incomplete executions Errors that don't create incomplete executions Most of the errors that can happen in Make are connected with the flow of data in your scenario (like the DataError) or with the third party application (like the ConnectionError).

## However, some errors don't create an incomplete execution: * When the error happens on the first module in the scenario.

However, you can add the **Break** error handler ot the first module in the scenario. With the **Break** error handler, Make stores the incomplete execution even when the first module in the scenario outputs an error. * When your incomplete executions storage is full. If your incomplete executions storage is full, Make checks the  setting: * If the data loss is disabled, Make disables the scenario. * If the data loss is enabled, Make keeps scheduling scenario runs and discards the incomplete execution if it cannot be stored in your account.

* When the scenario runs longer than the scenario run duration limit. You can check the limit for your plan on the Make. * When an error happens during the initialization or rollback . Since these errors happen outside of the scenario operation phase, there is no incomplete scenario run. Always Active Clear