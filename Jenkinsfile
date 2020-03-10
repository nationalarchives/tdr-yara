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
        def accountNumber = "328920706552"
        sh "rm -rf lambda && mkdir -p lambda"
        sh "aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin ${accountNumber}.dkr.ecr.eu-west-2.amazonaws.com"
        sh "docker run -itd --rm --name dependencies ${accountNumber}.dkr.ecr.eu-west-2.amazonaws.com/yara-dependencies:${params.TO_DEPLOY}"
        sh "docker build -f Dockerfile-compile -t yara-rules --build-arg ACCOUNT_NUMBER=$accountNumber ."
        sh "docker run -itd --rm --name rules yara-rules"
        sh "docker cp dependencies:/lambda/dependencies.zip /"
        sh "docker cp rules:/output ./lambda"
        sh "unzip -q /dependencies.zip -d ./lambda"
        sh "cp main.py ./lambda"
        dir("lambda") {
            sh "ls -la"
            sh "zip -r9 /function.zip ."
        }

        sh "aws lambda update-function-code --function-name TestYara --zip-file fileb:///function.zip"
        }
      }
    }
  }
  post {
        always {
            sh 'rm -rf lambda'
            sh "docker stop dependencies rules"
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
