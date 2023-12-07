# Simple Student Information System

This is a web application built using Flask designed to manage basic information about students, courses, and colleges.

### Prerequisites

Before you begin, make sure you have the following installed:

- [Python](https://www.python.org/)
- [Git](https://git-scm.com/)

### Setting Up the .env File

To configure your local environment, follow these steps:

1. Clone this repository to your local machine:

  ```shell
    git clone https://github.com/nasviil/app-ssis.git
  ```

2. Change to this project's directory:

  ```shell
    cd app-ssis
  ```

3. Create a .env file:

  ```shell
    touch <filename>.env
  ```
   
5. Open the .env file in a text editor of your choice and fill in the required environment variables with your own values. Here's an example:

```shell
  DATABASE_URL=mysql://yourdbuser:yourdbpassword@localhost/yourdbname
  SECRET_KEY=<your_secret_key>
  MYSQL_HOST=localhost
  MYSQL_USER=yourmysqluser
  MYSQL_PASSWORD=yourmysqlpassword
  MYSQL_DATABASE=yourmysqldatabase
  CLOUDY_NAME=yourcloudinaryusername
  CLOUDY_KEY=yourcloudinaryapikey
  CLOUDY_SECRET=yourcloudinarysecretkey
  CLOUDY_URL=yourcloudinaryurl
```
  Ensure you replace the placeholder values with your actual credentials.
