pipeline {
  agent any   // Jenkins dùng bất kỳ agent nào (container, máy ảo...)

  stages {
    stage('Checkout') {
      steps {
        git url: 'https://github.com/NguyenTongAnhQuan443/chatbox', branch: 'main'
        // clone source từ GitHub branch main
      }
    }

    stage('Build Docker Image') {
      steps {
        sh 'docker-compose build'
        // build tất cả image trong docker-compose.yml
      }
    }

    stage('Setup Python & Install deps') {
        steps {
            sh '''
            python -m venv .venv
            . .venv/bin/activate
            pip install -U pip
            pip install fastapi uvicorn requests rasa
            '''
        }
        }

    stage('Deploy to Railway') {
      steps {
        withCredentials([string(credentialsId: 'railway_token', variable: 'RAILWAY_TOKEN')]) {
          // Railway CLI login và deploy
          sh '''
            npm install -g railway
            railway login --token $RAILWAY_TOKEN
            railway up --service your-service-name
          '''
        }
      }
    }
  }
}
