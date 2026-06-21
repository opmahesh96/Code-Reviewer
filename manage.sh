#!/bin/bash
case $1 in
  "start")
    export SUPABASE_URL="https://cqybcbtlpdvzjzusqcha.supabase.co"
    export SUPABASE_KEY="sb_publishable_lWIgrMQpGtcoUcE1kHiUFg_cL8TrihY"
    python app.py
    ;;
  "clean")
    echo "Clearing local cache..."
    find . -type d -name "__pycache__" -exec rm -rf {} +
    ;;
  "test")
    curl -X POST http://127.0.0.1:5000/new_review
    ;;
esac