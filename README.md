# Educator Module
## 1. Run the docker image
- get OpenAI key
- get Azure subscription key and Azure region
    1. create Azure subscription [here](https://azure.microsoft.com/en-gb/free/cognitive-services/)
    2. create a Speech resource [here](https://portal.azure.com/#create/Microsoft.CognitiveServicesSpeechServices)
    3. get the subscription key and region (follow the instructions [here](https://docs.microsoft.com/en-us/azure/cognitive-services/cognitive-services-apis-create-account?tabs=multiservice%2Cwindows#get-the-keys-for-your-resource))
- replace "replace" in Dockerfile with OpenAI key, Azure subscription key and Azure region
- to build: `docker build --no-cache --progress=plain -t backend`
- to run: `docker run --rm -it  -p 5000:5000/tcp backend:latest`

## 2. Instructions of Dependency Installation

### Backend
- create virtual environment with Python 3.8 and more
- get OpenAI key
- get Azure subscription key and Azure region
    1. create Azure subscription [here](https://azure.microsoft.com/en-gb/free/cognitive-services/)
    2. create a Speech resource [here](https://portal.azure.com/#create/Microsoft.CognitiveServicesSpeechServices)
    3. get the subscription key and region (follow the instructions [here](https://docs.microsoft.com/en-us/azure/cognitive-services/cognitive-services-apis-create-account?tabs=multiservice%2Cwindows#get-the-keys-for-your-resource))
- put OpenAI key, Azure subscription key and Azure region into environment variable with variable name as openai_api_key, azure_subscription and azure_region respectively
- `pip install -r requirements.txt`
- `pip install sentence-transformers`
- install Aeneas (for Mac) (adjusting from [here](https://github.com/readbeyond/aeneas/blob/master/wiki/INSTALL.md))
    1. make sure brew is installed, if not,
        * `xcode-select –install`
        * `ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"`
    2. `brew install danielbair/tap/aeneas`
- install Aeneas (for Windows) (adjusted from [here](https://github.com/readbeyond/aeneas/blob/master/wiki/INSTALL.md))
    1. go to [all in one installer](https://github.com/sillsdev/aeneas-installer/releases)
    2. `install aeneas-windows-setup-1.7.3.0_2.exe` (this will install external apps to make aeneas work)
    3. espeak_sapi.dll from eSpeak directory must be copied and renamed to: C:\Windows\System32\espeak.dll
    4. espeak.lib from [thirdparty directory of aeneas repo](https://github.com/readbeyond/aeneas) must be copied to PYTHONDIR\libs\espeak.lib (PYTHONDIR is directory of the virtual env)
    5. open command prompt, run `set AENEAS_WITH_CEW=False`
    6. `pip install aeneas`
    7. _(optional)_ If `pip install aeneas` returns C++ dependency error, install latest C++ redistributable from [here](https://docs.microsoft.com/en-US/cpp/windows/latest-supported-vc-redist?view=msvc-170)
    8. repeat 5. and 6

### Frontend
- navgiate to educator folder
- run `npm start`

## Others
- You can run api.py to start the server.

- Will run on python >=3.8.x

- Install all required dependencies with "pip install -r requirements.txt" from project folder.

- Access it on http://127.0.0.1:5000/

- Access the API documentation on http://127.0.0.1:5000/apidocs

- The main page will show you the full api documentation (not ready yet).

- Note: Install sentence-transformers seperately, as installing it with requirements.txt won't work.
More info here: https://www.sbert.net/

