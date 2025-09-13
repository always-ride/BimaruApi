curl -X POST "https://bimaruapi.fly.dev/api/solve" \
     -H "Content-Type: text/plain" \
     --data-binary @- <<EOF
2 | . . . . . . . . . .
1 | . . . . . . . . . .
4 | . . . . . . < . . .
2 | . . . . . . . . . .
3 | . . . . < . . . . .
1 | . . . . . . . . . .
4 | . . . . . . . . . .
2 | . . . . . . . . . .
1 | . . . . . . . . . .
0 | . . . . . . . . . .
    3 2 1 4 1 3 1 4 1 0
EOF
