cd "$(dirname "${BASH_SOURCE[0]}")"

url=$2
if [ -z $url ] 
then
	url="http://localhost"
fi
if [ -z $1 ]
then
    echo "Usage : createContextUsecase use_case_name cab_url"
else
    source ../getToken.sh "admin" $url
    echo "Create context usecase $1 on $url"
    curl -X POST $url:3200/cabcontext/api/v1/usecases -H "Content-type:application/json" -H "Authorization:Bearer $token" --data @$1.json -v
    echo ""
fi