# 6. Data security and RAG

Next, let's work with some data level security features. Just because you are using RAG patterns with AI does not mean you no longer have control over your data; more so, what data is available to RAG, AI, and the application users.

For example, Adventure Works has a special product that they are offering only to employees. It can never show up as available for regular customers. So how can we restrict this data so that it cannot be bypassed by application code or AI searches? 

The answer is Row Level Security. Row-level security (RLS) enables you to use group membership or execution context to control access to rows in a database table. In this part of the lab, you will apply a policy on the products table that limits what data our aiuser can see when using our chat application. Seeing this policy is set on the user level and not at a level higher up in the application stack, it cannot be bypassed by removing application logic or direct connections to the database.

Row-level security (RLS) supports two types of security predicates:

* **Filter predicates** silently filter the rows available to read operations (SELECT, UPDATE, and DELETE).
* **Block predicates** explicitly block write operations (AFTER INSERT, AFTER UPDATE, BEFORE UPDATE, BEFORE DELETE) that violate the predicate.

For this lab, we will be working with Filter Predicates.

## Create a filter predicate

Filter predicates are applied while reading data from the base table so here is where we will block access to those employee only products. RLS filter predicates are functionally equivalent to appending a WHERE clause to a SQL statement. The predicate can be as sophisticated as business practices dictate or can be as simple as WHERE ProductId = 42.

1. Start by clicking the **SQL Extension** on the left side of Visual Studio Code.

    ![A picture of clicking Add Connection in the SQL Extension](instructions275758/Screenshot 2024-10-22 at 1.34.33 PM.png){300}

1. First, we need to create a inline table-valued function that will check to see which user is accessing the table and then blocking all products who have the category ID of 25. Run the following SQL in a blank query editor in VS Code:

    ```SQL
    CREATE or alter FUNCTION tvf_securitypredicate(@ProductCategoryID AS int)
        RETURNS TABLE
    WITH SCHEMABINDING
    AS
        RETURN SELECT 1 AS tvf_securitypredicate_result
        WHERE (@ProductCategoryID != 25 and USER_NAME() = 'aiuser') or (USER_NAME() != 'aiuser');
    GO
    ```

1. Next, we create a security policy adding the function you just created as a filter predicate. Note: The STATE must be set to ON to enable the policy. Run the following SQL in a blank query editor in VS Code:

    ```SQL
    CREATE SECURITY POLICY ProductFilter
    ADD FILTER PREDICATE dbo.tvf_securitypredicate(ProductCategoryID)
    ON [SalesLT].[ProductCategory]
    WITH (STATE = ON);
    GO
    ```

1. The last step is to ensure that the user or group has been granted the SELECT permissions to the tvf_securitypredicate function. Run the following SQL in a blank query editor in VS Code:

    ```SQL
    GRANT SELECT ON dbo.tvf_securitypredicate TO aiuser;
    ```

1. Now, test the filtering predicate by trying to select products which are in category 25 from the products table. This SQL will inpersonate the aiuser then we will run it as the connected sqladmin user. Run the following SQL in a blank query editor in VS Code:

    ```SQL
    EXECUTE AS USER = 'aiuser';
    SELECT  p.Name as product_name,
            ISNULL(p.Color,'No Color') as product_color,
            c.Name as category_name,        m.Name as model_name,
            d.Description as product_description,
            p.ListPrice as list_price,
            p.weight as product_weight
    FROM  [SalesLT].[Product] p,
        [SalesLT].[ProductCategory] c,
        [SalesLT].[ProductModel] m,
        [SalesLT].[vProductAndDescription] d
    WHERE p.ProductID = d.ProductID
    and p.ProductCategoryID = c.ProductCategoryID
    and p.ProductModelID = m.ProductModelID
    and p.ProductID = d.ProductID
    and d.Culture = 'en'
    and p.ProductCategoryID = 25;
    REVERT;
    ```

    Now, as sqladmin. Run the following SQL in a blank query editor in VS Code:

    ```SQL
    SELECT  p.Name as product_name,
            ISNULL(p.Color,'No Color') as product_color,
            c.Name as category_name,        m.Name as model_name,
            d.Description as product_description,
            p.ListPrice as list_price,
            p.weight as product_weight
    FROM  [SalesLT].[Product] p,
        [SalesLT].[ProductCategory] c,
        [SalesLT].[ProductModel] m,
        [SalesLT].[vProductAndDescription] d
    WHERE p.ProductID = d.ProductID
    and p.ProductCategoryID = c.ProductCategoryID
    and p.ProductModelID = m.ProductModelID
    and p.ProductID = d.ProductID
    and d.Culture = 'en'
    and p.ProductCategoryID = 25;
    ```

    | product_name | product_color | category_name | model_name | product_description | list_price | product_weight |
    |:---------|:---------|:---------|:---------|:---------|:---------|:---------|
    | Long-Sleeve Logo Jersey, S | Multi | Jerseys | Long-Sleeve Logo Jersey | Unisex long-sleeve AWC logo microfiber cycling jersey | 49.99 | NULL |
    | Long-Sleeve Logo Jersey, M | Multi | Jerseys | Long-Sleeve Logo Jersey | Unisex long-sleeve AWC logo microfiber cycling jersey | 49.99 | NULL |
    | Long-Sleeve Logo Jersey, L | Multi | Jerseys | Long-Sleeve Logo Jersey | Unisex long-sleeve AWC logo microfiber cycling jersey | 49.99 | NULL |
    | Long-Sleeve Logo Jersey, XL | Multi | Jerseys | Long-Sleeve Logo Jersey | Unisex long-sleeve AWC logo microfiber cycling jersey | 49.99 | NULL |
    | Short-Sleeve Classic Jersey, S | Yellow | Jerseys | Short-Sleeve Classic Jersey | Short sleeve classic breathable jersey with superior moisture control, front zipper, and 3 back pockets. | 53.99 | NULL |
    | Short-Sleeve Classic Jersey, M | Yellow | Jerseys | Short-Sleeve Classic Jersey | Short sleeve classic breathable jersey with superior moisture control, front zipper, and 3 back pockets. | 53.99 | NULL |
    | Short-Sleeve Classic Jersey, L | Yellow | Jerseys | Short-Sleeve Classic Jersey | Short sleeve classic breathable jersey with superior moisture control, front zipper, and 3 back pockets. | 53.99 | NULL |
    | Short-Sleeve Classic Jersey, XL | Yellow | Jerseys | Short-Sleeve Classic Jersey | Short sleeve classic breathable jersey with superior moisture control, front zipper, and 3 back pockets. | 53.99 | NULL |


1. As the aiuser, you no longer can see these products. Moving to our application, ask it the following question:

    ```TEXT
    do you sell any yellow jerseys?
    ```

    Previously, we were provided an answer as you saw in the last section. Now, we are told that it cannot find anything that matches that query.

    ![A picture of asking the question "Do you sell any yellow jerseys?" and not seeing any products because of the security policy.](instructions275758/Screenshot 2024-10-29 at 9.15.15 AM.png){1000}

    Using AI does not mean we have to compromise the security of our data; existing database security best practices still apply!