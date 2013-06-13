pelican -s pelicanconf.py content -o ../jiangjinaxiao.github.com

git add .
git commit -m "update"
git push origin master

cd ../jiangjianxiao.github.com
git add . 
git commit -m "Update"
git push origin master
cd ../blog