<h1>Лабораторная №4</h1>

<h2>Задание</h2>

<h3>Обычная:</h3> 
<ol>
  <li>Написать “плохой” CI/CD файл, который работает, но в нём есть не менее пяти плохих практик по написанию CI/CD</li>
  <li>Написать “хороший” CI/CD, в котором все плохие практики исправлены</li>
  <li>Указать, как были исправлены плохие практики на хорошие, сравнить полученный результат</li>
</ol>

<h2>Ход работы</h2>

<p>
Для задания был выбран GitHub Actions. С его помощью мы создали два workflow: плохой (с ошибками) и хорошенький (с исправлениями).
</p>

<h3>Плохой CI/CD</h3>
<p>
В этом файле были показаны плохие CI/CD, позже разберем плохихие практики из него:
</p>

```yml
name: Bad CI/CD Workflow

on:
  push:
    branches:
      - '*'

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: First step
        uses: actions/checkout@v4

      - name: Install dependencies
        run: |
          sudo apt-get update
          sudo apt-get install -y nodejs npm
          cd lab_4 && npm install

      - name: Run tests
        run: cd lab_4 && npm test || echo "Если тесты провалились, мы продолжим))"

      - name: Deploy application
        env:
          APP_SECRET: "my_super_secret"
        run: |
          echo "Деплоим..."
          echo "Задеплоили!" 
```

<h3>Хороший CI/CD</h3>
<p>
Исправленный файл с учётом хороших практик, позже расскажем расскажем почему он так хорош:
</p>

```yml
name: Good CI/CD Workflow

on:
  push:
    branches:
      - main

jobs:
  test-and-deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: npm install --prefix lab_4

      - name: Run tests
        id: test_step
        run: npm test --prefix lab_4
        continue-on-error: false

      - name: Deploy to production
        if: ${{ success() }}
        env:
          APP_SECRET: ${{ secrets.APP_SECRET }}
        run: |
          echo "Начинаем деплой..."
          echo "Успешно задеплоили!"  

      - name: Notify deployment status
        if: ${{ success() }}
        run: echo "Все гуд!"
        
      - name: Notify on failure
        if: ${{ failure() }}
        run: echo "Что-то пошло не так, проверяйте тесты!"
```
