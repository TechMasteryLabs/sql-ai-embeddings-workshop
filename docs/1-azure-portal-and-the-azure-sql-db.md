# 1. The Azure Portal and Connecting to an Azure SQL Database

## Prerequisites

**Software**
 - Visual Studio Code with the SQL Extension (access from your own PC or from the optional SQL Developer VM)
 - SSMS

**Services**
 - Azure OpenAI instance with a text-embedding-ada-002 deployment and a gpt-4 deployment.
 - An Azure SQL Database

**Key Information Needed**
 - Azure SQL Database Server Name
 - Azure SQL Database Name
 - Azure OpenAI Endpoint Name (Home page of Azure AI Foundry)
 - Azute OpenAI Endpoint Key
![image](https://github.com/user-attachments/assets/9b7d2dd4-3ce5-4915-9b3d-93f99d1c1d74)


## Connect to the free Azure SQL Database

#### **Using Visual Studio Code**

Visual Studio Code will be used for working with the database. (access from your own PC or from the optional SQL Developer VM)

1. When Visual Studio Code opens, click the **SQL Extension** on the left side.

    ![A picture of clicking Add Connection in the SQL Extension](./media/Screenshot%202024-10-22%20at%201.34.33 PM.png)

1. Next, click **Add Connection** in the SQL Extension. *(The Add Connection option might take a few seconds to load.)*

    ![A picture of clicking Add Connection in the SQL Extension](./media/Screenshot%202024-10-22%20at%201.41.20 PM.png)

1. A SQL **Connection Dialog** tab will appear in the VS Code editor.

    ![A picture of the SQL Connection Dialog tab](./media/Screenshot%202024-10-24%20at%2010.17.57 AM.png)

1. For the **Profile Name** field, enter **SampleDB**.

    ![A picture of entering SampleDB in the Profile Name field](./media/Screenshot%202024-10-24%20at%2010.18.09 AM.png)


### example - use EntraID 
<details>
  <summary>Click to expand</summary>
1. Copy the name of the server from the Overview page of Azure SQL and paste it into the **server name** section
   
   ![image](https://github.com/user-attachments/assets/849cb3c2-8a4e-4611-9065-1f79fa217cdb)
   
   ![image](https://github.com/user-attachments/assets/f4f9a627-10d4-4019-8856-15633705570a)
 
1. Next, for **Authentication Type**, select the **Microsoft EntraID - Universal with MFA SUpport**.

1. Your Entra ID account will be auto filled
1. Type **sampleDB** for the name of the database and click the blue **Connect** button  ![image](https://github.com/user-attachments/assets/ca256cdf-8cc6-4b30-92d3-99b339683a51)

### end example - use EntraID
</details>

### example - use a SQL Admin username and password   

1. Next, for **Input type**, select the **Connection String** radio button.

    ![A picture of selecting the Connection String radio button for input type](./media/Screenshot%202024-10-24%20at%2010.18.17 AM.png)

1. In the **Connection String** text box, 

    ![A picture of the connection string text box](./media/Screenshot%202024-10-24%20at%2010.26.45 AM.png)

    copy and paste the following connect string:

    **Be sure to replace the following placeholders in the connection string:YOUR_AZURE_SQL_SERVER_NAME, YOUR_DATABASE_NAME, YOUR_SQLADMIN_PASSWORD** 

    ```
    Server=tcp:azuresql@YOUR_AZURE_SQL_SERVER_NAME.database.windows.net,1433;Initial Catalog=YOUR_DATABASE_NAME;Persist Security Info=False;User ID=sqladmin;Password=YOUR_SQLADMIN_PASSWORD;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;
    ```


### end of example - use a SQL Admin username and password   

    then press the **blue Connect button**.

    ![A picture of pressing the blue Connect button](./media/Screenshot%202024-10-24%20at%2010.28.11 AM.png)

1. Once connected to the database, **right click** on the database in the connection navigator on the left side and choose **New Query**.

    ![A picture of right clicking on the connection name in the connection navigator on the left side and choosing New Query](./media/Screenshot%202024-10-22%20at%202.02.00 PM.png)

1. You are now connected to the Azure SQL Database!
