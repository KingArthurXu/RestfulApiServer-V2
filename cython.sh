#!/usr/bin/bash
# cpython some module

chmod -R 755 ./static/uploads/*
rm -rf ./static/uploads-1
>./log/baas.log
>./log/baas_jobs.log

function for_dir()
{
    for file in `ls $1`
    do
        if [ -d $1'/'$file ]
        then
           # echo "$1/$file is directory"
           if [ -f $1'/'$file'/setup.py' ]
                then
                (cd $1/$file; python setup.py build_ext --inplace)
                #(cd $1/$file; grep '"*\.py"' setup.py | awk -F "\"" '{for(i=1;i<=NF;i++){if(match($i, /.*\.py/,r)){print r[0];print r[0]"c"} } }' | sed "s#^#rm\\ $1\\/$file\\/#g" )
                #(cd $1/$file; grep '"*\.py"' setup.py | awk -v a="$1/$file/" -F "\"" '{for(i=1;i<=NF;i++){if(match($i, /.*\.py/,r)){print a r[0];print a r[0]"c"} } }' | xargs rm -f)
                (cd $1/$file; grep '"*\.py"' setup.py | awk -v a="$1/$file/" -F "\"" '{for(i=1;i<=NF;i++){if(match($i, /.*\.py/,r)){print r[0];print r[0]"c"} } }' | xargs rm -f)
           fi
           for_dir $1'/'$file
        fi
    done
}

for_dir .

find . -name '*.pyc' | xargs rm -rf
find . -name '*.c' | xargs rm -rf
