curl -X POST "https://bimaruapi.fly.dev/api/solve" \
     -H "Content-Type: text/plain" \
     --data-binary @- <<EOF
2 | . . . . . . . o . .
1 | . . . . ~ . . . . .
4 | . . . . . . . < . .
0 | . . . . . . . . . .
1 | . . . . . . . . . .
6 | < . . . . . . . . .
0 | . . . . . . . . . .
3 | . . . □ . . . . . .
3 | . . . . . . . . . .
0 | . . . . . . . . . .
    1 3 2 2 3 2 1 3 3 0
EOF
