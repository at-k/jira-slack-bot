#!/bin/sh

cursor=""
count=0

while true
do
  file=userlist_${count}.json
  curl https://slack.com/api/users.list\?token=$SLACK_OAUTH_TOKEN\&cursor=$cursor > $file
  cursor=$(cat $file | jq -r .response_metadata.next_cursor)
  cat $file | jq -r '.members[] | [.id, .real_name] | @csv' >> userlist.txt
  if [ -z $cursor ]; then
    break
  fi
  count=$((++count))
done
