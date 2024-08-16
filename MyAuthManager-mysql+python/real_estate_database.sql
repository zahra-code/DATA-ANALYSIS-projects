--Creating a database for storing real estate data
CREATE DATABASE If NOT EXISTS real_estate_database;
USE real_estate_database;

CREATE TABLE IF NOT EXISTS housing_data
(
    property_id INT PRIMARY KEY AUTO_INCREMENT,
    country VARCHAR(20) DEFAULT "Pakistan",
    city VARCHAR(100),
    location VARCHAR(200),
    area varchar(100),
    bedrooms VARCHAR(50),
    price VARCHAR(100),
    property_type VARCHAR(20) DEFAULT "House",
    property_purpose VARCHAR(30),
    date DATETIME DEFAULT CURRENT_TIMESTAMP

);

SELECT * FROM housing_data;

--       CLEANINBG OF DATABASE

--Creating a dupklicated table so that the rew data remains unchanged
CREATE TABLE IF NOT housing_data_copy
LIKE housing_data;

INSERT INTO housing_data_copy
SELECT * FROM housing_data;

--Creatubg trigger to update the duplicated table as new data inserted in original housing_data table
CREATE TRIGGER update_copied_table
AFTER INSERT ON housing_data 
FOR EACH ROW 
BEGIN
    INSERT INTO housing_data_copy
    (property_id,country,city,location,area,bedrooms,price,property_type,property_purpose,date)
    VALUES
    (new.property_id,new.country,new.city,new.location,new.area,new.bedrooms,new.price,new.property_type,new.property_purpose,new.date);
END;
--Standarizing data and deleting duplicates trigger
CREATE TRIGGER cleaning_and_droping_duplicates_from_housing_data_copy
AFTER INSERT ON housing_data 
FOR EACH ROW 
BEGIN
    UPDATE housing_data_copy
    SET price=REPLACE(price,"PKR ",'')
    where price like "PKR%";

    UPDATE housing_data_copy h1
    JOIN housing_data_copy h2
        ON h1.city=h2.city and h1.location=h2.location AND h1.area=h2.area and h1.price=h2.price AND h1.property_purpose=h2.property_purpose 
    set h1.bedrooms=h2.bedrooms        
    where (h1.bedrooms="-" or h1.bedrooms is Null or h1.bedrooms=" ") and (h2.bedrooms!="-" or h2.bedrooms is not Null or h2.bedrooms!=" ");

    with CTE as
    (SELECT * ,
    Row_number()OVER(PARTITION BY city,location,area,bedrooms,price,property_purpose ORDER BY property_id)Row_num 
    FROM housing_data_copy)

    DELETE h1
    FROM housing_data_copy h1
    JOIN CTE ON CTE.property_id=h1.property_id
    where CTE.Row_num>1;
END;

-- update housing_data set city="Lahore" where city="lahorhh"
-- insert into housing_data
-- (city,location,area,bedrooms,price,property_purpose)
-- VALUES('Lahore','Jubilee Town - Block A, Jubilee Town','10 Marla','5','3.1 Crore','For Sale');

SELECT * FROM housing_data_copy;
SELECT count(*)TOTAL FROM housing_data_copy;
select count(*)TOTAL FROM housing_data;
