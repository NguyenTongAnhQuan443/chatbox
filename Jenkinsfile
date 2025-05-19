pipeline {
  agent any

  stages {
    stage('Checkout') {
      steps {
        git url: 'https://github.com/NguyenTongAnhQuan443/chatbox', branch: 'main'
      }
    }

    // Gửi request đến chatbot sau deploy để kiểm tra "bot còn sống"
    stage('Health Check (CD verification)') {
      steps {
        sh '''
          sleep 10  # chờ Railway restart nếu có
          curl -X POST https://chatbox-production-71c0.up.railway.app/webhooks/rest/webhook \
            -H "Content-Type: application/json" \
            -d '{"sender":"jenkins_test","message":"xin chào"}'
        '''
      }
    }
  }
}
