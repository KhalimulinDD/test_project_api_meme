# **Описание репозитория:**

### В данном репозитории находится проект с автоматизированными тестами, для тестирования API с помощью Pytest.

# **С чего начать?**

### Для запуска тестов в репозитории необходимо выполнить следующее:
* Нажать на вкладку Actions 
* Нажать на "Run autotests" в списке workflows
  
![image](https://github.com/user-attachments/assets/3e43f5a2-cd58-4995-98da-2258b7ac6098)

* Нажать на кнопку "Run workflow"
* В выпадающем списке "choose tests set" выбрать тесты которые необходимо запустить

![image](https://github.com/user-attachments/assets/2a85777a-381d-40db-81a7-939a7be8405b)

* Нажать зеленую кнопку "Run workflow"

### **Ознакомится с описанием вариантов запуска тестов, можно в файле pytest.ini**

### **Примечание: Если Run workflow не отображается значит у вас не достаточно прав на запуск, чтобы иметь право запуска нужно стать соавтором "Collaborators" репозитория**
**Отправте на dima.khalimulin@mail.ru ваше имя в github, я добавлю вас в список и вы можете продолжить запуск автотестов**

### **Для запуска тестов локально необходимо выполнить следующее:**
* Склонировать репозиторий любым удобным способом

![image](https://github.com/user-attachments/assets/c9d9f9b4-d2d2-40e9-bfb3-ca84ace43fb0)

* Запуск всех тестов

    `pytest -v -s`

* Запуск тестов с маркировкой (Маркировки в файле pytest.ini)

    `pytest -v -s -m smoke` - **вместо smoke указываем нужную маркировку**

* Запуск тестов с созданием отчета в Allure
  1. Запускаем тесты и получаем результат

        `pytest --alluredir=allure-results` - создается папка **allure-results** с результатами тестов
  2. Генерируем отчет в Allure

        `allure generate` - создается папка **allure-report** для формирования отчета

  3. Открываем отчет в Allure

        `allure serve` - отчет открывается в браузере

    Если нужно сгенерировать другой отчет с очисткой предыдущего, то можно воспользоваться командой:

    `allure generate --clear`
