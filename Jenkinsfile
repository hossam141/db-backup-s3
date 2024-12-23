pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'db-backup-app'
        AWS_DEFAULT_REGION = 'your-aws-region'
        AWS_BUCKET_NAME = 'your-s3-bucket-name'
    }

    triggers {
        cron('0 2 * * *') // Runs daily at 2:00 AM
    }

    stages {
        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE} ."
            }
        }
        
        stage('Run DB Backup') {
            steps {
                script {
                    withCredentials([
                        string(credentialsId: 'db-name', variable: 'DATABASE_NAME'),
                        usernamePassword(credentialsId: 'db-credentials', usernameVariable: 'DATABASE_USER', passwordVariable: 'DATABASE_PASSWORD'),
                        string(credentialsId: 'db-host', variable: 'DB_HOST'),
                        [$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-credentials']
                    ]) {
                        sh """
                            docker run --rm \
                            -e DATABASE_NAME=${DATABASE_NAME} \
                            -e DATABASE_USER=${DATABASE_USER} \
                            -e DATABASE_PASSWORD=${DATABASE_PASSWORD} \
                            -e DB_HOST=${DB_HOST} \
                            -e AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID} \
                            -e AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY} \
                            -e AWS_DEFAULT_REGION=${AWS_DEFAULT_REGION} \
                            -e AWS_BUCKET_NAME=${AWS_BUCKET_NAME} \
                            ${DOCKER_IMAGE}
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            emailext subject: "Database Backup Job Completed - ${currentBuild.currentResult}",
                     body: """
                     The database backup job has completed with status: ${currentBuild.currentResult}.
                     Check console output at: ${env.BUILD_URL}
                     """,
                     to: "your-email@example.com"
            
            // Clean workspace
            cleanWs()
        }
    }
}
