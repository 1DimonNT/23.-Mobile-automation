# 23. Mobile Automation Project

## 📱 Mobile QA Automation for Wikipedia App

Автоматизация тестирования мобильного приложения Wikipedia на Android и iOS с использованием **Appium**, **Selene**, **Pytest** и **Allure**.

---

## 🚀 Технологии и инструменты

- 🐍 **Python 3.12+** — язык программирования
- 🧪 **Selene** — обертка над Appium для удобного взаимодействия с мобильными элементами
- 📱 **Appium 2.0+** — фреймворк для автоматизации мобильных приложений
- 📐 **Pytest 8.0+** — тестовый фреймворк
- 📊 **Allure Report** — инструмент для генерации отчетов
- ☁️ **BrowserStack** — облачная платформа для тестирования на реальных устройствах
- ⚙️ **Pydantic v2** — валидация и управление конфигурацией

---

## 📁 Структура проекта

```text
mobile_automation/
├── data/                       # Тестовые данные
│   └── __init__.py
├── pages/                      # Реализация Page Object Model (POM)
│   ├── __init__.py
│   ├── onboarding_page.py      # Страницы экрана онбординга
│   └── wikipedia_app.py        # Основной Page Object приложения
├── tests/                      # Тестовые сценарии
│   ├── __init__.py
│   ├── test_onboarding.py      # Тесты онбординга
│   ├── test_wikipedia_article.py # Тесты чтения статей
│   └── test_wikipedia_search.py  # Тесты функционала поиска
├── utils/                      # Вспомогательные утилиты
│   ├── __init__.py
│   └── attach.py               # Хелперы для Allure-аттачментов (скриншоты, логи)
├── .env.bstack                 # Конфигурация для запуска в BrowserStack
├── .env.credentials            # Секретные данные (токена, пароли) — НЕ КОММИТИТЬ!
├── .env.example                # Шаблон конфигурационного файла
├── .env.local_emulator         # Конфигурация для локального эмулятора
├── .env.local_real             # Конфигурация для локального реального устройства
├── config.py                   # Инициализация и валидация настроек (Pydantic)
├── conftest.py                 # Фикстуры Pytest (запуск/остановка драйвера)
├── Jenkinsfile                 # Конфигурация CI/CD пайплайна Jenkins
├── pytest.ini                  # Системные настройки фреймворка Pytest
├── README.md                   # Документация проекта
└── requirements.txt            # Список зависимостей проекта
```

---

## 🔧 Установка и настройка

### 1. Клонирование репозитория

```bash
git clone https://github.com/1DimonNT/23.-Mobile-automation.git
cd "23. Mobile automation"
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # Для Linux/Mac
# или
.\venv\Scripts\activate   # Для Windows (PowerShell)
```

### 3. Установка зависимостей

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Настройка конфигурации

Скопируйте шаблон `.env.example` в нужные файлы конфигурации в зависимости от вашей среды выполнения:

```bash
# Для локального эмулятора
cp .env.example .env.local_emulator

# Для реального устройства
cp .env.example .env.local_real

# Для BrowserStack
cp .env.example .env.bstack
```
*Настройте параметры внутри каждого созданного файла (укажите ID устройства, версию ОС, точный путь к APK).*

### 5. Настройка секретных данных (BrowserStack)

Создайте файл `.env.credentials` в корне проекта и добавьте ваши доступы:

```env
BROWSERSTACK_USERNAME=your_username
BROWSERSTACK_ACCESS_KEY=your_access_key
REMOTE_URL=http://browserstack.com
```
> ⚠️ **Важно:** Файл `.env.credentials` добавлен в `.gitignore` и ни в коем случае **НЕ должен** попасть в удаленный репозиторий!

### 6. Подготовка APK CLI приложения

Для локального запуска скачайте Wikipedia APK (например, с APKMirror) и поместите его по пути: `./apps/wikipedia.apk`

---

## 🏃 Запуск тестов

### Локальный запуск на эмуляторе

```bash
# Установка переменной окружения (Linux/Mac)
export CONTEXT=local_emulator  
# или для Windows (PowerShell)
$env:CONTEXT="local_emulator"

# Запуск всех Android тестов
pytest tests/ --platform=android -m android -v

# Запуск конкретного тест-кейса
pytest tests/test_onboarding.py -v

# Запуск с генерацией данных для Allure-отчета
pytest tests/ --platform=android --alluredir=allure-results
```

### Запуск в облаке BrowserStack

```bash
export CONTEXT=bstack  # Для Windows: $env:CONTEXT="bstack"
pytest tests/ --platform=android -m bstack -v
```

### Запуск по тегам (маркерам)

