pipeline {
    agent any
    stages {
        stage('Example') {
            steps {
                gerritReview labels: [Verified: 0]
                echo 'Hello World'
                gerritComment path:'Jenkinsfile', line: 10, message: 'Invalid'
            }
        }
    }
    post {
        success { gerritReview labels: [Verified: 1] }
        unstable { gerritReview labels: [Verified: 0], message: 'Build is unstable' }
        failure { gerritReview labels: [Verified: -1] }
    }
}
