# SQL Reference Guide

## What is a JOIN in SQL?
A JOIN combines rows from two or more tables based on a related column. The most common types are INNER JOIN (matching rows only), LEFT JOIN (all rows from the left table), RIGHT JOIN (all rows from the right table), and FULL OUTER JOIN (all rows from both tables).

## What is the difference between WHERE and HAVING?
WHERE filters rows before any grouping occurs. HAVING filters groups after a GROUP BY clause has been applied. Aggregate functions like COUNT or SUM can be used in HAVING but not in WHERE.

## What is a subquery?
A subquery is a query nested inside another query. It can appear in the SELECT, FROM, or WHERE clause. Subqueries can return a single value, a list of values, or a full table depending on context.

## What is a CTE?
A Common Table Expression (CTE) is a temporary named result set defined with the WITH clause. CTEs improve readability and can be referenced multiple times in the same query. Recursive CTEs can process hierarchical data.

## What is a window function?
A window function performs calculations across a set of rows related to the current row without collapsing them into a single output row. Common functions include ROW_NUMBER, RANK, DENSE_RANK, LAG, LEAD, and SUM OVER.

## What is the difference between RANK and DENSE_RANK?
RANK assigns the same rank to tied rows but skips the next rank (e.g., 1, 2, 2, 4). DENSE_RANK also assigns the same rank to ties but does not skip values (e.g., 1, 2, 2, 3).

## What is normalization?
Normalization is the process of organizing a relational database to reduce data redundancy and improve integrity. It involves dividing large tables into smaller ones and defining relationships. Normal forms range from 1NF to BCNF and beyond.

## What is an index in SQL?
An index is a data structure that improves query performance by allowing the database engine to locate rows faster. While indexes speed up SELECT queries, they add overhead to INSERT, UPDATE, and DELETE operations.

## What is the difference between UNION and UNION ALL?
UNION combines result sets from two queries and removes duplicate rows. UNION ALL combines result sets and retains all duplicates, making it faster when duplicates are acceptable or expected.

## What is a stored procedure?
A stored procedure is a precompiled collection of SQL statements saved in the database. It can accept parameters, execute logic, and return results. Stored procedures improve performance and allow reuse of complex logic.
