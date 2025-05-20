pipeline {
  agent any

  environment {
    // Đặt webhook của Render (Web Service > Manual Deploy > Deploy Hook)
    RENDER_DEPLOY_HOOK = 'https://api.render.com/deploy/srv-xxxxxxxxxxxx?key=deploy_hook_key'
    RASA_CORE_URL = 'https://ten-app-cua-ban.onrender.com'
    ACTION_SERVER_URL = 'https://ten-action-server.onrender.com'
  }

  stages {
    stage('Checkout') {
      steps {
        git url: 'https://github.com/NguyenTongAnhQuan443/chatbox', branch: 'main'
      }
    }

    // Nếu bạn muốn build & push image lên registry, thêm stage này:
    // stage('Build and Push Docker Images') {
    //   steps {
    //     sh 'docker-compose build'
    //     sh 'docker-compose push'
    //   }
    // }

    stage('Trigger Render Deploy') {
      steps {
        sh """
          # Gọi webhook Render để redeploy multi-container từ GitHub
          curl -X POST $RENDER_DEPLOY_HOOK
        """
      }
    }

    stage('Wait for Deploy') {
      steps {
        // Tùy vào app, chờ 1-2 phút để Render build xong, có thể dùng sleep lâu hơn nếu project build lớn
        sh 'sleep 90'
      }
    }

    stage('Health Check - Rasa Core') {
      steps {
        script {
          def health = sh(script: "curl -s $RASA_CORE_URL/status | grep 'model_fingerprint'", returnStatus: true)
          if (health != 0) {
            error "Rasa Core is not up!"
          }
        }
      }
    }

    stage('Health Check - Action Server') {
      steps {
        script {
          def health = sh(script: "curl -s $ACTION_SERVER_URL/health | grep '\"status\":\"ok\"'", returnStatus: true)
          if (health != 0) {
            error "Action Server is not up!"
          }
        }
      }
    }

    stage('Chatbot API Test') {
      steps {
        sh """
          curl -X POST $RASA_CORE_URL/webhooks/rest/webhook \
            -H "Content-Type: application/json" \
            -d '{"sender":"jenkins_test","message":"xin chào"}'
        """
      }
    }
  }
}
