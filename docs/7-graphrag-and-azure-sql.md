# 7. Azure SQL and GraphRAG

GraphRAG aims to address the limitations of traditional Retrieval-Augmented Generation (RAG) methods, which often struggle with connecting disparate pieces of information and understanding large documents. By leveraging structured knowledge graphs, GraphRAG provides substantial improvements in question-and-answer performance, especially with private datasets that the LLM hasn't been trained on.

## What is a Graph Database?

A graph database is a collection of nodes (or vertices) and edges (or relationships). A node represents an entity (for example, a person or an organization) and an edge represents a relationship between the two nodes that it connects (for example, likes or friends).

## Overview

In this part of the lab, we will be creating a graph in the Azure SQL database based on the Adventure Works data. The situation is we want to create a bike configurator that can help suggest a frame, tires, and accessories using similarity searches and the relationships in the graph. The node tables will also contain embeddings so that we can do vector similarity searches.

## Creating the nodes and edges

Our graph will have 3 node tables. They will contain tires, bike frames and bike accessories. The edge tables will contain relationships between the frames and corresponding tires and accessories, helping to retrieve matching parts.

1. Run the following SQL in a blank query editor in VS Code:

    ```SQL
    CREATE TABLE BikeTires
    (
        ID INTEGER not null identity primary key,
        product_id int,
        category_id int,
        embeddings VECTOR(1536)
    ) AS NODE;

    CREATE TABLE BikeFrame
    (
        ID INTEGER not null identity primary key,
        product_id int,
        category_id int,
        embeddings VECTOR(1536)
    ) AS NODE;

    CREATE TABLE BikeAccessory
    (
        ID INTEGER not null identity primary key,
        product_id int,
        category_id int,
        embeddings VECTOR(1536)
    ) AS NODE;

    CREATE TABLE Tires AS EDGE;
    CREATE TABLE Accessory AS EDGE;
    ```

1. Next, we need to insert the parts we want to include in the node tables and create the embeddings for our vector searches.


    First, the Bike Frame Node. Run the following SQL in a blank query editor in VS Code:

    ```SQL
    SET NOCOUNT ON
    DROP TABLE IF EXISTS #MYTEMP 
    DECLARE @ProductID int
    DECLARE @CategoryID int
    declare @text nvarchar(max);
    declare @vector vector(1536);
    SELECT * INTO #MYTEMP FROM [SalesLT].Product where ProductCategoryID IN (16,18,20);
    SELECT @ProductID = ProductID FROM #MYTEMP
    SELECT TOP(1) @ProductID = ProductID FROM #MYTEMP
    WHILE @@ROWCOUNT <> 0
    BEGIN
        SELECT TOP(1) @CategoryID = ProductCategoryID FROM #MYTEMP;
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
        insert into BikeFrame (product_id, category_id, embeddings) values (@ProductID,@CategoryID, @vector);
        DELETE FROM #MYTEMP WHERE ProductID = @ProductID
        SELECT TOP(1) @ProductID = ProductID FROM #MYTEMP
    END
    ```

    Next, the Bike Tires. Run the following SQL in a blank query editor in VS Code:

    ```SQL
    SET NOCOUNT ON
    DROP TABLE IF EXISTS #MYTEMP 
    DECLARE @ProductID int
    DECLARE @CategoryID int
    declare @text nvarchar(max);
    declare @vector vector(1536);
    SELECT * INTO #MYTEMP FROM [SalesLT].Product where ProductCategoryID IN (21,41);
    SELECT @ProductID = ProductID FROM #MYTEMP
    SELECT TOP(1) @ProductID = ProductID FROM #MYTEMP
    WHILE @@ROWCOUNT <> 0
    BEGIN
        SELECT TOP(1) @CategoryID = ProductCategoryID FROM #MYTEMP;
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
        insert into BikeTires (product_id, category_id, embeddings) values (@ProductID,@CategoryID, @vector);
        DELETE FROM #MYTEMP WHERE ProductID = @ProductID
        SELECT TOP(1) @ProductID = ProductID FROM #MYTEMP
    END
    ```

    And last, the bike accessory node. Run the following SQL in a blank query editor in VS Code:

    ```SQL
    SET NOCOUNT ON
    DROP TABLE IF EXISTS #MYTEMP 
    DECLARE @ProductID int
    DECLARE @CategoryID int
    declare @text nvarchar(max);
    declare @vector vector(1536);
    SELECT * INTO #MYTEMP FROM [SalesLT].Product where ProductCategoryID IN (32,19,17,8);
    SELECT @ProductID = ProductID FROM #MYTEMP
    SELECT TOP(1) @ProductID = ProductID FROM #MYTEMP
    WHILE @@ROWCOUNT <> 0
    BEGIN
        SELECT TOP(1) @CategoryID = ProductCategoryID FROM #MYTEMP;
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
        insert into BikeAccessory (product_id, category_id, embeddings) values (@ProductID,@CategoryID, @vector);
        DELETE FROM #MYTEMP WHERE ProductID = @ProductID
        SELECT TOP(1) @ProductID = ProductID FROM #MYTEMP
    END
    ```

