pipeline {
  agent any

  stages {
    stage('Checkout') {
      steps {
        git url: 'https://github.com/your-repo.git', branch: 'main'
      }
    }

    stage('Build Docker Image') {
      steps {
        sh 'docker-compose build'
      }
    }

    stage('Test') {
      steps {
        // thay lệnh test tuỳ project (pytest, npm test...)
        sh 'docker-compose run --rm app pytest'
      }
    }

    stage('Deploy to Railway') {
      steps {
        withCredentials([string(credentialsId: 'railway_token', variable: 'RAILWAY_TOKEN')]) {
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
