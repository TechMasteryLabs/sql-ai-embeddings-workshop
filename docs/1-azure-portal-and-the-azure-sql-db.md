# 1. The Azure Portal and Connecting to an Azure SQL Database

The next section of the workshop you will be browsing pre-created resources, gathering connection information, and connecting to an Azure SQL Database.

## Logging into the Azure Portal

1. Once you have logged into the virtual machine, open the Edge browser by double clicking it.

    ![A picture of clicking the Edge browser shortcut on the desktop](./media/Screenshot%202024-10-21%20at%201.16.52 PM.png)

1. After the browser starts, you should be on the Azure Sign In page

    ![A picture of the Azure sign in page in Edge](./media/Screenshot%202024-10-21%20at%201.19.53 PM.png){640}

    If you do not get the Azure login page when Edge opens, please navigate to +++https://portal.azure.com+++ by typing it in the URL or by using the link in the bookmarks bar.

    ![A picture of clicking on the Azure Portal bookmark](./media/Screenshot%202024-10-21%20at%201.20.03 PM.png){400}

1. On the Sign In page, use the following username in the Email, phone, or Skype field:

    > [!TIP]
    > Remember, you can just click on the following text and it will type it in the VM for you.

    +++@lab.CloudPortalCredential(User1).Username+++

    ![A picture of filling in the username in the Email, phone, or Skype field](media/Screenshot%202024-10-21%20at%201.31.41 PM.png){400}

1. then click the **blue Next button** after the username has been entered

    ![A picture of clicking the blue Next button after the username has been entered](./media/Screenshot%202024-10-21%20at%201.34.33 PM.png){400}

1. Next, use the password field and enter the following password:

    > [!TIP]
    > Remember, you can just click on the following text and it will type it in the VM for you.

    +++@lab.CloudPortalCredential(User1).Password+++

    ![A picture of using the password field to enter the azure user password](./media/Screenshot%202024-10-21%20at%201.34.45 PM.png){400}

1. then click the **blue Sign in button** after the password has been entered

    ![A picture of clicking the blue Sign in button after the password has been entered](./media/Screenshot%202024-10-21%20at%201.34.54 PM.png){400}

1. For the next dialog window, select the **Blue Yes Button** so that you can stay logged into Azure without having to reenter the username and password.

    ![A picture of selecting the Blue Yes Button so that you can stay logged into Azure without having to reenter the username and password](./media/Screenshot%202024-10-21%20at%201.40.31 PM.png){400}

    You may get a Welcome to Azure page. If so, just click **Cancel** on the bottom right of the page.

    ![A picture of clicking Cancel on the bottom right of the Welcome to Azure page](./media/Screenshot%202024-10-21%20at%201.42.45 PM.png){800}

1. You are now logged into Azure!

    ![A picture of the azure portal home page](./media/Screenshot%202024-10-21%20at%201.46.09 PM.png){800}

## Azure Resources

1. While on the **Azure Portal Home Page**, find the **View all resources button** in the middle of the page. **Click** on this button.

    ![A picture of clicking on the View all resources button in the middle of the page](./media/Screenshot%202024-10-21%20at%201.47.39 PM.png){600}

1. On the following page, you will see 3 pre-created resources for you to use in the lab. An Azure SQL Server, a SQL Database, and an Azure OpenAI instance with 2 deployed models; one for creating embeddings and one to use for our chat application.

    ![A picture of the three pre-created resources in Azure. A SQL server, a SQL database, and an Azure OpenAI instance.](./media/Screenshot%202024-10-21%20at%201.49.21 PM.png){1200}

    > [!WARNING]
    > **If you don't see all 3 resources, they may still be in the process of creation. Wait a minute or 2 and click the refresh button.** 

1. Start by clicking the Azure OpenAI instance. It will be named **igniteai@lab.LabInstance.Id**.

    ![A picture of clicking on the Azure OpenAI instance](./media/Screenshot%202024-10-21%20at%201.49.21 PM copy.png){1200}

