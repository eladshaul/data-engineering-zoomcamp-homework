# Data Engineering Zoomcamp 2026 - Module 5 Homework

This repository contains the solution for the fifth module of the Data Engineering Zoomcamp. In this homework, we'll use Bruin to build a complete data pipeline, from ingestion to reporting.



## Question 1: 

**Answer:** In a Bruin project, the required files/directories are **`.bruin.yml` and `pipeline/` with `pipeline.yml` and `assets/`**.


***

## Question 2: 

**Answer:** The best incremental strategy for processing a specific interval by deleting and inserting data for that period is **time_interval - incremental based on a time column**.

The other options are not suited for this specific strategy; they are either inefficient or fail to prevent duplicate rows. 

***

## Question 3: 

**Answer:** To override the settings and process only yellow taxi data, use the  **`bruin run --var 'taxi_types=["yellow"]'`**.

Since the variable taxi_types expects a list, the value must be defined in the CLI using JSON array format, such as: `--var list='["a", "b"]'`.

***

## Question 4: 

**Answer:** The correct command is  **bruin run ingestion/trips.py --downstream**.

According to the Bruin CLI documentation, the `--downstream` flag is used to execute a specific asset along with all its subsequent dependent assets in the pipeline. The command targets the asset using its relative file path.

***

## Question 5: 

**Answer:** The correct quality check is **`name: not_null`**.

In Bruin, the not_null check ensures that the specified column (in this case, pickup_datetime) contains no missing values. If a NULL value is detected during the pipeline run, the quality check will fail, preventing bad data from flowing downstream.

***

## Question 6: 

**Answer:** The correct command is **`bruin lineage`**.

In Bruin, the `lineage` command is specifically designed to visualize the dependency graph between assets. It helps developers understand the data flow and the relationships (upstream and downstream) within the pipeline.

***

## Question 7: 

**Answer:** The correct command is **`--full-refresh`**.

When running a pipeline for the first time or after making schema changes, the `--full-refresh` flag ensures that Bruin drops any existing tables and recreates them from scratch, ignoring any previous incremental state or progress.

***