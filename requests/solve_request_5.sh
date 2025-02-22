curl -X POST "https://bimaruapi.fly.dev/api/solve" \
     -H "Content-Type: text/plain" \
     --data-binary @- <<EOF
4 | . . . . . . . . . .
3 | . . . . . . . . . .
2 | . . . . . . > . . .
0 | . . . . . . . . . .
4 | . . . . o . ~ . . .
1 | . . . . . . . . . .
3 | . . . o . . . . . .
1 | □ . . . . . . . . .
1 | . . . . . . . . . .
1 | ~ . . . . . . . . .
    4 2 1 2 2 1 4 1 2 1
EOF
