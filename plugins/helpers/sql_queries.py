class SQLQueries:
    create_staging_restaurants_table = """
        CREATE TABLE IF NOT EXISTS public.staging_restaurants (
            url VARCHAR(2048),
            address VARCHAR(512),
            name VARCHAR(256),
            online_order VARCHAR(8),
            book_table VARCHAR(8),
            rate VARCHAR(256),
            votes VARCHAR(256),
            phone VARCHAR(64),
            location VARCHAR(512),
            rest_type VARCHAR(256),
            dish_liked VARCHAR(512),
            cuisines VARCHAR(256),
            approx_cost_for_two_people VARCHAR(256),
            listed_in_type VARCHAR(64),
            listed_in_city VARCHAR(64)
        );
        """

    create_sales_table = """
        CREATE TABLE IF NOT EXISTS public.sales (
            id INT IDENTITY(1,1) PRIMARY KEY,
            restaurant_id INT4,
            rating_id INT4,
            order_id INT4,
            sale_id INT4,
            cost NUMERIC
        )
        DISTSTYLE AUTO
        SORTKEY(id);
        """

    create_orders_table = """
        CREATE TABLE IF NOT EXISTS public.orders (
            id INT IDENTITY(1,1) PRIMARY KEY,
            online_order BOOL,
            book_table BOOL,
            dish_liked VARCHAR(512),
            url VARCHAR(2048)
        )
        DISTSTYLE AUTO
        SORTKEY(id);
        """

    create_restaurant_table = """
        CREATE TABLE IF NOT EXISTS public.restaurants (
            id INT IDENTITY(1,1) PRIMARY KEY,
            name VARCHAR(256),
            url VARCHAR(2048),
            address VARCHAR(512),
            phone VARCHAR(64),
            location VARCHAR(256),
            rest_type VARCHAR(256),
            listed_in_type VARCHAR(64),
            listed_in_city VARCHAR(64),
            cuisines VARCHAR(256)
        )
        DISTSTYLE AUTO
        SORTKEY(id);
        """

    # create_dates_table = (
    #     """
    #     CREATE TABLE IF NOT EXISTS public.dates(
    #         id INT IDENTITY(1,1) PRIMARY KEY,
    #         "hour" INT4,
    #         "day" INT4,
    #         week INT4,
    #         "month" VARCHAR(256),
    #         "year" INT4
    #     )
    #     """
    # )

    create_ratings_table = """
        CREATE TABLE IF NOT EXISTS public.ratings (
            id INT IDENTITY(1,1) PRIMARY KEY,
            votes INT4,
            rating NUMERIC,
            url VARCHAR(2048)
        )
        DISTSTYLE AUTO
        SORTKEY(id);
    """

    # dates_table_insert = (
    #     """
    #     """
    # )

    ratings_table_insert = """
        INSERT INTO public.ratings (votes, rating, url)
        SELECT 
            CAST(votes AS INT) as votes, 
            CAST(SPLIT_PART(rate, '/', 1) AS NUMERIC) as rating, url
        FROM staging_restaurants limit 10;
        """

    restaurants_table_insert = """
        INSERT INTO public.restaurants (
            name,
            url,
            address,
            phone,
            location,
            rest_type,
            listed_in_type,
            listed_in_city,
            cuisines
        )
        SELECT
            name,
            url,
            address,
            phone,
            location,
            rest_type,
            listed_in_type,
            listed_in_city,
            cuisines
        FROM
            staging_restaurants
        """

    orders_table_insert = """
        INSERT INTO public.orders (online_order, book_table, dish_liked, url)
        SELECT
            CASE online_order WHEN 'Yes' THEN 1 ELSE 0 END AS online_order,
            CASE book_table WHEN 'Yes' THEN 1 ELSE 0 END AS book_table,
            dish_liked,
            url
        FROM
            staging_restaurants
        """

    sales_table_insert = """
        INSERT INTO public.sales (restaurant_id, rating_id, order_id, cost)
        SELECT
            r.id as restaurant_id,
            rt.id as rating_id,
            o.id as order_id,
            CAST(REPLACE(sr.approx_cost_for_two_people, ',','') AS NUMERIC) as cost
        FROM public.staging_restaurants AS sr
        LEFT JOIN public.restaurants AS r ON sr.url = r.url
        LEFT JOIN public.orders AS o ON sr.url = o.url
        LEFT JOIN public.ratings AS rt ON sr.url = rt.url
        """

    restaurants_count_test = """
        SELECT COUNT(*)
        FROM public.restaurants
        """

    sales_count_test = """
        SELECT COUNT(*)
        FROM public.sales
        """

    orders_count_test = """
        SELECT COUNT(*)
        FROM public.orders
        """

    sales_count_test = """
        SELECT COUNT(*)
        FROM public.sales
        """

    ratings_count_test = """
        SELECT COUNT(*)
        FROM public.ratings
        """
