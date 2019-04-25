pipeline {
    agent {
        docker { image 'alpine/flake8' }
    }
    stages {
        stage('Example') {
            steps {
                gerritReview labels: [Verified: 0]
                echo 'Hello World'
                gerritComment path:'Jenkinsfile', line: 10, message: 'Invalid'
            }
        }
        stage('Flake8') {
            steps {
                FLAKE_ANSWER = sh(returnStdout: true, script: 'flake8 --config flake8.config')
                currentBuild.result = 'FAILURE'
                if (FLAKE_ANSWER.length() > 7) {
                    for (String s : li) {
                        currentBuild.result = 'FAILURE'
                        def args = s.split()
                        def message = "flake8:" + args[1..args.size() - 1].join(' ')
                        def path_and_line = args[0].split(':')
                        def path = path_and_line[0]
                        def line = path_and_line[1]
                        def symbol = path_and_line[2]
                        echo path
                        echo line
                        echo symbol
                        echo message
                    }
                }
            }
        }
    }
    post {
        success { gerritReview labels: [Verified: 1] }
        unstable { gerritReview labels: [Verified: 0], message: 'Build is unstable' }
        failure { gerritReview labels: [Verified: -1] }
    }
}
