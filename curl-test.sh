#since it was written in a continuous stream
#added the -s and -H to resolve issue
curl -s -X POST http://localhost:5000/api/timeline_post -H "Content-Type: application/x-www-form-urlencoded" -d "name=Margaret&email=margaret.diaz05@myhunter.cuny.edu&content=Testing if this works"

curl --request GET http://localhost:5000/api/timeline_post

curl -X DELETE http://localhost:5000/api/timeline_post/1
