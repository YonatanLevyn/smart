# Database Documentation for Smart Platform 

## Overview
This document outlines the role of PostgreSQL in our Django project, compares it with other database options like SQLite and Redis, 
and discusses future considerations for database selection.

### Why PostgreSQL?

PostgreSQL is a powerful, open-source object-relational database system known for its robustness, scalability, and compliance with SQL standards. It offers advanced features such as:
- Complex queries
- Foreign keys
- Triggers
- Updatable views
- Transactional integrity
- Multiversion concurrency control

# Database Features Explained 

## Complex Queries

**Definition:** Complex queries allow for advanced data retrieval, involving multiple conditions, joins, subqueries, and aggregations.

**Example:** Retrieving names of students with an average grade above 90.

```sql
SELECT students.name
FROM students
JOIN grades ON students.id = grades.student_id
GROUP BY students.name
HAVING AVG(grades.score) > 90;
```

# Foreign Keys 

Foreign keys create a crucial link between two tables in a database, ensuring the integrity of the data by enforcing relationships between these tables.

## Example
Consider a database for a school system, where you have a `students` table and a `grades` table. Each grade record needs to be associated with a student. To enforce this relationship and ensure that no grade is recorded without a corresponding student, a foreign key can be used:

```sql
CREATE TABLE grades (
  id SERIAL PRIMARY KEY,
  score INT NOT NULL,
  student_id INT,
  FOREIGN KEY (student_id) REFERENCES students(id)
);
```

# Triggers 

Triggers are special procedures that are automatically executed or fired when specific database operations occur, such as insert, update, or delete actions. They are used to maintain data integrity and implement complex business logic automatically.

## Example
Imagine you have a `students` table, and you want to track whenever a student's information is updated. You can use a trigger to automatically update a `last_updated` timestamp field in the `students` table.

First, ensure your `students` table has a `last_updated` column:
```sql
ALTER TABLE students ADD COLUMN last_updated TIMESTAMP;
CREATE OR REPLACE FUNCTION update_student_last_updated()
RETURNS TRIGGER AS $$
BEGIN
    NEW.last_updated = NOW(); -- Set the last_updated column to the current time
    RETURN NEW; -- Return the updated record
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER students_before_update
BEFORE UPDATE ON students
FOR EACH ROW
EXECUTE FUNCTION update_student_last_updated();
```

# Updatable Views 

Updatable views in databases allow you to perform insert, update, or delete operations on views that are normally read-only. A view is essentially a stored query visible as a virtual table composed of result sets from one or more tables. Making a view updatable means you can modify data through it, indirectly affecting the base tables.

Example:
Imagine you have a database for a bookstore with tables for books and authors. You create a view to simplify accessing book titles along with their authors' names. To allow updates on this view directly, ensuring changes reflect in the underlying tables, you could define an updatable view (depending on your DBMS support and specific syntax):

To create an updatable view, you can use the following SQL statement:

```sql
CREATE VIEW book_info AS
SELECT books.title, authors.name
FROM books
JOIN authors ON books.author_id = authors.id;
```

To update a book title through the book_info view:

```sql
UPDATE book_info
SET title = 'New Book Title'
WHERE name = 'Author Name';
```

# Transactional Integrity 
Transactional integrity, often part of the ACID properties (Atomicity, Consistency, Isolation, Durability) of database systems, ensures that all parts of a database transaction are completed successfully. If any part of the transaction fails, the entire transaction is rolled back, leaving the database in its initial state before the transaction began. This concept is crucial for maintaining data accuracy and consistency.

Example:
Consider an online banking system where a transaction involves transferring money from one account to another. This process would typically involve two steps: debiting an amount from the sender's account and crediting it to the recipient's account.

```sql
BEGIN TRANSACTION;

-- Step 1: Deduct amount from sender's account
UPDATE accounts SET balance = balance - 100 WHERE account_id = 1;

-- Step 2: Add amount to recipient's account
UPDATE accounts SET balance = balance + 100 WHERE account_id = 2;

-- Commit the transaction if both steps are successful
COMMIT TRANSACTION;
```
If either step fails, for instance, due to a violation of data integrity rules (like not allowing negative balances), the entire transaction is rolled back:
```sql
ROLLBACK TRANSACTION;
```
This rollback prevents incomplete operations, such as money being taken from one account without being deposited into another, 
ensuring transactional integrity.


### Data Storage Locations and Types

#### SQLite (File-based Database)
- Stores the entire database as a single file on disk.
- Ideal for smaller projects, embedded systems, or local storage in applications.
- Offers simplicity and portability but lacks scalability for high-concurrency applications.

#### Redis (In-memory Database)
- An in-memory data structure store used as a database, cache, and message broker.
- Data is stored in RAM, offering low latency and high throughput.
- Best for caching, session management, and temporary data storage where speed is critical.

#### PostgreSQL (Local vs. Remote)
- **Local PostgreSQL**: Data is stored on the disk of the same machine running the application. Suitable for applications with moderate data volumes and where minimal latency is desired.
- **Remote PostgreSQL**: The database runs on a separate server or cloud instance. Preferred for larger, distributed applications requiring scalability and high availability.

### Choosing the Right Storage Option
- **SQLite vs. PostgreSQL**: Use SQLite for development, testing, or small-scale applications. PostgreSQL is preferred for production environments requiring advanced features and scalability.
- **Redis vs. Disk-based Databases**: Redis complements persistent databases by providing fast access to frequently read data. It's not a replacement for databases like PostgreSQL that offer durable storage.
- **Local vs. Remote PostgreSQL**: A local database simplifies development but may be limited by machine resources. A remote database supports scalability and is essential for distributed, high-traffic applications.

### Future Database Considerations
As the project evolves, we might consider transitioning to a service-oriented architecture, which could involve using different databases for specific services. Factors like data model complexity, transaction volumes, and the need for real-time processing will guide these decisions.

### Conclusion
Our current choice of PostgreSQL aligns with the project's need for a robust, scalable database solution capable of handling complex queries and ensuring data integrity. As we expand, the flexibility to integrate with other databases like Redis for caching or exploring NoSQL options for unstructured data will enable us to optimize performance and scale effectively.

