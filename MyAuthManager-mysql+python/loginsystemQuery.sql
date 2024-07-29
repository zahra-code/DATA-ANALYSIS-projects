--Create a database named logindatabase
CREATE DATABASE IF not EXISTS loginDatabase;
USE loginDatabase;

--table for storing users information
CREATE TABLE IF NOT EXISTS usernames_information(
      id INT primary key AUTO_INCREMENT,
      username VARCHAR(50) UNIQUE,
      email VARCHAR(50),
      password VARCHAR(50),
      signup_date DATETIME DEFAULT CURRENT_TIMESTAMP
);

--table for storing login information
CREATE TABLE IF NOT EXISTS login_information(
    login_id INT PRIMARY KEY auto_INCREMENT,
    user_id INT,
    username VARCHAR(50),
    login_date DATETIME DEFAULT CURRENT_TIMESTAMP
);

--table for storing deletrd accounts records
CREATE TABLE IF NOT EXISTS deleted_accounts_records(
    delete_id INT PRIMARY KEY AUTO_INCREMENT,
    acc_id INT,
    acc_name VARCHAR(50),
    gmail VARCHAR(50),
    create_date DATETIME,
    delete_date DATETIME default CURRENT_TIMESTAMP

)

--trigger for automatically filling user_id in login table from usernames_information table
create TRIGGER autofill_loginid_corresponding_to_user_info
BEFORE insert on login_information
FOR EACH ROW
BEGIN
    DECLARE usID INT;
    select id into usID
    from usernames_information where username=new.username;

    set new.user_id=usID;
end;

--trigger for automatically storing deleted accounts in deleted_accounts records
create TRIGGER saving_account_records_before_deleteing_an_account
BEFORE DELETE on usernames_information
FOR EACH ROW
BEGIN
    INSERT INTO deleted_accounts_records(acc_id,acc_name,gmail,create_date)
    VALUES(old.id,old.username,old.email,old.signup_date);
END;

select * from usernames_information;
select * from login_information;
SELECT* FROM deleted_accounts_records;
-- DROP DATABASE IF exists loginDatabase;