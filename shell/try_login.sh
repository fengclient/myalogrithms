#!/usr/bin/sh
for i in {0..500}
do
  echo 'try login:'+$i
  mysql -utest -p111111 -h localhost --protocol=tcp -e 'select current_user();' 2>&1|grep current_user
  if [ $? == 0 ]
  then
    echo 'yes'
  fi
done