1. The next task is to create relationships in the edge tables. We will start with the frame to tires relationships. Run the following SQL in a blank query editor in VS Code:

    ```SQL
    with cte (frame_node, tire_node) as (
        select distinct B.$node_id, 
                        T.$node_id 
        from BikeFrame B, 
            BikeTires T
        where T.product_id in (815, 816, 817, 823, 824, 825, 928, 929, 930, 921, 873)
        and B.category_id = 16)
    insert into Tires 
    select frame_node,tire_node from cte;

    with cte (frame_node, tire_node) as (
        select distinct B.$node_id, 
                        T.$node_id 
        from BikeFrame B, 
            BikeTires T
        where T.product_id in (818, 826, 931, 932, 933, 922, 873)
        and B.category_id = 18)
    insert into Tires 
    select frame_node,tire_node from cte;

    with cte (frame_node, tire_node) as (
        select distinct B.$node_id, 
                        T.$node_id 
        from BikeFrame B, 
            BikeTires T
        where T.product_id in (829, 821, 934, 923, 873)
        and B.category_id = 20)
    insert into Tires
    select frame_node,tire_node from cte;
    ```

1. Now, the frame to accessories relationships. Run the following SQL in a blank query editor in VS Code:

    ```SQL
    with cte (frame_node, accessory_node) as (
        select distinct B.$node_id, 
                        T.$node_id 
        from BikeFrame B, 
            BikeAccessory T
        where T.product_id in (908, 909, 910, 871, 935, 936, 937, 808, 809, 810)
        and B.category_id = 16)
    insert into Accessory 
    select frame_node, accessory_node from cte;

    with cte (frame_node, accessory_node) as (
        select distinct B.$node_id, 
                        T.$node_id 
        from BikeFrame B, 
            BikeAccessory T
        where T.product_id in (911, 912, 913, 872, 938, 939, 940, 811, 812, 813)
        and B.category_id = 18)
    insert into Accessory 
    select frame_node, accessory_node from cte;

    with cte (frame_node, accessory_node) as (
        select distinct B.$node_id, 
                        T.$node_id 
        from BikeFrame B, 
            BikeAccessory T
        where T.product_id in (914, 915, 916, 870, 941, 946, 947)
        and B.category_id = 20)
    insert into Accessory
    select frame_node, accessory_node from cte;
    ```

