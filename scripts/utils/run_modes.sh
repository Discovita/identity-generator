#!/bin/bash

run_dev_mode() {
    local app_name=$1
    
    cd frontend
    if [ "$app_name" = "new-coach" ]; then
        ./node_modules/.bin/concurrently \
            --kill-others \
            --prefix "[{name}]" \
            --names "backend,frontend" \
            --prefix-colors "yellow.bold,cyan.bold" \
            "cd ../backend && source venv/bin/activate && uvicorn discovita.app:app --reload" \
            "cd apps/new-coach && npm run dev"
    else
        ./node_modules/.bin/concurrently \
            --kill-others \
            --prefix "[{name}]" \
            --names "backend,frontend" \
            --prefix-colors "yellow.bold,cyan.bold" \
            "cd ../backend && source venv/bin/activate && uvicorn discovita.app:app --reload" \
            "cd apps/$app_name && PORT=3000 npm start"
    fi
}

run_prod_mode() {
    local app_name=$1
    
    cd frontend
    if [ "$app_name" = "new-coach" ]; then
        (cd apps/new-coach && npm run build)
        cd ..
        rm -rf backend/public/*
        cp -r frontend/apps/new-coach/dist/* backend/public/
    else
        npm run build:$app_name
        cd ..
        rm -rf backend/public/*
        cp -r frontend/apps/$app_name/build/* backend/public/
    fi
    cd backend
    source venv/bin/activate
    uvicorn discovita.app:app
}

install_dependencies() {
    local app_name=$1
    
    cd backend
    source venv/bin/activate
    python -m pip install -e .
    cd ..

    cd frontend
    npm install
    if [ "$app_name" = "new-coach" ]; then
        (cd apps/new-coach && npm install)
    else
        npm run install:$app_name
    fi
    cd ..
}
