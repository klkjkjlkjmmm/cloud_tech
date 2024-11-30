<h1>Лабораторная №4 (со звездочкой)</h1>

<h3>Задание:</h3>
Сделать красиво работу с секретами. Например, поднять Hashicorp Vault и сделать так, чтобы ci/cd пайплайн (или любой другой ваш сервис) ходил туда, брал секрет, использовал его не светя в логах. В Readme аргументировать почему ваш способ красивый, а также описать, почему хранение секретов в CI/CD переменных репозитория не является хорошей практикой.

<h2>Ход работы</h2>

Предисловие: автор отчета приносит извинения за излишнюю эмоциональность, но команде, в которой оказались аналитик, два тестировщика и сетевой инженер, секреты оказались по зубам не с первого, и даже не со второго дня

<details>

<summary>CI/CD пайплайн</summary>
    
    name: Secret Secret
    
    on:
      push:
        branches:
          - main

    jobs:
      fetch-secret:
        runs-on: ubuntu-latest

    env:
      HCP_CLIENT_ID: ${{ secrets.HCP_CLIENT_ID }}
      HCP_CLIENT_SECRET: ${{ secrets.HCP_CLIENT_SECRET }}
      HCP_LOCATION: "https://api.cloud.hashicorp.com/secrets/2023-11-28/organizations/6683972e-be8c-4e46-92f8-b299e1ad7674/projects/120c304b-9f4d-4d10-a0f6-8ec1d2f0fa19/apps/cloudTech/secrets:open"

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Install jq for JSON parsing
        run: sudo apt-get update && sudo apt-get install -y jq

      - name: Fetch secret from HashiCorp Vault
        run: |
          echo "Fetching secret from HashiCorp Vault..."

          HCP_API_TOKEN=$(curl --location "https://auth.idp.hashicorp.com/oauth2/token" \
            --header "Content-Type: application/x-www-form-urlencoded" \
            --data-urlencode "client_id=$HCP_CLIENT_ID" \
            --data-urlencode "client_secret=$HCP_CLIENT_SECRET" \
            --data-urlencode "grant_type=client_credentials" \
            --data-urlencode "audience=https://api.hashicorp.cloud" | jq -r .access_token)

          SECRET_RESPONSE=$(curl -s --request GET \
            --url "$HCP_LOCATION" \
            --header "Authorization: Bearer $HCP_API_TOKEN")

          SECRET_APP=$(echo "$SECRET_RESPONSE" | jq -r '.secrets[] | select(.name == "SECRET_APP") | .static_version.value')
          echo "::add-mask::${SECRET_APP}"

          echo "SECRET_APP=***" >> $GITHUB_ENV

      - name: Use the secret
        run: |
          echo "Using the fetched secret..." > secret.txt
          cat secret.txt
          echo "Secret used successfully."
</details>

В раскрывающемся окне представлен код итогового пайплайна, а пока мы начнем наш длинный рассказ о том, как мы пришли к такому результату и скрытому значению секрета в лог-файлах. Спойлер: это было очень нелегко.

