# 3. Creating embeddings for relational data

## Understanding embeddings in Azure OpenAI

An embedding is a special format of data representation that machine learning models and algorithms can easily use. The embedding is an information dense representation of the semantic meaning of a piece of text. Each embedding is a vector of floating-point numbers. Vector embeddings can help with semantic search by capturing the semantic similarity between terms. For example, "cat" and "kitty" have similar meanings, even though they are spelled differently. 

Embeddings created and stored in the Azure SQL Database during this lab will power a vector similarity search in a chat app you will build.

## The Azure OpenAI embeddings endpoint

1. Using an empty query sheet in VS Code, copy and paste the following code. This code calls an Azure OpenAI embeddings endpoint. The result will be a JSON array of vectors.

    ```SQL
    declare @url nvarchar(4000) = N'https://igniteai@lab.LabInstance.Id.openai.azure.com/openai/deployments/text-embedding-ada-002/embeddings?api-version=2024-06-01';
    declare @message nvarchar(max) = 'Hello World!';
    declare @payload nvarchar(max) = N'{"input": "' + @message + '"}';

    declare @ret int, @response nvarchar(max);

    exec @ret = sp_invoke_external_rest_endpoint 
        @url = @url,
        @method = 'POST',
        @payload = @payload,
        @credential = [https://igniteai@lab.LabInstance.Id.openai.azure.com/],
        @timeout = 230,
        @response = @response output;

    select @ret as ReturnCode, json_query(@response, '$.result.data[0].embedding') as "JSON Vector Array";
    ```