1. With the nodes and edges done, and the embeddings created, lets query the database to find us a mountain bike frame and matching parts. Run the following SQL in a blank query editor in VS Code:

    ```SQL
    declare @search_text nvarchar(max) = 'I am looking for a mountain bike configuration for the trail riding';
    declare @search_vector vector(1536);
    DROP TABLE #MYTEMPGRAPH;
    exec dbo.create_embeddings @search_text, @search_vector output;
    declare @frame_id INT = (SELECT TOP(1) p.product_id
        FROM BikeFrame p
        ORDER BY vector_distance('cosine', @search_vector, p.embeddings) );

    -- add the frame details
    SELECT 
            p.Name as product_name,
            ISNULL(p.Color,'No Color') as product_color,
            c.Name as category_name,
            m.Name as model_name,
            d.Description as product_description,
            p.ListPrice as list_price,
            p.weight as product_weight,
            vector_distance('cosine', @search_vector, p.embeddings) AS distance
            INTO #MYTEMPGRAPH
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
    and p.ProductID = @frame_id;

    -- get top X tires
    with tireCTE (product_id) as (select top(4) BikeTires.product_id
    from BikeFrame, Tires, BikeTires
    where MATCH(BikeFrame-(Tires)->BikeTires)
    and BikeFrame.product_id = @frame_id
    ORDER BY vector_distance('cosine', @search_vector, BikeTires.embeddings))
    INSERT INTO #MYTEMPGRAPH
    SELECT 
            p.Name as product_name,
            ISNULL(p.Color,'No Color') as product_color,
            c.Name as category_name,
            m.Name as model_name,
            d.Description as product_description,
            p.ListPrice as list_price,
            p.weight as product_weight,
            vector_distance('cosine', @search_vector, p.embeddings) AS distance
    FROM
        [SalesLT].[ProductCategory] c,
        [SalesLT].[ProductModel] m,
        tireCTE tireCTE,
        [SalesLT].[Product] p
        LEFT OUTER JOIN
        [SalesLT].[vProductAndDescription] d
        on p.ProductID = d.ProductID
        and d.Culture = 'en'    
    where p.ProductCategoryID = c.ProductCategoryID
    and p.ProductModelID = m.ProductModelID
    and tireCTE.product_id = p.ProductID;


    -- get top X accessories

    with accCTE (product_id) as (select top(10) BikeAccessory.product_id
    from BikeFrame, Accessory, BikeAccessory
    where MATCH(BikeFrame-(Accessory)->BikeAccessory)
    and BikeFrame.product_id = @frame_id
    ORDER BY vector_distance('cosine', @search_vector, BikeAccessory.embeddings))
    INSERT INTO #MYTEMPGRAPH
    SELECT 
            p.Name as product_name,
            ISNULL(p.Color,'No Color') as product_color,
            c.Name as category_name,
            m.Name as model_name,
            d.Description as product_description,
            p.ListPrice as list_price,
            p.weight as product_weight,
            vector_distance('cosine', @search_vector, p.embeddings) AS distance
    FROM
        [SalesLT].[ProductCategory] c,
        [SalesLT].[ProductModel] m,
        accCTE accCTE,
        [SalesLT].[Product] p
        LEFT OUTER JOIN
        [SalesLT].[vProductAndDescription] d
        on p.ProductID = d.ProductID
        and d.Culture = 'en'    
    where p.ProductCategoryID = c.ProductCategoryID
    and p.ProductModelID = m.ProductModelID
    and accCTE.product_id = p.ProductID;

    WITH RankedItems AS (
        select * ,
            ROW_NUMBER() OVER (PARTITION BY category_name ORDER BY distance) AS rn
        FROM 
            #MYTEMPGRAPH
    )
    SELECT 
        *
    FROM 
        RankedItems
    WHERE 
        rn <= 4
    order by category_name, distance;
    ```

    With the results being similar to the following:

    | product_name | product_color | category_name | model_name | product_description | list_price | product_weight | distance
    |:---------|:---------|:---------|:---------|:---------|:---------|:---------|:---------|
    | Mountain Bottle Cage | No Color | Bottles and Cages | Mountain Bottle Cage | Tough aluminum cage holds bottle securly on tough terrain. | 9.99 | NULL | 0.20920676313715192 | 1 |
    | HL Mountain Handlebars | No Color | Handlebars | HL Mountain Handlebars | Flat bar strong enough for the pro circuit. | 120.27 | NULL | 0.19550746040424205 | 1 |
    | ML Mountain Handlebars | No Color | Handlebars | ML Mountain Handlebars | Tough aluminum alloy bars for downhill. | 61.92 | NULL | 0.1956435861276451 | 2 |
    | LL Mountain Handlebars | No Color | Handlebars | LL Mountain Handlebars | All-purpose bar for on or off-road. | 44.54 | NULL | 0.20118043374007089 | 3 |
    | HL Mountain Frame - Black, 38 | Black | Mountain Frames | HL Mountain Frame | Each frame is hand-crafted in our Bothell facility to the optimum diameter and wall-thickness required of a premium mountain frame. The heat-treated welded aluminum frame has a larger diameter tube that absorbs the bumps. | 1349.60 | 1215.62 | 0.19637531926307394 | 1 |
    | LL Mountain Pedal | Silver/Black | Pedals | LL Mountain Pedal | Expanded platform so you can ride in any shoes; great for all-around riding. | 40.49 | 218.00 | 0.1917491860753906 | 1 |
    | ML Mountain Pedal | Silver/Black | Pedals | ML Mountain Pedal | Lightweight, durable, clipless pedal with adjustable tension. | 62.09 | 215.00 | 0.19631826597584334 | 2 |
    | HL Mountain Pedal | Silver/Black | Pedals | HL Mountain Pedal | Stainless steel; designed to shed mud easily. | 80.99 | 185.00 | 0.2100401247410475 | 3 |
    | ML Mountain Seat/Saddle | No Color | Saddles | ML Mountain Seat/Saddle 2 | Designed to absorb shock. | 39.14 | NULL | 0.20531089111677991 | 1 |
    | HL Mountain Seat/Saddle | No Color | Saddles | HL Mountain Seat/Saddle 2 | Anatomic design for a full-day of riding in comfort. Durable leather. | 52.64 | NULL | 0.2054324642746579 | 2 |
    | LL Mountain Seat/Saddle | No Color | Saddles | LL Mountain Seat/Saddle 2 | Synthetic leather. Features gel for increased comfort. | 27.12 | NULL | 0.21854078868800952 | 3 |
    | HL Mountain Tire | No Color | Tires and Tubes | HL Mountain Tire | Incredible traction, lightweight carbon reinforced. | 35.00 | NULL | 0.20503153552308662 | 1 |
    | ML Mountain Tire | No Color | Tires and Tubes | ML Mountain Tire | Great traction, high-density rubber. | 29.99 | NULL | 0.21246534623134783 | 2 |
    | LL Mountain Tire | No Color | Tires and Tubes | LL Mountain Tire | Comparible traction, less expensive wire bead casing. | 24.99 | NULL | 0.22264953577992153 | 3 |
    | Mountain Tire Tube | No Color | Tires and Tubes | Mountain Tire Tube | Self-sealing tube. | 4.99 | NULL | 0.22423332763644688 | 4 |
    | ML Mountain Rear Wheel | Black | Wheels | ML Mountain Rear Wheel | Replacement mountain wheel for the casual to serious rider. | 236.025 | NULL | 0.17473628887091464 | 1 |
    | LL Mountain Rear Wheel | Black | Wheels | LL Mountain Rear Wheel | Replacement mountain wheel for entry-level rider. | 87.745 | NULL | 0.17751845404738964 | 2 |
    | ML Mountain Front Wheel | Black | Wheels | ML Mountain Front Wheel | Replacement mountain wheel for the casual to serious rider. | 209.025 | NULL | 0.17901706764557435 | 3 |
    | LL Mountain Front Wheel | Black | Wheels | LL Mountain Front Wheel | Replacement mountain wheel for entry-level rider. | 60.745 | NULL | 0.1817263114704344 | 4 |

