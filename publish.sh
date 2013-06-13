#!/usr/bin/env bash
# 生成内容
pelican -s pelicanconf.py content -o ../jiangjinaxiao.github.com
# 提交blog
git add .
git commit -m "update"
git push origin master
# 提交生成内容
cd ../jiangjianxiao.github.com
git add . 
git commit -m "Update"
git push origin master
cd ../blog