1. Again, click the run button on the query sheet. The result will be a JSON vector array.

    ![A picture of the JSON vector array as a result of the query](./media/Screenshot%202024-10-24%20at%2010.45.10 AM.png)

    Using the built in JSON function json_query, we are able to extract JSON array from REST response payloads. In the above T-SQL, json_query(@response, '$.result.data[0].embedding') as "JSON Vector Array" will extract the vector array from the result payload returned to us from the Azure OpenAI REST endpoint. 
    
    For reference, the JSON response message from the Azure OpenAI embeddings endpoint will look similar to the following and you can see how we extract the array found at **$.result.data[0].embedding**.

    > [!TIP]
    > **This code is for reference only** 

    ```JSON-nocopy
    {
        "response": {
            "status": {
                "http": {
                    "code": 200,
                    "description": ""
                }
            },
            "headers": {
                "Date": "Thu, 24 Oct 2024 19:32:59 GMT",
                "Content-Length": "33542",
                "Content-Type": "application/json",
                "access-control-allow-origin": "*",
                "apim-request-id": "ac67032f-41c1-4ec3-acc6-3f697c262764",
                "strict-transport-security": "max-age=31536000; includeSubDomains; preload",
                "x-content-type-options": "nosniff",
                "x-ms-region": "West US",
                "x-request-id": "84baf32d-f1f7-4183-9403-a95365d01a3e",
                "x-ms-client-request-id": "ac67032f-41c1-4ec3-acc6-3f697c262764",
                "x-ratelimit-remaining-requests": "349",
                "azureml-model-session": "d007-20240925154241",
                "x-ratelimit-remaining-tokens": "349994"
            }
        },
        "result": {
            "object": "list",
            "data": [
                {
                    "object": "embedding",
                    "index": 0,
                    "embedding": [
                        0.0023929428,
                        0.00034713413,
                        -0.0023142276,
                        -0.025654867,
                        -0.011492423,
                        0.0010358924,
                        -0.014836246,
                        0.0035484824,
                        0.000045630233,
                        -0.027581815,
                        0.023816079,
                        0.005012586,
                        -0.027732948,
                        -0.010088143,
                        ...
                        -0.014571763
                    ]
                }
            ],
            "model": "text-embedding-ada-002",
            "usage": {
                "prompt_tokens": 3,
                "total_tokens": 3
            }
        }
    }
    ```

    This JSON vector array can now be used with [new vector datatype](https://learn.microsoft.com/sql/t-sql/data-types/vector-data-type?view=azuresqldb-current&tabs=csharp-sample) and functions in the Azure SQL database such as [VECTOR_DISTANCE](https://learn.microsoft.com/sql/t-sql/functions/vector-distance-transact-sql?view=azuresqldb-current). 

## Preparing the database and creating embeddings

This next section of the lab will have you alter the Adventure Works product table to add a [new vector datatype](https://learn.microsoft.com/sql/t-sql/data-types/vector-data-type?view=azuresqldb-current&tabs=csharp-sample) column. You will then use a stored procedure to create embeddings for the products and store the vector arrays in that column.

1. In a new query sheet or an existing bank one in VS Code, copy and paste the following T-SQL:

    ```SQL
    alter table [SalesLT].[Product]
    add  embeddings VECTOR(1536), chunk nvarchar(2000);
    ```

    this code adds a vector datatype column to the Product table. It also adds a column named chunk where we will store the text we send over to the embeddings REST endpoint.

1. Then click the run button on the query sheet

    ![A picture of clicking the run button on the query sheet](./media/Screenshot%202024-10-24%20at%2010.49.00 AM.png)

1. Next, we are going to use the External REST Endpoint Invocation procedure (sp_invoke_external_rest_endpoint) to create a stored procedure that will create embeddings for text we supply as an input. Copy and paste the following code into a blank query editor in VS Code:

    ```SQL
    create or alter procedure dbo.create_embeddings
    (
        @input_text nvarchar(max),
        @embedding vector(1536) output
    )
    AS
    BEGIN
    declare @url varchar(max) = 'https://igniteai@lab.LabInstance.Id.openai.azure.com/openai/deployments/text-embedding-ada-002/embeddings?api-version=2024-06-01';
    declare @payload nvarchar(max) = json_object('input': @input_text);
    declare @response nvarchar(max);
    declare @retval int;

    -- Call to Azure OpenAI to get the embedding of the search text
    begin try
        exec @retval = sp_invoke_external_rest_endpoint
            @url = @url,
            @method = 'POST',
            @credential = [https://igniteai@lab.LabInstance.Id.openai.azure.com/],
            @payload = @payload,
            @response = @response output;
    end try
    begin catch
        select 
            'SQL' as error_source, 
            error_number() as error_code,
            error_message() as error_message
        return;
    end catch
    if (@retval != 0) begin
        select 
            'OPENAI' as error_source, 
            json_value(@response, '$.result.error.code') as error_code,
            json_value(@response, '$.result.error.message') as error_message,
            @response as error_response
        return;
    end
    -- Parse the embedding returned by Azure OpenAI
    declare @json_embedding nvarchar(max) = json_query(@response, '$.result.data[0].embedding');

    -- Convert the JSON array to a vector and set return parameter
    set @embedding = CAST(@json_embedding AS VECTOR(1536));
    END;
    ```

1. Click the run button on the query sheet to create the procedure in the database.

1. We have our embeddings procedure, now we can use it with data from the various products table. We are taking descriptive elements from each product and concatenating them into a single string to send to the embeddings endpoint. We construct this text string with the following SQL:

    > [!TIP]
    > **This code is for reference only** 

    ```SQL-nocopy
    SELECT p.Name + ' '+ ISNULL(p.Color,'No Color') + ' '+  c.Name + ' '+  m.Name + ' '+  d.Description
    FROM 
    [SalesLT].[Product] p,
    [SalesLT].[ProductCategory] c,
    [SalesLT].[ProductModel] m,
    [SalesLT].[vProductAndDescription] d
    where p.ProductCategoryID = c.ProductCategoryID
    and p.ProductModelID = m.ProductModelID
    and p.ProductID = d.ProductID
    and d.Culture = 'en'
    and p.ProductID = @ProductID
    ```
    
    Looking at the SQL, the text we are embedding contains the product name, product color (if available), the category name the product belongs to, the model name of the product, and the description of the product.

    
1. Run the following T-SQL in a blank query editor in VS Code to create embeddings for all products in the Products table:

    > [!Knowledge]
    > **This code will take from 10 to 20 seconds to run** 

    ```SQL
    SET NOCOUNT ON
    DROP TABLE IF EXISTS #MYTEMP 
    DECLARE @ProductID int
    declare @text nvarchar(max);
    declare @vector vector(1536);
    SELECT * INTO #MYTEMP FROM [SalesLT].Product
    SELECT @ProductID = ProductID FROM #MYTEMP
    SELECT TOP(1) @ProductID = ProductID FROM #MYTEMP
    WHILE @@ROWCOUNT <> 0
    BEGIN
        set @text = (SELECT p.Name + ' '+ ISNULL(p.Color,'No Color') + ' '+  c.Name + ' '+  m.Name + ' '+  ISNULL(d.Description,'')
                        FROM 
                        [SalesLT].[ProductCategory] c,
                        [SalesLT].[ProductModel] m,
                        [SalesLT].[Product] p
                        LEFT OUTER JOIN
                        [SalesLT].[vProductAndDescription] d
                        on p.ProductID = d.ProductID
                        and d.Culture = 'en'
                        where p.ProductCategoryID = c.ProductCategoryID
                        and p.ProductModelID = m.ProductModelID
                        and p.ProductID = @ProductID);
        exec dbo.create_embeddings @text, @vector output;
        update [SalesLT].[Product] set [embeddings] = @vector, [chunk] = @text where ProductID = @ProductID;
        DELETE FROM #MYTEMP WHERE ProductID = @ProductID
        SELECT TOP(1) @ProductID = ProductID FROM #MYTEMP
    END
    ```

1. To ensure all the embeddings were created, run the following code in a blank query editor in VS Code: 

    ```SQL
    select count(*) from SalesLT.Product where embeddings is null;
    ```

    You should get 0 for the result.

1. Run the next query in a blank query editor in VS Code to see the results of the above update to the Products table:

    ```SQL
    select top 10 chunk, embeddings from SalesLT.Product
    ```

    You can see that the chunk column is the combination of multiple data points about a product and the embeddings column contains the vector arrays.

    ![A picture of the query result showing the chunk and embeddings columns and their data.](./media/Screenshot%202024-10-24%20at%2011.02.59 AM.png)