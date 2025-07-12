---
title: "Google SAML"
description: "Learn about Google SAML in Make.com automation platform"
sidebar_position: 2
---

# Google SAML

Access management Google SAML This feature is available to Enterprise customers. The following manual configuration creates an SAML SSO configuration for your Enterprise organization. 

## Prerequisites 

* Owner role in an Enterprise organization 
* Google Admin console account 

## Supported features 

This configuration supports the following: 

* Service Provider initiated SSO 
* Single Log Out  

Before configuring SSO, you need to assign a namespace and download your service provider certificate in Make.
These steps provide information you need to enter later.

### Create your namespace in Make 

1. Click **Organization** in the left sidebar.
2. Click the **SSO** tab. 
3. Under **Namespace**, enter the namespace you want for your organization. For example, acmecorp. Your organization members enter this namespace when they log in via SSO. 
4. Under **SSO type**, select **SAML 2.0**. 
5. Copy the **Redirect URL** and save it in a safe place.

You will use this later when you create your SAML integration in the Google admin portal.

### Create an SAML application in the Google admin portal 

1. Login to the Google admin console. 
2. From the dashboard's left menu, click **Apps > Web and mobile apps**. 
3. Click **Add app** and select **Add custom SAML app**. 
4. Enter an **App name** and **Description**. 
5. Copy the **SSO URL** and save it in a safe place. You will use this later. 
6. On the same screen, download the certificate and save it in a safe place. 
7. Click **Continue**. 
8. Enter the **Service provider details**.

You can find this information in the Make SSO configuration tab. 

**ACS URL:** `https://www.make.com/sso/saml/{namespace}` 

**Entity ID:** `https://www.make.com/sso/saml/{namespace}/metadata.xml` 

Replace `{namespace}` with your namespace.

9. Click **Continue**. 
10. Enter the App attributes. 
11. Update the **User access** to On for everyone. 

### Update the SSO in Make 

1. Click **Organization** in the left sidebar. 
2. Click the **SSO** tab.
3. Activate the **Service Provider Certificate** and download it. 
4. In the **IDP certificate** section, upload the certificate downloaded from step 6 above. 
5. Enter the SSO URL from step 5 above and paste it into the **IDP Login URL** field in Make. 
6. Enter the **Login IML resolve**.

Optional: It is a good practice to validate the JSON string in IML Resolve to ensure it is correct.

7. Enter the following additional information: 
   - Allows Unencrypted Assertions: Yes 
   - Allow Unsigned Responses: No 
   - Sign Requests: Yes 

## Service provider initiated SSO 

1. Go to Make.com. 
2. Click **Sign in with SSO**. 
3. Enter the namespace you chose for your organization.