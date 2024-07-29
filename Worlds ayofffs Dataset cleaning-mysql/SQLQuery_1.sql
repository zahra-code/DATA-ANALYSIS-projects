--Create DATABASE world_layoffs
CREATE DATABASE IF NOT EXISTS world_layoffs;
--Create TABLE to import data from a .csv file
create TABLE if not exists layoffs(
    company varchar(50),
    location varchar(50),
    industry varchar(50),
    total_laid_off int,
    percentage_laid_off float(10,5),
    date varchar(50),
    stage VARCHAR(50),
    country varchar(50),
    funds_raised_millions int
);
--displaying raw data table layoffs
select * from layoffs;

--creating copy of data ,so that raw data should not be affected
CREATE table if not exists layoffs_copy
LIKE layoffs;

--Inserting data into layoffs_copy from original raw data table layoffs
INSERT layoffs_copy
select *
from layoffs;

--Displaying whole table layoffs_copy
select * from layoffs_copy;

--remove duplicates using CTE
WITH duplicate_cte as 
(
select *,
row_number()over
(PARTITION BY company,`location`,industry,total_laid_off,percentage_laid_off,`date`,stage,country,funds_raised_millions) as row_num
from layoffs_copy
)
delete 
from duplicate_cte 
where row_num>1
;

--Creating another table to store data after removing duplicates
create table layoffs_copy2
like layoffs_copy;
alter TABLE layoffs_copy2
add column row_num int;

insert into layoffs_copy2
select *,
row_number()over
(PARTITION BY company,`location`,industry,total_laid_off,percentage_laid_off,`date`,stage,country,funds_raised_millions) as row_num
from layoffs_copy;

delete 
from layoffs_copy2
where row_num>1;

--standardizing data
update layoffs_copy2
set company=trim(company);

update layoffs_copy2
set industry='Crypto'
where industry like 'Crypto%';

update layoffs_copy2
set country='United States'
where country like 'United States%';

update layoffs_copy2
set `date` =case
when date='NULL' then NULL
ELSE str_to_date(`date`,'%m/%d/%Y')
end;
alter table layoffs_copy2
modify column `date` DATE;

--Handling blanks and nulls
update layoffs_copy2 l1
join layoffs_copy2 l2
    on l1.company=l2.company and l1.location=l2.location
set l1.industry=l2.industry
where (l1.industry is null or l1.industry='')
and l2.industry is not null;

update layoffs_copy2 
set industry=NULL
where industry='null';

--droping unnecessary rows and columns

alter table layoffs_copy2
drop column row_num ;

delete
from layoffs_copy2
where total_laid_off is null and percentage_laid_off is null;

--EDA

ALTER TABLE layoffs_copy2
add COLUMN year int;

UPDATE layoffs_copy2
SET `year` = SUBSTRING(`date`, 1, 4);

alter table layoffs_copy2
drop column month;
ALTER TABLE layoffs_copy2
add COLUMN month varchar(50);

UPDATE layoffs_copy2
SET `month` = SUBSTRING(`date`, 1, 7);

select company,sum(total_laid_off) as total_laid
from layoffs_copy2
group by company
order by 2 desc;

SELECT company,sum(funds_raised_millions) total
from layoffs_copy2
GROUP by company
order by 2 desc;

SELECT industry,sum(total_laid_off) total
from layoffs_copy2
GROUP by industry 
order by 2 desc;

SELECT country,sum(total_laid_off) total
from layoffs_copy2
GROUP by country 
order by 2 desc;

SELECT min(date),max(date)
from layoffs_copy2;

with ranking_cte as
(select company,year,sum(total_laid_off) total_laid,
dense_rank()over(partition by year order by sum(total_laid_off) desc)as ranking
from layoffs_copy2
where total_laid_off is not null and `year` is not null
GROUP by company,year)
select * 
from ranking_cte
where year=2023 and ranking<=5 
;

with rolling_total as
(select month,sum(total_laid_off) total_laid
from layoffs_copy2
where month is not null
GROUP by month
order by 1)

select month,total_laid,sum(total_laid)over(order by month)as rolling_tot
from rolling_total
;

select sum(total_laid_off)
from layoffs_copy2;

select * 
from layoffs_copy2
where total_laid_off=(select max(total_laid_off) from layoffs_copy2);

update layoffs_copy2
set total_laid_off=0
where total_laid_off is null;

update layoffs_copy2
set percentage_laid_off=0
where percentage_laid_off is null;

--Cleaned Table layoffs_copy2
select * 
from layoffs_copy2;




