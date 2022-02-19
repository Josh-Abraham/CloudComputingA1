#################
#  ECE 1779 A1  #
#################

cd CloudComputingA1/src
gunicorn --bind 0.0.0.0:5001 wsgi_memcache:webapp &
gunicorn --bind 0.0.0.0:5000 wsgi_app:webapp &

echo "Webapps started"