1. Once clicked, you will be on the Azure OpenAI instance details page.

    ![A picture of the Azure OpenAI instance details page](./media/Screenshot%202024-10-21%20at%201.50.24 PM.png){1200}

1. On the right side of the page, find the **Manage Keys** item and click where it says **"Click here to manage keys"**.

    ![A picture of finding the Manager Keys item on the details page and clicking Clike here to manage keys.](./media/Screenshot 2024-10-23 at 7.01.09 AM.png){1200}

1. On the **Keys and Endpoints** details page,

    ![A picture of the Keys and Endpoints details page.](./media/Screenshot%202024-10-21%20at%201.50.43 PM.png){1200}

1. Click the copy link for **KEY 1**. This will copy the key into your clipboard.

    ![A picture of clicking the copy link for KEY 1 to copy the key into your clipboard](./media/Screenshot 2024-10-21232323 at 1.50.422223 PM copy.png){1200}

1. Paste the key in this text box so that it can be used in upcoming code sections.

    > [!ALERT]
    > **Paste the Azure OpenAI Key Here -->** @lab.TextBox(aiKey)

1. Did you remember to paste the key into the above text field?

1. To make the next sections a bit more navigation friendly, **click the zoom/maximize/window button** in the **upper right corner** of the browser window.

    ![A picture of clicking the zoom/maximize/window button in the upper right corner of the browser window ](./media/Screenshot 2024-11-01 at 9.16.01 AM.png){400}

## Connect to the free Azure SQL Database

#### **Using Visual Studio Code**

Visual Studio Code will be used for working with the database.

1. Back on the Windows desktop, double click the **Visual Studio Code icon** on the right side.

    ![A picture of double clicking the Visual Studio Code icon on the right side of the dektop to open the application](./media/Screenshot 2024-10-22 at 10.44.56 AM.png){100}

1. When Visual Studio Code opens, click the **SQL Extension** on the left side.

    ![A picture of clicking Add Connection in the SQL Extension](./media/Screenshot 2024-10-22 at 1.34.33 PM.png){300}

1. Next, click **Add Connection** in the SQL Extension. *(The Add Connection option might take a few seconds to load.)*

    ![A picture of clicking Add Connection in the SQL Extension](./media/Screenshot 2024-10-22 at 1.41.20 PM.png){300}

1. A SQL **Connection Dialog** tab will appear in the VS Code editor.

    ![A picture of the SQL Connection Dialog tab](./media/Screenshot 2024-10-24 at 10.17.57 AM.png){900}

1. For the **Profile Name** field, enter **SampleDB**.

    ![A picture of entering SampleDB in the Profile Name field](./media/Screenshot 2024-10-24 at 10.18.09 AM.png){800}

1. Next, for **Input type**, select the **Connection String** radio button.

    ![A picture of selecting the Connection String radio button for input type](./media/Screenshot 2024-10-24 at 10.18.17 AM.png){800}

1. In the **Connection String** text box, 

    ![A picture of the connection string text box](./media/Screenshot 2024-10-24 at 10.26.45 AM.png){800}

    copy and paste the following connect string:

    ```
    Server=tcp:azuresql@lab.LabInstance.Id.database.windows.net,1433;Initial Catalog=SampleDB;Persist Security Info=False;User ID=sqladmin;Password=@lab.CloudPortalCredential(User1).Password;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Connection Timeout=30;
    ```

    then press the **blue Connect button**.

    ![A picture of pressing the blue Connect button](./media/Screenshot 2024-10-24 at 10.28.11 AM.png){800}

1. Once connected to the database, **right click** on the database in the connection navigator on the left side and choose **New Query**.

    ![A picture of right clicking on the connection name in the connection navigator on the left side and choosing New Query](./media/Screenshot 2024-10-22 at 2.02.00 PM.png)

1. You are now connected to the Azure SQL Database!