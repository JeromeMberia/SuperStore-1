# this is for the developers

**Note**
Do not push to dev branch
Delete print
## Admin
  Email     - jake@gmail.com
  password  - testing123
  
## API endpoints

* For [Login](https://api-shop-url.herokuapp.com/login/)
* For [Purchases](https://api-shop-url.herokuapp.com/api/purchases/)
* For [Shops](https://api-shop-url.herokuapp.com/api/shop/)
* For [Items](https://api-shop-url.herokuapp.com/api/items/)
* For [Sales](https://api-shop-url.herokuapp.com/api/sales/)

* For [product-batch](https://api-shop-url.herokuapp.com/api/product-batch/)
* For **each** [product-batch](https://api-shop-url.herokuapp.com/api/merchant/api/product-batch/<int:pk>/)
  - it won't work until you switch **pk** with an integer
  - pk stand for primary key.

* Register [Clerk](https://api-shop-url.herokuapp.com/register-clerk/)
* For [Clerk](https://api-shop-url.herokuapp.com/api/clerk/)
* For **each** [Clerk](https://api-shop-url.herokuapp.com/api/clerk/clerk-id/<int:pk>)
  - it won't work until you switch **pk** with an integer
  - pk stand for primary key.
* Activate or Deactive **each** [Clerk](https://api-shop-url.herokuapp.com/api/clerk/clerk-id/activate/<int:pk>/)

* Register [Merchant](https://api-shop-url.herokuapp.com/register-merchant/)
* For [Merchant](https://api-shop-url.herokuapp.com/api/merchant)
* For **each** [Merchant](https://api-shop-url.herokuapp.com/api/merchant/merchant-id/<int:pk>)
  - it won't work until you switch **pk** with an integer
  - pk stand for primary key.

* Register [Manager](https://api-shop-url.herokuapp.com/register-manager/)
* For [Manager](https://api-shop-url.herokuapp.com/api/manager)
* For **each** [Manager](https://api-shop-url.herokuapp.com/api/manager/manager-id/<int:pk>)
  * it won't work until you switch **pk** with an integer
  * pk stand for primary key.
* Activate or Deactive **each** [Manager](https://api-shop-url.herokuapp.com/api/manager/manager-id/activate/<int:pk>/)

## Runing it on your local server

* Creating a virtual environment

    ```

    $ sudo apt-get install python3-venv
    $ python3 -m venv virtual
    ```

* Activating the virtual environment

    ```

    $ . virtual/bin/activate
    ```

* Install all dependencies with the code **bellow** before you begin

    ```
    $ pip install -r requirements.txt
    ```

### Setting up a database on Remotely

* First type **psql** in your terminal
  
    ```
    $ psql
    ```

* Second in the shell type **CREATE DATABASE shop;**

    ```
    $ psql
    psql (12.2 (Ubuntu 12.2-4))
    Type "help" for help.

    david=# CREATE DATABASE shop;
    ```

* Conform you will know if it's successful when you see **CREATE DATABASE**

    ```
    $ psql
    psql (12.2 (Ubuntu 12.2-4))
    Type "help" for help.

    david=# CREATE DATABASE shop;
    CREATE DATABASE
    david=#
    ```

### then you

* Create a file named .env
  
* In that file type the code below:

    ```
    source virtual/bin/activate

    export DB_NAME='shop'
    export DB_USER='username of your database'
    export DB_PASSWORD='password of your database'
    export SECRET_KEY='< your secert key >'
    export DEBUG=True
    ```

* Then you go to your terminal and type this to run this application

    ```
    $ . .env
    $ python3 manage.py runserver
    ```
