# Database Backup to Amazon S3

## Overview

This project automates the process of backing up a database and securely uploading the backup file to an Amazon S3 bucket. It provides a robust and scalable solution for managing database backups using Python, Docker, and Jenkins.

---

## Simple Flow

1. **Database Backup Creation**:
   - The Python script connects to the database using credentials.
   - It generates a backup file using `mysqldump`.

2. **Backup File Processing**:
   - The backup file is compressed for efficient storage.
   - It is encrypted to ensure data security.

3. **Upload to Amazon S3**:
   - The processed backup file is uploaded to an Amazon S3 bucket using the AWS SDK.

4. **Automation**:
   - The backup and upload process is containerized using Docker for portability.
   - Jenkins triggers the backup process automatically based on a schedule (e.g., daily at 2:00 AM).

5. **Notifications**:
   - Jenkins sends an email notification upon completion of the backup process.

---

## Features

- **Automated Backups**: Creates and schedules database backups.
- **Secure Storage**: Uploads encrypted and compressed backups to Amazon S3.
- **Dockerized Workflow**: Ensures a consistent runtime environment.
- **Jenkins Integration**: Automates and monitors the process.