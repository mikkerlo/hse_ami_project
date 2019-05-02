pipeline {
    agent {
        docker { image 'mikkerlo/ci' }
    }
    stages {
        stage("Clonning Git") {
            steps {
                checkout scm
            }
        }
        stage("Flake8") {
            steps {
                script {
                    def flake_output = sh(returnStdout: true, script: 'flake8 --config flake8.config || true')

                    if (flake_output.length() > 7) {
                        for (String s : flake_output.split('\n')) {
                            def args = s.split()
                            def message = "flake8:" + args[1..args.size() - 1].join(' ')
                            def path_and_line = args[0].split(':')
                            def path = path_and_line[0]
                            def line = path_and_line[1]

                            if (path.startsWith('./')) {
                                path = path[2..-1]
                            }

                            gerritComment path: path, line: line, message: message
                            echo path
                            echo line
                            echo message
                        }
                        error 'Flake8 failed'
                    }
                }
            }
        }
    }
    stage("Backend tests") {
        steps {
            sh "pip install -r backend/requirements.txt"
            sh "cd backend"
            script {
                def test_output = sh(returnStdout: true, script: 'manage.py test || true')
                gerritComment test_output
            }
        }
    }
    post {
        success { gerritReview labels: [Verified: 1] }
        unstable { gerritReview labels: [Verified: 0], message: 'Build is unstable' }
        failure { gerritReview labels: [Verified: -1] }
    }
}
