all: compass uglify

coffee:
	coffee -c --join djangotcha/static/js/main.js \
		source/coffeescript/main.coffee \
		source/coffeescript/config.coffee \
		source/coffeescript/helpers.coffee \
		source/coffeescript/_pages.coffee \
		source/coffeescript/pages/*.coffee



uglify: coffee
	node_modules/.bin/uglifyjs -o djangotcha/static/js/main.js \
		 djangotcha/static/js/main.js


compass:
	cd source; compass compile; cd -;

watch:
	@echo "\n# watch coffee-script and compass"
	cd source; compass clean; cd -;
	coffee --watch --compile --join djangotcha/static/js/main.js source/coffeescript/* &
	coffee --watch --compile --output tmp/ source/coffeescript/* &
	cd source; compass watch; cd -;

reload:
	git pull;
	./manage.py migrate djangotcha;
	make compass;
	sudo service djangotcha restart;

