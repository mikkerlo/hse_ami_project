node {
  checkout scm
  try {
    gerritReview labels: [Verified: 0]
    stage('Hello') {
      echo 'Hello World'
      gerritComment path:'JenkinsFile', line: 10, message: 'invalid syntax'
    }
    gerritReview labels: [Verified: 1]
  } catch (e) {
    gerritReview labels: [Verified: -1]
    throw e
  }
}

