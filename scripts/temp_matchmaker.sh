for i in {1..3}
do
cat <<EOT >> output.txt
add_tasks_customdb({
            "entry_id": $i,
            "team_num": 5,
            "match_num": $i,
            "alliance": 1,
            "user_id": 0
        })
EOT
done

c=3
for i in {4..6}
do
    j=$[$i-c]
cat <<EOT >> output.txt
add_tasks_customdb({
            "entry_id": $i,
            "team_num": 7,
            "match_num": $j,
            "alliance": 1,
            "user_id": 0
        })
EOT
done
