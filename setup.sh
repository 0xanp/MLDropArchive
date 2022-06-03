mkdir -p ~/.streamlit

echo "[theme]
base=‘dark’
font=‘monospace’
[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml