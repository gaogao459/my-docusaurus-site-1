---
title: "Data stores"
---

# Data stores

# Title: Data stores -

Data stores allow you to store data from a scenario or transfer data between individual scenarios or scenario runs. You can use data stores to store data from apps during scenario execution. Data stores are similar to a simple database.

Data storage allowance
------------------------------------------------------------------

Before creating a data store, take note of your data storage allowance. Total data storage is based on number of operations in your plan, with every 1,000 operations equaling 1 MB of data storage.

As 1 MB is the minimum size of a data store in Make, you will need at least 1 MB of data storage available to create a new data store.

Consider the following data storage allowances for data stores, depending on your :

As an Enterprise user, calculate your total data store by determining your average monthly operations, and then dividing your monthly operations by 1,000. For example, with 1,000,000 operations per year, you have 83.3 MB of data storage available to allocate to your data stores. 1,000,000 operations / 12 months = 83,333 operations 83,333 operations / 1,000 = 83.33 MB Each data store is at least 1 MB in size.

To adjust the data storage allocated to your existing data stores, see .

How to create a data store
---------------------------------------------------------------------

1

In the left sidebar, click **Data stores**.

2

Click **+ Add data store**.

3

Enter settings for the new data store.

| **Field** | **Description** |
| --- | --- |
| **Data store name** | Enter the name for the data store. For example, Contacts. |
| **Data structure** | A data structure is a list of the columns for a table that indicates the column name and data type. You have three options: * **Select a data structure that has been already created** * **Leave the field empty** If you don't select a data structure, the database will only contain the primary key. Such a database type is useful if you only want to save keys and are only interested in knowing whether or not a specific key exists in the database. * **Add a new data structure** Click the **Add**button to create a new data structure. |
| **Data storage size in MB** | Allocate the size for the data store from your total data storage. The amount can be changed at any time. 1 MB is the minimum data storage size per data store. You can see your available storage space in the text below the**Data storage size in MB** field. |

Manage the data structure of a data store
------------------------------------------------------------------------------------

### Add a new data structure

During the process of setting up a data store, you can set up a new data structure.

To set up the data structure while adding a data store, click the Add button for the Data structure field

You can access this dialog by clicking the **Add** button when creating or editing the data store:

|  |  |
| --- | --- |
| **Data structure name** | Enter the name for the data structure. The data structure name is its unique identifier and cannot be changed later. |
| **Specification** | There are two options for how you can specify the data store columns. * Click the **Add item** button to specify the properties of one column manually. Enter the **Name** and **Type** for the data store column and define the corresponding properties. * Use the _Generator button_ to determine the columns from the sample data you provide. For example, the following JSON sample data creates three columns (name, age, phone number) with phone number as a collection of mobile and landline:  "name":"John", "age":30, "phone number":   |
| **Strict** | If enabled, the data structure will be compared to the structure of the payload and if the payload contains extra items not specified in the data structure, the payload will be rejected. |

### Update the data structure of a data store

Be careful when updating the data structure of a data store. Before updating the structure, make a backup of the data.

Changes in the data structure of a data store might lead to unexpected results.

When you want to update the data structure of a data store, you should keep in mind that:

*   The data structure field names are unique identifiers of the data store columns. When you rename a field of a data structure, Make cannot retrieve the original data in the data store column, because they use a different column identifier.

*   You can update the data structure field label anytime without the effects mentioned in the previous point.

*   The changes to the data store structure apply only to the new data you put in the data store. Make doesn't change or validate the original data to fit the updated structure.

The best approach to updating the data structure of a data store is to create temporary fields with copies of your data. Update the data in the temporary fields and make sure they conform to the final data structure.

### Rename a field of the data store structure

You can update the **Label** of a data store structure field anytime.

To change the data store structure field **Name**:

1

2

Create a field in your data store with the new name.

3

Copy all data from the oroginal column to the new column.

4

Update all data in the original column to empty fields. This step prevents storing the data in the original column alongside the data in the new column.

You have put the data from the original data store column into the new data store column. In addition, you have a data store backup to check that the update was successful.

### Change the type of a field of the data store structure

1

2

Either create a temporary field for the updated data type, or you can skip this step and update the field type in place.

3

Use a conversion function to update the type of all values in the data store column to the new type. For example, to convert text to date, use the parseDate function.

Actions
--------------------------------------------------

Adds or replaces a record in the data store.

| **Field** | **Description** |
| --- | --- |
| Data store | Select or add the data store where you want to create a record. |
| Key | Enter the unique key. The key can be used later to retrieve the record. If you leave this field blank, the key will be generated. |
| Overwrite an existing record | Enable this option to overwrite the record. The record you want to overwrite must be specified in the **Key** field above. |
| Record | Enter the desired values to the record's fields. The maximum size of the record in the data store is 15 MB. |

The module throws an error when you try to add the record which is already in the data store under the same name and the **Overwrite an existing record**option is disabled.

Updates a record in the selected data store.

| **Field** | **Description** |
| --- | --- |
| Data store | Select or add the data store where you want to create a record. |
| Key | Enter the unique key of the record you want to update. |
| Insert missing record | Enable this option to create a new record if the record with the specified key doesn't already exist. |
| Record | Enter the desired values to the record's fields that you want to update. The maximum size of the record in the data store is 15 MB. |

Retrieves a record from the selected data store.

| **Field** | **Description** |
| --- | --- |
| Data store | Select the data store you want to retrieve a record from. |
| Key | Enter the unique key of the record you want to retrieve. |
| Return Wrapped Output | Choose if you want the output to be returned in the same way that the Search records module returns data. |

Returns the value true if the record exists in the specified data store or false if the record doesn't exist in the data store.

| **Field** | **Description** |
| --- | --- |
| Data store | Select the data store you want to check for the record existence. |
| Key | Enter the key of the record you want to check for existence |

Deletes a specified record from the selected data store.

| **Field** | **Description** |
| --- | --- |
| Data store | Select the data store you want to check for the record existence. |
| Key | Enter the key of the record you want to delete. |

Deletes all records from the selected data store.

| **Field** | **Description** |
| --- | --- |
| Data store | Select the data store you want to delete all records from. |

Performs a search for records based on filter settings.

| **Field** | **Description** |
| --- | --- |
| Data store | Select the data store you want to check for the record's existence. |
| Filter | Set the filter for the search. Select the column, operator and required value (search term) for the search. If you use the **datetime** operators, you need to provide a value in a date format. Use the parseDate function for this purpose. |
| Sort | * Key: Select the column name you want to sort the results by. * Order : Select whether you want to sort results in ascending or descending order. |
| Limit | Set the maximum number of search results Make will return during one execution cycle. |
| Continue the execution of the route even if the module returns no results | If enabled, the scenario will not be stopped by this module. |

Returns the number of records in the selected data store.

| **Field** | **Description** |
| --- | --- |
| Data store | Select the data store whose records you want to count. |

Manage records in a data store
-------------------------------------------------------------------------

Make allows you to view, update, and delete the records in your data store.

1

In the left sidebar, click **Data stores**.

2

Click **Browse** next to your data store.

Troubleshooting
----------------------------------------------------------