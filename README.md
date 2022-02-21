# CloudComputingA1

Assignment 1 for ECE 1779

## Project Architecture
### 2 Flask applications: 

1. `src/app` 

    The `app` runs on port `5000` and is the exposed UI.


2. `src/memcache_app`
    The `memcache_app` runs on port `5001` and is used internally by the `app` holding the memory cache of the system.

### Database
A local mysql database is used along side this system

## Project Description
The project is used to store images with an image key store in your local file system. The database is used to store the references between the key and the file location

The memcache is used to store the most recently searched images within the system. The cache stores the key and the image in Base64. The memcache supports LRU and RR methods

The UI is used to navigate the system and do things like: add images, list keys, get images by key, reset memcache, and view memcache statistics

## Project Usage
To use this project you need to have `Flask, gunicorn, cachetools, mysql.connector, matplotlib.figure`
You also need to have mysql installed, and then run the SQL commands in `/database/ImageStore.sql`

To run the project move the `start.sh` file up one level to the parent directory
Then run `./start.sh` to start both applications