1. Let's see if we can get our chat application to help us configure a bike! We need to alter the find_products stored procedure to use the graph in the database. Run the following SQL in a blank query editor in VS Code:

    ```SQL
    create or alter procedure [dbo].[find_products]
    @text nvarchar(max),
    @top int = 15,
    @min_similarity decimal(19,16) = 0.70
    as
    if (@text is null) return;
    declare @retval int, @search_vector vector(1536);
    DROP TABLE IF EXISTS #MYTEMPPROC;
    exec @retval = dbo.create_embeddings @text, @search_vector output;
    if (@retval != 0) return;
    declare @frame_id INT = (SELECT TOP(1) p.product_id
        FROM BikeFrame p
        ORDER BY vector_distance('cosine', @search_vector, p.embeddings));
    SELECT 
            p.Name as product_name,
            ISNULL(p.Color,'No Color') as product_color,
            c.Name as category_name,
            m.Name as model_name,
            d.Description as product_description,
            p.ListPrice as list_price,
            p.weight as product_weight,
            vector_distance('cosine', @search_vector, p.embeddings) AS distance
            INTO #MYTEMPPROC
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
    and p.ProductID = @frame_id;

    -- get top X tires
    with tireCTE (product_id) as (select top(4) BikeTires.product_id
    from BikeFrame, Tires, BikeTires
    where MATCH(BikeFrame-(Tires)->BikeTires)
    and BikeFrame.product_id = @frame_id
    ORDER BY vector_distance('cosine', @search_vector, BikeTires.embeddings))
    INSERT INTO #MYTEMPPROC
    SELECT 
            p.Name as product_name,
            ISNULL(p.Color,'No Color') as product_color,
            c.Name as category_name,
            m.Name as model_name,
            d.Description as product_description,
            p.ListPrice as list_price,
            p.weight as product_weight,
            vector_distance('cosine', @search_vector, p.embeddings) AS distance
    FROM
        [SalesLT].[ProductCategory] c,
        [SalesLT].[ProductModel] m,
        tireCTE tireCTE,
        [SalesLT].[Product] p
        LEFT OUTER JOIN
        [SalesLT].[vProductAndDescription] d
        on p.ProductID = d.ProductID
        and d.Culture = 'en'    
    where p.ProductCategoryID = c.ProductCategoryID
    and p.ProductModelID = m.ProductModelID
    and tireCTE.product_id = p.ProductID;


    -- get top X accessories

    with accCTE (product_id) as (select top(10) BikeAccessory.product_id
    from BikeFrame, Accessory, BikeAccessory
    where MATCH(BikeFrame-(Accessory)->BikeAccessory)
    and BikeFrame.product_id = @frame_id
    ORDER BY vector_distance('cosine', @search_vector, BikeAccessory.embeddings))
    INSERT INTO #MYTEMPPROC
    SELECT 
            p.Name as product_name,
            ISNULL(p.Color,'No Color') as product_color,
            c.Name as category_name,
            m.Name as model_name,
            d.Description as product_description,
            p.ListPrice as list_price,
            p.weight as product_weight,
            vector_distance('cosine', @search_vector, p.embeddings) AS distance
    FROM
        [SalesLT].[ProductCategory] c,
        [SalesLT].[ProductModel] m,
        accCTE accCTE,
        [SalesLT].[Product] p
        LEFT OUTER JOIN
        [SalesLT].[vProductAndDescription] d
        on p.ProductID = d.ProductID
        and d.Culture = 'en'    
    where p.ProductCategoryID = c.ProductCategoryID
    and p.ProductModelID = m.ProductModelID
    and accCTE.product_id = p.ProductID;
    with vector_results as (

        select * ,
            ROW_NUMBER() OVER (PARTITION BY category_name ORDER BY category_name, distance) AS rn
        FROM 
            #MYTEMPPROC
    )
    select TOP(@top) product_name, product_color, category_name, model_name, product_description, list_price, product_weight, distance
    from vector_results
    where (1-distance) > @min_similarity
    and rn <= 4
    order by    
        distance asc;
    GO
    ```

1. Back in the Chainlit application, ask the following question:

    ```TEXT
    I am looking for a touring bike configuration for casual riding. I want a yellow bike
    ```

    ```TEXT
    I am looking for a mountain bike configuration for trail riding
    ```

    and see what bike was configured for you!

    ![A picture of the bike configured via GraphRAG](instructions275758/Screenshot 2024-10-30 at 10.09.16 AM.png){1000}

1. Try other configurations!

    ```TEXT
    Im looking for a road bike configuration that I can race with.
    ```
