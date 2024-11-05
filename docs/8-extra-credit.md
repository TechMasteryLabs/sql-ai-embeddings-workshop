# 8. Extra Credit Activities

## Chat history storage

Prompt data is something that companies and organizations will want to preserve for training, evaluation, and analytics. How well did it perform? How are customers using it? What questions are being asked. This data can also fall into the realm of high security. In this section of the lab, we will alter our stored procedure being used by Chainlit to store all prompts in a ledger table; more specifically an Append-only ledger table. Append-only ledger tables allow only INSERT operations on your tables, which ensure that privileged users such as database administrators can't alter data through traditional Data Manipulation Language operations.

1. First, we will create an Append-only ledger table. Run the following SQL in a blank query editor in VS Code:

    ```SQL
    create table dbo.PromptHistory
    (prompt_id bigint not null identity primary key,
    user_name nvarchar(100) not null,
    prompt nvarchar (max) not null)
    WITH (LEDGER = ON (APPEND_ONLY = ON)) ;
    ```


1. Next, we will alter our find_products stored procedure to insert all prompts into this ledger table. Run the following SQL in a blank query editor in VS Code:

    ```SQL
    create or alter procedure [dbo].[find_products]
    @text nvarchar(max),
    @top int = 10,
    @min_similarity decimal(19,16) = 0.80
    as
    if (@text is null) return;
    declare @retval int, @qv vector(1536);

    -- Insert into our ledger table
    begin
        insert into dbo.PromptHistory (user_name, prompt) values(USER_NAME(), @text);
        commit;
    end

    -- Continue with search
    exec @retval = dbo.create_embeddings @text, @qv output;
    if (@retval != 0) return;
    with vector_results as (
    SELECT 
            p.Name as product_name,
            ISNULL(p.Color,'No Color') as product_color,
            c.Name as category_name,
            m.Name as model_name,
            d.Description as product_description,
            p.ListPrice as list_price,
            p.weight as product_weight,
            vector_distance('cosine', @qv, p.embeddings) AS distance
    FROM
        [SalesLT].[Product] p,
        [SalesLT].[ProductCategory] c,
        [SalesLT].[ProductModel] m,
        [SalesLT].[vProductAndDescription] d
    where p.ProductID = d.ProductID
    and p.ProductCategoryID = c.ProductCategoryID
    and p.ProductModelID = m.ProductModelID
    and p.ProductID = d.ProductID
    and d.Culture = 'en')
    select TOP(@top) product_name, product_color, category_name, model_name, product_description, list_price, product_weight, distance
    from vector_results
    where (1-distance) > @min_similarity
    order by    
        distance asc;
    GO
    ```

1. Now, test the Chainlit application and query the ledger table. 

    In the application, ask the following question:

    ```TEXT
    do you sell black gloves?
    ```

    ![A picture of asking the chainlit application a question to be inserted into the ledger table](./media/Screenshot%202024-10-29%20at%209.18.19 AM.png)

    Now, run the following SQL in a blank query editor in VS Code:

    ```SQL
    select * from dbo.PromptHistory;
    ```

    ![A picture of querying the ledger table and seeing the question just asked in the prompt field.](./media/Screenshot%202024-10-29%20at%209.22.50 AM.png)

1. Can we update an Append-only ledger table? Run the following SQL in a blank query editor in VS Code:

    ```SQL
    update dbo.PromptHistory set prompt = 'do you sell any red golves?' where prompt_id = 1;
    ```

    No, we get the error "Msg 37359, Level 16, State 1, Line 1 Updates are not allowed for the append only Ledger table 'dbo.PromptHistory'."

    ![A picture of getting an error when trying to update an append only ledger table](./media/Screenshot%202024-10-29%20at%209.23.41 AM.png)