
install 
========================

目前版本用vc编译有问题, 使用mingw编译

setup.py install --compiler=mingw32


事先需要设置JAVA_HOME

需要将 %JAVA_HOME%\jre\bin\client 加入到环境变量, 用server会有问题

jnius.ByteArray.tostring 有问题