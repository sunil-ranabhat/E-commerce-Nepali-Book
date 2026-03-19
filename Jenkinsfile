pipeline {
    agent any

    environment {
        IMAGE = '767397778698.dkr.ecr.us-east-1.amazonaws.com/nepali-book-app:latest'
    }

    stages {
        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE .'
            }
        }

        stage('Login to ECR') {
            steps {
                sh '''
                aws ecr get-login-password --region us-east-1 | \
                docker login --username AWS --password-stdin 767397778698.dkr.ecr.us-east-1.amazonaws.com
                '''
            }
        }

        stage('Push Docker Image to ECR') {
            steps {
                sh 'docker push $IMAGE'
            }
        }

        stage('Deploy to EKS') {
            steps {
                sh '''
                # Optional: Apply Kubernetes manifests pointing to your ECR image
                kubectl apply -f deployment.yaml
                kubectl apply -f service.yaml
                '''
            }
        }
    }
}
