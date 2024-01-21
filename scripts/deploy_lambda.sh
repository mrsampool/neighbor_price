echo "Deploying function..."
function_name=$1
echo "FUNCTION NAME: $function_name"

source .env
function_arn=""
if [ "$function_name" == "data_collector" ]; then
  function_arn="$LAMBDA_ARN_DATA_COLLECTOR"
elif [ "$function_name" == "data_analyzer" ]; then
  function_arn="$LAMBDA_ARN_DATA_ANALYZER"
else
  echo "ERROR: Unknown function: $function_name. Exiting."
  exit 1
fi

mkdir -p package/components
touch package/components/__init__.py

cp -r components/event_manager package/components/
cp -r components/regions package/components/
if [ "$function_name" == "data_collector" ]; then
  cp -r components/region_csv_endpoint_worker package/components/
fi

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