```bash
# Только тесты функционала поиска
pytest tests/ -m search -v

# Только тесты приветственного экрана (онбординга)
pytest tests/ -m onboarding -v

# Только тесты работы со статьями
pytest tests/ -m article -v
```

---

## 📊 Allure-отчетность

Для построения и просмотра красивых графических отчетов используйте следующие команды:

```bash
# 1. Запуск тестов с сохранением результатов во временную папку
pytest tests/ --alluredir=allure-results

# 2. Генерация статичного HTML отчета в папку allure-report
allure generate allure-results --clean -o allure-report

# 3. Открытие локального веб-сервера с отчетом в браузере
allure open allure-report

## ☁️ BrowserStack Dashboard

Видео выполнения тестов можно посмотреть в [BrowserStack Dashboard](https://app-automate.browserstack.com/dashboard).

После каждого запуска в логах появляется прямая ссылка на сессию: 
BrowserStack session: https://app-automate.browserstack.com/dashboard/v2/builds/sessions/[session_id]
```
---

## 🐳 Запуск через Docker (Опционально)

```bash
# Сборка Docker-образа проекта
docker build -t mobile-automation .

# Запуск тестов внутри контейнера (для BrowserStack)
docker run --env CONTEXT=bstack mobile-automation
```

---

## 🔄 CI/CD (Jenkins Freestyle Job)

Для автоматизации запуска в Jenkins настройте Freestyle job:

### 1. Создание новой задачи
- Нажмите **"New Item"**
- Введите имя задачи
- Выберите **"Freestyle project"**
- Нажмите **OK**

### 2. Настройка Git
- В разделе **Source Code Management** выберите **Git**
- Repository URL: `https://github.com/1DimonNT/23.-Mobile-automation.git`
- Branch: `*/main`

### 3. Настройка параметров сборки
- В разделе **General** → **This project is parameterized** → **Add Parameter**
- Добавьте 4 параметра типа **Choice Parameter** и **String Parameter**:

| Имя параметра | Тип | Значения (для Choice) |
|---------------|-----|----------------------|
| `CONTEXT` | Choice Parameter | `bstack` `local_emulator` `local_real` |
| `PLATFORM` | Choice Parameter | `android` `ios` |
| `BROWSERSTACK_USERNAME` | String Parameter | ваш логин |
| `BROWSERSTACK_ACCESS_KEY` | String Parameter | ваш ключ |

### 4. Настройка шага сборки
- В разделе **Build** → **Add build step** → **Execute Windows batch command** (для Windows) или **Execute shell** (для Linux)
- Добавьте команду:

```bash
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
set CONTEXT=%CONTEXT%
pytest tests/ --platform=%PLATFORM% -m android -v --alluredir=allure-results5. Настройка публикации Allure отчета
После сборки добавьте шаг Allure Report

Путь к результатам: allure-results

6. Сохранение и запуск
Нажмите Save

Нажмите Build with Parameters

Выберите параметры и запустите сборку

text

---

**Этот вариант подходит для Freestyle job в Jenkins.** Сохраните изменения в README.md.

5. Настройка публикации Allure отчета
После сборки добавьте шаг Allure Report

Путь к результатам: allure-results

6. Сохранение и запуск
Нажмите Save

Нажмите Build with Parameters

Выберите параметры и запустите сборку

text

---

**Этот вариант подходит для Freestyle job в Jenkins.** Сохраните изменения в README.md.


---

## 📝 Тестовые сценарии

### 🔹 Онбординг (Onboarding)
- [x] Успешное прохождение всех 4 стартовых экранов.
- [x] Возможность пропуска (Skip) приветственного экрана.
- [x] Проверка корректности текстовых блоков на каждом шаге.

# 23. Mobile Automation Project

## 📱 Mobile QA Automation for Wikipedia App

Автоматизация тестирования мобильного приложения Wikipedia на Android и iOS с использованием **Appium**, **Selene**, **Pytest** и **Allure**.

---

## 🚀 Технологии и инструменты

- 🐍 **Python 3.12+** — язык программирования
- 🧪 **Selene** — обертка над Appium для удобного взаимодействия с мобильными элементами
- 📱 **Appium 2.0+** — фреймворк для автоматизации мобильных приложений
- 📐 **Pytest 8.0+** — тестовый фреймворк
- 📊 **Allure Report** — инструмент для генерации отчетов
- ☁️ **BrowserStack** — облачная платформа для тестирования на реальных устройствах
- ⚙️ **Pydantic v2** — валидация и управление конфигурацией

---

## 📁 Структура проекта

```text
mobile_automation/
├── data/                       # Тестовые данные
│   └── __init__.py
├── pages/                      # Реализация Page Object Model (POM)
│   ├── __init__.py
│   ├── onboarding_page.py      # Страницы экрана онбординга
│   └── wikipedia_app.py        # Основной Page Object приложения
├── tests/                      # Тестовые сценарии
│   ├── __init__.py
│   ├── test_onboarding.py      # Тесты онбординга
│   ├── test_wikipedia_article.py # Тесты чтения статей
│   └── test_wikipedia_search.py  # Тесты функционала поиска
├── utils/                      # Вспомогательные утилиты
│   ├── __init__.py
│   └── attach.py               # Хелперы для Allure-аттачментов (скриншоты, логи)
├── .env.bstack                 # Конфигурация для запуска в BrowserStack
├── .env.credentials            # Секретные данные (токена, пароли) — НЕ КОММИТИТЬ!
├── .env.example                # Шаблон конфигурационного файла
├── .env.local_emulator         # Конфигурация для локального эмулятора
├── .env.local_real             # Конфигурация для локального реального устройства
├── config.py                   # Инициализация и валидация настроек (Pydantic)
├── conftest.py                 # Фикстуры Pytest (запуск/остановка драйвера)
├── Jenkinsfile                 # Конфигурация CI/CD пайплайна Jenkins
├── pytest.ini                  # Системные настройки фреймворка Pytest
├── README.md                   # Документация проекта
└── requirements.txt            # Список зависимостей проекта
```

---

## 🔧 Установка и настройка

### 1. Клонирование репозитория

```bash
git clone https://github.com
cd "23. Mobile automation"
```

### 2. Создание виртуального окружения

```bash
python -m venv venv
source venv/bin/activate  # Для Linux/Mac
# или
.\venv\Scripts\activate   # Для Windows (PowerShell)
```

### 3. Установка зависимостей

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Настройка конфигурации

Скопируйте шаблон `.env.example` в нужные файлы конфигурации в зависимости от вашей среды выполнения:

```bash
# Для локального эмулятора
cp .env.example .env.local_emulator

