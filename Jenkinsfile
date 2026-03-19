pipeline {
    agent any

    stages {
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t nepali-book-app .'
            }
        }

        stage('Stop Old Container') {
            steps {
                sh 'docker stop nepali-book-container || true'
                sh 'docker rm nepali-book-container || true'
            }
        }

        stage('Run Container') {
            steps {
                sh 'docker run -d -p 8000:8000 --name nepali-book-container nepali-book-app'
            }
        }
    }
}
