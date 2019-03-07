wait_for_db() {
    # url=`echo $SQLALCHEMY_DATABASE_URI | awk -F[@//] '{print $4}'`
    # database=`echo $url | awk -F[:] '{print $1}'`
    # port=`echo $url | awk -F[:] '{print $2}'`
    echo $SQLALCHEMY_DATABASE_URI
    database=$DB_HOST
    echo "Waiting for $database:$port to be ready"
    while ! mysqladmin ping -h "$database" -P "$port" --silent; do
        # Show some progress
        sleep 5;
    done
    echo "$database is ready"
    # Give it another second.
    sleep 1;
}

wait_for_db


python3 -c "from web import db; db.create_all()"
gunicorn --config gunicorn_config.py web:app