# Для реального устройства
cp .env.example .env.local_real

# Для BrowserStack
cp .env.example .env.bstack
```
*Настройте параметры внутри каждого созданного файла (укажите ID устройства, версию ОС, точный путь к APK).*

### 5. Настройка секретных данных (BrowserStack)

Создайте файл `.env.credentials` в корне проекта и добавьте ваши доступы:

```env
BROWSERSTACK_USERNAME=your_username
BROWSERSTACK_ACCESS_KEY=your_access_key
REMOTE_URL=http://browserstack.com
```
> ⚠️ **Важно:** Файл `.env.credentials` добавлен в `.gitignore` и ни в коем случае **НЕ должен** попасть в удаленный репозиторий!

### 6. Подготовка APK приложения

Для локального запуска скачайте Wikipedia APK (например, с APKMirror) и поместите его по пути: `./apps/wikipedia.apk`

---

## 🏃 Запуск тестов

### Локальный запуск на эмуляторе

```bash
# Установка переменной окружения (Linux/Mac)
export CONTEXT=local_emulator  
# или для Windows (PowerShell)
$env:CONTEXT="local_emulator"

# Запуск всех Android тестов
pytest tests/ --platform=android -m android -v

# Запуск конкретного тест-кейса
pytest tests/test_onboarding.py -v

# Запуск с генерацией данных для Allure-отчета
pytest tests/ --platform=android --alluredir=allure-results
```

### Запуск в облаке BrowserStack

```bash
export CONTEXT=bstack  # Для Windows: $env:CONTEXT="bstack"
pytest tests/ --platform=android -m bstack -v
```

### Запуск по тегам (маркерам)

```bash
# Только тесты функционала поиска
pytest tests/ -m search -v

# Только тесты приветственного экрана (онбординга)
pytest tests/ -m onboarding -v

# Только тесты работы со статьями
pytest tests/ -m article -v
```

---

## 📊 Allure-отчетность

Для построения и просмотра красивых графических отчетов используйте следующие команды:

```bash
# 1. Запуск тестов с сохранением результатов во временную папку
pytest tests/ --alluredir=allure-results

# 2. Генерация статичного HTML отчета в папку allure-report
allure generate allure-results --clean -o allure-report

# 3. Открытие локального веб-сервера с отчетом в браузере
allure open allure-report
```

---

## ☁️ BrowserStack Dashboard

Видео выполнения тестов можно посмотреть в [BrowserStack Dashboard](https://browserstack.com).

После каждого запуска в логах появляется прямая ссылка на сессию: 
```text
BrowserStack session: https://browserstack.com/v2/builds/sessions/[session_id]
```

---

## 🐳 Запуск через Docker (Опционально)

```bash
# Сборка Docker-образа проекта
docker build -t mobile-automation .

