#/usr/bash

for i in lab*/ 
do
    if [ -d ./$i/obj/ ]
    then 
        echo 'Folder "obj" is existed'
    else mkdir ./$i/obj
    fi
done

for i in lab*/ 
do
    if [ -d ./$i/result/ ]
    then 
        echo 'Folder "result" is existed'
    else mkdir ./$i/result
    fi
done