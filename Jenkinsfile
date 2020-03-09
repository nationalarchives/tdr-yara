pipeline {
  agent {
    label "master"
  }
  parameters {
    choice(name: "STAGE", choices: ["intg", "staging", "prod"], description: "The stage you are building the front end for")
    string(name: "TO_DEPLOY", description: "The git tag, branch or commit reference to deploy, e.g. 'v123'")
  }
  stages {
    stage("Docker") {
      agent {
        label "master"
      }
      steps {
        script {
          def accountNumber = getAccountNumberFromStage()
            sh "mkdir lambda"
          docker.withRegistry("${accountNumber}.dkr.ecr.eu-west-2.amazonaws.com") {
            sh "aws ecr get-login --registry-ids ${accountNumber} --no-include-email | sed 's|https://||' | bash"
            sh "docker pull yara-dependencies:${params.TO_DEPLOY}"
            sh "docker run -itd --name dependencies yara-dependencies:${params.TO_DEPLOY}"
            sh "docker build -t ${accountNumber}.dkr.ecr.eu-west-2.amazonaws.com/yara-rules --build-arg ACCOUNT_NUMBER=$accountNumber ."
            sh "docker run -itd --name rules yara-rules:${params.TO_DEPLOY}"
            sh "docker cp dependencies:/lambda/dependencies.zip ."
            sh "docker cp rules:/output /lambda"
            sh "unzip dependencies.zip -d /lambda"
            sh "cp main.py /lambda"
            sh "cd /lambda"
            sh "zip -r9 ../function.zip"
            sh "aws lambda update-function-code --function-name TestYara --zip-file fileb:///function.zip"            
          }
        }
      }
    }
  }
}

def getAccountNumberFromStage() {
  def stageToAccountMap = [
      "intg": env.INTG_ACCOUNT,
      "staging": env.STAGING_ACCOUNT,
      "prod": env.PROD_ACCOUNT
  ]

  return stageToAccountMap.get(params.STAGE)
}
