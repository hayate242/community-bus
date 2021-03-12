#!/bin/sh

set -e

host="$1"
shift
user="$1"
shift
password="$1"
shift
cmd="$@"

echo "Waiting for mysql"
until mysql -h"$host" -u"$user" -p"$password";do
        echo -n "."
        sleep 2
done

echo "MySQL is up - executing command"
exec $cmd