Для начала мы авторизовались в HashiCorp Cloud Platform. После входа там уже создается необходимое рабочее пространство и даже минимально настраивается Vault Secret. Наше пространство выглядит примерно так: <br/>
![image](https://github.com/user-attachments/assets/908684f1-4fc1-495e-bc24-11e4c4d825e4) 

Далее мы создали первый секрет SECRET_APP, который мы дальше и будем пытаться достать. В дальнейшем нам также необходимы секреты HCP_CLIENT_ID и HCP_CLIENT_SECRET, в которых хранятся сгенерированные для работы с API значения. И вот тут и начались первые проблемы, потому что как оказалась генерация этих ключей спрятана на той же странице, что и секреты, а не где-то в пространстве HashiCorp Cloud Platform на вкладке API. Делимся этим секретом в отчете, чтоб больше не тратить несколько десятков минут на разгадку этой тайной тайны.

И вот, преодолев первые проблемы, мы начали интеграцию платформы в Git нашей команды. Но и тут нам повстречался Змей Горыныч, который не давал настроить эту интеграцию. А все потому, что изначально при выдаче прав на репозиторий не всем были выданы права на администрирование, и тут человек, ответсвенный за интеграцию, начал грустить. Так наша команда стала организацией с самым креативным названием, в чье пространство переехал репозиторий. И в этом идеальном мире мы смогли настроить интеграцию: </br>
![image](https://github.com/user-attachments/assets/8f051e38-cda0-4ec1-bb3c-b131a8a2bd54) 

Отдельный респект документации HashiCorp Cloud Platform, которая сделала за нас половину пайплайна по инеграции с платформой. Однако осознание места, куда списывать с документации, приходило очень долго. И тут мы переходим в репозиторий нашей организации и создаем новый yml-файл.

Казалось, что не светить секрет в логах очень просто, но после осознания, принятия формата json-ки и настройки правильного чтения нашего секрета, значение все же светилось в следующем пункте пайплайна. Тут было очень долгое осознание и загрузка понимания, но мы решили пропустить этот этап и быстрее исправлять этот беспредел: <br/>
![image](https://github.com/user-attachments/assets/99694a18-e4f5-4867-8405-3bec7c1c363b)

Итак, перейдем к самому пайплайну. Основной блок для нас — это Fetch secret from HashiCorp Vault. Напомним его итоговое содержимое.

    run: |
          echo "Fetching secret from HashiCorp Vault..."

          HCP_API_TOKEN=$(curl --location "https://auth.idp.hashicorp.com/oauth2/token" \
            --header "Content-Type: application/x-www-form-urlencoded" \
            --data-urlencode "client_id=$HCP_CLIENT_ID" \
            --data-urlencode "client_secret=$HCP_CLIENT_SECRET" \
            --data-urlencode "grant_type=client_credentials" \
            --data-urlencode "audience=https://api.hashicorp.cloud" | jq -r .access_token)

          SECRET_RESPONSE=$(curl -s --request GET \
            --url "$HCP_LOCATION" \
            --header "Authorization: Bearer $HCP_API_TOKEN")

          SECRET_APP=$(echo "$SECRET_RESPONSE" | jq -r '.secrets[] | select(.name == "SECRET_APP") | .static_version.value')
          echo "::add-mask::${SECRET_APP}"

          echo "SECRET_APP=***" >> $GITHUB_ENV
          
Первые три параграфа не вызывают вопросов. Эта та самая прекрасная документация сервиса и вывод процесса. А вот далее начинается самое интересное. По сути, мы считываем из той самой json-ки значение нашего секрета SECRET_APP. Структура файла получилась сложная, поэтому мы получили много разных обращений к различным ее частям, чтоб докопаться до сути. Далее с помощью ::add-mask:: мы указываем, что именно к этому логу будет применена маскировка при следующих выводах.
Посмотрев на следующую команду, кто-то скажет, что так нельзя и вообще это как-то неправильно. Мы скажем, что устанавливаем переменной окружения SECRET_APP маскированное значение ***. Это делается как раз для того, чтобы даже если переменная будет использована в дальнейшем, то ее значение не будет выводится в логах. Интересный факт: если перед этой командой обращаться к данной переменной, мы получим ее истинное значение и даже в лог-файлах ее засветим. Имеено поэтому мы считаем, что наш способ очень даже красивый для нашего уровня познаний.

И как итог мы добились засекречивания хомяка: <br/>
![image](https://github.com/user-attachments/assets/3a2db797-4629-4fe6-9b74-bfc69e58020e)

Если же говорить про то, почему хранение секретов в CI/CD переменных репозитория не является хорошей практикой, то это именно потому, что к ним намного проще получить доступ. Иногда такая возможность есть в публичных репозиториях, где злоумышленник как раз через лог-файлы может получить значения секретов, куда обычно складывают самые главные секреты, в том числе логины и пароли (и мы так делали). Владельцы секретов могут хранить и другую важную информацию в секретах, а никому из нас не нужна утечка информации. Ведь даже такие неопытные пользователи, как мы, смогли засветить хомяка в логах, а кто-то более опытный теперь сможет достать значение этого секрета через логи. Хорошо, что ни у кого из нас хомяк не является ключевым словом при смене пароля. Или является?!
