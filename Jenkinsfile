pipeline {
    agent any

    parameters {
        choice(
            name: 'CONTEXT',
            choices: ['bstack', 'local_emulator', 'local_real'],
            description: 'Execution context for tests'
        )
        choice(
            name: 'PLATFORM',
            choices: ['android', 'ios'],
            description: 'Mobile platform'
        )
        string(
            name: 'BROWSERSTACK_USERNAME',
            defaultValue: '',
            description: 'BrowserStack Username (leave empty to use from .env.credentials)'
        )
        string(
            name: 'BROWSERSTACK_ACCESS_KEY',
            defaultValue: '',
            description: 'BrowserStack Access Key (leave empty to use from .env.credentials)',
            trim: true
        )
    }

    environment {
        // Set Python path
        PATH = "$PATH:/usr/local/bin"

        // Allure results directory
        ALLURE_RESULTS_DIR = 'allure-results'

        // Build info
        BUILD_NAME = "Wikipedia Mobile Tests - ${env.BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo "📦 Checking out code from repository"
            }
        }

        stage('Setup Environment') {
            steps {
                echo "🔧 Setting up Python environment"
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
                echo "✅ Environment setup complete"
            }
        }

        stage('Configure Credentials') {
            steps {
                script {
                    // Create .env.credentials file from Jenkins parameters if provided
                    if (params.BROWSERSTACK_USERNAME && params.BROWSERSTACK_ACCESS_KEY) {
                        writeFile(
                            file: '.env.credentials',
                            text: """# BrowserStack Credentials
BROWSERSTACK_USERNAME=${params.BROWSERSTACK_USERNAME}
BROWSERSTACK_ACCESS_KEY=${params.BROWSERSTACK_ACCESS_KEY}
REMOTE_URL=http://hub.browserstack.com/wd/hub
"""
                        )
                        echo "✅ Credentials file created from Jenkins parameters"
                    } else {
                        // Check if .env.credentials exists in repo (should NOT be committed)
                        if (fileExists('.env.credentials')) {
                            echo "⚠️ Using existing .env.credentials file"
                        } else {
                            echo "⚠️ No credentials provided. Local execution will proceed without BrowserStack."
                        }
                    }
                }
            }
        }

        stage('Run Tests') {
            steps {
                echo "🚀 Running tests on ${params.PLATFORM} with context: ${params.CONTEXT}"
                script {
                    try {
                        sh """
                            . venv/bin/activate
                            export CONTEXT=${params.CONTEXT}
                            pytest tests/ \
                                --platform=${params.PLATFORM} \
                                -m "${params.PLATFORM}" \
                                --alluredir=${ALLURE_RESULTS_DIR} \
                                --clean-alluredir \
                                -v
                        """
                    } catch (Exception e) {
                        echo "❌ Tests failed with error: ${e.message}"
                        throw e
                    }
                }
            }
        }

        stage('Generate Allure Report') {
            steps {
                echo "📊 Generating Allure report"
                script {
                    // Install allure if not available
                    sh '''
                        if ! command -v allure &> /dev/null; then
                            echo "Installing Allure..."
                            wget -q https://github.com/allure-framework/allure2/releases/download/2.24.1/allure-2.24.1.tgz
                            tar -xzf allure-2.24.1.tgz
                            export PATH=$PATH:$(pwd)/allure-2.24.1/bin
                        fi
                    '''
                }
                sh '''
                    . venv/bin/activate
                    allure generate ${ALLURE_RESULTS_DIR} --clean -o allure-report
                '''
                echo "✅ Allure report generated"
            }
        }
    }

    post {
        always {
            script {
                echo "🧹 Cleaning up..."
                // Archive Allure results
                archiveArtifacts artifacts: "${ALLURE_RESULTS_DIR}/**/*", allowEmptyArchive: true

                // Publish Allure report
                allure includeProperties: false, jdk: '', results: [[path: ALLURE_RESULTS_DIR]]
            }
        }
        success {
            echo "✅ All tests passed successfully!"
            echo "📊 Allure report available at: ${env.JENKINS_URL}/job/${env.JOB_NAME}/${env.BUILD_NUMBER}/allure"
        }
        failure {
            echo "❌ Some tests failed. Check Allure report for details."
        }
        cleanup {
            // Remove virtual environment to save space
            sh '''
                rm -rf venv
                rm -rf allure-2.24.1*
                echo "✅ Cleanup complete"
            '''
        }
    }
}