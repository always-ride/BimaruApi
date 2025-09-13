curl -X POST "https://bimaruapi.fly.dev/api/solve" \
     -H "Content-Type: text/plain" \
     --data-binary @- <<EOF
2 | . . . . . > . . . .
1 | . . . . . . . . . .
3 | . . . . . . . . . .
5 | . . . . . . . . . .
1 | . . . . . . . . . .
4 | . . ~ . v . . . . .
0 | . . . . . . . . . .
0 | . . . . . . . . . .
4 | . . . . . . . . . .
0 | . . . . . . . . . .
    1 2 4 1 5 1 1 1 4 0
EOF
