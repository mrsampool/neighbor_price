function_name=$1
function_arn=$2

source .env

mkdir -p package/components
cp -r components/event_manager package/components/
cp -r components/regions package/components/
touch package/components/__init__.py
cp -r "$function_name" package/

cp lambdas/"$function_name"/* package/

source venv/bin/activate
pip install \
-r lambdas/"$function_name"/requirements.txt \
  --target ./package \
  --platform manylinux2014_x86_64 \
  --implementation cp \
  --python-version 3.12 \
  --only-binary=:all: --upgrade \

cd package
zip -r ../"$function_name"_package.zip .
cd ..
rm -rf package
aws lambda update-function-code \
--function-name "$function_arn" \
--zip-file fileb://"$function_name"_package.zip;
rm "$function_name"_package.zip