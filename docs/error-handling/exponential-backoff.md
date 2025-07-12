---
title: "Exponential backoff"
---

# Exponential backoff

# Title: Exponential backoff -

Exponential backoff -

 to automatically schedule scenario reruns with increasing time delays. The scenario reruns trigger when a module in the scenario outputs:

*   RateLimitError
*   ConnectionError
*   ModuleTimeoutError

The time delays between the scenario reruns depend on whether  are enabled or not:

| **Rerun number** | **Incomplete executions enabled** | **Incomplete executions disabled** |
| --- | --- | --- |
| 1 | 1 minute | 1 minute |
| 2 | 10 minutes | 2 minutes |
| 3 | 10 minutes | 5 minutes |
| 4 | 30 minutes | 10 minutes |
| 5 | 30 minutes | 1 hour |
| 6 | 30 minutes | 3 hours |
| 7 | 3 hours | 12 hours |
| 8 | 3 hours | 24 hours |

This means that when a module in your scenario outputs the ConnectionError because the third-party service is unavailable, Make schedules the rerunning of the scenario one minute after the error occurs.

If a module during the rerun outputs the ConnectionError again, Make schedules another rerun after 2 minutes and so on. If the 8th attempt fails, Make disables scheduling of the scenario.

Until Make disables scheduling the scenario, the scenario follows the run schedule in addition to the exponential backoff reruns (though there are ).

If you want Make to wait with scheduling the next scenario runs until the reruns finish, enable  in scenario settings.

If you enable the option to store incomplete executions in the scenario settings, Make stores the scenario run in incomplete executions.

Make then schedules scenario reruns from the incomplete execution data. If all rerun attempts fail, Make keeps the scenario incomplete execution for you to resolve manually.

Yes

No

Allow All
### Manage Consent Preferences

#### Necessary Cookies

- ](https://www.onetrust.com/products/cookie-consent/)