# Запуск тестов внутри контейнера (для BrowserStack)
docker run --env CONTEXT=bstack mobile-automation
```

---

## 🔄 CI/CD (Jenkins Freestyle Job)

Для автоматизации запуска тестов настройте конфигурацию Freestyle проекта в Jenkins по следующим шагам:

### 1. Создание новой задачи
- Нажмите **"New Item"** в главном меню Jenkins.
- Введите имя для вашей задачи.
- Выберите тип **"Freestyle project"** и нажмите **OK**.

### 2. Настройка Git-репозитория
- Перейдите в раздел **Source Code Management** и выберите **Git**.
- В поле **Repository URL** укажите: `https://github.com`
- В поле **Branch Specifier** укажите вашу ветку: `*/main`

### 3. Настройка параметров сборки
- В разделе **General** активируйте чекбокс **"This project is parameterized"**.
- Через кнопку **Add Parameter** добавьте следующие переменные:


| Имя параметра | Тип параметра | Значение / Описание |
|:---|:---|:---|
| `CONTEXT` | Choice Parameter | `bstack`<br>`local_emulator`<br>`local_real` |
| `PLATFORM` | Choice Parameter | `android`<br>`ios` |
| `BROWSERSTACK_USERNAME` | String Parameter | Ваш логин в системе BrowserStack |
| `BROWSERSTACK_ACCESS_KEY` | String Parameter | Ваш секретный ключ доступа |

### 4. Настройка шагов сборки (Build Steps)
- В разделе **Build Steps** нажмите **Add build step** и выберите:
  - **Execute Windows batch command** (если Jenkins на Windows)
  - **Execute shell** (если Jenkins на Linux/Mac)
- Добавьте следующий скрипт:

```bash
python -m venv venv
# Для Windows: call venv\Scripts\activate
source venv/bin/activate
pip install -r requirements.txt
pytest tests/ --platform=%PLATFORM% -m android -v --alluredir=allure-results
```

### 5. Настройка публикации Allure-отчета
- В разделе **Post-build Actions** нажмите **Add post-build action** и выберите **Allure Report**.
- В поле **Results** -> **Path** укажите: `allure-results`

### 6. Сохранение и запуск
- Нажмите кнопку **Save**.
- Для старта нажмите **Build with Parameters**, выберите окружение и запустите сборку.

---

## 📝 Тестовые сценарии

### 🔹 Онбординг (Onboarding)
- [x] Успешное прохождение всех 4 стартовых экранов.
- [x] Возможность пропуска (Skip) приветственного экрана.
- [x] Проверка корректности текстовых блоков на каждом шаге.

### 🔹 Поиск (Search)
- [x] Поиск статей по валидному ключевому слову.
- [x] Проверка соответствия и количества выданных результатов.
- [x] Обработка пустой выдачи при невалидном поисковом запросе.

### 🔹 Статьи (Article)
- [x] Открытие детальной страницы статьи из поисковой выдачи.
- [x] Прямое открытие конкретной статьи по ссылке.
- [x] Возврат назад к списку результатов поиска (кнопка Back).

---

## 🛠 Технические требования

* **Python:** версия `3.12` или выше.
* **Appium Server:** версия `2.0+` (требуется строго для локального запуска).
* **Android SDK:** настроенные переменные среды (для локального эмулятора).
* **Java JDK:** версия `11+` (необходима для работы Appium-сервера).

---

## 📦 Ключевые зависимости

Полный список зафиксирован в файле `requirements.txt`:

```text
Appium-Python-Client==4.0.0
pytest==8.2.1
selene==2.0.0rc9
pydantic==2.4.2
pydantic-settings==2.1.0
python-dotenv==1.0.0
allure-pytest==2.13.5
requests==2.31.0
```

---

## 🤝 Контрибьюция

1. Сделайте Форк (Fork) проекта.
2. Создайте ветку для новой фичи: `git checkout -b feature/amazing-feature`
3. Зафиксируйте изменения: `git commit -m 'Add amazing feature'`
4. Отправьте ветку в ваш репозиторий: `git push origin feature/amazing-feature`
5. Откройте новый **Pull Request**.

---

## 📧 Контакты

* **Автор:** Dmitrii Ivantsov  
* **GitHub:** [@1DimonNT](https://github.com)

---

## 📄 Лицензия

Этот проект создан исключительно в учебных и образовательных целях.

---

## ✅ Статус проекта

<table>
  <tr>
    <td><b>Build Status</b></td>
    <td><kbd>🟢 passing</kbd></td>
  </tr>
  <tr>
    <td><b>Tests Status</b></td>
    <td><kbd>🔵 6 passed</kbd></td>
  </tr>
  <tr>
    <td><b>Allure Report</b></td>
    <td><kbd>🟠 generated</kbd></td>
  </tr>
</table>



