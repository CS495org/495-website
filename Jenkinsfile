pipeline {
    agent server

    environment {
        OUR_AIRBYTE='https://github.com/CS495org/airbyte.git'
        DJANGO_PG_SCHEMA='DJANGO_PG_SCHEMA'
        RHOST='redis'
        RPORT='6379'
        HOST='db'
        PORT='5432'

        POSTGRES_USER=tate
        POSTGRES_PASSWORD=credentials('POSTGRES_PASSWORD')
        POSTGRES_DB=tate
        DJANGO_SECURE_KEY=credentials('DJANGO_SECURE_KEY')
        DJANGO_USER=credentials('DJANGO_USER')
    }

    stages {

        stage('Fill .env') {
            steps {
                script {
                    writeFile file: '.env', text: """
POSTGRES_USER='${POSTGRES_USER}'
POSTGRES_PASSWORD='${POSTGRES_PASSWORD}'
POSTGRES_DB='${POSTGRES_DB}'
HOST='${HOST}'
PORT='${PORT}'

# django
DJANGO_SECURE_KEY='${DJANGO_SECURE_KEY}'
DJANGO_USER='${DJANGO_USER}'
DJANGO_PG_SCHEMA='${DJANGO_PG_SCHEMA}'

# redis
RHOST='${RHOST}'
RPORT='${RPORT}'

OUR_AIRBYTE='${OUR_AIRBYTE}'
"""
                }
            }
        }

        stage('Compose Down && Up'){
            steps {
                script {

                    try {
                        sh 'docker compose down'
                        sh 'unzip database/init-2.zip'
                        sh 'docker compose up --build --detach'
                    } catch (Exception e) {
                        // wasn't running in the first place
                        sh 'docker compose up --build --detach'
                    }

                }
            }
        }
    }
}
