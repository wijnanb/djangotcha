Djangotcha
================

Desktop website for place management for Djangotcha.

# Install dependencies

    mkvirtualenv djangotcha
    pip install -r deployment/requirements.txt

# Install coffee-scripts

    npm install -g coffee-script

# Install compass

    gem install compass

# Compile and watch coffeescript and compass

    make watch

# Translations

    ## Generate PO files:
    python manage.py makemessages -l nl
    python manage.py makemessages -l fr

    ## Compile PO files to MO format
    python manage.py compilemessages
    
    
# Assign random target to everyone
	
	./manage.py assign_targets