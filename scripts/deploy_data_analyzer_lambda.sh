source .env

mkdir -p package/components
cp -r components/event_manager package/components/
cp -r components/regions package/components/
touch package/components/__init__.py
cp -r data_analyzer package/

cp lambdas/data_analyzer/* package/

source venv/bin/activate
pip install \
-r lambdas/data_analyzer/requirements.txt \
  --target ./package \
  --platform manylinux2014_x86_64 \
  --implementation cp \
  --python-version 3.12 \
  --only-binary=:all: --upgrade \

cd package
zip -r ../data_analyzer_package.zip .
cd ..
rm -rf package
aws lambda update-function-code \
--function-name arn:aws:lambda:us-west-1:065361442221:function:data_analyzer \
--zip-file fileb://data_analyzer_package.zip;
rm data_analyzer_package.zip