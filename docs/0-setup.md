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
   1. Search for **Virtual Machine** ![image](https://github.com/user-attachments/assets/7db852f0-42c2-4657-aad4-b37617399848)
   2. Name your VM and select the **Windows 11 Pro** image ![image](https://github.com/user-attachments/assets/002a10a6-bc84-4ac1-b173-aaf6183a75a2)
   3. Provide a username and password for your VM. ![image](https://github.com/user-attachments/assets/3b3295cd-aae6-4f82-b1e7-cb177ca3f316) **NOTE: the password must be 12 characters or more**
   4. Click **Review + Create** and wait for the VM to be provisioned
  
1. RDP to the Windows 11 VM
   1. Click **Connect** ![image](https://github.com/user-attachments/assets/1f0441b0-76ce-4187-83c6-72753547d66a)
   2. Under **Native RDP** click **Select** ![image](https://github.com/user-attachments/assets/ab3f8c84-4553-4798-8e9d-eac097451cca)
   3. Wait for the validation and then check the box that explains the **Just in time policy** ![image](https://github.com/user-attachments/assets/52c26d69-c4d3-480e-a992-47c2d54476f0)
   4. Click the **configure** button  ![image](https://github.com/user-attachments/assets/68ed4abc-62cb-4698-badc-10b5cf6fdd99)
   5. Click **Download RDP File** and select **Keep**  ![image](https://github.com/user-attachments/assets/1a6c2b7b-eca7-4b08-9dab-c4e35ce88934)
   6. Open your new RDP file by clicking **Open File** and select **Connect** ![image](https://github.com/user-attachments/assets/01c63b2d-0496-4aa8-b29b-82dfd14bcd8e)
   7. NOTE: You may need to examine your VPN settings and try a few times to connect.  Eentually you will get to a dialog box where you can type in the password for the VM  ![image](https://github.com/user-attachments/assets/80e7af1f-90b5-46c5-b904-057698ed7cd8)
   8. Click **Yes** ![image](https://github.com/user-attachments/assets/cbab34d7-8020-468b-8ff3-92bc43751a95)
   9. You will then get access to the VM Desktop ![image](https://github.com/user-attachments/assets/a0b857d3-12f5-4eaa-8717-6f2bcc5e6b46)

1. Download and install SSMS ![image](https://github.com/user-attachments/assets/856ffaf2-e515-47fc-93f3-0e5f040f3071)
   
1. Download and Install the Azure CLI ![image](https://github.com/user-attachments/assets/cac0b32d-da33-4cdd-81dc-2ad9d534100a)

1. Download and install Visual Studio Code ![image](https://github.com/user-attachments/assets/23594cfb-0a78-45a2-a005-9486e3cfc5c6)


## Create an Azure AI Foundry project
