#!/bin/bash

version=$1
text=$2
branch=$(git rev-parse --abbrev-ref HEAD)
repo_full_name=$(git config --get remote.origin.url | sed 's/.*:\/\/github.com\///;s/.git$//')
token=$(git config --global github.token)

generate_post_data()
{
  cat <<EOF
{
  "tag_name": "$version",
  "target_commitish": "$branch",
  "name": "$version",
  "body": "$text",
  "draft": false,
  "prerelease": false
}
EOF
}

echo "Create release $version for repo: $repo_full_name branch: $branch"
curl --data "$(generate_post_data)" "https://api.github.com/repos/$repo_full_name/releases?access_token=$token"

read -p ">twine upload dist/* TO UPLOAD TO PYPI..."


--------------------------------------

#!/bin/bash

#works to ssh & http link

token="your_token"

repo_full_name=$(git config --get remote.origin.url)
url=$repo_full_name
re="^(https|git)(:\/\/|@)([^\/:]+)[\/:]([^\/:]+)\/(.+).git$"

if [[ $url =~ $re ]]; then
protocol=${BASH_REMATCH[1]}
separator=${BASH_REMATCH[2]}
hostname=${BASH_REMATCH[3]}
user=${BASH_REMATCH[4]}
repo=${BASH_REMATCH[5]}
fi

echo "https://api.github.com/repos/$user/$repo/releases?access_token=$token"

read -p ">twine upload dist/* TO UPLOAD TO PYPI..."
