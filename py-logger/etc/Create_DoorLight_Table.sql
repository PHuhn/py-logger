-- Copyright (c) 2019 Northern Software Group
-- This software is owned by Northern Software Group.  Unauthorized copying,
-- distribution or changing of this software is prohibited.
-- Written by: Phil Huhn
-- Create the door and light log table
USE [master]
CREATE LOGIN RaspPI
  WITH PASSWORD = 'Colony0RaspberryPI0';
GO
CREATE DATABASE Logging
GO
USE Logging;		-- change to your db name
GO
CREATE USER RaspPI
  FOR LOGIN RaspPI
  WITH DEFAULT_SCHEMA = dbo;
GO
sp_addrolemember @rolename='db_owner', @membername ='RaspPI'
--
sp_addrolemember @rolename='db_datareader', @membername ='RaspPI'
--
sp_addrolemember @rolename='db_datawriter', @membername ='RaspPI'
--
GO
USE Logging;		-- change to your db name
GO
-- 0=Date, 1=key, 2=name, 3=location, 4=status, 5=log msg
-- DROP TABLE DoorLight
CREATE TABLE DoorLight (
 Id			BIGINT NOT NULL IDENTITY(1,1),
 LogDate	DATETIME NOT NULL,
 [Key]		NVARCHAR(50) NOT NULL,
 [Type]		NVARCHAR(50) NOT NULL,
 [Location]	NVARCHAR(50) NOT NULL,
 [Status]	NVARCHAR(10) NOT NULL,
 Msg		NVARCHAR(255) NOT NULL,
 [Log]		NVARCHAR(500) NOT NULL,
 CreateDate	DATETIME NOT NULL
 CONSTRAINT PK_DoorLight PRIMARY KEY CLUSTERED 
 (
  Id ASC
 ) WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
