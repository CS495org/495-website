pipeline {
    agent {
        node 'server'
    }

    environment {
        DJANGO_PG_SCHEMA='DJANGO_PG_SCHEMA'
        RHOST='redis'
        RPORT='6379'
        HOST='db'
        PORT='5432'

        POSTGRES_USER=credentials('POSTGRES_USER')
        POSTGRES_PASSWORD=credentials('POSTGRES_PASSWORD')
        POSTGRES_DB=credentials('POSTGRES_DB')
        DJANGO_SECURE_KEY=credentials('DJANGO_SECURE_KEY')
        DJANGO_USER=credentials('DJANGO_USER')
        GMAIL=credentials('GMAIL')
        GMAILPSWD=credentials('GMAILPSWD')
        TMDB_API_KEY=credentials('TMDB_API_KEY')
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

GMAIL='${GMAIL}'
GMAILPSWD='${GMAILPSWD}'
TMDB_API_KEY='${TMDB_API_KEY}'
DEBUG=False
"""
                }
            }
        }

        stage('Compose Down && Up'){
            steps {
                script {
                    sh './all.sh'
                }
            }
        }
    }
}
