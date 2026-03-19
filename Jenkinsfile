pipeline {
    agent any

    stages {
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t nepali-book-app .'
            }
        }
    }
}
