1. Clone with git

git clone https://github.com/GrazhdanochkaMariya/Helper.git


2. Create virtual environment
   
python3 -m venv venv

source venv/bin/activate  # for Linux/Mac

.\venv\Scripts\activate  # for Windows

3. Create env file 

Use the template .env.example

4. Install pre-commit

pre-commit install

pre-commit run

5. Create test database

6. Run docker-compose

docker-compose -f docker-compose.local.yml up

7. To use Swagger locally follow

http://127.0.0.1:8000/docs

with your creds

Username: AndersenLeads

Password: eVxuw88jWpajhyJI

8. Stop docker-compose

docker-compose -f docker-compose.local.yml down
