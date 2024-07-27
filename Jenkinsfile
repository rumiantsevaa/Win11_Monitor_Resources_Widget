pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'lab_work_v', url: 'https://github.com/rumiantsevaa/Win11_Monitor_Resources_Widget.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t win11_monitor:%BUILD_ID% .'
            }
        }

        stage('Run Container') {
            steps {
                bat 'docker run -d --name win11_monitor_container win11_monitor:%BUILD_ID%'
            }
        }

        stage('Collect Logs') {
            steps {
                bat 'docker logs win11_monitor_container > app_logs.txt'
            }
        }
    }

    post {
        always {
            bat 'docker stop win11_monitor_container || exit 0'
            bat 'docker rm win11_monitor_container || exit 0'
            bat 'docker rmi win11_monitor:%BUILD_ID% || exit 0'
            archiveArtifacts artifacts: 'app_logs.txt', allowEmptyArchive: true
        }
    }
}
