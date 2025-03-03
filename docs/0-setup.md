# Setup for SQL lab

## Create a new Resource Group
1. From the Home screen of the Azure Portal click **Create a resource** ![image](https://github.com/user-attachments/assets/c1e64aee-aa4c-4c42-9e98-df4a0fba38a7)

2. Search for **Resource Group** ![image](https://github.com/user-attachments/assets/ccc0e0ad-0c69-42db-bc39-fa72f285afc9)

3. Click **Create** ![image](https://github.com/user-attachments/assets/cefefe94-ce57-43d9-823e-8a476a4fc4bb)

4. Give your Resource Group a name ![image](https://github.com/user-attachments/assets/73c752d0-868e-4542-b687-de9ca54259de)

5. Click **Review + Create**

## Create an Azure SQL resource
1. From the Home screen of the Azure Portal click **Create a resource** ![image](https://github.com/user-attachments/assets/c1e64aee-aa4c-4c42-9e98-df4a0fba38a7)
2. Search for **Azure SQL** ![image](https://github.com/user-attachments/assets/b3c333bf-3864-4e00-9f22-52b7ee7294a8)
3. Select **Azure SQL** ![image](https://github.com/user-attachments/assets/41a5283c-22dc-4f03-94f2-9de4df5b87d6)
4. Create a Single Database  ![image](https://github.com/user-attachments/assets/ea57664e-992c-4fb9-a78a-5252e95629a2)
5. Select the Resource Group you created earlier and type **sampleDB** for the name of the database (DO NOT click Review + Create yet) ![image](https://github.com/user-attachments/assets/ae6c390b-bd21-4184-915d-c4d86b8742a9)
6. Find the **Additional settings** tab and select **Sample** for the database contents ![image](https://github.com/user-attachments/assets/402e03a4-fef4-40fa-98f9-901473b0c16d)
7. Click **OK** the click the **Review and Create** tab and the **Create** button.
**NOTE: This will create a new Azure database server with a database called **sampleDB** with the AdventureworksLT data  

 




## Optional - create a Windows 11 VM 

1. Create a Windows 11 VM in the same subscription and VM as your SQL resources
   1. Select **Create a resource** from the Home screen of the Azure Portal
   1. Search for **Virtual Machine**
1. RDP to the Windows 11 VM 
1. Download and install SSMS
1. Download and install Visual Studio Code

## Create an Azure AI Foundry project
