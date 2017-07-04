node {
    stage('Checkout') {
        checkout scm
    }
    stage('Build') {
        sh "docker-compose down --volumes --remove-orphans"
        sh "cp compose-override-for-jenkins.yml docker-compose.override.yml"
        sh "docker-compose build"
        sh "docker-compose run --rm model-databank python bootstrap.py"
        sh "docker-compose run --rm model-databank bin/buildout"
    }
    stage('Test') {
        sh "docker-compose run --rm model-databank bin/test"
    }
    stage('Cleanup') {
        sh "docker-compose down --volumes"
    }
}
