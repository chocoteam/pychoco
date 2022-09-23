# NOTE: befaure launching ensure that $JAVA_HOME points
# to graalVM

# Build choco-solver-capi
cd choco-solver-capi
git pull origin master
sh ./build.sh
cd ..



pip3 install wheel
python3 setup.py bdist_wheel