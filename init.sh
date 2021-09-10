#/usr/bash

for i in lab*/ 
do
    if [ -d ./$i/obj/ ]
    then 
        echo 'Folder "obj" is existed'
    else mkdir ./$i/obj
    fi
done