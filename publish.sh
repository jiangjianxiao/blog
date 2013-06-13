pelican -s pelicanconf.py content -o ../jiangjinaxiao.github.com
cd ../jiangjianxiao.github.com
git add . 
git commit -m "Update"
git push origin master
cd ../blog