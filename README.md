# YggMap
Map of nodes for yggdrasil-network

# Demo

Тестовая установка работает по адресу http://[21d:758e:d790:dd2b:6a62:f494:87ef:2ef7]:51880/

Обновление проводится раз в 6 часов

# Как добавить узел на карту

1. Настройте узел Yggdrasil и точку доступа Wi-Fi, предоставляющую подключение к этому узлу.

2. Подберите себе адрес "посложнее". Просто запустите соответствующую утилиту из набора Yggdrasil и подождите... ну хотя бы час (лучше - больше). А потом скопируйте параметры публичного и закрытого ключа в соостветсвующие секции конфикурационного файла.
Это не имеет большого значения сейчас, но может использоваться если кто-то решит добавить фейковые точки.

3. Добавьте в раздел NodeInfo своего конфигурационного файла блок physical. Например:
```json
"physical": {
    "coord":"55.753215, 37.622504",
    "SSID":"YGG",
    "description":"demo посреди Красной Площади ориентироваться на мавзолей",
    "mode":"AP",
    "password":"12345678",
    "exconninfo":"channel 14, Hidden SSID"
 }
 ```
  
 * coord - Обязательный параметр! Ваше примерное расположение. Найдите себя на https://www.openstreetmap.org/ а потом нажмите правой клавишей и выберите "показать адрес". Помимо адреса первым же пунктом будут показаны координаты.
 * SSID - Обязательный параметр! Название (SSID) вашей вай-фай сети. Так люди узнают, к какой сети им подключаться.
 * description - Не обязательный, но желательный параметр. Расскажите людям как вас найти. Куда смотрят ваши окна? Как лучше подключаться к вам - откуда ваш вай-фай лучше ловится?
 * mode - Wi-Fi имеет несколько режимов работы. Какой используете вы? 802.11s? Обычная точка доступа(AP)? А может вы готовы только к единственному прямому Ad-Hoc подключению...
 * password - Лучше, конечно, иметь точку доступа без пароля. Но если вам зачем-то понадобилось его установить - укажите его здесь.
 * exconninfo - Вы используете какие-то ещё нестандартные настройки? Укажите их здесь.
  
4. Добавьте также в раздел NodeInfo параметр contact, чтобы люди знали как с вами связаться при необходимости.

Таким образом типичный вариант NodeInfo должен включать что-то вроде 
```javascript
  "physical": {
    "coord":"55.7935, 37.37467",
    "SSID":"YGG",
    "description":"На дереве, смотрит на шоссе",
    "mode":"AP"
    },
  "contact": "me@demo.com"
```
