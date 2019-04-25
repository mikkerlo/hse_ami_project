node {
  checkout scm
  try {
    gerritReview labels: [Verified: 0]
    stage('Hello') {
      echo 'Hello World'
      gerritComment path:'Jenkinsfile', line: 10, message: 'Invalid'
    }
    gerritReview labels: [Verified: 1]
  } catch (e) {
    gerritReview labels: [Verified: -1]
    throw e
  }
}

