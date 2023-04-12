Real Estate Search
It's a project for programming practice. 

The project helps looking for real estate property at a reasonable price at polish websites.

In first version the module scrapingOLX scraps sites by using users settings and sends results to the database through API.
This module is running by schedule. I am going to rebuild the module to run from django level and without RESTapi. It was made for an experiment.

The first web portal is olx.pl. In the future, it will be more.

You can see how it work on http://ec2-52-87-232-67.compute-1.amazonaws.com/

For run this project:

1. Copy .env-sample and .prod-sample to .env folder. Delete from names -sample.
2. Run terminal and prompt
    - for development:

        docker-compose -f docker-compose.yml -p real-estate-search up -d --build

    or
    - for production:
    
        docker-compose -f docker-compose-deploy.yml -p real-estate-search-deploy up -d --build

3. prompt for create superuser (enter email address for sending email)
    
    docker exec -it real-estate-search-web-1 sh
    or
    docker exec -it real-estate-search-deploy-web-1 sh

    python manage.py createsuperuser

